import gym
import numpy as np
import math
from copy import deepcopy
from tabulate import tabulate
from itertools import combinations

from typing import Tuple, List


class TicTacToeEnv(gym.Env):
    """
    Implementation of a TicTacToe Environment based on OpenAI Gym standards
    """

    def __init__(self, small: int = -1, large: int = 10) -> None:
        """This class contains a TicTacToe environment for OpenAI Gym

        Args:
            small (int): small reward
            large (int): large reward
        """
        n_actions = 9
        n_states = 8953  # 8953 = 3**n**2 (n=3) possible combinations
        self.action_space = gym.spaces.Discrete(n_actions)
        self.observation_space = gym.spaces.Discrete(n_states)
        self.colors = [1, 2]
        self.small = small
        self.large = large
        self.fields_per_side = int(math.sqrt(n_actions))
        self.enemy_agent = 'random'
        self.reset()

    def reset(self, adversary_first=False) -> Tuple[np.ndarray, dict]:
        """
        reset the board game and state
        """

        self.state: np.ndarray = np.zeros(
            (self.fields_per_side, self.fields_per_side), dtype=int
        )

        self.info = {"players": {1: {"actions": []}, 2: {"actions": []}}}

        self.turn = 0
        if adversary_first:
            self._adversary_move()
        
        return self.state.flatten(), self.info

    def step(self, user_action: Tuple[int, int]) -> Tuple[np.ndarray, int, bool, dict]:
        """step function of the tictactoeEnv

        Args:
          Tuple(int, int):
            action (int): integer between 0-8, each representing a field on the board
            color (int): 1 or 2, representing the color of stones of the players

        Returns:
          self.state (np.array): state of the current board position, 0 means no stone, 1 or 2 are stones placed by the players
          reward (int): reward of the currrent step
          done (boolean): true, if the game is finished
          (dict): empty dict for futur game related information
        """
        # unpack the input Tuple into action and color
        action = user_action
        my_color = 1 + self.turn

        if not self.action_space.contains(action):
            raise ValueError(f"action '{action}' is not in action_space")

        if not my_color in self.colors:
            raise ValueError(f"color '{my_color}' is not an allowed color")

        reward = self.small  # assign (negative) reward for every move done
        (row, col) = self.decode_action(action)

        if self.state[row, col] != 0:        
            self.info["players"][my_color]["actions"].append(action)
            return self.state, -self.large, True, self.info

        self.state[row, col] = my_color  # postion the token on the field
        self.info["players"][my_color]["actions"].append(action)

        if self._is_winner(my_color):
            done = True
            reward += self.large
            return self.state.copy(), reward, done, self.info
        
        elif self._is_draw():
            done = True
            return self.state.copy(), reward, done, self.info
        
        elif self.enemy_agent == 'random':
            # Change turn to enemy
            self.turn = 1 - self.turn
            enemy_color = 1 + self.turn
            self._adversary_move() # changes turn internally

            
            
            if self._is_winner(enemy_color):
                done = True
                reward -= self.large
                return self.state.copy(), reward, done, self.info
            elif self._is_draw():
                
                done = True
                return self.state.copy(), reward, done, self.info
            else:
                return self.state.copy(), reward, False, self.info
        

                # self.info["players"][color]["actions"].append(action)

            # if not done and self._is_draw():
            #     return self.state, reward, True, self.info
            
    def _adversary_move(self):
        if self.enemy_agent == 'random':
            flatten_state = np.array(self.state).flatten()
            available_plays = [i for i in range(len(flatten_state)) if flatten_state[i] == 0]
            random_play = np.random.choice(available_plays)
            row, col = self.decode_action(random_play)
            self.state[row, col] = 1 + self.turn # = color

            enemy_color = 1 + self.turn
            self.info["players"][enemy_color]["actions"].append(random_play)
        else:
            raise Exception(f"Adversary {self.enemy_agent} not known")

        self.turn = 1 - self.turn

    def _is_draw(self):
        return np.sum( self.state == 0 ) == 0

    def _is_winner(self, color: int) -> bool:
        """check if there is a winner

        Args:
            color (int): of the player

        Returns:
            bool: indicating if there is a winner
        """
        magic_square = np.array(
            [[2,7,6],
             [9,5,1],
             [4,3,8]]
        ).flatten()

        elements = [magic_square[i] for i in range(len(self.state.flatten())) if self.state.flatten()[i] == color]

        return any(sum(c) == 15 for c in combinations(elements, 3))

    def decode_action(self, action: int) -> List[int]:
        """decode the action integer into a colum and row value

        0 = upper left corner
        8 = lower right corner

        Args:
            action (int): action

        Returns:
            List[int, int]: a list with the [row, col] values
        """
        col = action % 3
        row = action // 3
        assert 0 <= col < 3
        return [row, col]

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
        board = np.zeros((3, 3), dtype=str)
        for ii in range(3):
            for jj in range(3):
                if self.state[ii, jj] == 0:
                    board[ii, jj] = "-"
                elif self.state[ii, jj] == 1:
                    board[ii, jj] = "X"
                elif self.state[ii, jj] == 2:
                    board[ii, jj] = "O"

        if mode == "human":
            board = tabulate(board, tablefmt="fancy_grid")
        return board


if __name__ == "__main__":
    env = gym.envs.make("TTT-v0", small=-1, large=10)
