from typing import List, Tuple

import numpy as np

from gym_tak.tak.piece import Colors
from gym_tak.tak.player import Hand


class Player:

    def __init__(self, name: str, game, color: Colors) -> None:
        self.name = name
        self.game = game
        self.hand = Hand(game.preset.capstones, game.preset.stones, color)

    def surrender(self) -> None:
        self.game.surrender(self)

    def get_valid_actions(self, board: np.ndarray) -> List[Tuple]:
        actions = []

        for i, action in enumerate(self.game.preset.actions):
            if (action[0] is 2 and self.game.can_place(self, action[1], action[2], action[3], board)) or \
                    (action[0] is 1 and self.game.can_move(self, action[1][0], action[1][1],
                                                           action[2][0], action[2][1], action[3])):
                actions.append(action)

        return actions
