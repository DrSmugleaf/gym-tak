import numpy as np

from gym_tak.tak.board import Presets
from gym_tak.tak.piece import Types


class Board:

    def __init__(self, preset: Presets) -> None:
        self.preset = preset
        self.rows = np.zeros((preset.size, preset.size, preset.stones * 2 + 1), np.int8)

    def can_place(self, column: int, row: int) -> bool:
        return self.rows[row, column, 0] == 0

    def can_move(self, column_from: int, row_from: int, column_to: int, row_to: int, pieces: int) -> bool:
        adjacent = self.is_adjacent(column_from, row_from, column_to, row_to)
        under_limit = pieces <= self.preset.carry_limit
        origin = self.rows[row_from, column_from]
        under_stack_size = pieces <= np.count_nonzero(origin)
        if not adjacent or not under_limit or pieces < 0 or not under_stack_size:
            return False

        destination = self.rows[row_to, column_to]
        destination_empty = destination[0] == 0
        if destination_empty:
            return True

        destination_top_value = destination[np.nonzero(destination)][-1]
        destination_top_type = Types.from_int(destination_top_value)
        destination_top_blocks = destination_top_type.blocks
        origin_top_value = origin[np.nonzero(origin)][-1]
        origin_top_type = Types.from_int(origin_top_value)
        if pieces == 1:
            return origin_top_type.can_move(destination_top_type)
        else:
            return not destination_top_blocks

    @staticmethod
    def is_adjacent(column1: int, row1: int, column2: int, row2: int) -> bool:
        return abs(column1 - column2) <= 1 and abs(row1 - row2) <= 1
