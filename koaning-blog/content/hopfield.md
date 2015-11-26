Title: Intro to Hopfield Networks
Date: 2015-07-23

In this document I will show how a hopfield recurrent network works by building one with numpy. First we'll create a hello world example, after which we'll create a method that will use these networks on simple images.

> If preferable, instead of reading here, you can also view this post as an ipython notebook [here](http://nbviewer.ipython.org/gist/anonymous/01df7e791c1b2cc46baf). 

### A quick demo 

The idea behind a hopfield network is to supply it with 'memories' where it can learn patterns from. It will not remember the values of the memories but will learn from the correlations within the data itself. Maybe this code can explain it better than words can. 

	import numpy as np
	import os

	inputs = [[1,-1,1,-1,1,-1],[-1,1,-1,1,-1,1]]

	def learn(learn_data):
	    k = len(learn_data[0])
	    hopfield = np.zeros([k,k])
	    for in_data in learn_data: 
	        np_arr = np.matrix(in_data)
	        lesson = np_arr.T*np_arr
	        np.fill_diagonal(lesson, 0)
	        hopfield = hopfield + lesson
	    return hopfield

	hopfield_matrix = learn(inputs)

We take two inputs which we learn from and create a matrix containing co-occurence information. This resulting hopfield matrix contains the following: 

	[[ 0. -2.  2. -2.  2. -2.]
	 [-2.  0. -2.  2. -2.  2.]
	 [ 2. -2.  0. -2.  2. -2.]
	 [-2.  2. -2.  0. -2.  2.]
	 [ 2. -2.  2. -2.  0. -2.]
	 [-2.  2. -2.  2. -2.  0.]]

Note that this matrix has learned from the alternating series. Which can also be visualized in graph form. 

![](http://i.imgur.com/xKWDnW1.png)

This matrix can be multiplied with an input vector which will result in a new array that should closed resemble of the input memories. 

	def normalize(res):
	    res[res > 0] = 1
	    res[res < 0] = -1
	    return res

	res = hopfield_matrix * np.matrix([1,1,1,1,-1,1]).T
	normalize(res)

I apply normalisation to make sure the number stay either +1 or -1. The result makes sense: 

	[-1,1,-1,1,-1,1]

Let's now learn such a network on some images with digits. 

### To simple images

	import matplotlib.pyplot as plt
	%matplotlib inline  
	import cv2

	fig, (ax1, ax2) = plt.subplots(1,2)
	img = cv2.imread(os.getcwd() + '/hamilton_images/0.jpg')
	ax1.imshow(img)

	img = cv2.imread(os.getcwd() + '/hamilton_images/1.jpg')
	ax2.imshow(img)


![](http://i.imgur.com/hIQakIV.png)

Again, these images will serve us as memories, not labels. This makes a hopfield neural network different from classification or clustering methods. We are doing neither but something very similar. Let's try and get our hamilton network to learn the patterns from the images. 

We will redefine the `learn` method to work for images now. 

	def learn(learn_data):
	    k = len(learn_data[0])
	    hamilton = np.zeros([k,k])
	    for in_data in learn_data:
	        np_arr = np.matrix(in_data)
	        lesson = np_arr*np_arr.T
	        np.fill_diagonal(lesson, 0)
	        hamilton = hamilton + lesson
	    return hamilton

	inputs = [] 
	for i in ['0', '1']:
	    img = cv2.imread(os.getcwd() + '/hamilton_images/' + str(i) + '.jpg')
	    an_input = normalize(np.sum(img, axis=2) - 766/2.0)
	    an_input.resize((50*50,1))
	    inputs.append(list(an_input))
	    
	hamilton = learn(inputs)

This learning might take a while. It is interesting to see the hamiltonian matrix. Certain regions in the image don't matter in distringuishing the images. 

	plt.imshow(hamilton)

![](http://i.imgur.com/WR9MLDt.png)

Now we'll creata a method that can take a noisy image and it will try to find the right memory. 

	def network_output(problem):
	    an_input = normalize(np.sum(problem, axis=2) - 766/2.0)
	    an_input.resize((problem.shape[0]*problem.shape[1],1))
	    output = hamilton * an_input
	    output.resize(problem.shape[0],problem.shape[1])

	    pltr = np.zeros(img.shape) 
	    for i in range(pltr.shape[0]):
	        for j in range(pltr.shape[1]):
	            for k in range(pltr.shape[2]):
	                pltr[i,j,k] = output[i,j]
	                
	    return normalize(pltr)

	def recurse(f, i, n):
	    if n == 1: 
	        return f(i)
	    return f(recurse(f, i, n - 1))

Note that I am normalizing the network output to force pixel to either be black or white. Now let's try out our method on a few images. 

	fig, axis = plt.subplots(2,6)
	fig.set_size_inches(12,5)
	for i, problem in enumerate(['01', '02', '11', '12', 'n1', 'n2']):
	    problem = cv2.imread(os.getcwd() + '/hamilton_images/' + problem + '.jpg')
	    axis[0][i].imshow(problem)
	    axis[1][i].imshow(network_output(problem))

Let's have a look at the output. 

![](http://i.imgur.com/porrx76.png)

The first four images behave just as expected.

The last two images might seem counter intuitive. The 5th image contains a lot of whitespace and the original 1 image contains more whitespace than the zero. So it might feel likely that the 5th image is a one. But then why is the 6th image also a one? 

It's because the hopfield network doesn't care about a pixel being black or white, it only cares about the correlation between pixels. This means that all black pixel are the same as all input pixels. This may give unexpected side effects but this is not unwanted behavior per se. 

Hopfield networks are fun. They offer an alternative way to think about neural networks and give insight in why having recurrence in such a network can be a good thing. 

Again, the ipython notebook file for this can be found [here](http://nbviewer.ipython.org/gist/anonymous/01df7e791c1b2cc46baf). 
