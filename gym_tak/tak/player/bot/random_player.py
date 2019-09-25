import random

from gym_tak.tak.player import Player


class RandomPlayer:

    @staticmethod
    def do_action(player: Player) -> None:
        action = random.choice(player.get_valid_actions())
        player.do_action(action)
