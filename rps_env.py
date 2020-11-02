import gym
from gym import spaces
from rps_policy import RPSPolicy, simulate_turn, Result, Action
from rps_policy import fixed_rock_policy, fixed_paper_policy, copycat_policy, random_policy, aggressive_policy
import numpy as np

N_DISCRETE_ACTIONS = 3
DENSE_DIM = 10

class RPSEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    def __init__(self, opp_policy, max_games = 5):
        super(RPSEnv, self).__init__()
        self.games_count = 0
        self.opponent_policy = opp_policy
        self.action_space = spaces.Discrete(N_DISCRETE_ACTIONS)
        self.observation_space = spaces.Box(low=0, high=255, shape=
                                        (DENSE_DIM,), dtype=np.uint8)
        self.max_games = max_games

    def get_reward(self, action_one, action_two):
        winner = simulate_turn(action_one, action_two)
        if (winner == Result.PLAYER_ONE):
            return 1
        elif (winner == Result.PLAYER_TWO):
            return -1
        else:
            return 0

    def convert_action(self, action):
        argmax_pos = np.argmax(action)
        converted_action = Action(argmax_pos)
        ### TODO GET THIS RIGHT
        return converted_action

    def get_latent_encoding(self, opponent_history):
        ### TODO: IMPLEMENT THIS PROPERLY
        return np.random.uniform(low = 0.0, high = 255.0, size = (DENSE_DIM,))

    def step(self, action):
        converted_action = self.convert_action(action)
        opponent_action = self.opponent_policy.get_next_move()
        self.opponent_policy.update_opponent_history(converted_action)
        reward = self.get_reward(converted_action, opponent_action)
        self.games_count += 1
        done = (self.games_count == self.max_games)
        obs = self.get_latent_encoding(self.opponent_policy.history)
        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state
        self.games_count = 0
        self.opponent_policy.reset_policy()
        self.render()

    def render(self, mode='human', close=False):
        # Render the environment to the screen
        print(self.opponent_policy.opponent_history, self.opponent_policy.history)


policies = [
    fixed_rock_policy,
    fixed_paper_policy,
    copycat_policy,
    random_policy,
    aggressive_policy,
]

for policy in policies:
    env = RPSEnv(policy)
    obs = env.reset()
    done = False
    while not done:
        action = np.array([1, 0, 0])
        obs, rewards, done, info = env.step(action)
        env.render()