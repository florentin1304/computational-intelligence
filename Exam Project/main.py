import random
import numpy as np
import tqdm
import torch

from stable_baselines3.common import env_checker
from stable_baselines3 import PPO, SAC

from Agent import PPOAgent
from game import Game, Move, Player
from QuixoEnv import QuixoEnv
from ActionDecoder import ActionDecoder
from StateEncoder import StateEncoder
from PolicyFeatureExtractor import PolicyFeatureExtractor

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'Game') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move

if __name__ == '__main__':
    q_env = QuixoEnv()
    env_checker.check_env(q_env, warn=True, skip_render_check=True)
    policy_kwargs = dict(activation_fn=torch.nn.ReLU,
                         net_arch=dict(pi=[128, 128, 64, 64],
                                        vf=[128, 128, 64, 64]),
                         features_extractor_class=PolicyFeatureExtractor,
                         features_extractor_kwargs=dict(features_dim=256)
                         )

    model = PPO("CnnPolicy", q_env, ent_coef=0.01, verbose=1, policy_kwargs=policy_kwargs)
    # Policy training 
    for i in range(0, 5):
        print("="*30, i ,"="*30)
        model.learn(total_timesteps = 100_000)
        model.save(f"models/checkpoints_random/ppo_{i}.ai")
        model.save(f"models/checkpoints_random/ppo_last_random.ai")
    model.save(f"models/ppo_best_random.ai")

    # # Self play
    q_env = QuixoEnv()
    adv_list = []
    adv_list.append( PPOAgent("models/ppo_best_random.ai") )
    q_env.set_adversary_list(adv_list)
    model = PPO.load("models/checkpoints_random/ppo_last_random.ai", q_env , policy_kwargs=policy_kwargs)
    # model = PPO.load("models/checkpoints_selfplay/ppo_11.ai", q_env , policy_kwargs=policy_kwargs)

    for i in range(0, 20):
        print("="*30, i ,"="*30)
        model.learn(total_timesteps = 250_000)
        model.save(f"models/checkpoints_selfplay/ppo_{i}.ai")
        model.save(f"models/checkpoints_selfplay/ppo_last_selfplay.ai")

        # Add checkpoint to adversaries
        new_checkpoint_agent = PPOAgent(f"models/checkpoints_selfplay/ppo_last_selfplay.ai")
        adv_list.append(new_checkpoint_agent)
        adv_list = adv_list[-10:]

        # Update adv list and model
        q_env = QuixoEnv()
        q_env.set_adversary_list(adv_list)
        model = PPO.load("models/checkpoints_selfplay/ppo_last_selfplay.ai", q_env , policy_kwargs=policy_kwargs)

    model.save(f"models/ppo_best_selfplay.ai")

    
    # Self play
    # q_env = QuixoEnv()
    # adv_list = [MyPlayer(f"models/checkpoints_selfplay/ppo_{i}.ai", 0) for i in range(25, 50)]
    # adv_list.append(MyPlayer(f"models/ppo_best_vsrandom.ai", 0))
    # q_env.set_adversary_list(adv_list)
    # model = PPO.load("models/ppo_best.ai", q_env , policy_kwargs=policy_kwargs)

    # model.learn(total_timesteps = 2_000_000)
    # model.save(f"models/ppo_best_2m.ai")

