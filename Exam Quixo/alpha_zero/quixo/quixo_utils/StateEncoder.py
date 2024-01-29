import numpy as np
from copy import deepcopy 

class StateEncoder:
    def __init__(self):
        pass

    def to_neutral(self, state, player_id):
        empty_mask = np.where(state == -1)
        p1_mask = np.where(state == 0)
        p2_mask = np.where(state == 1)

        new_state = deepcopy(state)
        new_state[empty_mask] = 0
        new_state[p1_mask] = 1
        new_state[p2_mask] = -1 

        if player_id == 1:
            new_state = -1 * new_state
        
        return new_state

    def to_game(self, state, player_id=0):
        player_symbol_game = player_id
        adv_symbol_game = 1 - player_symbol_game

        empty_mask = np.where(state == 0)
        player_mask = np.where(state == 1)
        adv_mask = np.where(state == -1)

        new_state = deepcopy(state)
        new_state[empty_mask] = -1
        new_state[player_mask] = player_symbol_game
        new_state[adv_mask] = adv_symbol_game

        return new_state
