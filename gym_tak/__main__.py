from gym_tak import *
from tf_agents.environments import suite_gym, tf_py_environment

env = suite_gym.load('tak-v0')
tf_env = tf_py_environment.TFPyEnvironment(env)
print(tf_env.time_step_spec())
print(tf_env.action_spec())
