import random

from gym_tak.tak.player import Player


class RandomPlayer:

    @staticmethod
    def do_action(player: Player) -> bool:
        actions = player.get_valid_actions()
        if len(actions) == 0:
            player.surrender()
            return False

        action = random.choice(actions)
        return player.do_action(action)
