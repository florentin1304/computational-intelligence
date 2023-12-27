import gymnasium as gym
import numpy as np
import math
from copy import deepcopy
import random
# from tabulate import tabulate
# from itertools import combinations
from typing import Tuple, List

from ActionDecoder import ActionDecoder
from StateEncoder import StateEncoder
from game import Game, Move


class QuixoEnv(gym.Env):
    """
    Implementation of a TicTacToe Environment based on OpenAI Gym standards
    """

    def __init__(self, small: int = -0.25, large: int = 10) -> None:
        """This class contains a TicTacToe environment for OpenAI Gym

        Args:
            small (int): small reward
            large (int): large reward
        """
        n_actions = 44
        n_states = 3*np.ones(shape=(5,5))
        self.action_space = gym.spaces.Discrete(n_actions)
        self.observation_space = gym.spaces.Box(low=-1, high=1, shape=(1,5,5), dtype=np.int16)
        
        self.actiondecoder = ActionDecoder()
        self.state_encoder = StateEncoder()

        self.small = small
        self.large = large
        self.adversary_list = None
        self.enemy_agent = None
        self.reset()

    def reset(self, seed=319029, enemy_agent="random", file=None) -> Tuple[np.ndarray, dict]:
        """
        reset the board game and state
        """
        self.num_steps = 0
        self.game = Game()
        self.info = {"players": {0: {"actions": []}, 1: {"actions": []}}}
        

        self.game.current_player_idx = 0
        self.adversary_first = np.random.choice([True, False])

        if self.adversary_list is not None:
            self.enemy_agent = np.random.choice(self.adversary_list)
            self.enemy_agent.player_id = 0 if self.adversary_first else 1

        if self.adversary_first:
            self._adversary_move()
        
        return self._get_state(), self.info

    def step(self, action) -> Tuple[np.ndarray, int, bool, dict]:

        if not self.action_space.contains(action):
            raise ValueError(f"action '{action}' is not in action_space")

        self.num_steps += 1
        reward = self.small  # assign (negative) reward for every move done
        if self.num_steps > 200:
            return self._get_state(), -10*self.large, True, False, self.info

        pos, slide = self.actiondecoder.decode_action(action)
        valid = self.game.move(pos, slide, self.game.current_player_idx)
        self.info["players"][self.game.current_player_idx]["actions"].append([pos, slide])

        if not valid:
            done = True
            self.info["ending"] = "illegal"
            return self._get_state(), -10*self.large, done, False, self.info

        if self.game.check_winner() == self.game.current_player_idx:
            done = True
            reward += self.large
            self.info["ending"] = "win"
            return self._get_state(), reward, done, False, self.info
        
        # ENEMY
        else:
            # Change turn to enemy
            self.game.current_player_idx = 1 - self.game.current_player_idx
            self._adversary_move() # changes turn internally
            
            if self.game.check_winner() == self.game.current_player_idx:
                done = True
                reward -= self.large
                self.info["ending"] = "lose"
                return self._get_state(), reward, done, False, self.info
            else:
                return self._get_state(), reward, False, False, self.info
        
        
        return self._get_state(), reward, done, False, self.info

    def set_adversary_list(self, adv_list):
        self.adversary_list = adv_list

    def _get_state(self, for_adv=False):
        player_id = 1 if self.adversary_first else 0
        player_id = (1 - player_id) if for_adv else player_id 
        return self.state_encoder(self.game.get_board(), player_id).astype(np.int16)

    def _adversary_move(self):
        if self.enemy_agent:
            play = self.enemy_agent.make_move( self.game )
            pos, slide = play
            self.game.move(pos, slide, self.game.current_player_idx)            
        else:
            play = self._random_opponent_move()

        self.info["players"][self.game.current_player_idx]["actions"].append(play)
        self.game.current_player_idx = 1 - self.game.current_player_idx

    def _random_opponent_move(self):
        ok = False
        while not ok:
            from_pos = (random.randint(0, 4), random.randint(0, 4))
            slide = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
            ok = self.game.move(from_pos, slide, self.game.current_player_idx)

        return from_pos, slide

    def _trained_agent_opponent(self):
        action = self.trained_agent.get_action(self.game.get_board())
        pos, slide = self.actiondecoder.decode_action(action)
        return pos, slide


    def render(self, mode="human") -> None:
        """render the board

        The following charachters are used to represent the fields,
            '-' no stone
            'O' for player 0
            'X' for player 1

        example:
            ╒═══╤═══╤═══╕
            │ O │ - │ - │
            ├───┼───┼───┤
            │ - │ X │ - │
            ├───┼───┼───┤
            │ - │ - │ - │
            ╘═══╧═══╧═══╛
        """
        board = np.zeros((5, 5), dtype=str)
        for ii in range(5):
            for jj in range(5):
                if self.state[ii, jj] == 0:
                    board[ii, jj] = "-"
                elif self.state[ii, jj] == 1:
                    board[ii, jj] = "X"
                elif self.state[ii, jj] == 2:
                    board[ii, jj] = "O"

        if mode == "human":
            board = tabulate(board, tablefmt="fancy_grid")
        return board
