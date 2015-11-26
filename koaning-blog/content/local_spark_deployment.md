# Local SparkR Deployment Guide 

In this small guide we'll download and install spark for local development. This includes PySpark and Scala Spark with notebook support as well as SparkR with Rstudio support. 

### Step 1 

Download spark, [here](http://www.apache.org/dyn/closer.cgi/spark/spark-1.4.1/spark-1.4.1-bin-hadoop2.6.tgz). Unzip it, remember where you put it. 

### Step 2 

If you don't have the tools just yet, the following will download pip, jupyter and rstudio. 

```

```

### Step 3

Go to the unzipped spark folder and make sure that the following commands at least work;

```
./bin/spark-shell 
./bin/pyspark
./bin/sparkr --driver-memory 5g
```

### Step 4: PySpark 

The python version that comes with spark is modern enough to get the notebook working. 

```
IPYTHON_OPTS="notebook" ./bin/pyspark
```

### Step 5: ScalaSpark

Not there yet. Should try: https://github.com/tribbloid/ISpark/issues/12

```
ipython notebook --KernelManager.kernel_cmd='["/Users/code/Downloads/spark-1.4.1-bin-hadoop2.6/bin/spark-submit", "--master", "spark://codes-MacBook-Pro.local:7077", "--driver-memory", "2G", "--class", "org.refptr.iscala.IScala", "/Users/code/Downloads/IScala-0.1/lib/IScala.jar", "--parent"]'

```

### Step 6: SparkR with Rstudio

You might need to make sure [this](http://databricks.gitbooks.io/databricks-spark-knowledge-base/content/troubleshooting/port_22_connection_refused.html) is set before taking further steps. 

> You need to enable "Remote Login" for your machine. From System Preferences, select Sharing, and then turn on Remote Login.

Then run; 

```
/Users/code/Downloads/spark-1.4.1-bin-hadoop2.6/sbin/start-all.sh -c 6 -m 4g --executor-memory 8G
```

> No need to run the above part.

Start Rstudio and fill in the following in an Rscript. 

```
spark_link <- "spark://codes-MacBook-Pro.local:7077" 
spark_path <- "/Users/code/Downloads/spark-1.5.0-bin-hadoop2.6"
.libPaths(c(.libPaths(), paste0(spark_path, '/R/lib'))) 
Sys.setenv(SPARK_HOME = spark_path) 
Sys.setenv(PATH = paste(Sys.getenv(c('PATH')), paste0(spark_path, '/bin'), sep=':')) 
library(SparkR) 
library(ggplot2)
library(magrittr)

sc <- sparkR.init("local[2]", "SparkR", spark_path, list(spark.executor.memory="8g"))
sqlContext <- sparkRSQL.init(sc) 
```

Run it and you guessed it. SparkR is now ready to use with Rstudio.