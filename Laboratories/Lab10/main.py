import gym_TicTacToe
import gym

# initialize the tictactoe environment
env = gym.envs.make("TTT-v0", small=-1, large=10)
state = env.reset()


# start playing
color = 1
action = 0
new_state, reward, done, _ = env.step((action, color))