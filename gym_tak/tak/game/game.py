from gym_tak.tak import Presets
from gym_tak.tak.piece import Colors
from gym_tak.tak.player import Player


class Game:

    def __init__(self, preset: Presets, player1: str, player2: str) -> None:
        self.preset = preset
        self.player1 = Player(player1, self, Colors.BLACK)
        self.player2 = Player(player2, self, Colors.WHITE)
        self.winner = None
        self.next_player = player1
        self.active = True
