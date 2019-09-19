import numpy as np
from alpha_zero_general import Game

from gym_tak.tak.board import Presets
from gym_tak.tak.board import Board
from gym_tak.tak.piece import Colors, Types
from gym_tak.tak.player import Player
from gym_tak.tak.player.actions import Actions


class TakGame(Game):

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
        assert self.can_move(player, column_from, row_from, column_to, row_to, pieces)
        self.board.move(column_from, row_from, column_to, row_to, pieces)

    def can_place(self, player: Player, column: int, row: int) -> bool:
        return self.active and player is self.next_player and self.board.can_place(column, row)

    def place(self, player: Player, type_: Types, column: int, row: int) -> None:
        assert self.can_place(player, column, row)
        piece = player.hand.take_piece(type_)
        self.board.place(piece, column, row)

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

    def getInitBoard(self) -> np.ndarray:
        return self.board.rows.flatten()

    def getBoardSize(self) -> int:
        return self.preset.size

    def getActionSize(self) -> int:
        return len(self.preset.actions)

    def getNextState(self, board, player: int, action):
        color = Colors.from_piece_value(player)
        player = self.get_player(color)

        if action[0] is Actions.PLACE.int_value and self.can_place(player, action[1], action[2]):
            self.place(player, action[3], action[1], action[2])
        elif action[0] is Actions.MOVE.int_value and self.can_move(player, action[1][0], action[1][1], action[2][0],
                                                                   action[2][1], action[3]):
            self.move(player, action[1][0], action[1][1], action[2][0], action[2][1], action[3])
        else:
            raise ValueError('Unrecognized or invalid action %s' % action[0])

    def getValidMoves(self, board, player: int) -> np.ndarray:
        color = Colors.from_piece_value(player)
        player = self.get_player(color)
        valid = [0] * len(self.preset.actions)

        for i, action in enumerate(self.preset.actions):
            if action[0] is Actions.PLACE.int_value and self.can_place(player, action[1], action[2]):
                valid[i] = 1
            elif action[0] is Actions.MOVE.int_value and self.can_move(player, action[1][0], action[1][1], action[2][0],
                                                                       action[2][1], action[3]):
                valid[i] = 1
            else:
                raise ValueError('Unrecognized action %s' % action[0])

        return np.array(valid)

    def getGameEnded(self, board, player: int) -> int:
        color = Colors.from_piece_value(player)
        player = self.get_player(color)

        if self.active:
            return 0
        elif self.winner is player:
            return 1
        else:
            return -1

    def getCanonicalForm(self, board, player: int) -> np.ndarray:
        return board * player

    def getSymmetries(self, board, pi) -> []:
        size = self.preset.size
        assert len(pi) is size ** 2 + 1
        pi_board = np.reshape(pi[:-1], (size, size))
        ret = []

        for i in range(1, 5):
            for j in [True, False]:
                new_b = np.rot90(board, i)
                new_pi = np.rot90(pi_board, i)
                if j:
                    new_b = np.fliplr(new_b)
                    new_pi = np.fliplr(new_pi)
                ret += [(new_b, list(new_pi.ravel()) + [pi[-1]])]

        return ret

    def stringRepresentation(self, board):
        board.tostring()
