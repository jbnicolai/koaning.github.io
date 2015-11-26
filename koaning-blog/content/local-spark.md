Title: Local Spark
Date: 2015-03-18

<p><img class="center"src="/theme/images/local-spark.png" width="50%"/></p>


<p><a href="https://spark.apache.org">Spark</a> is cool. It's like writing code and never having to worry about parallelism. This is nice if you have a cluster but also if your local machine has multiple cores and sufficient memory. No need for extra packages or workarounds, the api will handle the scaling automatically.</p>

<h3>Show of force</h3>

<p>Suppose I run the following parallel spark code;</p>

<pre><code>val count = spark.parallelize(1 to 100000000).map{i =&gt;
  val x = Math.random()
  val y = Math.random()
  if (x*x + y*y &lt; 1) 1 else 0
}.reduce(_ + _)
</code></pre>

<p>The moment that I run this code, the <code>top</code> command in my terminal will show that I'm almost reaching the full 800% of 8-core mac cpu power.</p>

<p><img src="http://imgur.com/ec2m4lH.png" alt="" /></p>

<p>That's 8x more computing power that's available to you as a programmer just by following the standard spark api. No multicore library needed.</p>

<h3>More numbers</h3>

<p>To show the potential gain in performance I've set up two benchmarks to compare local spark to local python. One will count bins from a uniform distribution through and the other will aggregate a large data file. I will use the ipython notebook <code>%%time</code> magic and the following scala function to measure the performance:</p>

<pre><code>def time[A](f: =&gt; A) = {
  val s = System.nanoTime
  val ret = f
  println("time: "+(System.nanoTime-s)/1e6+"ms")
  ret
}
</code></pre>

<h3>Binning random numbers</h3>

<h5><b>Python Code 3min 23s</b></h5>

<p>The quickest way for python without extra hassle involves using vectorized numpy.</p>

<pre><code>[len(i) for i in pd.cut(np.random.uniform(0,1,10000000),100)]
</code></pre>

<h5><b>Scala Spark Code 25.2s</b></h5>

<p>Notice that the scala spark code hardly has to be verbose. You only need to appreciate the functional method chaining.</p>

<pre><code>sc.parallelize(1 to 100000000)
  .map(_ =&gt; scala.util.Random.nextDouble())
  .map(x =&gt; (x - x % 0.01, 1))
  .reduceByKey( (a,b) =&gt; a + b )
  .collect()
</code></pre>

<h5><b>Fast Scala Spark Code</b></h5>

<p>Spark can even be quicker. The documentation is not entirely up to par but there is support for creating random variables instead of casting random variables as an intermediate <code>.map</code> step. It's like using <code>numpy</code> instead of normal python but in spark with scala.</p>

<pre><code>import org.apache.spark.SparkContext
import org.apache.spark.mllib.random.RandomRDDs._
uniformRDD(sc, 100000000, 10).sum()
</code></pre>

<h3>Handling large files</h3>

<p>I took a 1.1Gb .csv file from my local drive to do some benchmarks as well. Here's a small hint at performance for just opening the file and doing a linecount:</p>

<h5><b>Python 13.3 s</b></h5>

<pre><code>df = pd.read_csv("/some/path/largefile.csv")
df.shape
</code></pre>

<h5><b>Scala Spark 1.8s</b></h5>

<pre><code>val txtfile = sc.textFile("/some/path/largefile.csv")
txtfile.count()
</code></pre>

<h5><b>Bash 1.0s</b></h5>

<pre><code>$ time wc -l /some/path/largefile.csv
real    0m1.002s
user    0m0.786s
sys     0m0.213s
</code></pre>

<h3>Aggregation</h3>

<p>Aggregation would make a better indication of performance in a real life scenario. Here I aggregate the sum on the third column of a file and show the top 100.</p>

<h5><b>Python 11.1s</b></h5>

<p>For the python code I excluded the 13.3s needed to load in the file.</p>

<pre><code>df.groupby(['col3']).count().sort("col3").head(100)['col3']
</code></pre>

<h5><b>Scala Spark 4.6s</b></h5>

<pre><code>val txtfile = sc.textFile("/some/path/largefile.csv")
txtfile.map(line =&gt; line.split(" ")(3)).map( x =&gt; (x, 1) ).reduceByKey((a,b) =&gt; a + b)
  .map(item =&gt; item.swap)
  .sortByKey(false, 1)
  .map(item =&gt; item.swap)
  .take(100)
</code></pre>

<h1>Conclusion</h1>

<p>Benchmarks are always stenchmarks because there are ways to get more juice out of pandas. Still, the numpy/pandas stack of python is one of the most performant pieces of python and with some basic examples spark seems to be outperforming without any trouble.</p>

<p>The api of numpy and pandas still seems more convenient for middle sized data. For bigger datasets, spark provides an easy enough api that is fast and flexible. I've only scratched the surface here as spark also offers scalable machine learning algorithms as well as graph analysis tools.</p>

<p>Did I mention you can also run all of this on a Hadoop cluster? Profit.</p>
