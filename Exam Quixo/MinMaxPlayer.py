import numpy as np
import copy
import math
import collections
import time

from game import Game, Player, Move

import sys
sys.path.append("./minmax")
from minmax.QuixoGameLogicWrapper import GameLogicWrapper
from minmax.AlphaBeta import AlphaBeta

class MinMaxPlayer(Player):
    def __init__(self, depth, verbose=False):
        Player.__init__(self)
        self.depth = depth
        self.alphabeta = AlphaBeta() 
        self.verbose = verbose

    def make_move(self, game: 'Game'):
        if self.verbose: print("MinMax is thinking...", end="")
        a = time.time()
        g = GameLogicWrapper()
        g.set_state(game.get_board())
        g.current_player_idx = game.get_current_player()
        move = self.alphabeta(g, -math.inf, math.inf, self.depth)[1]
        from_pos, slide = move
        for m in Move:
            if m.value == slide.value:
                slide = m
                break
        # print(g.current_player_idx)
        # print(g._board)
        # print(from_pos, slide)
        b=time.time()        
        if self.verbose: print(f"{(b-a):.4} seconds")

    
        return from_pos, slide