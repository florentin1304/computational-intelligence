# Evloutionary Neural Networks
#### Strategy description
The nim game is a so called 'impartial game'. This means that every state of the game can be labbeled as a P-state (P-position) or a N-state (N-position). In particular, the P-state means that the state is advantageous for the previous player (the one that just moved), while the N-state means that the state is advantageous for the next player.

The strategy is to optimise the parameters of a neural network that can predict if the next state (after my agent makes the moves) is a P-state or a N-state, in order to always move into a P-state. The way we choose the next move is by simulating all possible moves and evaluating every possible next state, choosing finally the one we are more confident its advantageous to us. 

The input of the neural network is the nim game state (nim.rows), in the hope it will be able to approximate the nim-sum function without ever seeing it.

#### Implementation details
The __genome__ is the neural network's weights as a whole.

The __mutations__ are done by adding a random numbers sampled from a gaussian to an entire layer. The standard deviation of the gaussian gets smaller as we get closer to the final generation, in order to produce finer deviations from the best solutions as we get to the end.

The __crossover__ chosen is the one-cut crossover for each layer. For each individual layer of the offspring a random number is chosen between one and the number of rows in that 

The __parent selection__ is done by having a steady-state approach. We always keep the quarter of the population that had the best performance, then create the offsprings from them.

The __fitness__ used during training is simply the average win-rate against the ```pure_random``` strategy over 100 games. The fitness used in the results, instead, takes the best agent in the last generation (selected with the 100 games) and plays 1000 games (to decrease uncertainty) against both ```pure_random``` and ```optimal```.

The __simulation length__ was of 150 generations, each having 50 individuals. The simulation was sped up by threading the evaluation step.


#### Results
```
Fitness (vs. random) -> 0.831
Fitness (vs. optimal) -> 0.596
```
