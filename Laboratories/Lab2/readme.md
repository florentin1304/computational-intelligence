# Lab2 - Nim game: Agent using Evolutionary strategy

The objective of this second laboratory is to create an agent able to play the nim game. The agent should be using an evolutionary strategy.

I developed three different approaches to this problem, discussed below. For each strategy, more informations and plots are to be found in their respective Jupyter Notebooks.

### Evolutionary Logistic Classifier

The nim game is a so called 'impartial game'. This means that every state of the game can be labbeled as a P-state (P-position) or a N-state (N-position). In particular, the P-state means that the state is advantageous for the previous player (the one that just moved), while the N-state means that the state is advantageous for the next player.

The strategy is to get a logistic classifier that can predict if the next state (after my agent makes the moves) is a P-state or a N-state, in order to always move into a P-state. 

The inputs of the logistic classifier are some hand-made extracted features that give information about the state of the game, eg. number of non-zero rows, maximum row, meadian value of non-zero rows, ecc.. Furthermore, the initial features are then enriched with their polynomial features, up to the third degree, thus having to optimise up to 165 weights.

Since the problem of training a logistic classifier is a 'supervised learning' one, meaning we have to give the model inputs and answers for him to train, and we don't have a dataset (furthermore we cannot create it, as we pretend not to have the optimal agent), the way the agent was optimised was by searching for its weights through an evolutionary strategy taking as a fitness the estimated average win-rate against another agent.

The fitness used during training is simply the average win-rate against the ```pure_random``` strategy over 100 games. The fitness used in the results, instead, takes the best agent in the last generation (selected with the 100 games) and plays 1000 games (to decrease uncertainty) against both ```pure_random``` and ```optimal```.

**Results**:
```
Fitness (vs. random) -> 0.893
Fitness (vs. optimal) -> 0.656
```

### Evloutionary Neural Networks

The nim game is a so called 'impartial game'. This means that every state of the game can be labbeled as a P-state (P-position) or a N-state (N-position). In particular, the P-state means that the state is advantageous for the previous player (the one that just moved), while the N-state means that the state is advantageous for the next player.

The strategy is to optimise the parameters of a neural network that can predict if the next state (after my agent makes the moves) is a P-state or a N-state, in order to always move into a P-state.

The input of the neural network is the nim game state (nim.rows), in the hope it will be able to approximate the nim-sum function without ever seeing it.

The fitness used during training is simply the average win-rate against the ```pure_random``` strategy over 100 games. The fitness used in the results, instead, takes the best agent in the last generation (selected with the 100 games) and plays 1000 games (to decrease uncertainty) against both ```pure_random``` and ```optimal```.

**Results**:
```
Fitness (vs. random) -> 0.831
Fitness (vs. optimal) -> 0.596
```

### Evolutionary Rule Weighting 

The idea is to have a set of 'interesting' rules, but letting the agent understand if they are relevant or not (eg. can select only the rows that have a prime number of items, always select the row with the minimum number of object within the fasible ones, ecc). 

The way that the strategy works is in the following way:
- The parameter optimised works as a threshold
- Next a random number in the range (0,1) is generated with an uniform probability
- If the number is below the threshold, then the rule is activated and will continue accordingly

The fitness used during training is simply the average win-rate against the ```pure_random``` strategy over 100 games. The fitness used in the results, instead, takes the best agent in the last generation (selected with the 100 games) and plays 1000 games (to decrease uncertainty) against both ```pure_random``` and ```optimal```.

**Results**:
```
Fitness (vs. random) -> 0.663
Fitness (vs. optimal) -> 0.42
```