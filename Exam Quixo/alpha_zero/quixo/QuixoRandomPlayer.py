import numpy as np

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid = self.game.getValidMoves(board, 0)
        return np.random.choice([i for i in range(len(valid)) if valid[i] == 1])