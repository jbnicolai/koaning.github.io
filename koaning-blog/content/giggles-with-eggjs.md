Title: Giggles with egg.js
Date: 2015-05-01

<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
<script type="text/javascript" src="https://cdn.rawgit.com/mikeflynn/egg.js/master/egg.min.js"></script>

I have a soft spot for fun yet unproductive code and it occured to me that I didn't yet place an easter egg on my website. Then I found [egg.js](http://thatmikeflynn.com/egg.js/). It allows you to make easter eggs on your website similar to something [vogue](http://www.vogue.co.uk/) did (go there and type the Konami code for a giggle).

If you know what easter eggs are, you know what to do with the following table: 

<img id="egg0" src="/theme/images/giggles_egg_0.gif" alt="" style="display: none;">
<img id="egg1" src="/theme/images/giggles_egg_1.gif" alt="" style="display: none;">
<img id="egg2" src="/theme/images/giggles_egg_2.gif" alt="" style="display: none;">
<img id="egg3" src="/theme/images/giggles_egg_3.gif" alt="" style="display: none;">
<img id="egg4" src="/theme/images/giggles_egg_4.jpg" alt="" style="display: none;">

<table>
	<thead>
	  <tr>
	     <th>Code</th>
	     <th>Effect</th>
	  </tr>
	 </thead>
	<tr>
		<td><i class="fa fa-arrow-up"></i><i class="fa fa-arrow-down"></i><i class="fa fa-arrow-up"></i><i class="fa fa-arrow-down"></i></td>
		<td>falling cat</td>
	</tr>
	<tr>
		<td><i class="fa fa-arrow-right"><i class="fa fa-arrow-left"><i class="fa fa-arrow-right"><i class="fa fa-arrow-left"><i class="fa fa-arrow-right"><i class="fa fa-arrow-left"></td>
		<td>happy dog</td>
	</tr>
	<tr>
		<td><i class="fa fa-arrow-left"><i class="fa fa-arrow-right"><i class="fa fa-arrow-left"><i class="fa fa-arrow-right"><i class="fa fa-arrow-left"><i class="fa fa-arrow-right"></td>
		<td>dancing cat</td>
	</tr>
	<tr>
		<td><i class="fa fa-arrow-down"><i class="fa fa-arrow-up"><i class="fa fa-arrow-down"><i class="fa fa-arrow-left"><i class="fa fa-arrow-down"></i></td>
		<td>approval</td>
	</tr>
</table>

<br> 

Hint, there is one code that is not on the table. Stay sassy internet.

<script>
var egg0 = new Egg("up,down,up,down", function() {
	jQuery('#egg0').fadeIn(500, function() {
		window.setTimeout(function() { jQuery('#egg0').hide(); }, 2000);
	});
}).listen();
var egg1 = new Egg("right,left,right,left,right,left", function() {
	jQuery('#egg1').fadeIn(500, function() {
		window.setTimeout(function() { jQuery('#egg1').hide(); }, 2000);
	});
}).listen();
var egg2 = new Egg("left,right,left,right,left,right", function() {
	jQuery('#egg2').fadeIn(500, function() {
		window.setTimeout(function() { jQuery('#egg2').hide(); }, 2000);
	});
}).listen();
var egg3 = new Egg("down,up,down,left,down", function() {
	jQuery('#egg3').fadeIn(500, function() {
		window.setTimeout(function() { jQuery('#egg3').hide(); }, 2000);
	});
}).listen();
var egg4 = new Egg("up,up,down,down,left,right,left,right,b,a", function() {
	jQuery('#egg4').fadeIn(500, function() {
		window.setTimeout(function() { jQuery('#egg4').hide(); }, 2000);
	});
}).listen();
</script>
