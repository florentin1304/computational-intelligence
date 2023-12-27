import torch
import numpy as np

from QuixoEnv import QuixoEnv
from game import Player, Move, Game
from stable_baselines3 import PPO
from ActionDecoder import ActionDecoder
from StateEncoder import StateEncoder

class PPOAgent(Player):
    def __init__(self, path) -> None:
        super().__init__()
        policy_kwargs = dict(activation_fn=torch.nn.ReLU)

        self.model = PPO.load(path, env=QuixoEnv())
        self.action_decoder = ActionDecoder()
        self.state_encoder = StateEncoder()

    def make_move(self, game, decode=True) -> tuple[tuple[int, int], Move]:
        # First encode the state in policy-language
        board = game.get_board()
        turn = game.get_current_player()
        state = self.state_encoder(board, turn)

        # Get policy action, then decode it in game-language
        action = self.get_action(state, board)
        from_pos, move = self.action_decoder(action)

        return from_pos, move

    def get_action(self, state, board):
        policy = self.model.policy

        valid_moves = []
        for action_i in range(self.action_decoder.get_len_valid_moves()):
            from_pos, slide = self.action_decoder(action_i)
            
            # If occupied by the other player
            if state[0][from_pos[1]][from_pos[0]] == -1:
                continue

            valid_moves.append(action_i)
        
        moves_eval = policy.evaluate_actions(torch.Tensor(state), \
                         torch.Tensor(valid_moves))[1]

        return valid_moves[ torch.argmax(moves_eval) ]

        