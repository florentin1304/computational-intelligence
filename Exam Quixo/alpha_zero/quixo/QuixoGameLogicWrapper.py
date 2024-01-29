import numpy as np
from .QuixoGameLogicOrig import Game as QuixoGameOrig 
from .QuixoGameLogicOrig import Move 

class GameLogicWrapper(QuixoGameOrig):
    def __init__(self) -> None:
        super().__init__()

    def move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
        return self._Game__move(from_pos, slide, player_id) # inheritance of private methods: https://stackoverflow.com/questions/20261517/inheritance-of-private-and-protected-methods-in-python

    def set_state(self, state):
        self._board = state
    