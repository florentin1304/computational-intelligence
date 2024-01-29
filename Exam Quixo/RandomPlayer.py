from game import Player, Move, Game
from abc import ABC, abstractmethod
import numpy as np
import time
import random
from gui.GameUI import GameUI


class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, gameUI: 'GameUI') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move