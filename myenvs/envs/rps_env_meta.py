import gym
from gym import spaces
import numpy as np

N_DISCRETE_ACTIONS = 3
DENSE_DIM = 10
MAX_GAMES = 20

class RPSEnvMeta(gym.Env):
    """Custom Environment that follows gym interface"""
    def __init__(self, opp_repeat_length=5, max_games=MAX_GAMES):
        super(RPSEnvMeta, self).__init__()
        self.games_count = 0
        self.policy_count = 0
        self.opponent_repeat_length = opp_repeat_length     # number of distinct opponents = 3^{self.opponent_repeat_length}
        self.opponent_policy = np.random.randint(3, size=self.opponent_repeat_length)
        self.opponent_action_counter = 0

        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        self.observation_space = spaces.MultiDiscrete([MAX_GAMES+1])
        self.max_games = max_games

        self.fixed_opponent_policy = None # used when testing

    def get_reward(self, action_one, action_two):
        we_win = (action_one == (action_two + 1) % 3)
        we_lose = (action_one == (action_two - 1) % 3)
        return int(we_win) - int(we_lose)

    def step(self, action):
        my_action = action
        opponent_action = self.opponent_policy[self.opponent_action_counter]
        self.opponent_action_counter = (self.opponent_action_counter + 1) % self.opponent_repeat_length

        reward = self.get_reward(my_action, opponent_action)
        self.games_count += 1
        obs = np.array([self.games_count])
        done = (self.games_count == self.max_games)
        #print(self.games_count, my_action, opponent_action, reward)
        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.games_count = 0
        self.policy_count += 1
        self.opponent_policy = np.random.randint(3, size=self.opponent_repeat_length)
        if self.fixed_opponent_policy is not None: self.opponent_policy = self.fixed_opponent_policy
        self.opponent_action_counter = 0
        self.render()
        return np.array([self.games_count])

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        # return self.opponent_policy.opponent_history, self.opponent_policy.history
        pass

    # def run_sim(self, curr_policy, num_games, model, policy_index = 0):
    #     self.games_count = 0
    #     curr_policy.reset_policy()
    #     rewards_list = []
    #     obs = np.array([0, 0])
    #     for i in range(num_games):
    #         action, _states = model.predict(obs)
    #         obs, rewards, dones, info = self.step(action)
    #         rewards_list.append(rewards)
    #     return rewards_list

