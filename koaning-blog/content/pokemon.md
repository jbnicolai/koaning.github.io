Title: Pokemon Recommendations, part 1
Date: 2015-05-06

<style>
.background {
  fill: #eee;
}

line {
  stroke: #fff;
}

text.active {
  opacity: 1;
}

rect.active{
	fill-opacity: 1;
}

text{
	opacity: 0.6;
}

.d3text{
	font-size: 6px;
}
</style>
<link href="/theme/css/c3.css" rel="stylesheet" type="text/css">
<script src="/theme/js/c3.js"></script>

> Hint: this page works much better on a pc if you want to enjoy the scale of the visualisations. Mobile phones tend to break; I use this blogpost to explain why d3 is not always a good idea.

The goal of this document is to show off some [d3](http:d3js.org) and to try to explain how you can apply a bit of mathematics to pick an optimal portfolio of pokemon. Why? Pokemon has left a [mark](http://www.dragonflycave.com/obsession.htm) on this world and even though I've never been the biggest fan, it's part of my generation. Everybody that I can relate with knows what pokemon is. This makes a pokemon dataset very nice to play and teach with. It is accessible dataset for a lot of people which makes the math somewhat easier to swallow. 


### Pokemon theory. 

For those not familiar: there exists such thing as a pokemon class. There are grass pokemon, fire pokemon, water pokemon, etc. It is a bit like rock/paper/scissors. For example; plant pokemon are weak against fire pokemon, which in turn are weak against water pokmon which in turn are weak against plant pokemon. 

To give an impression of how complex the pokemon weakness system can be (<a href="http://www.gamesprecipice.com/wp-content/uploads/2014/01/pokemon.png">source</a>): 

<img src="/theme/images/pokemon_graph.png" alt="" width="100%">

A pokemon also has other characteristics that are non specefic to its type. Some are inheretly stronger than others and each pokemon has different properties (some have more health, some have more attack).

The goal of this document is to figure out what an optimal portfolio of pokemon is. After all; a pokemon master can only have 5 pokeballs (prisons for pokemon that you can carry around) and it is unknown which pokemon the opponent has.

### Some Math 

You can google how [damage](http://pokemon.wikia.com/wiki/Damage_Calculation) between pokemon is determined and you can download pokemon information from a reliable [api](http://pokeapi.co/docs/). To compare pokemon I will take the number of turns that a pokemon would be able to stand against an opponent. Because I want to capture that a single pokemon might be able to beat two other pokemon in succession but might be beaten as well this seems like a good metric. 

Note that for the remained of this document I assume that each pokemon will only use it's basic attack and no items will be used during combat. Without these assumption the computation becomes a whole lot harder (maybe even <a href="http://arxiv.org/pdf/1203.1895.pdf">NP-Hard</a>).

This 'turns that a pokemon lasts' metric is defined by the following formulae: 

$$ T_{ij} = \frac{HP_i}{DMG_{ji}} $$ 

where $T_{ij}$ is the number of turns the pokemon $i$ would be able to survive the opponent $j$ if it were to be attacked indefinately, $HP_i$ is the amount of hitpoints that pokemon $i$ has and $DMG_ji$ is the amount of damage a basic attack pokemon $j$ would deal to pokemon $i$. This damage is defined via: 

$$ DMG_{ji} = \frac{2L_j+10}{250} \times \frac{A_j}{D_i} \times w_{ji}$$ 

where $L_a$ is the level of pokemon $a$, $A_a$ is the attack power of pokemon $a$, $D_a$ is the defencive power of pokemon $a$ and $w_{ab}$ is the weakness coefficient between pokemon $a$ and $b$ which is defined by the types of the pokemon. The data that I used for these weaknesses can be found <a href="/theme/data/pokemon_weakness.csv"></a>here.


This is a simplified model where I assume that all pokemon use simple basic attacks continously. Without this assumption the computation becomes a whole lot harder (maybe even [NP-Hard](http://jeremykun.com/2012/03/22/nintendo-np-hard/)).

This is what they look like if you put them in pokedex order. 

<div id="matrix1"></div>

Notice that this graph is assymetric by design. A green cell indicates that the row will win from the column, a yellow colour indicates a draw and a red cell indicates that the row will loose.  

Immediately you should be able to see that a few pokemon will rarely win (this corresponds to a horizontal red line). You don't need the data to know that Diglet, Abra and Magicarp suck, but it is a good confirmation. 

You could also sort this matrix per group, which might allow you to see the effect of the type of pokemon.
<div id="matrix2"></div>

You should be able to see a relationship between pokemon type and damage weakness. 

<script>

var margin = {top: 50, right: 0, bottom: 10, left: 100},
    width = d3.select("#matrix1").node().clientWidth,
    height = d3.select("#matrix1").node().clientWidth;

var types = ['normal','fire','water','electric','grass','ice','fighting','poison','ground','flying','psychic','bug','rock','ghost','dragon'];

var x = d3.scale.ordinal().rangeBands([0, width]),
    z = d3.scale.linear().domain([0, 4]).clamp(true),
    c = d3.scale.linear().domain([-10, 0, 10]).range(["red", "yellow", "green"]),
    t = d3.scale.category20(types);

var svg1 = d3.select("#matrix1").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .style("margin-left", -margin.left + "px")
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var svg2 = d3.select("#matrix2").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .style("margin-left", -margin.left + "px")
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// the first matrix
d3.json("/theme/data/pokemon.json", function(pokemon) {
	var data = pokemon
    	matrix = [],
    	nodes = pokemon.nodes,
    	n = nodes.length;

  // Compute index per node.
  nodes.forEach(function(node, i) {
    node.index = i;
    node.count = 0;
    matrix[i] = d3.range(n).map(function(j) { return {x: j, y: i, z: 0}; });
  });

  // Convert links to matrix; count character occurrences.
  pokemon.links.forEach(function(link) {
    matrix[link.source][link.target].z = -link.value;
    matrix[link.target][link.source].z = link.value;
    matrix[link.source][link.source].z = 0;
    matrix[link.target][link.target].z = 0;
  });

  // Precompute the orders.
  var orders = {
    name: d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].id, nodes[b].id); }),
    group: d3.range(n).sort(function(a, b) { return nodes[b].group_id - nodes[a].group_id; })
  };

  // The default sort order.
  x.domain(orders.name);

  svg1.append("rect")
      .attr("class", "background")
      .attr("width", width)
      .attr("height", height);

  var row1 = svg1.selectAll(".row")
      .data(matrix)
      .enter().append("g")
      .attr("class", "row")
      .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
      .each(row1);

  row1.append("line")
      .attr("x2", width);

  row1.append("text")
      .attr("x", -6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "end")
      .attr("class","d3text")
      .text(function(d, i) { return nodes[i].name; });

  var column1 = svg1.selectAll(".column")
      .data(matrix)
    .enter().append("g")
      .attr("class", "column")
      .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

  column1.append("line")
      .attr("x1", -width);

  column1.append("text")
      .attr("x", 6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "start")
      .attr("class","d3text")
      .text(function(d, i) { return nodes[i].name; });

  function row1(row) {
    var cell = d3.select(this).selectAll(".cell")
        .data(row.filter(function(d) { return d.z; }))
      	.enter().append("rect")
        .attr("class", "cell")
        .attr("x", function(d) { return x(d.x); })
        .attr("width", x.rangeBand())
        .attr("height", x.rangeBand())
        .style("fill-opacity", function(d) { return 0.8; })
        .style("fill", function(d) { return c(d.z)})
        .on("mouseover", mouseover1)
        .on("mouseout", mouseout1);
  }

  function mouseover1(p) {
    d3.selectAll(".row text").classed("active", function(d, i) { 
    	return i == p.y; 
    });
    d3.selectAll(".column text").classed("active", function(d, i) { 
    	return i == p.x; 
    });
  }

  function mouseout1() {
    d3.selectAll("text").classed("active", false);
    d3.selectAll(".cell rect").classed("active", false);
  }

  // The default sort order for matrix 2
  x.domain(orders.group);

  svg2.append("rect")
      .attr("class", "background")
      .attr("width", width)
      .attr("height", height);

  var row2 = svg2.selectAll(".row")
      .data(matrix)
      .enter().append("g")
      .attr("class", "row")
      .attr("transform", function(d, i) { return "translate(0," + x(i) + ")"; })
      .each(row2);

  row2.append("line")
      .attr("x2", width);

  row2.append("text")
      .attr("x", -6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "end")
      .attr("class","d3text")
      .text(function(d, i) { return nodes[i].name; })
      .style("fill", function(d,i){return t(nodes[i].group_id)})
      .style("opacity", 1);;

  var column2 = svg2.selectAll(".column")
      .data(matrix)
    .enter().append("g")
      .attr("class", "column")
      .attr("transform", function(d, i) { return "translate(" + x(i) + ")rotate(-90)"; });

  column2.append("line")
      .attr("x1", -width);

  column2.append("text")
      .attr("x", 6)
      .attr("y", x.rangeBand() / 2)
      .attr("dy", ".32em")
      .attr("text-anchor", "start")
      .attr("class","d3text")
      .text(function(d, i) { return nodes[i].name; })
      .style("fill", function(d,i){return t(nodes[i].group_id)})
      .style("opacity", 1);

  function row2(row) {
    var cell = d3.select(this).selectAll(".cell")
        .data(row.filter(function(d) { return d.z; }))
      	.enter().append("rect")
        .attr("class", "cell")
        .attr("x", function(d) { return x(d.x); })
        .attr("width", x.rangeBand())
        .attr("height", x.rangeBand())
        .style("fill-opacity", function(d) { return 0.8; })
        .style("fill", function(d) { return c(d.z)});
  }
});


</script>

## Optimal Portfolio 

Assuming that when you are walking the plains of Pokemon-land you can't predict which pokemon will attack you, you need to average the performance of the pokemon over all others to be able say something about how good of a choice a pokemon is. The average performance is not enough though because we'd also want to be able to account for the risk that a pokemon encounters it's weakness. A pokemon might perform well on average unless it meets its ultimate foe. 


In financial mathematics a similar problem occurs with the valuation of a stock portfolio. The stock might perform well on average but it will most likely have a lot of volatility. 

For this dataset we calculate two values per pokemon: 

<li>$\mu_p$: the average performance of the assosciated pokemon </li>
<li>$\sigma_p$: the variance (or risk) of the assosciated pokemon </li>

$$\mu_i = \frac{\sum_{j=1}^N T_{ij}}{N} $$
$$\sigma_i = \sqrt{\frac{\sum_{j=1}^N (T_{ij} - \mu_i)^2}{N - 1}} $$ 

The top 5 performning pokemon according to $T_{ij}$ are: 

	                 mu      sigma
	name                          
	Mewtwo     2.827446   5.332813
	Lapras     2.947499   6.977950
	Dragonite  3.099368  11.387448
	Snorlax    3.267974   3.917765
	Rhydon     3.341182  12.839635

Notice that the $\sigma_p$ values vary. If we plot these values of all pokemon with a positive $\mu_p$ we can see that a disparity exists. 

<img src="/theme/images/pokemon_volatility.png" alt="">

Some pokemon are more efficient in the return/volatility ratio than others. If I now select all pokemon that have a high return but a low volatility I end up with a different top 5: 

	                 mu    sigma
	Wigglytuff 2.296484 3.173598
	Snorlax    3.267974 3.917765
	Exeggutor  2.349300 5.135687
	Mewtwo     2.827446 5.332813
	Muk        2.370720 5.680507

So yeah, turns out that you can apply the <a href="http://en.wikipedia.org/wiki/Capital_asset_pricing_model">CAPM</a> model to pokemon. Nice!