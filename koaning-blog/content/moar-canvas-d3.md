Title: Canvas, Trees and Communities 
Date: 2015-11-25

[D3](http://d3js.org/) sometimes falls short in performance. Browsers just aren't meant to draw and update many svg elements. Canvas can help adress some of these problems and in this document I will demo some things that I've hacked together. All this work is heavily (!) inspired by the recent work of Mike Bostock found [here](http://bl.ocks.org/mbostock/280d83080497c8c13152). 

## Minimum Spanning Tree

In d3, you would be able to keep track of the state of your visualisation via the DOM of the browser. It would keep track of where svg elements are located as well as have event bindings. Canvas will not give you this luxury, you'll need to track the state of the drawn objects yourself. 

You can still use many utility functions from d3 though, or any other front end javascript code. In this next example I'm using `d3.timer` and lodash extensively. 

### A use case 
Imagine that we have a set number of drones that is each doing random searches on a plane. A random search is not the best way to go about this, but the coverage would not be terrible. The plot below shows location of 100 of these drones.

<div class="container">
  <div class="row">
    <div class="col-sm-1"></div>
      <div class="col-sm-10">
        <canvas height="300" width="550" id="canvas2"></canvas>
      </div>
    <div class="col-sm-1"></div>
  </div>
</div>

Now suppose that these drones need to be in contact with eachother. They don't all need to be communicating to everybody but they do need to span a network such that no message will end up missing. The further drones are away from eachother, the more battery it costs to send a message. Can we calculate which drones need to be connected to which drones in real time such that each drone is linked? 

Below you'll see the same cloud of drones with the according minimum spanning tree. Points that are generally very close to eachother will have extra blue connections drawn.

<div class="container">
  <div class="row">
    <div class="col-sm-1"></div>
      <div class="col-sm-10">
        <canvas height="300" width="550" id="canvas1"></canvas>
      </div>
    <div class="col-sm-1"></div>
  </div>
</div>


The code used to create this is very (!) similar to Mike's example except that I'm also drawing lines for the minimum spanning tree as well. You can check the source code of this blog post for a full implementation, beware that it is pretty naive as it checks distances for points that it does not need to. 

The algorithm for minimum spanning tree boils down to keeping track of points in the spanning tree and points that still need to be added. At each iteration you add a point to the tree that has the shortest distance.

    function calc_link(set_in, set_out){
      var new_connection = [],
          min_dist = 10000;

      for (var i = set_in.length - 1; i >= 0; i--) {
        for (var j = set_out.length - 1; j >= 0; j--) {
          var p1 = particles[set_in[i]],
              p2 = particles[set_out[j]];
          var new_dist = dist_particle(p1, p2);
          if(new_dist < min_dist){
            new_connection = [set_in[i], set_out[j]];
            min_dist = new_dist;
          }
        };
      };
      return new_connection;
    }

    function calc_tree(){
      var connections = [];
      var set_in = [particles.length - 1],
          set_out = d3.range(particles.length - 1); 
      for(i in set_out){
        connections.push(calc_link(set_in, set_out));
        set_in = _.unique(_.flatten(connections)),
        set_out = _.difference(d3.range(particles.length), set_in);
      }
      return connections;
    }

## Community Detection 

What now if we want to split these drones up, ie. cluster them according to their location? We could use their location and use kmeans but that seems a bit naive, knowing that location alone is no guarantee that two drones are connected. 

Doing a MST has an extra benefit: we can use it to help find communities. It gives an extra dimension to the drone data which we can exploit to create suitable communities of drones. 

The simplest heuristic I could come up with was to use the following algorithm:


    1. Determine which paths in the tree are leaf paths
    2. Remove them.
    3. Repeat until only a few paths of the tree are left. 
    4. Pick one of these remaining paths.

The intuition behind the algorithm is that a good path to cut would be a path that is located centrally. By recursively removing leaf nodes, you'll end up with one of these paths. Below is the same tree as above but now with a recommendation for a cut. 

<div class="container">
  <div class="row">
    <div class="col-sm-1"></div>
      <div class="col-sm-10">
        <canvas height="300" width="550" id="canvas3"></canvas>
      </div>
    <div class="col-sm-1"></div>
  </div>
</div>


If you want to expand this to more than two communities you might take the two subtrees and apply the same algorithm. 

## Conclusions 

Canvas is pretty darn worthwhile and has some performance benefits compared to d3. You'll need to write more javascript though, which isn't too bad if you can use `d3` and `lodash`. 



<script>
/* https://github.com/d3/d3-timer Copyright 2015 Mike Bostock */
"undefined"==typeof requestAnimationFrame&&(requestAnimationFrame="undefined"!=typeof window&&(window.msRequestAnimationFrame||window.mozRequestAnimationFrame||window.webkitRequestAnimationFrame||window.oRequestAnimationFrame)||function(e){return setTimeout(e,17)}),function(e,n){"object"==typeof exports&&"undefined"!=typeof module?n(exports):"function"==typeof define&&define.amd?define(["exports"],n):n(e.timer={})}(this,function(e){"use strict";function n(){r=m=0,c=1/0,t(u())}function t(e){if(!r){var t=e-Date.now();t>24?c>e&&(m&&clearTimeout(m),m=setTimeout(n,t),c=e):(m&&(m=clearTimeout(m),c=1/0),r=requestAnimationFrame(n))}}function i(e,n,i){i=null==i?Date.now():+i,null!=n&&(i+=+n);var o={callback:e,time:i,flush:!1,next:null};a?a.next=o:f=o,a=o,t(i)}function o(e,n,t){t=null==t?Date.now():+t,null!=n&&(t+=+n),l.callback=e,l.time=t}function u(e){e=null==e?Date.now():+e;var n=l;for(l=f;l;)e>=l.time&&(l.flush=l.callback(e-l.time,e)),l=l.next;l=n,e=1/0;for(var t,i=f;i;)i.flush?i=t?t.next=i.next:f=i.next:(i.time<e&&(e=i.time),i=(t=i).next);return a=t,e}var a,m,r,f,l,c=1/0;e.timer=i,e.timerReplace=o,e.timerFlush=u});

var canvas = document.querySelector("#canvas1"),
    context = canvas.getContext("2d"),
    canvas2 = document.querySelector("#canvas2"),
    context2 = canvas2.getContext("2d"),
    canvas3 = document.querySelector("#canvas3"),
    context3 = canvas3.getContext("2d"),
    width = canvas.width,
    height = canvas.height,
    radius = 2.5,
    minDistance = 10,
    maxDistance = 10,
    minDistance2 = minDistance * minDistance,
    maxDistance2 = maxDistance * maxDistance;

var tau = 2 * Math.PI,
    n = 100;

var particles = d3.range(n).map(function(d){
  return {
    i: d,
    x: (Math.random()-0.5) * width * 0.8 + 0.5 * width,
    y: (Math.random()-0.5) * height * 0.8 + 0.5 * height,
    vx: 0,
    vy: 0
  };
})

function other_particles(particle_id){
  var arr = [] 
  for(p in particles){
    if(particles[p].i != particle_id){
      arr.push(particles[p])
    }
  }
  return arr
}

function dist_particle(part1, part2){
  return Math.sqrt(
    Math.pow(part1.x - part2.x, 2) + Math.pow(part1.y - part2.y,2)
  );
}

function find_closest(particle_id){
  var single = particles[particle_id], 
      arr = other_particles(particle_id), 
      min_dist = 10000, 
      closest = -1;

  for(i in arr){
    var new_dist = dist_particle(arr[i], single);
    if(new_dist < min_dist){
      min_dist = new_dist;
      closest = arr[i].i;
    }
  }
  return closest;
}

function calc_link(set_in, set_out){
  var new_connection = [],
      min_dist = 10000;

  for (var i = set_in.length - 1; i >= 0; i--) {
    for (var j = set_out.length - 1; j >= 0; j--) {
      var p1 = particles[set_in[i]],
          p2 = particles[set_out[j]];
      var new_dist = dist_particle(p1, p2);
      if(new_dist < min_dist){
        new_connection = [set_in[i], set_out[j]];
        min_dist = new_dist;
      }
    };
  };
  return new_connection;
}

function calc_tree(){
  var connections = [];
  var set_in = [particles.length - 1],
      set_out = d3.range(particles.length - 1); 
  for(i in set_out){
    connections.push(calc_link(set_in, set_out));
    set_in = _.unique(_.flatten(connections)),
    set_out = _.difference(d3.range(particles.length), set_in);
  }
  return connections;
}

function draw_between(context, id1, id2, color, width, alpha){
  var p1 = particles[id1],
      p2 = particles[id2]; 
  context.beginPath();
  context.globalAlpha = alpha;
  context.moveTo(p1.x, p1.y);
  context.lineTo(p2.x, p2.y);
  context.strokeStyle = color;
  context.lineWidth = width;
  context.stroke();
}

var equal_func = function(i){
  return function(d){
    return d[1] == i || d[0] == i
  }
};

var isin = function(arr1, arr2){
  var res = []; 
  for(i in arr1){
    res[i] = false;
    for(j in arr2){
      if(equal_func(arr2[j])(arr1[i])){
        res[i] = true;
      }
    }
  }
  return res;
};

timer.timer(function(elapsed) {
  context.save();
  context.clearRect(0, 0, width, height);
  context2.clearRect(0, 0, width, height);
  context3.clearRect(0, 0, width, height);
  edges = []
  // update point position
  for (var i = 0; i < n; ++i) {
    var p = particles[i];
    p.x += p.vx; if (p.x < 0) p.x += 5 + 5 * Math.random(); else if (p.x > width) p.x -= 5 + 5 * Math.random();
    p.y += p.vy; if (p.y < 0) p.y += 5 + 5 * Math.random(); else if (p.y > height) p.y -= 5 + 5 * Math.random();;
    p.vx += 0.1 * (Math.random() - .5) - 0.01 * p.vx;
    p.vy += 0.1 * (Math.random() - .5) - 0.01 * p.vy;

    context.beginPath();
    context.arc(p.x, p.y, radius, 0, tau);
    context.fill();

    context2.beginPath();
    context2.arc(p.x, p.y, radius, 0, tau);
    context2.globalAlpha = 1;
    context2.fillStyle = "black";
    context2.fill();

    context3.beginPath();
    context3.arc(p.x, p.y, radius, 0, tau);
    context3.fill();
  }

  // draw lines based on min/max dist
  for (var i = 0; i < n; ++i) {
    for (var j = i + 1; j < n; ++j) {
      var pi = particles[i],
          pj = particles[j],
          dx = pi.x - pj.x,
          dy = pi.y - pj.y,
          dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 20) {
        context.globalAlpha = 0.5;
        context.strokeStyle = 'steelblue';
        context.lineWidth = 1;
        context.beginPath();
        context.moveTo(pi.x, pi.y);
        context.lineTo(pj.x, pj.y);
        context.stroke();

        context3.globalAlpha = 0.5;
        context3.strokeStyle = 'steelblue';
        context3.lineWidth = 1;
        context3.beginPath();
        context3.moveTo(pi.x, pi.y);
        context3.lineTo(pj.x, pj.y);
        context3.stroke();
      }
    }
  }

  // draw lines based on minimum spanning tree
  var tree = calc_tree();
  tree.map(function(d){draw_between(context, d[0], d[1], "black", 2, 0.9)})
  tree.map(function(d){draw_between(context3, d[0], d[1], "black", 2, 0.9)})

  while(tree.length > 8) {
    var particle_counts = _.chain(tree)
      .flatten()
      .countBy(_.identity)
      .pairs()
      .value();

    var leaf_nodes = particle_counts
      .filter(function(d){ return d[1] == 1 })
      .map(function(d){return Number(d[0])});

    var leaf_paths = isin(tree, leaf_nodes);
    
    var tree = _.filter(tree, function(d,i){
      return !leaf_paths[i];
    }); 
  };

  draw_between(context3, tree[0][0], tree[0][1], "red", 5, 1);

  context.restore();
});

</script>