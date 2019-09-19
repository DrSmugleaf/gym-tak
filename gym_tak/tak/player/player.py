from gym_tak.tak.piece import Colors
from gym_tak.tak.player import Hand


class Player:

    def __init__(self, name: str, game, color: Colors) -> None:
        self.name = name
        self.game = game
        self.hand = Hand(game.preset.capstones, game.preset.stones, color)

    def surrender(self) -> None:
        self.game.surrender(self)
