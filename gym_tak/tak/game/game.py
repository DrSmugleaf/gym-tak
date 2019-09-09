from gym_tak.tak.board import Presets
from gym_tak.tak.board import Board
from gym_tak.tak.piece import Colors
from gym_tak.tak.player import Player


class Game:

    def __init__(self, preset: Presets, player1: str, player2: str) -> None:
        self.preset = preset
        self.board = Board(preset)
        self.player1 = Player(player1, self, Colors.BLACK)
        self.player2 = Player(player2, self, Colors.WHITE)
        self.winner = None
        self.next_player = player1
        self.active = True

    def can_place(self, player: Player, column: int, row: int) -> bool:
        return self.active and player is self.next_player and self.board.can_place(column, row)

    def can_move(self, player: Player, column_from: int, row_from: int, column_to: int, row_to: int, pieces: int) -> bool:
        return self.active and player is self.next_player and self.board.can_move(column_from, row_from, column_to, row_to, pieces)
