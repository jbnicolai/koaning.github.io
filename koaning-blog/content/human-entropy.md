Title: Human Entropy
Date: 2017-01-26

<script src="/theme/js/d3.min.js"></script>
<script src="/theme/js/redux.js"></script>
<script src="/theme/js/lazy.js"></script>
<script src="/theme/js/lodash.js"></script>
<script src="/theme/js/base-charts.js"></script>

<style>

.bar {
  fill: steelblue;
}

.bar:hover {
  fill: brown;
}

.axis {
  font: 10px sans-serif;
}

.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.x.axis path {
  display: none;
}

</style>

Let's do an experiment to see if humans perhaps can generate random numbers effectively. Please click the heads/tails button as randomly as you can. You may also use the 1 (heads) or 0 (tails) keys on your keyboards (which probably is a whole lot faster).

<style>
  button.btn{
    background-color: white;
    border-color: black;

  }
</style>
<button class="btn btn-default btn-block btn-lg" id="heads">Heads</button>
<button class="btn btn-block btn-lg" id="tails">Tails</button>

You've currently generated <span class="num_items">0</span> numbers, please ensure that you got about 100 before moving on. 

<div id="container">
  <div class="markov1"></div>
  <div class="markov2"></div>
  <div class="markov3"></div>
  <div class="markov4"></div>
  <div class="markov5"></div>
</div>

<script>
const counter = (state = [], action) => {
  switch (action.type) {
    case '0':
      return _.flatten([state, 0])
    case '1':
      return _.flatten([state, 1])
    case 'reset':
      return []
    default:
      return state;
  }
}; 

const { createStore } = Redux;
const store = createStore(counter);

function calcAllPairs(len){
  var args = [ len > 0 ? ["1", "0"] : []]
  for (var i = 0; i < len - 1; i++) {
    args.push([",1", ",0"]);
  }
  
  var base = _.reduce(args, function(a,b){
    return _.flatten(_.map(a, function(x){
      return _.map(b, function(y){
        return x.concat([y]);
      });
    }), true);
  }, [[]]);

  return base.map(function(d){ return [d, 0]})
}
const PAIRS = [0,1,2,3,4].map(calcAllPairs)
  .map(function(d){return _.object(d)})

const render = function(){
  d3.select('.num_items').text(store.getState().length);
};

const markov = function(rank){
  return Lazy(store.getState())
  .consecutive(rank)
  .countBy(function(d){return d})
  .toArray()
}

const renderPlot = function(cssLoc, rank){
  if(store.getState().length < rank){
    return
  }
  const state_map = _.extend({}, PAIRS[rank], _.object(markov(rank)))
  const mk = Object.keys(state_map).map(
    function(k){return [k, state_map[k]]}
  )
  const sum = mk.reduce(function(x,y){return x + y[1]}, 0)
  barChart(cssLoc, mk.map(function(d){return [d[0], d[1]/sum]}))
}

store.subscribe(render);
store.subscribe(markov);
store.subscribe(function(){renderPlot(".markov1", 1)});
store.subscribe(function(){renderPlot(".markov2", 2)});
store.subscribe(function(){renderPlot(".markov3", 3)});
store.subscribe(function(){renderPlot(".markov4", 4)});
store.subscribe(function(){renderPlot(".markov5", 5)});

render();

d3.select("body").on("keydown", function(){
  const type = ({ 49: '1', 48: '0'})[d3.event.keyCode]
  store.dispatch({'type': type})
})

d3.select("button#heads").on("click", function(){
    store.dispatch({ type: '1' });
})

d3.select("button#tails").on("click", function(){
    store.dispatch({ type: '0' });
})

// setInterval(function(){ 
//   if(Math.random() < 0.5){
//     store.dispatch({ type: '1' });
//   }else{
//     store.dispatch({ type: '0' });
//   }
// }, 100)

</script>
