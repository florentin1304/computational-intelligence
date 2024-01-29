import numpy as np

from QuixoGameLogicOrig import Game as QuixoGameOrig 
from QuixoGameLogicOrig import Move 

class ActionDecoder:
    def __init__(self):
        slides = [Move.BOTTOM, Move.TOP, Move.RIGHT, Move.LEFT]

        self.valid_moves = []
        for i in range(5):
            for j in range(5):
                for s in slides:
                    g = GameLogicWrapper()
                    acceptable = g.move(from_pos=(i,j), slide=s, player_id=0)
                    if acceptable:
                        self.valid_moves.append( [ (i,j), s ] )
        
        self.num_valid_moves = len(self.valid_moves)

    def decode_action(self, index):
        """
        decodes the action
        returns: from_pos: tuple[int, int], slide: Move
        """
        assert index < self.get_num_valid_moves()
        action = self.valid_moves[index]
        return action[0], action[1]

    def get_num_valid_moves(self):
        return self.num_valid_moves

    def __call__(self, index):
        return self.decode_action(index)
                        

class GameLogicWrapper(QuixoGameOrig):
    def __init__(self) -> None:
        super().__init__()

    def move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
        # inheritance of private methods: https://stackoverflow.com/questions/20261517/inheritance-of-private-and-protected-methods-in-python
        ok = self._Game__move(from_pos, slide, player_id)
        # change the current player
        self.current_player_idx += 1
        self.current_player_idx %= 2
        return ok
    
    def set_state(self, state):
        self._board = state
    
    def get_possible_moves(self):
        action_decoder = ActionDecoder()
        action_size = action_decoder.get_num_valid_moves()
        valid_moves =[]
        for action_i in range(action_size):
            from_pos, slide = action_decoder(action_i)
            if self._board[from_pos[1], from_pos[0]] == -1 or self._board[from_pos[1], from_pos[0]] == self.current_player_idx:
                valid_moves.append([from_pos, slide])

        return valid_moves