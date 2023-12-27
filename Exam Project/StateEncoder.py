import numpy as np
from copy import deepcopy 

class StateEncoder:
    def __init__(self):
        pass

    def encode_state(self, state, player_turn):
        empty_mask = np.where(state == -1)
        p1_mask = np.where(state == 0)
        p2_mask = np.where(state == 1)

        new_state = deepcopy(state)
        new_state[empty_mask] = 0
        new_state[p1_mask] = 1
        new_state[p2_mask] = -1 

        if player_turn == 1:
            new_state = -1 * new_state
        
        return np.expand_dims(new_state, axis=0)

    def __call__(self, state, player_turn):
        return self.encode_state(state, player_turn)