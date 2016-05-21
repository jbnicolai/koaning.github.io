Title: D3 as a Templating Tool
Date: 2014-04-18

<style>
	path {
		stroke: steelblue;
		stroke-width: 1;
		fill: none;
	}
	.catblock{
		background-color: rgb(239, 245, 250);
		margin: 5px;
	}

</style>

When you want to generate an html file client side you usually do that via a framework. If you are doing something light weight then setting up angular/backbone/spine/ember can be a bit overdoing it. Sometimes you just need a templating tool and nothing more. In this blogpost I would like to argue that d3 might be a better alternative to underscore/jquery. 

<br>
<h2> Generating a Table. </h2>
<br>

Let's start with creating a simple table. Suppose we want to generate a common table from the following JSON data; 

<pre><code class="language-python">var payments = [
	    {"id":"A001", "price":4.95, "client":"Cohn Jarmac", "paid":true},
	    {"id":"A002", "price":1.95, "client":"Buckerzerg", "paid":true},
	    {"id":"A003", "price":3.15, "client":"Jeve Stobs", "paid":false},
	    {"id":"B021", "price":6.25, "client":"Gill Bates", "paid":true},
	    {"id":"B022", "price":1.15, "client":"Gill Bates", "paid":true},
	    {"id":"B023", "price":3.45, "client":"Buckerzerg", "paid":false},
	    {"id":"A004", "price":4.95, "client":"Buckerzerg", "paid":true}
]
</code></pre>

<p> We then define a method in javascript with d3 that will allow us to render this; </p>

<pre><code class="language-javascript">function d3table( data, selector ){
	    var table = d3.select(selector).append("table").attr("class","table"),
		    th = table.append("tr");

    	for(var i in Object.keys(data[0]);){
    	    th.append("td").append("b").text(Object.keys(data[0])[i]);
    	}
    
    	for(var row in data;){
    	    var tr = table.append("tr");
        for(var td in data[row])
    	        tr.append("td").text(data[row][td]);
    	    }
}
</code></pre>

<p> This will simply generate a table; </p>

<div id="table"></div>

<h2> Adding logic. </h2>

<p> You could choose to add logic as you see fit; </p>

<pre><code class="language-javascript">function d3tableWithLogic( data, selector ){
    var table = d3.select(selector).append("table").attr("class","table"),
        th = table.append("tr"),
        check = &lt;i class="fa fa-check"&gt;&lt;/i&gt;;

    for(var i in Object.keys(data[0])){
        th.append("td").append("b").text(Object.keys(data[0])[i]);
    }

    for(var row in data){
        var tr = table.append("tr")
        for( var td in data[row] )
            if( td == "paid" ){
                data[row][td] ? tr.append("td").html(check) : tr.append("td").text('');
            }else if( td == "price"){
                tr.append("td").text("$" + data[row][td]);
            }else{
                tr.append("td").text(data[row][td]);
            }
    }
}
</code></pre>

<p> This will generate a table with more logic; </p>

<div id="table2"></div>

<p> Already I find this less time consuming then defining my own template through underscore and more clean than writing it all with jquery statement. </p>

<h2> DRY and Combine. </h2>

<p> D3 is very enjoyable to work with if you are used to functional programming but being able to add events to your created html functionally as you are generating them is a godsend. Let's assume that we want to make a dashboard for cats and that we receive the following data;</p>

<pre><code class="language-python">var cats = [
    {id:1, name:"Biggles", status: "hungry" },
    {id:2, name:"Nomnom", status: "hungry" },
    {id:3, name:"Mia", status: "haz cheezburgr" },
    {id:4, name:"Jim", status: "hates dawg" },
    {id:5, name:"Alice", status: "hates dawg" },
    {id:6, name:"Mr.Kitty", status: "hates dawg" },
    {id:7, name:"George", status: "found mouse" },
    {id:8, name:"Bubbah", status: "chasing lazrz" }
]
</code></pre>

<p> We can use all the classes given to us by bootstrap. Whatsmore, we have <a href="http://lorempixel.com">lorempixel</a> at our disposal to generate cat images. I will also use a random generator to generate a svg path so that you can also see how elegant d3 can create a dashboard for us. </p>

<p> First I'll make a javascript function that can attach an image to a d3 element. </p> 

<pre><code class="language-javascript">function attachCatImage( img_link, d3element ){
    d3element.append("div")
        .attr("class","col-xs-6")
        .append("img")
        .attr("src", img_link ) 
        .attr("class","img-circle")
        .style("margin-top","-15");
}
</code></pre>

<p> Note that I can add as much interaction to this element as I wish. Just like a templating engine I am able to define elements that I want for later use. A similar thing can be made for sparkline. I will use random data here, but it could have also been passed along to the function instead. </p>

<pre><code class="language-javascript">function randSparkline( d3element ){
    var height = d3element.attr("height"),
        width = d3element.attr("width"),
        graph = d3element.append("svg:svg")
            .attr("width", width)
            .attr("height", height);

    var data = d3.range(0,21).map(function(d){return Math.random()});

    var x = d3.scale.linear().domain([0, data.length]).range([0, width]);
    var y = d3.scale.linear().domain([0, 1]).range([0, height]);

    var line = d3.svg.line()
        .x(function(d,i) { return x(i); })
        .y(function(d) { return y(d); })

    var html = "&ltsvg height=" + height + " width=" + width + ">"
    html += '&ltpath d=' + line(data) + '/>&lt/svg>'

    return html
}
</code></pre>

<p> Notice that by using this construction, the generated svg will always fit precisely in the parent container. With these two functions, creating a small dashbord will suddenly feel like scripting; </p>

<h5>Javascript</h5>
<pre><code class="language-javascript">function kittenDashboard( data, selector ){
var row = d3.select(selector).append("div").attr("class","row"),
    api_link = 'http://lorempixel.com/100/100/cats/'; 

for( c in data ){
    var catSlot = row.append("div")
        .attr("class","col-xs-6")

    var title = catSlot.append("h3").text(data[c].name)
        .classed({"text-center":true})
    
    var catInfo = catSlot.append("div")
        .classed({'row':true, 'catblock': true});

    var imgslot = attachCatImage( api_link + data[c].id, catInfo )

    var infoslot = catInfo.append("div")
        .attr("class","col-xs-6")

    infoslot.append("h5").text("youtube hits:")

    var sparkslot = infoslot.append("div")
        .attr("width", 140)
        .attr("height", 30)
    
    sparkslot.html(randSparkline(sparkslot));

    var quote = infoslot.append("h6")
        .text( data[c].status)
    
	}
}</pre></code> 

<h5>Css</h5>
<pre><code class="language-css">path {
	stroke: steelblue;
	stroke-width: 1;
	fill: none;
}
.catblock{
	background-color: rgb(239, 245, 250);
	margin: 5px;
}
</pre></code> 

<p> The <b>kittenDashboard</b> function is long but it's an improvement compared to the underscore templating engine because all the code is now strictly in javascript and not an html/js hybrid. Also, you might be able to split the function into smaller code pieces depending on how many of these elements might reappear in your app. </p> 

<h2> The Result </h2>
<div id="catdb"></div>

<h2> Extra </h2> 
<p> In the end it all comes down to taste. I enjoy writing as much as possible in d3 because it is very clear to me and it allows to me script a webpage in a matter of minutes. A developer with more backbone experience might be confused by the functional syntax and might prefer the underscore templating system. Still, if you take into account how easy it is to add events via D3, I'd still say D3 is a winner here. </p> 

<p> It might be worth noting that there are many live examples using these techniques, some of which even go as far that they <b>only</b> use d3 to generate the html on the webapp. I can recommend looking at <a href="http://geojson.io">geojson.io</a> if you need more convincing. </p> 
<br><br><br><br><br>

<!-- Modal -->
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">Modal title</h4>
      </div>
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>

<script src="/theme/js/d3.min.js"></script>
<script src="/theme/js/lodash.js"></script>

<script>

	var payments = [
		{"id":"A001", "price":4.95, "client":"Cohn Jarmac", "paid":true},
		{"id":"A002", "price":1.95, "client":"Buckerzerg", "paid":true},
		{"id":"A003", "price":3.15, "client":"Jeve Stobs", "paid":false},
		{"id":"B021", "price":6.25, "client":"Gill Bates", "paid":true},
		{"id":"B022", "price":1.15, "client":"Gill Bates", "paid":true},
		{"id":"B023", "price":3.45, "client":"Buckerzerg", "paid":false},
		{"id":"A004", "price":4.95, "client":"Buckerzerg", "paid":true}
	]

	function d3table( data, selector ){
		var table = d3.select(selector).append("table").attr("class","table");
		var th = table.append("tr")

		for(var i in Object.keys(data[0])){
			th.append("td").append("b").text(Object.keys(data[0])[i])
		}

		for(var row in data){
			var tr = table.append("tr")
			for( var td in data[row] )
				tr.append("td").text( data[row][td] )
		}
	}

	function d3tableWithLogic( data, selector ){
		var table = d3.select(selector).append("table").attr("class","table");
		var th = table.append("tr")

		for(var i in Object.keys(data[0])){
			th.append("td").append("b").text(Object.keys(data[0])[i])
		}

		for(var row in data){
			var tr = table.append("tr")
			for( var td in data[row] )
				if( td == "paid" ){
					data[row][td] ? tr.append("td").html('<i class="fa fa-check"></i>') : tr.append("td").text('');
				}else if( td == "price"){
					tr.append("td").text( "$" + data[row][td] )
				}else{
					tr.append("td").text( data[row][td] )
				}
		}
	}

	d3table( payments, '#table')
	d3tableWithLogic( payments, '#table2')

	var cats = [
		{id:1, name:"Biggles", status: "hungry" },
		{id:2, name:"Nomnom", status: "hungry" },
		{id:3, name:"Mia", status: "haz cheezburgr" },
		{id:4, name:"Jim", status: "hates dawg" },
		{id:5, name:"Alice", status: "hates dawg" },
		{id:6, name:"Mr.Kitty", status: "hates dawg" },
		{id:7, name:"George", status: "found mouse" },
		{id:8, name:"Bubbah", status: "chasing lazrz" }
	]

	function randSparkline( d3element ){
		var height = d3element.attr("height"),
			width = d3element.attr("width"),
			graph = d3element.append("svg:svg").attr("width", width).attr("height", height);

		var data = d3.range(0,21).map(function(d){return Math.random()});

		var x = d3.scale.linear().domain([0, data.length]).range([0, width]);
		var y = d3.scale.linear().domain([0, 1]).range([0, height]);

		var line = d3.svg.line()
			.x(function(d,i) { return x(i); })
			.y(function(d) { return y(d); })

		var html = "<svg height=" + height + " width=" + width + ">"
		html += '<path d=' + line(data) + '/></svg>'
	
		return html
	}

	function attachCatImage( img_link, d3element ){
		d3element.append("div")
			.attr("class","col-xs-6")
			.append("img")
			.attr("src", img_link ) 
			.attr("class","img-circle")
			.style("margin-top","-15");
	}

	function kittenDashboard( data, selector ){
		var row = d3.select(selector).append("div").attr("class","row"),
			api_link = 'http://lorempixel.com/100/100/cats/'; 

		for( c in data ){
			var catSlot = row.append("div")
				.attr("class","col-xs-6")

			var title = catSlot.append("h3").text(data[c].name)
				.classed({"text-center":true})
			
			var catInfo = catSlot.append("div")
				.classed({'row':true, 'catblock': true});

			var imgslot = attachCatImage( api_link + data[c].id, catInfo )

			var infoslot = catInfo.append("div")
				.attr("class","col-xs-6")

			infoslot.append("h5").text("youtube hits:")

			var sparkslot = infoslot.append("div")
				.attr("width", 140)
				.attr("height", 30)
			
			sparkslot.html(randSparkline(sparkslot));

			var quote = infoslot.append("h6")
				.text( data[c].status)
			
		}
	}

	kittenDashboard( cats, '#catdb')
	</script>
	<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
