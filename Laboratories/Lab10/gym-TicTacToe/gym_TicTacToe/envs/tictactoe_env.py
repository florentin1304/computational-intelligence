import gym
import numpy as np
import math
from copy import deepcopy
from tabulate import tabulate
from itertools import combinations
 
import agent # im sure I deserve a place in hell for this

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

    def reset(self, adversary_first=False, enemy_agent="random", file=None) -> Tuple[np.ndarray, dict]:
        """
        reset the board game and state
        """

        self.state: np.ndarray = np.zeros(
            (self.fields_per_side, self.fields_per_side), dtype=int
        )

        self.info = {"players": {1: {"actions": []}, 2: {"actions": []}}}

        self.turn = 0
        self.enemy_agent = enemy_agent
        if enemy_agent == 'trained':
            if file is None:
                raise Exception(f"If {enemy_agent=} you need to provide a training file path.")
            self.trained_agent = agent.TicTacToeAgent(num_of_actions=self.action_space.n)
            self.trained_agent.q_table.load_csv(file)
            self.trained_agent.test()

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
            self.info["ending"] = "illegal"
            return self.state, -self.large, True, self.info

        self.state[row, col] = my_color  # postion the token on the field
        self.info["players"][my_color]["actions"].append(action)

        if self._is_winner(my_color):
            done = True
            reward += self.large
            self.info["ending"] = "win"
            return self.state.copy(), reward, done, self.info
        
        elif self._is_draw():
            done = True
            self.info["ending"] = "draw"
            return self.state.copy(), reward, done, self.info
        
        elif self.enemy_agent is not None:
            # Change turn to enemy
            self.turn = 1 - self.turn
            enemy_color = 1 + self.turn
            self._adversary_move() # changes turn internally
            
            if self._is_winner(enemy_color):
                done = True
                reward -= self.large
                self.info["ending"] = "lose"
                return self.state.copy(), reward, done, self.info
            elif self._is_draw():
                done = True
                self.info["ending"] = "draw"
                return self.state.copy(), reward, done, self.info
            else:
                return self.state.copy(), reward, False, self.info
        
        
        return self.state.copy(), reward, done, self.info
            
    def _adversary_move(self):
        if self.enemy_agent == 'random':
            play = self._random_opponent()
            row, col = self.decode_action(play)

        elif self.enemy_agent == "magic_square":
            play = self._magic_square_opponent()
            row, col = self.decode_action(play)

        elif self.enemy_agent == "trained":
            play = self._trained_agent_opponent()
            row, col = self.decode_action(play)
            
        else:
            raise Exception(f"Adversary {self.enemy_agent} not known")

        self.state[row, col] = 1 + self.turn # = color
        enemy_color = 1 + self.turn
        self.info["players"][enemy_color]["actions"].append(play)
        self.turn = 1 - self.turn

    def _random_opponent(self):
        flatten_state = np.array(self.state).flatten()
        available_plays = [i for i in range(len(flatten_state)) if flatten_state[i] == 0]
        random_play = np.random.choice(available_plays)
        return random_play
        
    def _magic_square_opponent(self):        
        magic_square = np.array([[2,7,6],
                                 [9,5,1],
                                 [4,3,8]]).flatten()
        
        flatten_state = np.array(self.state).flatten()

        magic_square_agent_mask = (flatten_state == 1 + self.turn)
        opponent_mask = (flatten_state == 1 + (1-self.turn))


        # If two (magic opponent) moves were done
        if (np.sum(magic_square_agent_mask)>=2):
            couples = combinations(magic_square[magic_square_agent_mask], 2)
            for couple in couples:
                new_place = 15 - np.sum(couple)
                if 0 < new_place <= 9:
                    if flatten_state[magic_square == new_place][0] == 0:
                        action = np.where(magic_square == new_place)[0][0]
                        # print("CONTRAST")
                        return action

        # If two player moves were done
        if (np.sum(opponent_mask)>=2):
            couples = combinations(magic_square[opponent_mask], 2)
            for couple in couples:
                new_place = 15 - np.sum(couple)
                if 0 < new_place <= 9:
                    if flatten_state[magic_square == new_place][0] == 0:
                        action = np.where(magic_square == new_place)[0][0]
                        # print("WIN")
                        return action

        # If center is 
        if flatten_state[4] == 0:
            action = 4
        else:
            action = np.random.choice(np.where(flatten_state==0)[0])
        return action
    
    def _trained_agent_opponent(self):
        return self.trained_agent.get_action(self.state)

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
