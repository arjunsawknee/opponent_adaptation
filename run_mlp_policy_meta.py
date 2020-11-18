import gym
import myenvs
import torch as th

from stable_baselines3 import PPO, DQN
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

opp_policies = policies
meta_env = gym.make('rps-meta-v0')
test_meta_env = gym.make('rps-meta-v0')


eval_callback = EvalCallback(test_meta_env, eval_freq=1000, deterministic=True, render=False)


policy_kwargs = dict(activation_fn=th.nn.ReLU, net_arch=[30,30])
n_steps, batch_size, n_epochs =  50, 50, 10

model = PPO("MlpPolicy", meta_env, policy_kwargs=policy_kwargs, n_steps=n_steps, batch_size=batch_size, n_epochs=n_epochs, verbose=0)
#model.learn(total_timesteps=100000, callback=eval_callback, meta_learn=False)        # no meta learning
model.learn(total_timesteps=100000, callback=eval_callback, meta_learn=True)     # meta learning

opponent_policies = [
    np.array([0,1,2,0,1]),
    np.array([1,2,2,1,0]),
    np.array([2,1,0,0,0]),
    #np.array([2,2,1,1,0]),
    #np.array([0,1,2,2,2]),
]
eval_callback_test = EvalCallback(test_meta_env, eval_freq=500, deterministic=True, render=False)
for opponent_policy in opponent_policies:
    meta_env.fixed_opponent_policy = opponent_policy
    test_meta_env.fixed_opponent_policy = opponent_policy
    model.set_env(meta_env)
    model.learn(total_timesteps=2000, callback=eval_callback_test, meta_learn=False)



# rewards_fixed_rock = meta_env.run_sim(policies[0], 50, model, 0)
# rewards_fixed_paper = meta_env.run_sim(policies[1], 50, model, 1)
# rewards_fixed_scissors = meta_env.run_sim(policies[2], 50, model, 2)
# rewards_copycat = meta_env.run_sim(policies[3], 50, model, 3)
# rewards_random = meta_env.run_sim(policies[4], 50, model, 4)
# rewards_aggressive = meta_env.run_sim(policies[5], 50, model, 5)
# rewards_passive = meta_env.run_sim(policies[6], 50, model, 6)
# avg_rewards = [np.mean(rewards_fixed_rock), np.mean(rewards_fixed_paper), np.mean(rewards_fixed_scissors), np.mean(rewards_copycat), np.mean(rewards_random), np.mean(rewards_aggressive), np.mean(rewards_passive)]
# x = [policy.name for policy in policies]
# x_pos = [i for i, _ in enumerate(x)]
# plt.bar(x_pos, avg_rewards, color='red')
# plt.xlabel("Opponent Policy")
# plt.ylabel("Average Simulated Reward")
# plt.title("Single Agent Trained (Expanded State Space): Average Simulated Reward vs Opponent Policy")
# plt.xticks(x_pos, x)
# #plt.show()
# plt.savefig('meta.png')


# model = PPO2("MlpLstmPolicy", env, nminibatches=1, policy_kwargs=policy_kwargs, n_steps=n_steps, batch_size=batch_size, n_epochs=n_epochs, verbose=0)
# model.learn(total_timesteps= 2000, callback = eval_callback)


# # Save the agent
# model.save("ppo-rps")

# del model
# # the policy_kwargs are automatically loaded
# model = PPO.load("ppo-rps")