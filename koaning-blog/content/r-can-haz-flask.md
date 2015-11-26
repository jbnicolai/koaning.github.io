Title: Via Plumbr, R can haz Flask
Date: 2015-08-01

Turning a simple machine learning model in R into an api just became a whole lot easier. Embarrisingly easy actually, thanks to a lovely package called [plumber](http://plumber.trestletech.com/).

<img class="center" src="http://i.imgur.com/YFSEgBQ.png" alt="" width="50%">

### Install 

Assuming that you have `devtools` installed, all you need to do is type the following: 


	library(devtools)
	install_github("trestletech/plumber")
	library(plumber)


With this installed, let's create a file that creates an endpoint! 

### Example 1 


	# prediction_serv.R

	library(magrittr)

	mod_chick <- lm(data = ChickWeight, weight ~ Time + Diet)
	mod_cars <- lm(data = cars, dist ~ speed)

	#' @get /
	hello_world <- function(){
	  '1 got 99 problems and flask aint one'
	}

	#' @get /predict_chick
	predict_chick <- function(time, diet){
	  data.frame(Time = time %>% as.numeric, Diet = diet %>% as.factor) %>% 
	    predict(mod_chick, newdata = .) %>% 
	    as.numeric
	}

	#' @get /predict_cars
	predict_cars <- function(speed){
	  data.frame(speed = speed %>% as.numeric) %>% 
	    predict(mod_cars, newdata = .) %>% 
	    as.numeric
	}

> Note that the last line `myfile.R` needs to be a an empty line. 

To get this script to act as a web endpoint you'll need to run the `plumber::plumb('/your/path/prediction_serv.R')$run(port=8000)` from Rstudio or an R shell. 

Once this is up, you can curl to the service. 

	$ curl --data "time=24&diet=3" http://localhost:8000/predict_chick
	[257.4356]
	$ curl --data "speed=30" http://localhost:8000/predict_cars
	[100.3932]
	$ curl "http://localhost:8000/"
	curl http://localhost:8000/predict_chick

You can also access this endpoint via the browser, or indeed another R script (via `rvest` or `httr`).

	$ R
	> library(rvest)
	> html('http://localhost:8000/predict_cars?speed=30') %>% 
	+   html_nodes('p') %>% 
	+   html_text
	[1] "[100.3932]"
	> library(httr)
	>  get_speed_pred <- function(speed){
	+   'http://localhost:8000/predict_cars?speed=' %>% 
	+  	   paste0(speed) %>% 
	+	   GET(encode = 'json') %>% 
	+	   content
	}
	> c(10, 30, 50, 12) %>% lapply(get_speed_pred) %>% unlist
	[1]  21.7450 100.3932 179.0413  29.6098

### Example 2 

The previous example only used `GET` requests. With `plumbr` you could post as well. Consider this second example. 

	# post_serv.R

	library(ggplot2)
	library(magrittr)

	df <- data.frame(x = rnorm(10, 0, 1), y = rnorm(10, 0, 1))

	#' @png
	#' @get /plot
	show_plot <- function(){
	  p = ggplot() + 
	    geom_point(data=df, aes(x,y), alpha = 0.5, size = 1.5) + 
	    ggtitle("a plot of all the points")
	  print(p)
	}

	#' @post /add_data
	add_data <- function(n){
	  df <<- data.frame(x = rnorm(n, 0, 1), 
	                   y = rnorm(n, 0, 1)) %>% 
	    rbind(df)
	}

	#' @get /all_data
	all_data <- function(){
	  df 
	}

> Again, note that the last line `post_serv.R` needs to be a an empty line. 

You can run `plumber::plumb('/your/path/post_serv.R')` to bring the service online. This new service allows you to post data and can create a plot for viewing as well. A dataframe can be retreived as a json blob which can be used to give data to a dashboard (d3 would work very well here). 

You can view this blob via: 

	curl http://localhost:8000/all_data

If you use `jsonlite` it is trivial to turn this json blob endpoint into a dataframe in R.

	> library(jsonlite)
	> http://localhost:8000/all_data' %>% GET %>% content('text') %>% fromJSON
	         x       y
	1  -1.4321 -1.1285
	2  -1.7547  1.7694
	3  -0.3472 -0.9206
	4  -0.8752 -0.0267
	5  -0.9626  1.2353
	6   0.9005  0.3753
	7   0.6310 -0.8690
	8  -0.4543  0.4175
	9  -0.7079 -0.6164
	10  0.1954  0.1112

You'll want to use `httr` if you want to use not just GET but also POST requests as well. But just `jsonlite` will also work. 

	> http://localhost:8000/all_data' %>% fromJSON
	         x       y
	1  -1.4321 -1.1285
	2  -1.7547  1.7694
	3  -0.3472 -0.9206
	4  -0.8752 -0.0267
	5  -0.9626  1.2353
	6   0.9005  0.3753
	7   0.6310 -0.8690
	8  -0.4543  0.4175
	9  -0.7079 -0.6164
	10  0.1954  0.1112

You can view all the points currently in the dataframe by pasting `http://localhost:8000/plot` in the browser.

![](http://i.imgur.com/7V6ihi5.png)

If you add points, you can see an update in the plot by refreshing. 

	curl --data "n=100" http://localhost:8000/add_data

![](http://i.imgur.com/GFcb9gP.png)

We can up the anty by adding even more points and refreshing. 

	curl --data "n=10000" http://localhost:8000/add_data

![](http://i.imgur.com/9AiDvKA.png)

### Conclustion 

I'm very enthousiastic about this project.

Don't get me wrong, I love flask/python and this project won't work for a lot of api's, but it does feel liberating to be able to do this sort of thing in R as well. Note that performance might still be a thing as R is single threaded so be careful if you want to start pushing this to something thats meant to be very fast and responsive. 
