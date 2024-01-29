import numpy as np
import math
import torch

import torch.nn as nn
import torch.nn.functional as F

class Node:
    def __init__(self, game, args, state, parent=None, action_taken=None, prior=0, visit_count=0):
        self.game = game
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken
        self.prior = prior
        
        self.children = []
        
        self.visit_count = visit_count
        self.value_sum = 0
        
    def is_fully_expanded(self):
        return len(self.children) > 0
    
    def select(self):
        best_child = None
        best_ucb = -np.inf
        
        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb
                
        return best_child
    
    def get_ucb(self, child):
        if child.visit_count == 0:
            q_value = 0
        else:
            q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return q_value + self.args['cpuct'] * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior
    

    def expand(self, policy):
        for action, prob in enumerate(policy):
            if prob > 0:
                child_state = self.state.copy()
                child_state = self.game.getNextState(board=child_state, action=action, player=1)[0]
                child_state = self.game.getCanonicalForm(child_state, player=-1)

                child = Node(self.game, self.args, child_state, self, action, prob)
                self.children.append(child)
                
        return child
            
    def backpropagate(self, value):
        # Updates the value of the node
        self.value_sum += value
        self.visit_count += 1
        
        # Backpropagates further
        value = self.game.getOpponentValue(value)
        if self.parent is not None:
            self.parent.backpropagate(value)  


class MCTS:
    def __init__(self, game, model, args):
        self.game = game
        self.args = args
        self.model = model
    
    def getActionProb(self, state, policy_only=False):
        if policy_only:
            policy, _ = self.model.predict(state)
            valid_moves = self.game.getValidMoves(state, None)
            policy *= valid_moves
            policy /= np.sum(policy)
            return policy
        return self.search(state)

    @torch.no_grad()
    def search(self, state):
        root = Node(self.game, self.args, state, visit_count=1)
        
        policy, _ = self.model.predict(state)

        valid_moves = self.game.getValidMoves(state, None)
        policy *= valid_moves
        policy /= np.sum(policy)
        root.expand(policy)
        
        for search in range(self.args['numMCTSSims']):
            node = root
            
            # Goes (not recursively) to a leaf node
            while node.is_fully_expanded():
                node = node.select()
            
            # value = 1 if self.game.getGameEnded(node.state, player=None) != 0 else 0
            # is_terminal = (value != 0)
            # value = self.game.getOpponentValue(value)
            
            # node.state is always in canonical form
            value = self.game.getGameEnded(node.state, player=None)
            is_terminal = (value != 0)

            if not is_terminal:
                policy, value = self.model.predict(node.state)
                
                valid_moves = self.game.getValidMoves(node.state, None)
                policy *= valid_moves
                policy /= np.sum(policy)
                
                value = value.item()

                node.expand(policy)
                
            node.backpropagate(value)    
            
            
        action_probs = np.zeros(self.game.getActionSize())
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs
        
