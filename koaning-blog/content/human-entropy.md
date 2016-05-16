Title: Human Entropy
Date: 2016-05-20

<link rel="stylesheet" type="text/css" href="/theme/css/c3.css"></link>
<style>
  button.btn{
    background-color: white;
    border-color: black;
  }
</style>
<script src="/theme/js/d3.min.js"></script>
<script src="/theme/js/c3.js"></script>
<script src="/theme/js/redux.js"></script>
<script src="/theme/js/lazy.js"></script>
<script src="/theme/js/lodash.js"></script>
<script src="/theme/js/base-charts.js"></script>

<hr>

**Edit:**

For good exerpience, don't read this blogpost on mobile. The **d3** stuff is heavy.</blockquote>

<hr>

We'll do an experiment to see if humans perhaps can generate random numbers effectively. Please click the heads/tails button as randomly as you can. You may also use the 1 (heads) or 0 (tails) keys on your keyboards (which probably is a whole lot faster if you are on a laptop).

<div id="chart"></div>

<button class="btn btn-default btn-block btn-lg" id="heads">Heads</button>
<button class="btn btn-block btn-lg" id="tails">Tails</button>

You've currently generated <span class="num_items">0</span> numbers, please ensure that you got about 100 before moving on. You are likely to cheat if you scroll down, which is fine when you try this a second time but it would be best to do a clean attempt beforehand.

## Inverse Turing Test

Let us do an inverse turing test.

![](/theme/images/turing.jpg)

You've just given your sequence of 'random' numbers. There are many axis for judging if you have given random data. In this document we will focus on the markov chain that we can learn from the generated input. The counts for these markov models are graphed below. You may see no bias in the first or second chart, but as you scroll down it may become more and more biased to a certain pattern.

<div id="container"></div>

<br>

<h3>Probability of predictions</h3>

Let us go a step further. It is well possible that you are such a terrible machine that an actual machine can predict your 'randomness'. We can use the counts from before to generate simple markov models $M_k$ (where $k$ the number of nodes in the markov chain). Each markov chain can then say how likely it is to see a heads (or a 1).

$$ P(H_t | M_k \{x_{t-1} ... x_{t-k}\}) $$

We can also combine these models. We train $M_1,...,M_5$ in real time and combine these via a naive ensemble rule.

$$ P(H_t | M_1,...,M_k X_{t-k}) \approx \Pi_{i=1}^5 P(H_t | M_i X_{t-i}) $$

This is a blunt model, especially because we're sticking to discrete-land while a beta distribution would be much better here. Still, this should be able to pick up a lot of common human patterns. We'll also introduce some smoothing in the beginning to prevent a very early overfit. When we do this the predictions over time are;

<div id="preds"></div>

The accuracy of this naive algorithm is depicted in the plot below.

<div id="acc"></div>

## Conclusion

So with these numbers, how random might the data be? Well, if the data truly was random then the number of correct predictions needs to come from the following distribution;

$$ P(a | H_0) \sim Bin(\frac{1}{2}, n) \sim {n \choose k} p^k (1-p)^{n-k} $$

It is a simple way to think about how likely our found accuracy is if we assume that the data is indeed random. With this data, $P(a | H_0) = $ <span class="metric">1</span>.

#### Bonus: What would a robot do?

You may be wondering what the result is if an actual robot filled this in. Press the button below to find out.

<button class="btn btn-block btn-lg" id="robot-go">Restart and robot</button>

## Shoutouts

This document was created together with @josh-the-man, props to him!

<script>
const counter = (state = [], action) => {
  switch (action.type) {
    case '0':
      state.push(0)
      return state
    case '1':
      state.push(1)
      return state
    case 'reset':
      return []
    default:
      return state;
  }
};

const predictor = (state = [], action) => {
  switch (action.type){
    case 'predict':
      res = state.pop()
      var totalCorrect = d3.sum(state.map(function(d){return d.correct}))
      var len = state.length
      var lag = 15
      var recentCorrect = d3.sum(state.slice(len - lag, len).map(function(d){return d.correct}))
      if (res) {
        res['v'] = _.last(rawInputStore.getState())
        res['correct'] = res['v'] == Math.round(res['pred'])
        res['cumacc'] = (totalCorrect + res['correct'])/(state.length + 1)
        res['curacc'] = (recentCorrect + res['correct'])/(state.slice(len - lag, len).length + 1)
        state.push(res)
      }
      state.push(predictCurrent())
      return state
    case 'reset':
      return []
    default:
      return state
  }
}

const { createStore } = Redux;
const rawInputStore = createStore(counter);
const predictionStore = createStore(predictor);

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

const NUM_CHARTS = 5
const PAIRS = d3.range(NUM_CHARTS + 1).map(calcAllPairs)
  .map(function(d){return _.object(d)})

const render = function(){
  d3.select('.num_items').text(rawInputStore.getState().length);
};

const markov = function(rank){
  return Lazy(rawInputStore.getState())
  .consecutive(rank)
  .countBy(function(d){return d})
  .toArray()
}

const lastFlips = function(n){return Lazy(rawInputStore.getState()).last(n).toArray()}

const prob = function(rank, outcome='1'){
  const past = lastFlips(rank - 1).join(',')
  const mk = markov(rank)
  const nextProbs = _.object(_.filter(mk, function(d){return d[0].indexOf(past) == 0}))
  var res = _.pick(nextProbs, function(v, k){
    return _.endsWith(k, outcome)
  })
  const outcomeP = 5 + (nextProbs[past + ',' + outcome] || 0)
  const notOutcomeP = 5 + (nextProbs[past + ',' + (outcome == '0' ? '1' : '0')] || 0)
  return outcomeP / (outcomeP + notOutcomeP)
}

const predictCurrent = function(){
  res = {
    'i' : rawInputStore.getState().length,
    'p1': prob(1),
    'p2': prob(2),
    'p3': prob(3),
    'p4': prob(4),
    'p5': prob(5)
  }
  l1 = res['p1'] * res['p2'] * res['p3'] * res['p4'] * res['p5']
  l0 = (1- res['p1']) * (1- res['p2']) * (1- res['p3']) * (1- res['p4']) * (1- res['p5'])
  res['pred'] = l1/(l0 + l1)
  return res
}

const getData = function(rank){
  var state_map = PAIRS[rank]
  if(rawInputStore.getState().length > rank){
    state_map = _.extend({}, state_map, _.object(markov(rank)))
  }

  const mk = Object.keys(state_map).map(
    function(k){return [k, state_map[k]]}
  )
  const sum = _.reduce(mk, function(x,y){return x + y[1]}, 0) || 1
  return _.sortBy(mk.map(function(d){return {'pattern': d[0], 'freq': d[1]/sum}}), 'pattern')
}


rawInputStore.subscribe(render);
rawInputStore.subscribe(markov);
rawInputStore.subscribe(function(){ predictionStore.dispatch({type: 'predict'}) } );

render();

d3.select("body").on("keydown", function(){
  const type = ({ 49: '1', 48: '0'})[d3.event.keyCode]
  if (type) {
    rawInputStore.dispatch({'type': type})
  }
})

d3.select("button#heads").on("click", function(){
    rawInputStore.dispatch({ type: '1' });
})

d3.select("button#tails").on("click", function(){
    rawInputStore.dispatch({ type: '0' });
})

d3.select("button#robot-go").on("click", function(){
  var count = 100
  rawInputStore.dispatch({type: 'reset'})
  predictionStore.dispatch({type: 'reset'})
  var tick = function(){
    count--;
    rawInputStore.dispatch({ type: Math.random() < 0.5 ? '1' : '0' });
    if (count > 0) {
      setTimeout(tick, 100)
    }
  }

  tick();
})

var genHist = function(cssLoc, rank){
  return c3.generate({
    bindto: cssLoc,
    data: {
      json: getData(rank),
      keys: {
        x: 'pattern',
        value: ['freq'],
      },
      type: 'bar'
    },
    axis: {
      x: {
        type: 'category'
      }
    },
    bar:{
      width:{
        ratio: 0.9
      }
    },
    size: {
      height: 200
    },
    legend: {
      show: false
    }
  });
}

var genChart = function(cssLoc, colnames, height = 400){
  return c3.generate({
    bindto: cssLoc,
    data: {
      json: predictionStore.getState(),
      keys: {
        x: 'i',
        value: colnames,
      },
    },
    point:{
      show: false
    },
    size: {
      height: height
    },
    axis: {
      y:{
        min:0,
        max:1
      }
    }
  });
}

var predChart = genChart("#preds", ['p1', 'p2', 'p3', 'p4', 'p5', 'pred'])
var accChart = genChart("#acc", ['cumacc', 'curacc'], 200)

predictionStore.subscribe(_.throttle(function () {
  predChart.load({'json': predictionStore.getState(), keys: {  x: 'i', value: ['p1', 'p2', 'p3', 'p4', 'p5', 'pred'] } });
}, 1000, {leading: true}))

predictionStore.subscribe(_.throttle(function () {
  accChart.load({'json': predictionStore.getState(), keys: {  x: 'i', value: ['cumacc', 'curacc'] } });
}, 1000, {leading: true}))

var initCharts = function(num){
  for (let i = 1; i <= num; i++) {
    d3.select('#container')
      .append('h5').text('Counts, Markov chainsize = ' + i).append('br')

    var newDiv = d3.select('#container').append('div').attr('id', 'markov' + i)
    setTimeout(function () {
      var chart = genHist('#markov' + i, i)
      rawInputStore.subscribe(_.throttle(function(){
        chart.load({'json': getData(i), keys: {x: 'pattern', value: ['freq']} })},
        100,
        { leading: true}));
    })
  }
}

initCharts(NUM_CHARTS)

var choose = function(n, k){
    if(k == 0){
      return 1
    }
    return (n * choose(n - 1, k - 1)) / k
}

var accLikelihood = function(numCorrect, numGenerated){
  var probs = d3.range(numCorrect, numGenerated+1)
    .map(function(d,i,l){return choose(numGenerated, d) * Math.pow(0.5, numGenerated)})
  return d3.sum(probs)
}

predictionStore.subscribe(function(){
  var accValues = predictionStore.getState().map(function(d){return d.correct})
  var metric = accLikelihood(d3.sum(accValues), Math.max(1, accValues.length - 1))
  d3.select('span.metric').text(d3.round(metric, 8))
})
</script>
