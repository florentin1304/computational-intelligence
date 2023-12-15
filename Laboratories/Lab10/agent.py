import numpy as np
from collections import defaultdict

class QTable(defaultdict):
    def __missing__(self, key):
        self[key] = self.default_factory(key) 
        return self[key] 

class TicTacToeAgent:
    def __init__(self, num_of_actions, gamma=0.98,
                lr=0.01, epsilon_min=0.01, epsilon_min_episode_reached=10_000):
        self.epsilon = 1
        self.epsilon_decay_param = int((epsilon_min/(1-epsilon_min)) * (epsilon_min_episode_reached))
        self.epsilon_min = epsilon_min

        self.test = False
        self.gamma = gamma
        self.lr = lr
        self.num_of_actions = num_of_actions
        self.q_table = QTable(lambda key: np.array([0 if x == "0" else -10 for x in key], dtype=np.float16))

    def learn(self, old_state, action, new_state, reward, done, talk=False):
        old_state_encoded = self.encode_state(old_state)
        new_state_encoded = self.encode_state(new_state)
        old_state_q = self.q_table[ old_state_encoded ]
        new_state_q = self.q_table[ new_state_encoded ]

        # Target value used for updating our current Q-function estimate at Q(old_state, action)
        if done is True:
            target_value = reward  # HINT: if the episode is finished, there is not next_state. Hence, the target value is simply the current reward.
        else:
            target_value = reward + self.gamma*np.max(new_state_q) # get_argmax_from(state) -> computed in QTable

        # Update Q value
        old_q_value = old_state_q[ action ]
        self.q_table[ old_state_encoded ][ action ] = old_q_value + self.lr*(target_value - old_q_value) # update_state_action_value_to(state,action,newv_alue)


    def get_action(self, state):
        encoded_state = self.encode_state(state)
        state_q = self.q_table[ encoded_state ]

        if self.test or not (np.random.rand() < self.epsilon): # TEST or Rand > epsilon
            best_action_estimated = np.argmax(state_q)  # TODO: greedy w.r.t. q_grid
            return best_action_estimated

        else: #Rand < epsilon
            # Random action
            action_chosen = np.random.choice(self.num_of_actions)  # TODO: choose random action with equal probability among all actions
            return action_chosen


    def encode_state(self, state):
        flatten_state = state.flatten().tolist()
        key = str(flatten_state).strip("[]").replace(',', '').replace(' ', '')

        return key

    def update_epsilon(self, episode):
        self.epsilon = max(self.epsilon_decay_param / (self.epsilon_decay_param + episode), self.epsilon_min)

    def train(self):
        self.test = False

    def test(self):
        self.test = True