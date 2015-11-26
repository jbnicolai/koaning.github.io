Title: Julia for Loops
Date: 2015-08-25

<hr>

### EDIT 

> This blogpost is in need of being revisioned after a discussion on [reddit](https://www.reddit.com/user/one_more_minute#page=1). This post attempts to do a benchmark and fails at doing a meaningful one.

<hr>

I've been dabbling at Julia for a while in some of my spare time and I like some of the things that I am seeing. It's a language that is mainly popular in academics, particularily statistics and operations research. It has a community with some impressive members that sets high goals; trying to create a language with many characteristics from other dynamically typed languages while trying to keep speed as a main feature.

I've never gotten the impression that Julia was out to replace other languages but some people have been asking me when (not if) they should transition from R/Python to Julia. This seems like a very strange question. For some reason some people feel as if Julia will cause a change that is iminent instead of perhaps possible. 

In this blogpost I'd like to shed some light on why I feel that Julia won't be replacing R/python any time soon (probably ever). On this premise, I would like to emphesize that I enjoy watching what the Julia project is doing. I merely want to warn people who focus on the benchmarks. 

## A comperison 

One of the main features of Julia, is it's speed without having to vectorize code. So for the most popular science languages (Julia, R and python). I'll repeat a very similar exercize. I'll loop over three very long loops to add a number; an exercize that Julia should excel in. For each primary language I'll show how I've benchmarked my code. 

## Julia 

	import Base.time 

	function f(n)
		a = 0
		for i = 1:n
			for j = 1:n
				for k = 1:n
					a += i
					a += j
					a += k
				end
			end	
		end
	end

	function time(f, n)
		tic = Base.time() 
		f(n)
		Base.time() - tic
	end
 
## Base Python

	import time

	def f(n):
		a = 0
		for i in range(n):
			for j in range(n):
				for k in range(n):
					a += i
					a += j
					a += k
		return a

	%%time
 
You might be temped to wonder how this might work in numpy because common sense would suggest that anything numeric in python should probably be done in numpy. Turns out not to be that true. 

Using numpy caused a memory overflow (and a very hot macbook). Translating the above into something that is vectorized will result in something like below:

	def f(n):
		return np.sum(np.sum(np.full((n, n, n), np.arange(n)), axis = 0)[0:n,n-1])
		
	def timit(f, n):
		tic = time.time()
		f(n)
		return time.time() - tic

Note that if $n$ is getting larger that we need to keep an object (`np.full((n, n, n), np.arange(n))`) in memory that is getting $n^3$ larger. Numpy doesn't seem like much help when $n >> 100$. 

## Base R 

	f <- function(n){
		a <- 0
		for(i in 1:n){
			for(j in 1:n){
				for(k in 1:n){
					a <- a + i
					a <- a + j 
					a <- a + k
				}
			}
		}
		a
	}

	timit <- function(f, n){
	  tic <- Sys.time()
	  f(n)
	  as.numeric(difftime(Sys.time(), tic, units = c("secs")))
	}

# First Comperisons 

For loops in R are notiriously slow. Even when $n=100$ it already takes 593 ms. Python does better with 2.5 seconds for $n=5000$ but Julia manages to win here with 0.007 seconds for $n=5000$. 

Julia now manages a speedup of about 350x, which is impressive considering that I am not using a type system or any form of parallism. Still, you should not be fully convinced just quite yet. 

# Skill to the rescue 

Writing code in python or R is meant to make *you* productive, not the code that is running. But the communities behind these languages have been aware of this and have added tools to make code run performant when it needs to. In python you can use numba as a just-in-time compiler to compile python to native machine code. In R, you can define functions in C++ which can then directly be used in the language. Code wise, it's not a huge investment. 

## Numba

	from numba import jit

	@jit
	def f(n):
		a = 0
		for i in range(n):
			for j in range(n):
				for k in range(n):
					a += i
					a += j
					a += k
		return a

	def timit(f, n):
		tic = time.time()
		f(n)
		return time.time() - tic

In case you didn't know yet; numba is **crazy** [fast](https://www.wakari.io/sharing/bundle/aron/Accelerating_Python_Libraries_with_Numba_-_Part_2). 

## Rcpp

	library(Rcpp)

	cppFunction('int f(int n){
		int a = 0;
		for(int i = 0; i < n; ++i) {
			for(int j = 0; j < n; ++j) {
				for(int k = 0; k < n; ++k) {
					a += i;	
					a += j;	
					a += k;	
				}
			}
		}
		return a;
	}')

# New statistics 

	   count    numba     rcpp       julia
	1   1000 1.00e-06 3.60e-05 0.000307798
	2   5000 1.29e-06 3.72e-05 0.007336140
	3  10000 1.00e-05 3.90e-05 0.029693100
	4  50000 1.00e-05 4.00e-05 0.729448000
	5 100000 1.00e-05 4.10e-05 2.910130000

Suddenly, numba turns out to be the clear winner and even Rcpp seems to outperform Julia on this one. That is not to say that Julia is not doing something impressive. Julia is performing very well as a general language here. It only happens to get beaten by specialist packages from other popular languages.

## Conclusion 

People want to use R or Python to make something quickly and not necessarily something that immediately runs fast. As a result these two langauges have common patterns to combat their comprimised speed: 

- for common tasks that do put pressure on a language they use packages/tools that are optimized and written in a language that performs better (like pandas/dplyr or spark)

- for something less common these languages allow ways to rewrite slow parts in another more performant and tightly intergrated language (Rcpp, cython, numba)

This combination works very well for most people, but not all. And for those people Julia is very interesting.

What Julia offers is a language that is inheritly a whole lot quicker if you write your own custom functions while keeping the syntax relatively clean. It might feel like Matlab, but is free and more open. If you are an academic, this is good news and it is no suprise that a lot of the community comes from the academic field switching over from Matlab. A lot of cool researchers use Julia. Keeping an eye on Julia also allows you to keep an eye on new algorithms. 

I'd be hard pressed to apply it in production anytime soon for a client though. R and Python are proven tools with gigantic communities and with proven methods to give great computational performance (which can compete with Julia's speed). Another downside of Julia is that it is very young and thus you may expect stackoverflow answers to be more sparse and packages to have more bugs.

I like to think that just like R and python have learned from eachother, Julia might also offer lessons. Already, it's fun and easy to dabble with it (although the plotting functionality is painfully slow at the moment). Only time will tell if and how Julia might go beyond the academic field though. It would certainly not be a bad language, just not one that is automagically a better alternative to python or R.
 