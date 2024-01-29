# MinMax Alpha-Beta Algorithm for Quixo Game

## Introduction
The provided Python implementation showcases a minimax Alpha-Beta algorithm adapted for the Quixo game. This documentation breaks down the functionality into distinct classes and functions.

### AlphaBeta Class
The `AlphaBeta` class is the core of the algorithm.

The `alphabeta` function is the core of the Alpha-Beta pruning algorithm for the Quixo game. It recursively explores possible moves in the game tree while applying heuristics to efficiently narrow down the search space.

In explanation, the `alphabeta` function
   - first checks either a winner has been determined or the depth of the search has reached zero.

Otherwise

   - the function, generates a list of possible moves for the current game state. To optimize the search, it evaluates each move by creating a deep copy of the game state and applying the move. These moves are then sorted based on their heuristic values. This ordering is crucial for the subsequent steps, as it helps prioritize more promising moves and potentially prune the search space faster.

   - Depending on the current player's turn, the function iterates through the ordered moves. For the maximizing player (player 0), it updates the alpha value and selects the best move if a better evaluation is found. For the minimizing player, it updates the beta value and selects the best move accordingly. The loop is designed to break early if the alpha-beta pruning condition is met, optimizing the search process.

   - The function returns a tuple with the final alpha or beta value, representing the best evaluation score, and the corresponding best move found during the search.


The `_evaluate` function, instead, computes a heuristic score for the current game state based on various factors. The formula for the evaluation involves counting occurrences of player and opponent pieces in rows, columns, and diagonals. The counts are then used to calculate a score that emphasizes maximizing the player's potential and minimizing the opponent's potential.

The detailed steps include:
   - Transposing the game board to analyze columns.
   - Counting occurrences of player and opponent pieces in rows and columns.
   - Calculating counts for main and secondary diagonals.
   - Applying a scoring formula that considers the maximum occurrence in each category.

The formula aims to reward configurations that align with the player's objectives while penalizing opponent-friendly configurations. This heuristic evaluation guides the Alpha-Beta algorithm to make informed decisions during the search process, prioritizing moves that lead to more favourable game states.

### GameLogicWrapper Class
The `GameLogicWrapper` class extends the base `QuixoGameOrig` class (the one provided by the professor), serving as a bridge between the game logic and the Alpha-Beta algorithm. It overrides the `move` function to accommodate Quixo moves, updates the current player index, and introduces a `set_state` function for explicit game state manipulation. The `get_possible_moves` function facilitates retrieving a list of valid moves for the current player.

### ActionDecoder Class
The `ActionDecoder` class acts as a utility, primarily involved in decoding actions. During initialization, it generates and stores all valid moves for the Quixo game. The `decode_action` function translates an index into a specific game action, and `get_num_valid_moves` provides the total count of valid moves.