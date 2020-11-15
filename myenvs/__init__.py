from gym.envs.registration import register

register(
    id='rps-v0',
    entry_point='myenvs.envs:RPSEnv',
)

register(
    id='rps-multitask-v0',
    entry_point='myenvs.envs:RPSEnvMultitask',
)