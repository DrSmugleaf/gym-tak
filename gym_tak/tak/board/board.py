import numpy as np
from numpy.core.multiarray import ndarray

from gym_tak.tak.board import Presets
from gym_tak.tak.piece import Types, Piece


class Board:

    def __init__(self, preset: Presets) -> None:
        self.preset = preset
        self.rows = np.zeros((preset.size, preset.size, preset.max_pieces), np.int8)

    @staticmethod
    def is_adjacent(column1: int, row1: int, column2: int, row2: int) -> bool:
        return abs(column1 - column2) <= 1 and abs(row1 - row2) <= 1

    def get_square(self, column: int, row: int) -> ndarray:
        return self.rows[row, column]

    def get_stack(self, column: int, row: int) -> ndarray:
        square = self.get_square(column, row)
        return square[square.nonzero()]

    def get_top_value(self, column: int, row: int) -> int:
        stack = self.get_stack(column, row)
        return stack[-1]

    def can_move(self, column_from: int, row_from: int, column_to: int, row_to: int, pieces: int) -> bool:
        adjacent = self.is_adjacent(column_from, row_from, column_to, row_to)
        under_limit = pieces <= self.preset.carry_limit
        origin = self.get_square(column_from, row_from)
        under_stack_size = pieces <= np.count_nonzero(origin)
        if not adjacent or not under_limit or pieces < 0 or not under_stack_size:
            return False

        destination_empty = self.get_square(column_to, row_to)[0] == 0
        if destination_empty:
            return True

        destination_top_value = self.get_top_value(column_to, row_to)
        destination_top_type = Types.from_int(destination_top_value)
        destination_top_blocks = destination_top_type.blocks
        origin_top_value = self.get_top_value(column_from, row_from)
        origin_top_type = Types.from_int(origin_top_value)
        if pieces == 1:
            return origin_top_type.can_move(destination_top_type)
        else:
            return not destination_top_blocks

    def move(self, column_from: int, row_from: int, column_to: int, row_to: int, pieces: int):
        origin_square = self.get_square(column_from, row_from)
        origin_top_index = origin_square.nonzero()[-1]
        destination_square = self.get_square(column_to, row_to)
        destination_top_index = destination_square.nonzero()[-1]

        while pieces > 0:
            piece = origin_square[origin_top_index]
            piece.move(destination_square, pieces)
            origin_square[origin_top_index] = 0
            origin_top_index -= 1
            destination_square[destination_top_index] = piece
            destination_top_index -= 1
            pieces -= 1

    def can_place(self, column: int, row: int) -> bool:
        return self.get_square(column, row)[0] == 0

    def place(self, piece: Piece, column: int, row: int) -> None:
        self.get_square(column, row)[0] = piece.to_int()

    def reset(self):
        self.rows = np.zeros((self.preset.size, self.preset.size, self.preset.max_pieces), np.int8)
