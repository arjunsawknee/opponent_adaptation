import gym
from gym import spaces
import numpy as np

N_DISCRETE_ACTIONS = 3
DENSE_DIM = 10

class RPSEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    def __init__(self, opp_policy, max_games=20):
        super(RPSEnv, self).__init__()
        self.games_count = 0
        self.opponent_policy = opp_policy
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        self.observation_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        self.max_games = max_games

    def get_reward(self, action_one, action_two):
        we_win = (action_one == (action_two + 1) % 3)
        we_lose = (action_one == (action_two - 1) % 3)
        return int(we_win) - int(we_lose)

    def step(self, action):
        my_action = action
        opponent_action = self.opponent_policy.get_next_move()
        self.opponent_policy.update_opponent_history(my_action)

        obs = opponent_action
        reward = self.get_reward(my_action, opponent_action)
        self.games_count += 1
        done = (self.games_count == self.max_games)

        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.games_count = 0
        self.opponent_policy.reset_policy()
        self.render()
        return 0

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        # return self.opponent_policy.opponent_history, self.opponent_policy.history
        pass
