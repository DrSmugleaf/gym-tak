from gym_tak.tak.board import Presets
from gym_tak.tak.board import Board
from gym_tak.tak.piece import Colors, Types
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

    def can_move(self, player: Player, column_from: int, row_from: int, column_to: int, row_to: int, pieces: int) -> bool:
        return self.active and player is self.next_player and self.board.can_move(column_from, row_from, column_to, row_to, pieces)

    def move(self, player: Player, column_from: int, row_from: int, column_to: int, row_to: int, pieces: int) -> None:
        assert self.can_move(player, column_from, row_from, column_to, row_to, pieces)
        self.board.move(column_from, row_from, column_to, row_to, pieces)

    def can_place(self, player: Player, column: int, row: int) -> bool:
        return self.active and player is self.next_player and self.board.can_place(column, row)

    def place(self, player: Player, type_: Types, column: int, row: int) -> None:
        assert self.can_place(player, column, row)
        piece = player.hand.take_piece(type_)
        self.board.place(piece, column, row)

    def get_other_player(self, player: Player) -> Player:
        if player is self.player1:
            return self.player2
        elif player is self.player2:
            return self.player1
        else:
            raise ValueError('Player %s is not in this game' % player.name)

    def surrender(self, player: Player) -> None:
        self.active = False
        self.winner = self.get_other_player(player)
