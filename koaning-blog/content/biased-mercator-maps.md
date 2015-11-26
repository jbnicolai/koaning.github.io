Title: Biased Mercator Maps
Date: 2013-10-14

> For this page to work properly you will need a pc for the mouse-support.

I've always been curious about how country sizes compare to eachother, hence I've made a small interactive map that allows you to drag Germany around. Move your mouse in the map to see the effect.

<iframe width='100%' height='450' frameborder='0' src='/theme/iframes/mercatorbias_DUITS.html'></iframe> 

Notice something weird? When you move Germany closer to the northern pole it seems to get bigger and more streched. The map coordinates remain constants but the shape of Germany differs because Google Maps applies a coordinate system that depends on where you are on the world. Why is that?

### The problem

Mapping the world to a flat surface is hard and any map is a compromise between true representation and convenience. There are many different standards on how you could do this. I mainly want to focus on the effect between two of such standards; the mercator projection (which has become somewhat of a standard) and the equirectangular projection. I found two images on wikimedia to show the difference.

### Equirectangular

![](/theme/images/biased-mercator-1.png)

Notice how everything is a square.

#### Mercator

![](/theme/images/biased-mercator-2.png)

Notice how everything is a square around the equator and a rectangle if further away.

To illustrate this further I've made a country in the shape of a sqaure.

<iframe width='100%' height='450' frameborder='0' src='/theme/iframes/mercatorbias.html'></iframe>

Notice how the location on earth is a big determinant factor when it comes to size. The actual landmass is always contstant here [8x8 latlon], it's the resulting projection that's different.

What about other places? I took the liberty of taking a few landmasses so you can try them out for youself.

#### Texas

<iframe width='100%' height='450' frameborder='0' src='/theme/iframes/mercatorbias_texas.html'></iframe>

It's known for being one of the biggest states of the US but to my suprise it's hardly bigger than France.

#### Alaska

<iframe width='100%' height='450' frameborder='0' src='/theme/iframes/mercatorbias_ALASKA.html'></iframe>

It looks really big on the map, but just try and get it ontop of Australia.

#### Australia


<iframe width='100%' height='450' frameborder='0' src='/theme/iframes/mercatorbias_AUS.html'></iframe>

Australia is only 30 latitudes below the equator so it's still sizable. Compare it with the US or Brazil.

#### Greenland

<iframe width='100%' height='450' frameborder='0' src='/theme/iframes/mercatorbias_GREEN.html'></iframe>

This is the most counter intuitive one for me, the United States is bigger than this landmass.

## Conclusion 

Google actually went a bit further than I did and created a mercator puzzle game that you can find [here](https://gmaps-samples.googlecode.com/svn/trunk/poly/puzzledrag.html). If you are interested in knowing more about projections in general I can recommend Mike Bostocks talk [here](https://vimeo.com/69448223).
