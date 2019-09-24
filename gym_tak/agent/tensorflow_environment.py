from __future__ import absolute_import, division, print_function

import base64

import IPython
import imageio
import matplotlib.pyplot as plt
import pyvirtualdisplay
import tensorflow as tf
from tf_agents.agents.dqn import dqn_agent
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.networks import q_network
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common

tf.compat.v1.enable_v2_behavior()


class TensorFlowEnvironment:

    def __init__(self) -> None:
        super().__init__()
        self.display = pyvirtualdisplay.Display(visible=0, size=(1400, 900)).start()
        self.num_iterations = 20000
        self.num_iterations = 20000

        self.initial_collect_steps = 1000
        self.collect_steps_per_iteration = 1
        self.replay_buffer_max_length = 100000

        self.batch_size = 64
        self.learning_rate = 1e-3
        self.log_interval = 200

        self.num_eval_episodes = 10
        self.eval_interval = 1000

        self.env_name = None
        self.env = None
        self.load()

        self.train_py_env = suite_gym.load(self.env_name)
        self.eval_py_env = suite_gym.load(self.env_name)

        self.train_env = tf_py_environment.TFPyEnvironment(self.train_py_env)
        self.eval_env = tf_py_environment.TFPyEnvironment(self.eval_py_env)

        self.fc_layer_params = (100,)
        self.q_net = q_network.QNetwork(
            self.train_env.observation_spec(),
            self.train_env.action_spec(),
            fc_layer_params=self.fc_layer_params
        )

        self.optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=self.learning_rate)
        self.train_step_counter = tf.Variable(0)
        self.agent = dqn_agent.DqnAgent(
            self.train_env.time_step_spec(),
            self.train_env.action_spec(),
            q_network=self.q_net,
            optimizer=self.optimizer,
            td_errors_loss_fn=common.element_wise_squared_loss,
            train_step_counter=self.train_step_counter
        )
        self.agent.initialize()

        self.eval_policy = self.agent.policy
        self.collect_policy = self.agent.collect_policy
        self.random_policy = random_tf_policy.RandomTFPolicy(
            self.train_env.time_step_spec(),
            self.train_env.action_spec()
        )

        self.example_environment = tf_py_environment.TFPyEnvironment(suite_gym.load(self.env_name))
        self.time_step = self.example_environment.reset()
        self.random_policy.action(self.time_step)

        self.replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
            data_spec=self.agent.collect_data_spec,
            batch_size=self.train_env.batch_size,
            max_length=self.replay_buffer_max_length
        )

        self.dataset = self.replay_buffer.as_dataset(
            num_parallel_calls=3,
            sample_batch_size=self.batch_size,
            num_steps=2
        ).prefetch(3)

    def load(self) -> None:
        self.env_name = 'tak-v0'
        self.env = suite_gym.load(self.env_name)
        self.env.reset()

    @staticmethod
    def compute_avg_return(environment, policy, num_episodes=10):
        total_return = 0.0
        for _ in range(num_episodes):
            time_step = environment.reset()
            episode_return = 0.0

            while not time_step.is_last():
                action_step = policy.action(time_step)
                time_step = environment.step(action_step.action)
                episode_return += time_step.reward

            total_return += episode_return

        avg_return = total_return / num_episodes
        return avg_return.numpy()[0]

    @staticmethod
    def collect_step(environment, policy, buffer):
        time_step = environment.current_time_step()
        action_step = policy.action(time_step)
        next_time_step = environment.step(action_step.action)
        traj = trajectory.from_transition(time_step, action_step, next_time_step)

        buffer.add_batch(traj)

    @staticmethod
    def collect_data(env, policy, buffer, steps):
        for _ in range(steps):
            TensorFlowEnvironment.collect_step(env, policy, buffer)

    def train(self):
        iterator = iter(self.dataset)

        # (Optional) Optimize by wrapping some of the code in a graph using TF function.
        self.agent.train = common.function(self.agent.train)

        # Reset the train step
        self.agent.train_step_counter.assign(0)

        # Evaluate the agent's policy once before training.
        avg_return = self.compute_avg_return(self.eval_env, self.agent.policy, self.num_eval_episodes)
        returns = [avg_return]

        for _ in range(self.num_iterations):

            # Collect a few steps using collect_policy and save to the replay buffer.
            for _ in range(self.collect_steps_per_iteration):
                self.collect_step(self.train_env, self.agent.collect_policy, self.replay_buffer)

            # Sample a batch of data from the buffer and update the agent's network.
            experience, unused_info = next(iterator)
            train_loss = self.agent.train(experience).loss

            step = self.agent.train_step_counter.numpy()

            if step % self.log_interval == 0:
                print('step = {0}: loss = {1}'.format(step, train_loss))

            if step % self.eval_interval == 0:
                avg_return = self.compute_avg_return(self.eval_env, self.agent.policy, self.num_eval_episodes)
                print('step = {0}: Average Return = {1}'.format(step, avg_return))
                returns.append(avg_return)

        iterations = range(0, self.num_iterations + 1, self.eval_interval)
        plt.plot(iterations, returns)
        plt.ylabel('Average Return')
        plt.xlabel('Iterations')
        plt.ylim(top=250)

    @staticmethod
    def embed_mp4(filename):
        """Embeds an mp4 file in the notebook."""
        video = open(filename, 'rb').read()
        b64 = base64.b64encode(video)
        tag = '''
        <video width="640" height="480" controls>
          <source src="data:video/mp4;base64,{0}" type="video/mp4">
        Your browser does not support the video tag.
        </video>'''.format(b64.decode())

        return IPython.display.HTML(tag)

    def create_policy_eval_video(self, policy, filename, num_episodes=5, fps=30):
        filename = filename + ".mp4"
        with imageio.get_writer(filename, fps=fps) as video:
            for _ in range(num_episodes):
                time_step = self.eval_env.reset()
                video.append_data(self.eval_py_env.render())
                while not time_step.is_last():
                    action_step = policy.action(time_step)
                    time_step = self.eval_env.step(action_step.action)
                    video.append_data(self.eval_py_env.render())
        return self.embed_mp4(filename)
