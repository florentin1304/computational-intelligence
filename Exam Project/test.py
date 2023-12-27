import random
import numpy as np
import tqdm
import torch

from stable_baselines3.common import env_checker
from stable_baselines3 import PPO, SAC

from game import Game, Move, Player
from QuixoEnv import QuixoEnv
from PolicyFeatureExtractor import PolicyFeatureExtractor
from Agent import PPOAgent

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move



if __name__ == '__main__':
    q_env = QuixoEnv()
    policy_kwargs = dict(activation_fn=torch.nn.ReLU)
    
    me_player = "models/checkpoints_selfplay/ppo_last_selfplay.ai"
    vs_player = "models/ppo_best_random.ai"

    ### PLAY
    test_games = 1000
    play_wins = 0
    play_lose = 0
    play_long = 0
    player1 = PPOAgent(me_player)
    player2 = RandomPlayer()#PPOAgent(vs_player)
    for i in tqdm.tqdm(range(test_games)):
        g = Game()
        winner = g.play(player1, player2)
        if winner == 0:
            play_wins += 1
        if winner == 1:
            play_lose += 1
        if winner == -1:
            play_long +=1

    print("Winrate as player1", play_wins/test_games)
    print("Lose as player1", play_lose/test_games)
    print("Long as player1", play_long/test_games)

    test_games = 1000
    play_wins = 0
    play_lose = 0
    play_long = 0
    player1 = RandomPlayer() #PPOAgent(vs_player)
    player2 = PPOAgent(me_player)
    for i in tqdm.tqdm(range(test_games)):
        g = Game()
        winner = g.play(player1, player2)
        if winner == 1:
            play_wins += 1
        if winner == 0:
            play_lose += 1
        if winner == -1:
            play_long +=1
    print("Winrate as player2", play_wins/test_games)
    print("Lose as player2", play_lose/test_games)
    print("Long as player2", play_long/test_games)