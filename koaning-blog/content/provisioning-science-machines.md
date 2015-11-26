Title: Basic Science Provisioning with Docker
Date: 2015-06-17

<br> 

<img src="https://upload.wikimedia.org/wikipedia/commons/7/79/Docker_(container_engine)_logo.png" alt="" width="10%">

<br> 

The old school way of provisioning machines is via the command line. To more dev savy people it may be straightforward to create an [ipython notebook server](http://badhessian.org/2013/11/cluster-computing-for-027hr-using-amazon-ec2-and-ipython-notebook) or an [rstudio server](http://www.rstudio.com/products/rstudio/download-server/) but to people who aren't too familiar to the command line this might be a daunting task. Thanks to docker, all of this has become a whole lot easier if you just want to have some notebooks ready. This blogpost is meant as a quick startup guide. 


## New School Provisioning 

The new school way of doing things is not to install everything in bash but to simply load a docker container with everything preinstalled. A docker container is like a virtual machine but much more lighteight. This means that once docker is installed on your machine, you only need a single line of code to get an entire science stack running. In this part I will explain how to get a container like that of [tmpnb](tmpnb.org) online on a server that you control. 

Installing docker usually doesn't involve much, but it does depend on your operating system.

#### CentOS 

	yum install -y docker; sudo service docker start

#### Ubuntu 

	wget -qO- https://get.docker.com/ | sh

#### Mac 

	https://docs.docker.com/installation/mac/

Another easy way to get started is to rent a server form digital ocean that comes with docker. Once you have a computer ready with docker, ssh into the machine via the command line and then run the following command: 

	$ docker run -dp 8888:8888 jupyter/demo 

This takes a while, but it will install a very complete docker image. In the background, docker will download a blueprint with all dependencies for you. 

If you run this on a ubuntu machine locally you can go do `localhost:8888` in your browser. Otherwise, if the server is on a network (or the internet) then you can go it's ip adress `<ip-adress>:8888` to see the result. It should look something like: 

This notebook is amazing, it contains notebook capabilities not just for python but also for bash, ruby, julia, R and even haskell. It also comes with packages for each of these languages that help you get started right away. Jupyter notebooks are meant as a language agnostic tool, this makes it very powerful in learning environments. 

Another popular and very powerful alternative to the jupyter notebook is to use the Rstudio server. Starting this is equally simple. 

	$ docker run -dp 8787:8787 rocker/hadleyverse

This doesn't allow full support for all languages, but has many extra features that the R users might miss in the notebook. This service can be reached from the browser as well, this time on port 8787. The username/password for this service is `rstudio`/`rstudio`. If you want to use a custom username/password you can use

	$ docker run -d -p 8787:8787 -e USER=<username> -e PASSWORD=<password> rocker/hadleyverse

For more info, please read the [github wiki](https://github.com/rocker-org/rocker/wiki/Using-the-RStudio-image) of this project.

## Security 

Be aware. Rstudio may have come with a password but the jupyter notebook didn't. This is a serious security issue. If the ip adress is public then anybody can just use the notebook and send all sorts of malisious code to it. The setup is fine if you are on a secure network and you are the only user who knows about the machine, but if it is not the case you could be in serious trouble. It is not hard to completely destroy a server through a notebook because you essentially have full access to it. 

Also, even if a user needs a password to log in, there might still be a problem. If the user is in a cafe with open wifi, then all the communication with the server can be listened to because the data that gets sent is not encrypted. This means that somebody might be listening and intercepting passwords together with usernames. Preferably, we want our service over https instead of http to combat this. 

The current setup should preferably only be used on machines that are on an internal network and shared only with people that you trust. 

Both [rstudio](https://s3.amazonaws.com/rstudio-server/rstudio-server-pro-0.98.507-admin-guide.pdf) and [ipython](http://ipython.org/ipython-doc/1/interactive/public_server.html) have documented solutions to this security problem. It involves creating a self-signed certificate and then having the notebook service point to it.  You can implement these yourself but please be warned that this is an advanced topic. If you feel uncomfortable in this area then please only use these docker containers on your internal machines that cannot be reached from the outside. 

## Performance 

You can specify how many resources from the machine a docker container can take from the command line. Use `-m` to specify how much memory the docker container can use (`512m` or `2g`) and use `--cpuset` to allocate which cpu's the docker container gets to use (you can specify `ALL`). 

#### Example 

	docker run -m 512m -cpuset ALL -p 8787:8787 rocker/hadleyverse

You can check the system usage via `mpstat`. 
