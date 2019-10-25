from typing import List, Tuple

from gym_tak.tak.piece import Colors
from gym_tak.tak.player import Hand


class Player:

    def __init__(self, name: str, game, color: Colors) -> None:
        self.name = name
        self.game = game
        self.hand = Hand(game.preset.capstones, game.preset.stones, color)

    def surrender(self) -> None:
        self.game.surrender(self)

    def get_valid_actions(self) -> List[Tuple]:
        actions = []

        for i, action in enumerate(self.game.preset.actions):
            if (action[0] is 2 and self.game.can_place(self, action[1], action[2], action[3])) or \
                    (action[0] is 1 and self.game.can_move(self, action[1][0], action[1][1], action[2][0],
                                                           action[2][1], action[3])):
                actions.append(action)

        return actions

    def reset(self) -> None:
        self.hand.reset()

    def do_action(self, action: Tuple) -> bool:
        if action[0] == 2:
            _, column, row, type_ = action
            if not self.game.can_place(self, column, row, type_):
                return False

            self.game.place(self, column, row, type_)
        elif action[0] == 1:
            _, from_, to, pieces = action
            column_from, row_from = from_
            column_to, row_to = to
            if not self.game.can_move(self, column_from, row_from, column_to, row_to, pieces):
                return False

            self.game.move(self, action[1][0], action[1][1], action[2][0], action[2][1], action[3])
        else:
            raise ValueError('Unrecognized action type ' + str(action))

        return True
