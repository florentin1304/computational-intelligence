import random
from game import Game, Move, Player

class ActionDecoder:
    def __init__(self):
        slides = [Move.BOTTOM, Move.TOP, Move.RIGHT, Move.LEFT]

        self.valid_moves = []
        for i in range(5):
            for j in range(5):
                for s in slides:
                    g = Game()
                    acceptable = g.move(from_pos=(i,j), slide=s, player_id=0)
                    if acceptable:
                        self.valid_moves.append( [ (i,j), s  ] )
        
        self.num_valid_moves = len(self.valid_moves)

    def decode_action(self, index):
        """
        decodes the action
        returns: from_pos: tuple[int, int], slide: Move
        """
        assert index < self.get_len_valid_moves()
        action = self.valid_moves[index]
        return action[0], action[1]

    def get_len_valid_moves(self):
        return self.num_valid_moves

    def __call__(self, index):
        return self.decode_action(index)
                        