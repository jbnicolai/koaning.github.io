Title: console.lol(kittens)
Date: 2013-01-17

> For all this to work, you'll need a modern Chrome browser.

### Two Moments of Console

It all started with something that seemed like a bug. Imagine the following javascript code;

	object = {list:[1]};
	console.log(object);
	object.list.push(1);

What is the length of the list in the object? An oddity in chrome's console is that you will first see;

	Object {list: Array[1]}

And only apon expanding will you see that the object contains the updated list;

	list: Array[2]

This is because the initial display is generated when the console first logs it. After expanding, it loads all of the current object's properties, and if the properties have changed in between logging it and opening it, it will show different values. When the object is expanded you will see a light-blue 'i' icon that you can hover over, Chrome will explain this to you.

This was completely new to me, I decided it might be useful to explore how the console should behave and what else it might do that I was not aware of.

### console.css

Did you know you can send css-style to your chrome console?

	console.log("%c Red text.","color: red;")

Open up devtools (CMD+ALT+J) and try these commands;

<button style="margin-left:45%;" onClick='console.log("%c Red text.","color: red;")'>Try this.</button>

	console.log("%c Green text.","color: green;")

<button style="margin-left:45%;" onClick='console.log("%c Green text.","color: green;")'>Try this.</button>

	console.log("%cDont make me angry. You wont like me when Im angry.",
				"color: green; font-size:25px;font-weight: bold;")

<button style="margin-left:45%;" onClick='console.log("%cDont make me angry. You wont like me when Im angry.","color: green; font-size:25px;font-weight: bold;")'>Try this.</button>

If you want full controll of your testing output this might come in very handy. I have had plenty of nasty clients who console.log anything and everything. If I want to use such a console, I can use a color code to distinguish what my print outputs are.

You can go completely nuts with any css style you want. If you want to annoy a developer you can fog the console with the following snippet;

	var _log = console.log;
	console.log = function() {
	  _log.call(console, '%c' +[].slice.call(arguments).join(' '), 'color:transparent;text-shadow:0 0 2px rgba(0,0,0,.5);');
	};

I purposefully did not add a try this button. This changes the original console.log function such that everything will be printed out blurry. This code will break the rest of the code in this blogpost.

### console.img 

We can add css, that means the console can get a little bit freaky. How about a background image? 

	console.log("lolcat %c", "background: url(http://i.imgur.com/m3PtyuR.jpg); padding-right: 300px; font-size: 171px; text-align: center")

<button style="margin-left:45%;" onClick='	console.log("lolcat %c", "background: url(http://i.imgur.com/llWeVXf.png); padding-right: 300px; font-size: 171px; text-align: center")'>Try this.</button>

We can even have moving images, gif anyone? 

	console.log("moving kitten %c", "background: url(http://i.imgur.com/TanUtXo.gif); padding-right: 300px; font-size: 250px; text-align: center")

<button style="margin-left:45%;" onClick='console.log("moving kitten %c", "background: url(http://i.imgur.com/TanUtXo.gif); padding-right: 300px; font-size: 250px; text-align: center")'>Try this.</button>

<h3> console.table </h3> 
<p> The console doesn't just allow for logs, it also allowed for tables.</p> 

<pre><code class="language-javascript">function Cat(firstName, petName, food){
this.firstName = firstName;
this.petName = petName;
this.food = food;
}

var cats = {};
cats.cat1 = new Cat('Bigglesworth','Smuffy','fish')
cats.cat2 = new Cat('Tom','Not Jerry','mice')
cats.cat3 = new Cat('Sylvester','Tweety','birds')
 
console.table(cats);
</code></pre>

<script type="text/javascript">
function Cat(firstName, petName, food){
    this.firstName = firstName;
    this.petName = petName;
    this.food = food;
}
 
var cats = {};
cats.cat1 = new Cat('Bigglesworth','Smuffy','fish')
cats.cat2 = new Cat('Tom','Not Jerry','mice')
cats.cat3 = new Cat('Sylvester','Tweety','birds')


function randColors(){
function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.round(Math.random() * 15)];
    }
    return color;
}

var colors = []
var str = ""
for (var i = 0; i < 30; i++) {
	str += '%c '
	var color = getRandomColor()
	colors.push( 'background:' + color )
};

console.log("New line of random colors:")
console.log.apply(console, [str].concat(colors))
}

function indicator( num ){  
    // +1 would be green, -1 would be red 
    var letters = '0123456789ABCDEF'.split(''),
        greenIdx = Math.max( Math.min( Math.round( 8*num + 8 ),15),0),
        greenVal = letters[ greenIdx ];
        redIdx = Math.max( Math.min( Math.round(-8*num + 8 ),15),0),
        redVal = letters[ redIdx ];
    return '#'+redVal+redVal+greenVal+greenVal+'06'
}

var data = [ 0 ] ;

function plotColors(){  
    if( data.length>30){
        data.shift( )
    }
    var new_number = data[ data.length - 1] + Math.random() - 0.5
    data.push( Math.min( Math.max( new_number, -1), 1 ) )

    var colors = [];
    var str = "";

    for (var i = 0; i < data.length; i++) {
        str += '%c ';
        var color = indicator( data[i] );
        colors.push( 'background:' + color + ';')
    };
    console.clear();
    console.log("Performance metrics :" + data[ data.length - 1 ]);
    console.log.apply(console, [str].concat(colors));
}
</script> 

<button style="margin-left:45%;" onClick='console.table(cats);'>Try this.</button>

<p> Note that the table is able to sort items alphabetically for you. </p> 

<h3> console.count </h3> 

<p>The console can also be used to keep track of how often a function is called. This is useful becauase it removes the need to build your own counters while debugging.</p>

<pre><code class="language-javascript">function scream(){
	console.log('ice cream')
	console.count('scream')
}
</code></pre>

<button style="margin-left:45%;" onClick="console.log('ice cream');console.count('scream')">Try this.</button>

<h3>Console Edit Document</h3>

<p>This line of code will allow you to change to website you are watching as if it were a text document. </p>

<pre><code class="language-javascript">document.body.contentEditable = true;
</code></pre>

<p>Just hover over any text on the page, click it and type. This feature was implemented by Microsoft to allow developers to make rich text editors on the web. The funniest thing is that this actually turns on the spelling check as you are typing on the webpage.</p>

<button style="margin-left:45%;" onClick='document.body.contentEditable = true;'>Try this.</button>


<h3> console.viz </h3> 

<p> You shouldn't want a visualisation in your console but you could try and build one. By using `console.log.apply` we can control the css style of independant characters in a string. We will be using the empty character `" "` such that we can give it a background-color that can show visual aspects. </p> 

<pre><code class="language-javascript">console.clear() 

function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.round(Math.random() * 15)];
    }
    return color;
}

var colors = []
var str = ""
for (var i = 0; i < 30; i++) {
	str += '%c '
	var color = getRandomColor()
	colors.push( 'background:' + color )
};

console.log("New line of random colors:")
console.log.apply(console, [str].concat(colors))
</code></pre> 

<button style="margin-left:45%;" onClick='randColors()'>Try this.</button>

<p> This just shows random colors, but we can assign meaning to these colors. With a little bit of javascript we could simulate some streaming data going in; </p> 

<pre><code class="language-javascript">function indicator( num ){
	// +1 would be green, -1 would be red 
	var letters = '0123456789ABCDEF'.split(''),
		greenIdx = Math.max( Math.min( Math.round( 8*num + 8 ),15),0),
		greenVal = letters[ greenIdx ];
		redIdx = Math.max( Math.min( Math.round(-8*num + 8 ),15),0),
		redVal = letters[ redIdx ];
	return '#'+redVal+redVal+greenVal+greenVal+'06'
}

var data = [ 0 ] ;

function plotColors(){
	if( data.length>30){
		data.shift( )
	}
	var new_number = data[ data.length - 1] + Math.random() - 0.5
	data.push( Math.min( Math.max( new_number, -1), 1 ) )
	
	var colors = [];
	var str = "";
	yyyy
	for (var i = 0; i < data.length; i++) {
		str += '%c ';
		var color = indicator( data[i] );
		colors.push( 'background:' + color + ';')
	};
	console.clear();
	console.log("Performance metrics :" + data[ data.length - 1 ]);
	console.log.apply(console, [str].concat(colors));
}

var interval = setInterval( plotColors, 200);
// to stop it : clearInterval(interval)
</code></pre> 

<button style="margin-left:45%;" onClick='var interval = setInterval( plotColors, 200)'>Try this.</button>

<p>Honestly though, as fun as it may be, I think that if you are going make a visualisation, you should refrain from building it in your console. </p> 

