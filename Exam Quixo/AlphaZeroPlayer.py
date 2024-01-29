from game import Player, Move, Game
from abc import ABC, abstractmethod
import numpy as np
import time


import sys
sys.path.append("./alpha_zero")
from alpha_zero.quixo.QuixoGame import QuixoGame
from alpha_zero.quixo.quixo_utils.StateEncoder import StateEncoder
from alpha_zero.quixo.quixo_utils.ActionDecoder import ActionDecoder
from alpha_zero.quixo.pytorch.QuixoNetWrapper import QuixoNetWrapper as nn
from alpha_zero.MCTS import MCTS


class dotdict(dict):
    def __getattr__(self, name):
        return self[name]

class AlphaZeroPlayer(Player):
    def __init__(self, C=2, num_searches=800, model_path='./alpha_zero/checkpoints', model_name="best.pth.tar", policy_only=False, verbose=False) -> None:
        self.args = dotdict({
            'numMCTSSims': num_searches,
            'cpuct': C,             
        })

        self.verbose = verbose
        self.policy_only = policy_only

        if verbose: print(f"({self.__class__.__name__}) Loading wrap stateless game...", end='')
        self.game = QuixoGame()
        if verbose: print("done")

        if verbose: print(f"({self.__class__.__name__}) Loading model...", end="")
        self.nnet = nn(self.game)
        self.nnet.load_checkpoint(model_path, model_name)
        if verbose: print("done")

        if verbose: print(f"({self.__class__.__name__}) Loading MCTS object...", end="")
        self.mcts = MCTS(self.game, self.nnet, self.args)
        if verbose: print("done")

        self.state_encoder = StateEncoder()
        self.action_decoder = ActionDecoder()
        self.action_history = []

    def check_hist_cycle(self):
        for i in range(2, len(self.action_history), 2):
            sub_hist = self.action_history[-i:]
            unique_hist = list(set(sub_hist))
            if len(unique_hist) == i//2:
                print(f"Cycle of {i//2}: {sub_hist}")
                return unique_hist
        return []

    def make_move(self, game: 'Game', decode=True) -> tuple[tuple[int, int], Move]:
        if self.verbose: print("AlphaZero is thinking...", end="")
        a = time.time()
        game_board = game.get_board()
        player = game.get_current_player()

        state = self.state_encoder.to_neutral(game_board, player_id=player)
        action_probs = self.mcts.getActionProb(state, policy_only=self.policy_only)

        action = np.argmax(action_probs)
        self.action_history.append(action)

        if not decode:
            return action

        from_pos, slide = self.action_decoder(action) 
        # oggetto Enum fa schifo madonna
        for m in Move:
            if m.value == slide.value:
                slide = m
                break
        
        b=time.time()
        if self.verbose: print(f"{(b-a):.4} seconds")

        return from_pos, slide

