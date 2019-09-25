from gym.envs.registration import register

register(
    id='tak-v0',
    entry_point='gym_tak.envs:GymEnv',
    max_episode_steps=1000000
)
