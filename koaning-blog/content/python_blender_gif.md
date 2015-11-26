Title: Python + Blender Gif
Date: 2015-07-22

In a [previous post](/posts/python-cubes-in-blender.html) I've described how to generate objects in blender through python. In this document I will describe how to use such python scripts from the command line to render animations. 

### TD;DR 

This small guide will allow you to make the following gif using the command line and python. 

![](http://i.imgur.com/Kc455r6.gif)

## Blender Python Script 

This script below generates a rain of randomly sized and colored cubes. You can paste this code into the blender command line to see the result.

	# filename: colored_rain.py

	import bpy
	import math 
	import random
	import uuid

	def select_type(meshtype="Cube"):
	    for ob in bpy.context.scene.objects:
	        ob.select = ob.type == 'MESH' and ob.name.startswith(meshtype)

	def deltype(meshtype="Cube"):
	    select_type(meshtype)
	    bpy.ops.object.delete()

	def makeMaterial(name, diffuse, specular, alpha):
	    mat = bpy.data.materials.new(name)
	    mat.diffuse_color = diffuse
	    mat.specular_color = specular
	    mat.alpha = alpha
	    return mat

	def randomMaterial():
	    randvec = (random.random(), random.random(), random.random())
	    return makeMaterial('mat' + uuid.uuid4().hex[0:6], randvec, (1,1,1), 1)

	def setMaterial(ob, mat):
	    me = ob.data
	    me.materials.append(mat)

	deltype()

	def block(x,y,z,rot):
		bpy.ops.mesh.primitive_cube_add( radius=random.random(), location = (x,y,z/2.0) )
		bpy.ops.rigidbody.object_add()
		bpy.context.active_object.rigid_body.type = 'ACTIVE'
		rand_axis = (random.random(),random.random(),random.random())
		bpy.ops.transform.rotate(value=rot, axis=rand_axis)
		setMaterial(bpy.context.object, randomMaterial())

	def blocks(x,y,z):
		for i in range(4):
			x = x + random.random()*2
			y = y + random.random()*2
			rot = random.random()*2*math.pi
			block(x,y,z,rot)

	for z in range(2,100):
		blocks(0,0,z)

Then if you run this next code, blender will start rendering images for the animation. 

	# these are the render settings
	bpy.data.scenes['Scene'].render.engine = 'CYCLES'
	bpy.data.scenes['Scene'].cycles.samples = 10
	bpy.data.scenes['Scene'].frame_end = 100
	bpy.data.scenes['Scene'].render.fps = 100
	bpy.context.scene.render.resolution_x = 600
	bpy.context.scene.render.resolution_y = 400

	# this command signals the actual render 
	bpy.ops.render.render(animation=True, use_viewport=True)

The [python script](https://gist.github.com/anonymous/31c7623b09465782d1eb) renders a scene, fills it with boxes, sets up a camera and applies render settings. This code can be run from blender but it could also be called from the command line. The two main benefits of doing this: 

- we are not slowed down by the also rendering a GUI 
- we can use a server to do the calculation for us, leaving our working computer free to do other things. 

### Blender from the command line

#### Getting the CL to work. 

We will first need to make sure that we can run blender from the command line. If you are running this on a mac you will need to make sure your ```.bash_profile``` knows where to find the blender command. On open source operating systems you will need to do something similar unless you installed it via ```apt-get install blender```. 

```
alias blender=/Applications/blender.app/Contents/MacOS/blender
```

For more info see [this link](http://blender.stackexchange.com/questions/2078/how-to-use-blender-command-lines-in-osx). 

#### Running the CL 

The blender command line offers many opportunities to automate things. Consider the following command: 

```
$ blender -y -b -x 1 -o /some/output/dir/ --engine CYCLES --python /path/to/script/python_script.py
```

The python script contains rendering details, so blender will just run these and output them in the specified folder. This command will not prompt the user to confirm anything (via ```-y```) and it will run in the background (so no gui, via ```-b```). Note that for extra performance you can specify a higher number of threads (`-t`) if your machine supports it. 

You can get more option info via `blender --help`.

#### Viewing the output 

In the output dir we will now see that files have been created. These are images. With a simple command line they can be joined together in a gif. 

```
convert -delay 10 -loop 0 *.png animation.gif
```

For this command line app you may need to need to `apt-get/brew install imagemagick`. 

### Conclusion

Blender can make an exellent tool to learn python, making these scripts is fun stuff. 

For people who want to do more with blender I would like to point out that any button in blender can be set via python as well. If you keep your mouse over a button, the python code that's needed appears. That also means that you can code the render settings, which is useful if you don't want to spend too many resources.
