import gym
import myenvs
import torch as th

from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
from rps_policy import policies
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 7})

# FOR REFERENCE
# policies[0] = fixed_rock_policy,
# policies[1] = fixed_paper_policy,
# policies[2] = fixed_scissors_policy,
# policies[3] = copycat_policy,
# policies[4] = random_policy,
# policies[5] = aggressive_policy,
# policies[6] = passive_policy,

opp_policy = policies[6]
env = gym.make('rps-v0', opp_policy=opp_policy)
test_env = gym.make('rps-v0', opp_policy=opp_policy)

# # env = gym.make('rps-v0', opp_policies=policies)
# # test_env = gym.make('rps-v0', opp_policies=policies)
eval_callback = EvalCallback(test_env, eval_freq=10, deterministic=True, render=False)


policy_kwargs = dict(activation_fn=th.nn.ReLU, net_arch=[8,8])
n_steps, batch_size, n_epochs =  10, 10, 10

model = PPO("MlpPolicy", env, policy_kwargs=policy_kwargs, n_steps=n_steps, batch_size=batch_size, n_epochs=n_epochs, verbose=0)
model.learn(total_timesteps=1000, callback=eval_callback)
rewards_fixed_rock = env.run_sim(policies[0], 50, model)
rewards_fixed_paper = env.run_sim(policies[1], 50, model)
rewards_fixed_scissors = env.run_sim(policies[2], 50, model)
rewards_copycat = env.run_sim(policies[3], 50, model)
rewards_random = env.run_sim(policies[4], 50, model)
rewards_aggressive = env.run_sim(policies[5], 50, model)
rewards_passive = env.run_sim(policies[6], 50, model)
avg_rewards = [np.mean(rewards_fixed_rock), np.mean(rewards_fixed_paper), np.mean(rewards_fixed_scissors), np.mean(rewards_copycat), np.mean(rewards_random), np.mean(rewards_aggressive), np.mean(rewards_passive)]
x = [policy.name for policy in policies]
x_pos = [i for i, _ in enumerate(x)]
plt.bar(x_pos, avg_rewards, color='red')
plt.xlabel("Opponent Policy")
plt.ylabel("Average Simulated Reward")
plt.title("Individual Agents Trained (Expanded State Space): Average Simulated Reward vs Opponent Policy")
plt.xticks(x_pos, x)
plt.show()



# model = PPO2("MlpLstmPolicy", env, nminibatches=1, policy_kwargs=policy_kwargs, n_steps=n_steps, batch_size=batch_size, n_epochs=n_epochs, verbose=0)
# model.learn(total_timesteps= 2000, callback = eval_callback)


# # Save the agent
# model.save("ppo-rps")

# del model
# # the policy_kwargs are automatically loaded
# model = PPO.load("ppo-rps")