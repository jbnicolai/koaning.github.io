Title: Monopoly Simulations
Date: 2015-12-09

<hr>

<br> 

### Edit

A previous version of this blogpost had the worst typo ever. I simulated everything using `np.random.randint(1,6)` which only samples between 1-5. This led to a lot more jail time because it was much more likely to get there. 

I've been trending on hackernews, I've been linked to in boing-boing; 14000 views later and nobody mentioned the error. Thankfully, I have a collegue who doesn't mind pointing out flaws in my code (holla at you Niels). The numbers have changes slightly and so have the conclusions.

<br>

![](/theme/images/monopoly.jpg)

In this document I'll have a go at some simulations of monopoly. The rules that I am following, as well as the data, was originally acquired from [here](http://monopoly.wikia.com/). In this document we will find out that the 'going to jail' mechanic of the game causes some drastic inbalances which you may want to be mindful of. If you want to win at monopoly, you'll probably want to resonably close to the jail exit.

### Simulation Goal 

We're interested in knowing the return on investment on different deeds in the game of monopoly. In terms of simulation that means that we won't need to keep track of the cash that different players have, we're merely interested in knowing the probability of landing on a tile in the board game. 

To keep things simple, I am considering the rules as follows;

- if you roll the same number on both dice you get to roll again in your turn
- if you get to roll three times in your turn you go to jail
- when you are in jail you get to roll two dice, if they are the same you get out of jail and you move the total number of eyes you've just rolled 
- you can't be in jail for more than 3 turns, after that you get to roll again
- when you land on tile 30, you move straight to jail 
- we'll ignore any effect of chance cards that allow you to move 
- we're interested in the amount of money you may earn by owning property. If a player lands on two parts of land during their turn then this increase the likelihood of landing on either parts of land equally and as much as if the player landed on a single tile. 

### Simulation Code

Python is best suited for simulations that involve objects that need to keep track of state. It is a bit verbose and a bit hard coded, but it get's the job done.

```
import numpy as np
import pandas as pd

class Player(object):
    def __init__(self, start_pos):
        """Return a Player object."""
        self.position = start_pos
        self.cash_spent = 0
        self.jail_turns_left = 0
        self.history = [start_pos]
        self.jail_tile = 10
        self.goto_jail_tile = 30

    def dice_roll(self, n = 1):
        d1, d2 = np.random.randint(1, 7, 2)
        if (d1 == d2) & (n <= 3): 
            return [d1 + d2] + self.dice_roll(n + 1)
        return [d1 + d2]
    
    def new_pos(self):
        if self.jail_turns_left > 0:
            d1, d2 = np.random.randint(1, 7, 2)
            if d1 != d2:
                self.jail_turns_left -= 1
                new_positions = [self.jail_tile]
            else: 
                self.jail_turns_left = 0
                new_positions = [(self.jail_tile + d1 + d2) % 40]
        else:
            rolled_eyes = self.dice_roll()
            deltas = list(np.cumsum([i for i in rolled_eyes]))
            new_positions = [(self.position + i) % 40 for i in deltas]

            if len(new_positions) == 4: 
                new_positions.pop() 
                new_positions[-1] = self.jail_tile
                self.jail_turns_left = 2

            if self.goto_jail_tile in new_positions:
                new_positions = new_positions[:new_positions.index(self.goto_jail_tile)]
                new_positions.append(self.jail_tile)
                self.jail_turns_left = 2
            
        self.history += new_positions
        self.position = self.history[-1]
        return self
```

Using such an object is a better practice then doing this all within for loops. Running the simulation for 1000 players where each game takes 100 turns on average can be done via;  

```
players = [Player(0) for i in range(1000)]
res = []
for player in players:
    for i in range(200):
        player = player.new_pos()
    res = res + player.history
_ = plt.hist(res, bins = 40)
```

![](/theme/images/monopoly_plot1.png)

People spend a lot of time in prison. Keep in mind tho, that I am using this simulation to figure out how good an investment opportunity in monopoly is. I am not intersted in where a player is at the end of their turn; I'm interested in the likelihood of landing on a tile at any point in the game or at any point in the turn. 

You may be wondering about the odd spikes after the visit to jail. It seems like only even numbers have a significantly higher spike. It is due to the rules of how you get out of jail. Notice that there's six of them and that they are even numberedly distanced from jail.

You can get out of jail by rolling doubles on any of that player's next three turns in Jail. Whoever succeeds in doing this immediately moves forward the number of spaces shown by the throw. Even if doubles are rolled, the player does NOT take another turn.

If you leave jail, you'll move an even number (because the two dice needed to be the same). 

The initial spike at tile 0 is due to the starting condition of the players. If we were to change this (to say, everybody starts out in jail) we get a less biased long term equalibrium picture, simulated below.

```
players = [Player(np.random.randint(40)) for i in range(1000)]
res = []
for player in players:
    for i in range(200):
        player = player.new_pos()
    res = res + player.history
_ = plt.hist(res, bins = 40)
```

![](/theme/images/monopoly_plot2.png)

### Combining Data 

The next step of this exercize is to combine these probabilities with data of the deeds that players can land on. This comes down to a simple join once you've scraped all nececary data. Feel free to get a copy of this data [here](/theme/data/monopoly.csv). 

### Biased Trainstations

To keep things simple, let's just look at the railroads of the game. If you normalize the probabilities for these four tiles then the probabilities are;

```
tile	name 			prob
5     	reading			0.233769
15    	pennsylvania	0.255849
25    	b&o railroad 	0.270930
35    	short line	 	0.239452
```

This seems to suggest that having a trainstation at tiles 15 or 25 is worth 5% more than having the other two. Not too shocking, but an inbalance nonetheless. Let's see if we can find a greater form on the other deeds.

### Biased Deeds

Looking at deeds is a little more complex. Deeds have different prices for purchase or rent and have different returns depending on how many houses you've bought. To keep things simple we'll first have a look at the probability of landing on a certain deed. If only look at the tiles that are deeds, the normalized probabilities show that the likelihood is not uniformly distributed.

![](/theme/images/monopoly_plot3.png)

It seems that it is very likely to fall on orange, yellow and red. Note that the low probability for blue and purple is also attributable to the fact that these streets contain only two deeds.

#### Expected income 

If we, just for now, assume that the income from the deed is given via the rent (so no houses/hotels) then we can get a glimpse of the relationship between somebody landing on a tile and earning from it.

![](/theme/images/monopoly_plot4.png)

The above plot shows rent income over the probability of landing on a certain tile. The size of the circle represents the expected value of the deed (rent times probability). Notice that there are a few deeds who give low returns and have a very low probability of landing on them. 

![](/theme/images/monopoly_plot5.png)

The shape of this plot seems to be repeated across deed upgrades as well. There's always a blob of deeds that have a low probability of landing on them and a low pay that's required. 

It seems that the deeds that perform very poorly are the ones that are hard to reach from prison. 

```
                  name      color
1 Mediterranean Avenue     purple
2        Baltic Avenue     purple
3      Oriental Avenue light_blue
4       Vermont Avenue light_blue
5   Connecticut Avenue light_blue
6    St. Charles Place       pink
7		 States Avenue		 pink
```

For reference I've listed all the deeds with their probabilities and expected return on rent. 

```
                    name      color      p      e
1   Mediterranean Avenue     purple 0.0410 0.0819
2          Baltic Avenue     purple 0.0424 0.1698
3        Oriental Avenue light_blue 0.0410 0.2458
4         Vermont Avenue light_blue 0.0417 0.2504
5     Connecticut Avenue light_blue 0.0415 0.3322
6      St. Charles Place       pink 0.0410 0.4096
7          States Avenue       pink 0.0434 0.4343
8        Virginia Avenue       pink 0.0471 0.5653
9       Tennessee Avenue     orange 0.0505 0.7066
10       St. James Place     orange 0.0513 0.7179
11       New York Avenue     orange 0.0480 0.7681
12       Kentucky Avenue        red 0.0481 0.8664
13        Indiana Avenue        red 0.0476 0.8568
14       Illinois Avenue        red 0.0484 0.9682
15       Atlantic Avenue     yellow 0.0487 1.0709
16        Ventnor Avenue     yellow 0.0491 1.0794
17        Marvin Gardens     yellow 0.0488 1.1716
18        Pacific Avenue      green 0.0490 1.2731
19 North Carolina Avenue      green 0.0468 1.2168
20   Pennsylvania Avenue      green 0.0442 1.2387
21            Park Place       blue 0.0397 1.3885
22             Boardwalk       blue 0.0407 2.0366
```

### Return on Costs

It looks like we have found us a few inefficient deeds. We haven't checked the cost of the deeds though, so calling these deeds inefficient may be a bit early. To make a double check, the bottom table contains the number of turns you'll need to have your investment paid back for every type of upgrade per deed. It still looks like you should never invest in mediterranean avenue.

```
                    name rent house_1 house_2 house_3 house_4 hotel
1   Mediterranean Avenue 30.0   11.00    5.33   2.333   1.625 1.240
2          Baltic Avenue 15.0    5.50    2.67   1.167   0.812 0.689
3        Oriental Avenue 16.7    5.00    2.22   0.926   0.750 0.636
4         Vermont Avenue 16.7    5.00    2.22   0.926   0.750 0.636
5     Connecticut Avenue 15.0    4.25    2.20   0.900   0.711 0.617
6      St. Charles Place 14.0    4.80    2.27   0.978   0.864 0.853
7          States Avenue 14.0    4.80    2.27   0.978   0.864 0.853
8        Virginia Avenue 13.3    4.33    2.00   0.920   0.800 0.733
9       Tennessee Avenue 12.9    4.00    1.90   0.873   0.773 0.716
10       St. James Place 12.9    4.00    1.90   0.873   0.773 0.716
11       New York Avenue 12.5    3.75    1.82   0.833   0.750 0.700
12       Kentucky Avenue 12.2    4.11    2.08   0.957   0.937 0.924
13        Indiana Avenue 12.2    4.11    2.08   0.957   0.937 0.924
14       Illinois Avenue 12.0    3.90    1.80   0.920   0.908 0.900
15       Atlantic Avenue 11.8    3.73    1.70   0.887   0.882 0.878
16        Ventnor Avenue 11.8    3.73    1.70   0.887   0.882 0.878
17        Marvin Gardens 11.7    3.58    1.61   0.859   0.859 0.858
18        Pacific Avenue 11.5    3.85    1.79   1.000   1.000 1.020
19 North Carolina Avenue 11.5    3.85    1.79   1.000   1.000 1.020
20   Pennsylvania Avenue 11.4    3.47    1.60   0.920   0.933 0.943
21            Park Place 10.0    3.14    1.50   0.864   0.885 0.900
22             Boardwalk  8.0    3.00    1.33   0.714   0.706 0.700
```

It now seems that you can earn your investment back a little bit sooner for the lower numbered tiles if you make the full upgrade to the hotel. Note that these return values are unnormalised for the likelihood of landing on the tiles. If you incorporate this then you'll still come to a similar conclusion.

```
                    name rent house_1 house_2 house_3 house_4 hotel
1   Mediterranean Avenue  732   268.5   130.2    57.0    39.7  30.3
2          Baltic Avenue  353   129.6    62.8    27.5    19.1  16.2
3        Oriental Avenue  407   122.0    54.2    22.6    18.3  15.5
4         Vermont Avenue  399   119.8    53.3    22.2    18.0  15.3
5     Connecticut Avenue  361   102.3    53.0    21.7    17.1  14.8
6      St. Charles Place  342   117.2    55.3    23.9    21.1  20.8
7          States Avenue  322   110.5    52.2    22.5    19.9  19.6
8        Virginia Avenue  283    92.0    42.5    19.5    17.0  15.6
9       Tennessee Avenue  255    79.3    37.6    17.3    15.3  14.2
10       St. James Place  251    78.0    37.1    17.0    15.1  14.0
11       New York Avenue  260    78.1    37.9    17.4    15.6  14.6
12       Kentucky Avenue  254    85.4    43.2    19.9    19.5  19.2
13        Indiana Avenue  257    86.4    43.7    20.1    19.7  19.4
14       Illinois Avenue  248    80.6    37.2    19.0    18.8  18.6
15       Atlantic Avenue  243    76.6    34.9    18.2    18.1  18.0
16        Ventnor Avenue  241    76.0    34.6    18.1    18.0  17.9
17        Marvin Gardens  239    73.4    33.0    17.6    17.6  17.6
18        Pacific Avenue  236    78.5    36.7    20.4    20.4  20.8
19 North Carolina Avenue  247    82.2    38.4    21.4    21.4  21.8
20   Pennsylvania Avenue  258    78.4    36.2    20.8    21.1  21.3
21            Park Place  252    79.2    37.8    21.8    22.3  22.7
22             Boardwalk  196    73.7    32.7    17.5    17.3  17.2
```

Notice that when you include the probabilties the first tiles aren't the best anymore. 

### Conclusion

There are imbalances in monopoly because of the jail mechanic. It seems that the tiles you'll hit before you hit jail from go are tiles that don't make as much sense to buy as the tiles after jail. The game tries to compensate this by having the payoff ratio between cost of upgrades and income be a bit better but it is only a minor compensation if you keep the probabilities in mind.

Monopoly is still a game of chance and there are many dimensions that we did not simulate:

- the number of players in the game
- chance cards tend to have an effect 
- you can trade deedsch
- players can go bankrupt
- if you pass go you get more cash, implying that the longer the game, the easier it is to make more investments
- you can try to buy all the houses early on in the game, causing other people to not be able to buy houses (credits **@blowski @hermanschaaf**)

Still, one clear result of this simulation is that you should keep an eye on that orange, red or yellow street. It should provide a very steady flow of income although tiles with a high number may have more of an expected profit. Investing in the tiles that are just before and just after jail seems like a poor investment choice unless your goal is to have houses before all other players. 
