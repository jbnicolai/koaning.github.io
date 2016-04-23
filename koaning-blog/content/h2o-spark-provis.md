Title: Sparling Water for Spark(R)
Date: 2016-04-23

SparkR offers R users to do data wrangling on bigger chunks of data. The machine learning algorithms that are supported are a bit modest (only linear models). Even if you go to PySpark or even Scala Spark, you'll notice that not every ML method is supported. This document explains how to append this problem by provisioning Spark with [h2o](http://h2o.ai/). It will focus on SparkR because that takes the most work to set up.

This document explains how to provision a single spark server with h2o and how to access it from spark. It will focus on SparkR because that takes the most work to set up. Most of this information can also be found while zooming through the [documentation](http://www.h2o.ai/download/sparkling-water/spark16) but I found it useful to make this reference for myself. In this document I'll also demonstrate some features of h2o that make it a worthwhile ecosystem to keep an eye on. 

## Download Spark + Sparkling Water 

You can download an appropriate version of Spark (version >= 1.5.2, with something prebuilt for Hadoop) [here](http://spark.apache.org/downloads.html) and you can download sparkling-water [here](http://www.h2o.ai/download/sparkling-water/spark16). Unzip everything. 

## Start Sparkling Water

Go to the folder where you downloaded sparkling water. Set your `SPARK_HOME` variable to the folder where you downloaded Spark. Since this is a local setup we'll only need to specify that the master node is `local[*]`. Next start the sparking-shell. 

```{bash}
export SPARK_HOME="/Users/code/Downloads/spark-1.6.0-bin-hadoop1"
export MASTER="local[*]"
./bin/sparkling-shell
```

This sparkling-shell prompt is a scala REPL. You'll have access to a sparkContext (`sc`) as well as a `sqlContext` just like the spark-shell. From this prompt, load in the appropriate h2o libraries and attach it to the spark context.

```{scala}
import org.apache.spark.h2o._
val h2oContext = H2OContext.getOrCreate(sc)
```

With this connection made, h2o can make use of Spark as a compute engine as well as access its dataframes. It should also prompt you with an ip adress and a port number. You can visit this endpoint in the browser to see the h2o notebook.

![](http://i.imgur.com/HgZc1O2.png)

## Spark -> H2o -> Rstudio 

We'll run some code in scala first, but you could also do some work in the browser and then still use R for intermediate commands. Let's first create a dataframe in scala and push it to h2o. 

```{scala}
import org.apache.spark.mllib.random.{RandomRDDs => r}
import org.apache.spark.sql.{functions => sf}

def gen_blob() = {
  if(scala.util.Random.nextDouble() > 0.5){
    (0, 
     scala.util.Random.nextDouble()*2,
     scala.util.Random.nextDouble(),
     scala.util.Random.nextDouble()*2)
  }else{
    (1, 
     1 + scala.util.Random.nextDouble(),
     1 + scala.util.Random.nextDouble()*2,
     1 + scala.util.Random.nextDouble())
  }
}

val n = 10000
val rdd = sc.parallelize(1 to n).map(x => gen_blob())

val ddf = rdd.toDF() 
val hdf = h2oContext.asH2OFrame(ddf, frameName = "foobar")
```

Once this is written in the shell, go to Rstudio and load some useful libraries. 

```{r}
library(magrittr)
library(dplyr)
library(ggplot2)
library(h2o)
```

With these libraries loaded, connect to the sparkling-water port we have made before. In this case I am connecting to localhost, but this might also be a functional h2o instance on a spark cluster on the local network.

```{r}
client <- h2o.init(ip = 'localhost', port=54321)
h2o.ls()
rddf <- h2o.getFrame("foobar")
```

You'll notice that this `rddf` is not a normal R dataframe. 

```
> typeof(rddf)
[1] "environment"
```

Because this RDD is small enough you can also import it as a normal R dataframe. 

```{r}
rddf %>% 
  as.data.frame %>% 
  sample_n(1000) %>% 
  plot(title = "random data from sparkling-shell")
```

Not only is this dataframe available in R, but you can also confirm that this frame is usable from the web-ui. 

![](http://i.imgur.com/m6GFC1G.png)

## More ML 

Because we now have access to this h2o frame we can run h2o commands against it from R. H2o will leverage Spark as a computational engine here which means that we now have a method to command large scala and performant machine learning algorithms from R. 

### Autoencoders 

One of the nice features is that you can run modestly complex neural networks with this h2o link. 

```{r}
mod_nn <- h2o.deeplearning(
  x = c("_2", "_3", "_4"),
  training_frame = rddf,
  hidden = c(4,2),
  epochs = 100,
  activation = 'Tanh',
  autoencoder = TRUE
)

features <- h2o.deepfeatures(mod_nn, rddf, layer=2)

pltr_nn <- features %>% 
  as.data.frame %>% 
  cbind(rddf %>% as.data.frame %>% .[1])

colnames(pltr_nn) <- c("l1", "l2", 'label')

ggplot() + 
  geom_point(data=pltr_nn, aes(l1, l2, colour = label), alpha = 0.5) + 
  ggtitle("encoder does a good job of splitting labels via clustering")
```

![](http://i.imgur.com/vkZFchq.png)

### Grid Search 

Another feature of h2o is that it has a very extensive grid search implemented. Let's define a list of hyper-parameters as well as some search criteria. 

```{r}
hyper_params = list(ntrees = c(100, 1000), 
                    max_depth = 1:4, 
                    learn_rate = seq(0.001,0.01),
                    sample_rate = seq(0.3,1))

search_criteria = list(strategy = "RandomDiscrete", max_runtime_secs = 600, 
                       max_models = 100, stopping_metric = "AUTO", 
                       stopping_tolerance = 0.00001, stopping_rounds = 5, seed = 123456)
```

We can use these to do a grid search on the hyperparameters of a gradient boosting machine which tries to predict the label of our generated dataset. You may note that the running the code below can take a bit of time on your machine (if you're doing this on a laptop, prepare for a bit of heat). 

```{r}
gbm_grid <- h2o.grid("gbm", grid_id = "mygrid",
                     x = c("_2", "_3", "_4"), 
                     y = c("_1"), 
                     training_frame = rddf, nfolds = 5,
                     distribution="gaussian", 
                     score_tree_interval = 100, 
                     seed = 123456, 
                     hyper_params = hyper_params,
                     search_criteria = search_criteria)

gbm_sorted_grid <- h2o.getGrid(grid_id = "mygrid", sort_by = "mse")
gbm_sorted_grid@summary_table %>% View
```

You can even select the best model. 

```{r}
best_model <- h2o.getModel(gbm_sorted_grid@model_ids[[1]])
```

## Making Friends with Engineers 

A nice feature of h2o is that it doesn't just make scientists happy, it makes engineers happy as well. H2o can output Plain Old Java Object files which can bring the machine learning algorithm in production quickly. 

```{r}
h2o.download_pojo(best_model, path = "/tmp/", getjar=TRUE)
# [1] "POJO written to: /tmp//mygrid_model_29.java"
```

You can also reach these files via the rest api which is documented [here](https://github.com/h2oai/h2o-3/blob/master/h2o-docs/src/product/howto/POJO_QuickStart.md). 

## Back to the flow 

If you want to see details, you could see all this in Rstudio, but you could also go back to the web-ui to inspect everything we've done here. 

![](http://i.imgur.com/9VVPcUG.png)

<br> 

## PySparkling 

I'm using a bit of hack here by opening a seperate sparling-shell and then connecting another h2o client to it from R. In the python world, this is more smooth. Through the `pysparkling` project you do everything we have done here by just starting a single notebook. More information (as well as install instructions) can be found [here](https://github.com/h2oai/sparkling-water) and [here](http://www.h2o.ai/download/sparkling-water/spark16). 

## Conclusion 

A lot of people will be interested in this pattern, because we've got another scalable way of machine learning. H2o runs on Spark after all. 

You may want to realize that h2o does not need Spark to run though. You can run all these algorithms in parallel on a cluster of machines that are provisioned with just h2o and no Spark. The fact that it can communicate with Spark has benefits but it is not a requirement. The fact that we have an intelligent grid search as well as a method for autoencoding is a welcome addition to the Spark ecosystem tho. 