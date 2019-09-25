from gym_tak.tak.board import Presets, Board
from gym_tak.tak.piece import Colors, Types
from gym_tak.tak.player import Player


class TakGame:

    def __init__(self, preset: Presets, player1: str, player2: str) -> None:
        super().__init__()
        self.preset = preset
        self.board = Board(preset)
        self.player1 = Player(player1, self, Colors.BLACK)
        self.player2 = Player(player2, self, Colors.WHITE)
        self.winner = None
        self.next_player = self.player1
        self.active = True

    def can_move(self, player: Player, column_from: int, row_from: int, column_to: int, row_to: int, pieces: int) -> bool:
        return self.active and player is self.next_player and self.board.can_move(column_from, row_from, column_to, row_to, pieces)

    def move(self, player: Player, column_from: int, row_from: int, column_to: int, row_to: int, pieces: int) -> None:
        print(player.name + " moving from column " + str(column_from) + " row " + str(row_from) + " to column " + str(column_to) + " row " + str(row_to))
        assert self.can_move(player, column_from, row_from, column_to, row_to, pieces)
        self.board.move(column_from, row_from, column_to, row_to, pieces)
        self.next_player = self.get_other_player(self.next_player)

    def can_place(self, player: Player, column: int, row: int, type_: Types) -> bool:
        return self.active and player is self.next_player and player.hand.has(type_) and self.board.rows[row, column, 0] == 0

    def place(self, player: Player, column: int, row: int, type_: Types) -> None:
        print(player.name + " placing in column " + str(column) + " row " + str(row))
        assert self.can_place(player, column, row, type_)
        piece = player.hand.take_piece(type_)
        self.board.place(piece, column, row)
        self.next_player = self.player2

    def get_player(self, color: Colors) -> Player:
        if color is Colors.BLACK:
            return self.player1
        elif color is Colors.WHITE:
            return self.player2
        else:
            raise ValueError('Unrecognized color %s' % color)

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

    def reset(self) -> None:
        self.board.reset()
        self.player1.reset()
        self.player2.reset()
        self.winner = None
        self.next_player = self.player1
        self.active = True
