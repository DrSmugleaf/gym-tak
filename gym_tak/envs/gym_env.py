import logging

import gym
import numpy as np

from gym_tak.tak.board import Presets
from gym_tak.tak.game import TakGame
from gym_tak.tak.player.bot import RandomPlayer

logger = logging.getLogger(__name__)


class GymEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    reward_range = (-1, 1)

    def __init__(self):
        self.game = TakGame(Presets.get_default(), 'Agent', 'Opponent')
        self.player = self.game.player1
        self.action_space = gym.spaces.Discrete(len(self.game.preset.actions))
        high = np.array([3] * len(self.game.board.rows.flatten()))
        self.observation_space = gym.spaces.Box(-high, high, dtype=np.float32)
        self.tries = 0

    def __del__(self):
        self.player.surrender()

    def step(self, action):
        return self._step(action)

    def _step(self, action):
        if not self.game.active:
            self.reset()

        action = self.game.preset.actions[action]
        valid = self.player.do_action(action)

        if valid:
            self.tries = 0
        else:
            self.tries += 1

            if self.tries > 100:
                print('Too many invalid actions')
                self.player.surrender()

        if self.game.active:
            RandomPlayer.do_action(self.game.player2)

        return self.get_response()

    def reset(self):
        self.tries = 0
        self.game.reset()
        return self.get_state()

    def render(self, mode='human'):
        pass

    def close(self):
        self.player.surrender()

    def get_state(self):
        return self.game.board.rows.flatten()

    def reward(self) -> float:
        if self.game.active:
            return 0
        elif self.game.winner == self.player:
            return 1
        elif self.game.winner == self.game.get_other_player(self.player):
            return -1
        else:
            return 1e-4

    def get_response(self):
        return self.get_state(), self.reward(), not self.game.active, {}
