import logging

import gym
import numpy as np

from gym_tak.tak.board import Presets
from gym_tak.tak.game import TakGame

logger = logging.getLogger(__name__)


class GymEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game = TakGame(Presets.get_default(), 'Agent', 'Opponent')
        self.player = self.game.player1
        self.action_space = gym.spaces.Discrete(len(self.game.preset.actions))
        high = np.array([3] * len(self.game.board.rows.flatten()))
        self.observation_space = gym.spaces.Box(-high, high, dtype=np.int8)

    def __del__(self):
        self.player.surrender()

    def step(self, action):
        response = self._step(action)
        if not self.game.active:
            self.reset()

        return response

    def _step(self, action):
        action = self.game.preset.actions[action]
        if action[0] == 2:
            _, column, row, type_ = action
            if not self.game.can_place(self.player, column, row, type_):
                self.player.surrender()
                return self.get_response()

            self.game.place(self.player, column, row, type_)
        elif action[0] == 1:
            _, from_, to, pieces = action
            column_from, row_from = from_
            column_to, row_to = to
            if not self.game.can_move(self.player, column_from, row_from, column_to, row_to, pieces):
                self.player.surrender()
                return self.get_response()

            self.game.move(self.player, action[1][0], action[1][1], action[2][0], action[2][1], action[3])
        else:
            raise ValueError('Unrecognized action type ' + str(action))

        return self.get_response()

    def reset(self):
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
