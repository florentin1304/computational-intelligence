import numpy as np
import copy
import math
import collections

from game import Game, Player, Move
from QuixoGameLogicWrapper import GameLogicWrapper

class AlphaBeta():
    def __init__(self):
        pass

    def __call__(self, game: 'GameLogicWrapper', alpha, beta, depth):
        self.max_depth = depth
        return self.alphabeta(game, alpha, beta, depth)

    def alphabeta(self, game: 'GameLogicWrapper', alpha, beta, depth):
        if (game.check_winner() != -1 or depth == 0):
            score = self._evaluate(game, depth)
            return (score, None)

        depth -= 1
        best_move = None

        possible_moves = game.get_possible_moves()
        move_values = np.ndarray(shape=(len(possible_moves), ))
        for i, move in enumerate(possible_moves):
            # sort possible moves evaluated by the heuristic
            game_copy = copy.deepcopy(game)
            game_copy.move(move[0], move[1], game_copy.get_current_player())
            move_values[i] = self._evaluate(game_copy, depth)
        
        ix_sorted_move_values = move_values.argsort()
        if (game.get_current_player() == 0):
            ix_sorted_move_values = ix_sorted_move_values[::-1]
        ordered_possible_moves = [possible_moves[i] for i in ix_sorted_move_values]
        # ordered_possible_moves = possible_moves

        if (game.get_current_player() == 0):
            for iter, move in enumerate(ordered_possible_moves):
                game_copy = copy.deepcopy(game)
                game_copy.move(move[0], move[1], game_copy.get_current_player())
                val = self.alphabeta(game_copy, alpha, beta, depth)[0]
                if (val > alpha):
                    alpha = val
                    best_move = move
                if (alpha >= beta):
                    break
            return (alpha, best_move)
        else:
            for iter, move in enumerate(ordered_possible_moves):
                game_copy = copy.deepcopy(game)
                game_copy.move(move[0], move[1], game_copy.get_current_player())
                val = self.alphabeta(game_copy, alpha, beta, depth)[0]
                if (val < beta):
                    beta = val
                    best_move = move
                if (alpha >= beta):
                    break
            return (beta, best_move)
    
    # Evaluates the current game state
    def _evaluate(self, game: 'Game', depth):
        transpose = game.get_board().transpose()
        count = []
        opponent_count = []
        for row, column in zip(game.get_board(), transpose):
            row_counter = collections.Counter(row)
            column_counter = collections.Counter(column)
            count.append(row_counter.get(0, 0))
            count.append(column_counter.get(0, 0))
            opponent_count.append(row_counter.get(1, 0))
            opponent_count.append(column_counter.get(1 , 0))

        element_in_codiagonal = game.get_board()[:, ::-1]
        diagonals = [np.diagonal(game.get_board()), np.diagonal(element_in_codiagonal)]
        main_diagonal_count = collections.Counter(diagonals[0])
        second_diagonal_count = collections.Counter(diagonals[1])
        count.append(main_diagonal_count.get(0, 0))
        count.append(second_diagonal_count.get(0, 0))
        opponent_count.append(main_diagonal_count.get(1, 0))
        opponent_count.append(second_diagonal_count.get(1, 0))

        score_max = 5 ** max(count)
        score_min = 5 ** max(opponent_count)

        return score_max - score_min