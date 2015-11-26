Title: Custom ML in R 
Date: 2015-11-05

Before writing this blogpost I did very little with object oriented code in R. I never really saw it as a useful feature because I am mostly using R as an analysis tool. The power of R comes partly from the fact that other people have done this work for you. Recently though, I've been tasked to write a custom machine learning library that needed to support the `predict` function. 

This document will describe the simplest machine learning method ever and some quick details on how to implement it in R via object oriented coding. This post is heavily inspired by [this pdf](https://cran.r-project.org/doc/contrib/Leisch-CreatingPackages.pdf) and [this tutorial](http://adv-r.had.co.nz/OO-essentials.html). My goal is to have a similar document but a bit shorter to make it easier for my own reference. I will try to compare python to R wherever possible such that other people may find it useful too. 

## S3 Classes 

Where python has dictionaries, R has lists. 

```
obj <- list(a = 1, b = 2)
```

Instead of having methods within these objects, R uses functions that can accept many different types of objects. Notice below that I am using the same function on a list as I am on a dataframe. 

```{r}
names(obj) 
# "a" "b"
names(ChickWeight)
# "weight" "Time"   "Chick"  "Diet" 
```

Where python has polymorphism, R (and Julia by the way) has multiple dispatch. Methods do not belong to objects, they belong to functions. Instead of binding a method to an object, R allows you to write many functions that share the same name but refer to different objects. For example, if you want to check out what objects can be handed to `summary`:

```{r}
> methods(summary)
 [1] summary.aov                    summary.aovlist*               summary.aspell*               
 [4] summary.check_packages_in_dir* summary.connection             summary.data.frame            
 [7] summary.Date                   summary.default                summary.ecdf*             
 ...   
```

You could also check for all methods that below to a certain class.

```{r}
> methods(class = "Date")
 [1] -             [             [[            [<-           +             as.character 
 [7] as.data.frame as.list       as.POSIXct    as.POSIXlt    Axis          c            
[13] coerce        cut           diff          format        hist          initialize   
[19] is.numeric    julian        Math          mean          months
...
```

If the function `mean()` were called on a `Date` object it would internally call `mean.Date()`. To keep track of what method a function should use R looks at the name of the function. In the case of `mean.Date()` the S3 class in R would recognize that the function `mean` can be used for `Date` by looking at the name. A silly example; `foo.bar()` would allow R to recognize that the function `foo` can be used on a `bar` object. 

This should feel very odd if you are a python programmer because it puts a lot of functions in the global namespace. 

Let's create an object of type foo again, just to be explicit.

```{r}
obj <- list(a = 1, b = 2)
class(obj) <- 'foo' 

> class(obj) 
"foo"
```

We will now create a method `mean.foo` which will be called by the generic function `mean` if it is passed an object of class `foo`. 

```{r}
mean.foo <- function(x){
  (x$a + x$b)/2
}

> mean(obj) 
1.5
```

The only thing missing right now is a way to generate our own generic function. Just like `mean` was a generic function here, we might want to create a generic function that can be used on multiple objects. 

```{r}
f <- function(x) UseMethod("f")
f.foo <- function(x){
  paste(x$a, "and",  x$b, "are in this foo obj")
}
f.numeric <- function(x){
  paste("this numeric has value", x)
}

> f(obj)
[1] "1 and 2 are in this foo obj"
> f(2)
[1] "this numeric has value 2"
```

## The model 

I want to make a model that assumes a continous variable $y$ and a discrete input $X$. It will average $y$ over all the $X$ combinations.

To create this machine learnin model I want a generic function that returns an object with a class. As long as I create a function via `UseMethod` that returns a `list` with an assigned class this should work. 

```
library(dplyr)

aggmod <- function(x, ...) UseMethod("aggmod")

aggmod.default <- function(form, data, ...){
  res <- list()
  
  agg <- aggregate(formula = form, FUN = mean, data = data)
  colnames(agg) <- c(form %>% all.vars %>% tail(-1), "pred")
  res$agg <- agg
  
  res$call <- match.call()
  res$formula <- form
  res$fitted.values <- data %>% left_join(res$agg) %>% .$pred
  res$y <- data %>% select_(form %>% all.vars %>% head(1))
  res$residuals <- res$y - res$fitted.values
  res$mae <- mean(sum(abs(res$residuals)/length(res$residuals)))
  res$mse <- mean(sum(res$residuals^2)/length(res$residuals))
  
  class(res) <- "aggmod"
  res
}
```

The `.default` method can be seen as a constructor. When we call `aggmod()` function it will point to the `aggmod.default` method and return a list of class `aggmod`. This object still needs some utility generics. Currently, this object has no pretty print representation and can also not be passed into the `predict` function. 

```{r}
print.aggmod <- function(x, ...){
  cat("Call:\n")
  print(x$call)
  cat("\nMSE:")
  print(x$mse)
  cat("MAE:")
  print(x$mae)
}

predict.aggmod <- function(x, newdata = NULL, ...){
  if(is.null(newdata)) return(fitted(x))
  newdata %>% left_join(x$agg) %>% .$pred
}
```

With this in place, it starts to feel like using the `lm` function.

```{r}
modl <- aggmod(weight ~ Time + Diet, ChickWeight) 
> modl %>% print
Call:
aggmod.default(form = weight ~ Time + Diet, data = ChickWeight)

MSE:[1] 631109.7
MAE:[1] 11692.11

> predict(modl, newdata = ChickWeight %>% sample_n(5))
Joining by: c("Time", "Diet")
[1] 187.70000  47.25000  79.68421  64.50000  66.78947
```

## Conclusion 

I found this exercize very helpful in understanding the R way of dealing with objects. If you are from a different programming language this may feel like a very strange way of doing things but it has it's benefits. By allowing our code to be written this way, we can do the following; 

```{r}
formulas <- c(weight ~ Time, weight ~ Time + Diet, weight ~ Diet)
ml_methods <- list(lm, aggmod)
df <- data.frame(variables = as.character(), model = as.character(), median_mse = as.numeric())

mse <- function(x,y){
  diff <- x - y
  mean(sum(diff^2)/length(diff))
}

for(f in formulas){
  for(m in ml_methods){
    mod <- m(f, ChickWeight)
    df <- df %>% rbind(data.frame(
      variables = f %>% all.vars %>% tail(-1) %>% paste(collapse=' '),
      model = mod$call %>% as.character %>% .[1], 
      median_mse = mse(mod %>% predict, ChickWeight$weight)
    ))
  }
}
```

Having a generic `predict` allows an R user to focus on the statistics because there is a common expectation of how an object should interact with it. Not all programmers will like this style, some may say that it offers too much sugar. Another example of things that feel trippy to programmers; 

```{r}
`%+%` <- function(a, b){
  paste(a,b, sep ='')
}

> 'a' %+% 'b' %+% 'c'
[1] "abc"
```

Where python can make use of polymorphism for it's operators, R imposes different rules, but allows you to write your own operators. Most statistician will enjoy this because this syntax allows them only worry about doing statistics with code that feels natural to them.
