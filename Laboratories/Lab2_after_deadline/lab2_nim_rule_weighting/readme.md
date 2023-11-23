
# Evolutionary Rule Weighting 
#### Strategy description
The idea is to have a set of 'interesting' rules, but letting the agent understand if they are relevant or not (eg. can select only the rows that have a prime number of items, always select the row with the minimum number of object within the fasible ones, ecc). 

The way that the strategy works is in the following way:
- The parameter optimised works as a threshold
- Next a random number in the range (0,1) is generated with an uniform probability
- If the number is below the threshold, then the rule is activated and will continue accordingly

The fitness used during training is simply the average win-rate against the ```pure_random``` strategy over 100 games. The fitness used in the results, instead, takes the best agent in the last generation (selected with the 100 games) and plays 1000 games (to decrease uncertainty) against both ```pure_random``` and ```optimal```.


#### Implementation details
The __genome__ is the neural network's weights as a whole.

The __mutations__ are done by adding a random number sampled from a gaussian to a random parameter. The standard deviation of the gaussian gets smaller as we get closer to the final generation, in order to produce finer deviations from the best solutions as we get to the end.

The __crossover__ chosen is the one-cut crossover. An index is randomly chosen, thus the offspring will have the first parent's parameters up to that point, then the second partent's parameters up to the end. 

The __parent selection__ is done by randomly picking the parents. The selective pressure is given by giving higher probabilities to the individuals having higher fitness score. The fitness scores are scaled between (0,1) in order to give the best performing individuals a better chance to survival.

The __fitness__ used during training is simply the average win-rate against the ```pure_random``` strategy over 100 games. The fitness used in the results, instead, takes the best agent in the last generation (selected with the 100 games) and plays 1000 games (to decrease uncertainty) against both ```pure_random``` and ```optimal```.

The __simulation length__ was of 300 generations, each having 100 individuals. 

#### Results
```
Fitness (vs. random) -> 0.663
Fitness (vs. optimal) -> 0.42
```