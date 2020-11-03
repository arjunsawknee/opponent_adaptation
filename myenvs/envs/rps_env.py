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
        # self.policy_count = 0
        # self.opponent_policies = opp_policies
        # self.opponent_policy = self.opponent_policies[self.policy_count % len(self.opponent_policies)]
        self.opponent_policy = opp_policy
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        self.observation_space = spaces.MultiDiscrete([N_DISCRETE_ACTIONS, N_DISCRETE_ACTIONS])
        self.max_games = max_games

    def get_reward(self, action_one, action_two):
        we_win = (action_one == (action_two + 1) % 3)
        we_lose = (action_one == (action_two - 1) % 3)
        return int(we_win) - int(we_lose)

    def step(self, action, opponent_policy = None):
        my_action = action
        if opponent_policy is None:
            opponent_action = self.opponent_policy.get_next_move()
            self.opponent_policy.update_opponent_history(my_action)
        else:
            opponent_action = opponent_policy.get_next_move()
            opponent_policy.update_opponent_history(my_action)

        obs = np.array([opponent_action, my_action])
        reward = self.get_reward(my_action, opponent_action)
        self.games_count += 1
        done = (self.games_count == self.max_games)

        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.games_count = 0
        # self.policy_count += 1
        # self.opponent_policy = self.opponent_policies[self.policy_count % len(self.opponent_policies)]
        self.opponent_policy.reset_policy()
        self.render()
        return np.array([0, 0])

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        # return self.opponent_policy.opponent_history, self.opponent_policy.history
        pass

    def run_sim(self, curr_policy, num_games, model):
        self.games_count = 0
        curr_policy.reset_policy()
        rewards_list = []
        obs = np.array([0, 0])
        for i in range(num_games):
            action, _states = model.predict(obs)
            obs, rewards, dones, info = self.step(action, opponent_policy = curr_policy)
            rewards_list.append(rewards)
        return rewards_list

