# Quixo Game - AlphaZero Player

## AlphaZero Algorithm Overview
AlphaZero is a groundbreaking RL algorithm developed by DeepMind published as the *Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm* paper published on arXiv.org on the 5th December 2017. It's unique in that it combines deep learning with a sophisticated tree search technique (MCTS). Unlike traditional AI algorithms that rely on hardcoded rules or databases of known strategies, AlphaZero learns to play games entirely from scratch through self-play and continuous learning.

#### Deep Learning in AlphaZero
- **Neural Networks**: At the core of AlphaZero is a deep neural network, typically consisting of several layers of neurons. This network is trained to evaluate game positions and predict the most promising moves.
- **Self-Improvement**: AlphaZero improves over time by playing games against itself. After each game, the outcomes are used to further train the neural network, refining its ability to evaluate positions and strategies.
- **Role of Training**: The neural network is initially trained on random data. Through self-play, it continuously updates its parameters to improve its understanding of the game, learning sophisticated strategies without any human input.


#### Monte Carlo Tree Search (MCTS) in AlphaZero
- **Search Algorithm**: MCTS is a heuristic search algorithm for decision processes. In the context of AlphaZero, it's used to explore the possible moves in a game.

- **Tree Exploration**: MCTS builds a search tree by exploring potential future moves, and evaluating them based on the predictions from the neural network. 

- **Balancing Exploration and Exploitation through UCB function**: The algorithm balances between exploring new, unknown parts of the search tree (exploration) and exploiting known strong moves (exploitation) by using the UCB function. This balance is crucial for both finding innovative strategies and refining known good strategies.

- **Selection of Moves**: As the search progresses, the algorithm becomes increasingly selective about which branches of the tree to explore, guided by the evaluations from the neural network.

- **Final moves probabilities**: The probability of each move is then the number of visits to the node representing the relative move (normalized between [0,1] in order to represent a categorical probability distribution)


#### Integration of MCTS and Deep Learning
- **Guided Search**: The neural network gives both the value and the probabilities of the most promising moves given the state. In practice, this allows a reduction of the search space both in depth and breadth. By indicating the most promising moves the algorithm will not be spending time expanding and analysing bad moves, effectively reducing the breadth of the search. Also by giving the approximate value of the state, when a leaf node is analysed the complete rollout is not needed, as the value given by the neural network is already the approximate mean value of being in that state, thus reducing the depth of the tree.

- **Continual Learning and Adaptation**: AlphaZero’s approach allows it to adapt its strategy to counter new opponents and situations, even those it has not encountered before. It doesn't rely on past databases but generates its knowledge dynamically.

#### The Upper Confidence Bound (UCB) selection function
The Upper Confidence Bound (UCB) formula used in AlphaZero is given by:

$` UCB(i) = \frac{Q(i)}{N(i)} + c \times P_{\text{prior}}(i|s) \times \sqrt{\frac{\ln(N(p))}{1 + N(i)}} `$, where:
  - $` UCB(i) `$ is the Upper Confidence Bound for node 'i'.
  - $` Q(i) `$ is the total accumulated reward of node 'i'.
  - $` N(i) `$ is the visit count of node 'i'.
  - $` c `$ is a tunable exploration parameter controlling the trade-off between exploration and exploitation.
  - $` P_{\text{prior}}(i|s) `$ is the prior probability of selecting the action corresponding to node 'i' from the current state 's' as provided by the neural network.
  - $` N(p) `$ is the visit count of the parent node of 'i'.

This formula combines traditional UCB terms with the prior probability term from the neural network. The \( P_{\text{prior}}(i|s) \) term encourages the selection of actions that are initially deemed more promising by the neural network, contributing to the exploration aspect. The trade-off between exploration and exploitation is controlled by the parameter 'c', allowing the algorithm to adapt its search strategy based on the specific characteristics of the problem at hand.

#### Practical Application in Quixo
In the Quixo game project, AlphaZero uses its neural network to evaluate board positions and potential moves. MCTS explores these moves, simulating various game scenarios. The results of these simulations are used to train the neural network, improving its move predictions and game evaluations over time. This integration enables the AlphaZero agent in the Quixo game to become an increasingly challenging opponent, capable of high-level strategic play.



## Credits to the original work and main differences
The core elements of this implementation of AlphaZero were inspired by [alpha-zero-general](https://github.com/suragnair/alpha-zero-general) GitHub repository by [suragnair](https://github.com/suragnair). Even though a lot of the code and the project structure were maintained, most of the core elements were modified/reimplemented in order to adapt to our project requirements. In particular, the following components were added/modified:

#### Modifications in Coach.py - Trainer of the AlphaZero Player

1. **Multithreading integration**: The modified Coach.py includes additional imports for threading. This suggests enhancements for parallel processing capabilities, potentially to speed up self-play and learning processes. In particular, each thread available on the training machine was assigned an equal number of self-play games to execute and store the results. At the end of the self-play procedure, the results from each thread are merged and the learning procedure proceeds as before.

2. **Added Arena vs RandomPlayer**: In order to understand if our agent is overfitting against past versions or itself or not an extra validation step was added: playing against RandomPlayer after each iteration. In the original work, after the training on the new data collected in the self-play procedure, the new agent played against the previous best agent in order to determine if the newly trained agent was better (thus saving the new agent checkpoint); in our version of the training procedure, the agent is also tested against a RandomPlayer in order to verify its generability and to assure it is not overfitting against its past versions.

#### Reimplementation of the MCTS - AlphaZero Core Algorithm

The original MCTS algorithm was based on a Python dictionary to keep track of the visited states and recursion to keep track of the search history in order to do the backpropagation. Unfortunately, this resulted in a very slow search as it had to create multiple function calls and then map back to the previous calls in the backpropagation phase. A further problem arose as Quixo allowed the player to find himself in the same game state. Because of the way MCTS was implemented, it would have never finished the recursion, as the stopping rule was finding a state never visited before (interpreted as a leaf in the MCTS tree search), thus it would fastly reach the maximum recursion depth. 

Because of these problems, it was decided to re-implement the MCTS algorithm. It leverages a tree data structure. It functions by having the base object `Node`, which has a reference to the parent node, as well as references to the children nodes if the node was expanded. This solved both problems, as each time a state was encountered a new `Node` object was created. This way it always finds a node that hasn't been expanded (solving the infinite recursion problem). The search for the leaf, instead, was no longer done by going down in the tree in a recursive way, but by leveraging the fact that the `Node` structure had references to its children and found a leaf node to expand in the following manner:
```
node = root
# Goes (not recursively) to a leaf node
while node.is_fully_expanded():
    node = node.select()
```
The method `Node.is_fully_expanded(self)` controls if the node has been expanded with a previous search. If it was not, the while loop stops and the `node` variable will be a leaf node by definition. This way there is no need for recursion, thus the search results are way faster.

This data-structure implementation also solves the recursion problem in the backpropagation phase. Each `Node` has information about its parent and, if the node is the root node it will have the parent-implemented as None. The `Node` class implements the backpropagation method as follows: 
```
Node.backpropagate(self, value):
  # Updates the value of the node
  self.value_sum += value
  self.visit_count += 1
  
  # Backpropagates further
  value = self.game.getOpponentValue(value)
  if self.parent is not None:
      self.parent.backpropagate(value)  
```
Even though it calls the same function on a different node and because of this it can be seen as a recursion (not solving the recursion speed problem), this can be seen as a tail-recursion, which is noticeably faster.

This implementation was initially found on [freeCodeCamp.org](https://www.youtube.com/watch?v=wuSQpLinRB4&t=3345s&ab_channel=freeCodeCamp.org) and then adapted to our needs.

#### Implementation of state-less QuixoGame 

In order for the AlphaZero algorithm to explore the possible moves it needs a model of the game. Particularly the implementation of the model has to be stateless, meaning that the object that implements the model of the game does not contain nor retain any information and only reacts to the information fed to it. For example: in order to get the next state of the game, a state has to be given as argument.

In order to implement it we used the following helper classes:

- **GameLogicWrapper Class**: The `GameLogicWrapper` class extends the base `QuixoGameOrig` class (the one provided by the professor), serving as a bridge between the game logic and the player's algorithm. It overrides the `move` function to accommodate Quixo moves, updates the current player index, and introduces a `set_state` function for explicit game state manipulation. The `get_possible_moves` function facilitates retrieving a list of valid moves for the current player.

- **ActionDecoder Class**: The `ActionDecoder` class acts as a utility, primarily involved in decoding actions. During initialization, it generates and stores all the allowed moves for the Quixo game. The object will contain all the moves that are possibly valid for the game, not given the state (e.g. the move `((0,2), MOVE.Top))` will be included, as generally, it is a valid move, while `((2,2), MOVE.Top))` will not be included, as it is never a valid move, independently of the state). The `decode_action` function translates an index into a specific game action, and `get_num_valid_moves` provides the total count of valid moves. This class is particularly useful as the neural network has no information about what a certain output represents, so we need to map it through an `ActionDecoder` object.

#### Implementation of Quixo Game Simmetry Calculator
The quixo game is inherently symmetric, both by rotating the board and by flipping the board. This is particularly useful in our case, as it can increase significantly the quantity of data given by a single game (x8). While the rotation and flip of the board are particularly simple to do, the rotation and the flip of the action probabilities used for the training are harder to compute. As explained previously, the neural network does not have information about what it is optimizing, thus it will give as an output a vector of probabilities, which are then interpreted through our `ActionDecoder` class. Because of this, in the version of the `ActionDecoder` used for the AlphaZero algorithm we also implemented two vector maps, that help us in the computations of the rotated and flipped action probability vectors. They are used as an index mapping in the following manner:

```
# The map computed in the ActionDecoder initialisation
rotate_map = action_decoder.rotate_list_translate
rot_pi = pi[rotate_map]
``` 

This way the probabilities are not changed, only their order is changed in such a way that the probability of the action before the rotation is moved to the index representing the correct action after the rotation.
