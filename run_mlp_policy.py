import gym
import myenvs
import torch as th

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from rps_policy import policies

# FOR REFERENCE
# policies[0] = fixed_rock_policy,
# policies[1] = fixed_paper_policy,
# policies[2] = fixed_scissors_policy,
# policies[3] = copycat_policy,
# policies[4] = random_policy,
# policies[5] = aggressive_policy,
# policies[6] = passive_policy,

opp_policy = policies[5]
env = gym.make('rps-v0', opp_policy=opp_policy)
test_env = gym.make('rps-v0', opp_policy=opp_policy)
eval_callback = EvalCallback(test_env, eval_freq=10, deterministic=True, render=False)


policy_kwargs = dict(activation_fn=th.nn.ReLU, net_arch=[8, 8])
n_steps, batch_size, n_epochs =  10, 10, 10

model = PPO("MlpPolicy", env, policy_kwargs=policy_kwargs, n_steps=n_steps, batch_size=batch_size, n_epochs=n_epochs, verbose=0)
model.learn(total_timesteps=200, callback=eval_callback)

# Save the agent
model.save("ppo-rps")

del model
# the policy_kwargs are automatically loaded
model = PPO.load("ppo-rps")