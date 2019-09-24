from enum import Enum
from typing import List, Tuple

from gym_tak.read_only import read_only_enum
from gym_tak.tak.piece import Types


@read_only_enum('size', 'capstones', 'stones', 'pieces', 'carry_limit', 'actions')
class Presets(Enum):
    FOUR = 4, 0, 15
    FIVE = 5, 1, 21
    SIX = 6, 1, 30
    EIGHT = 8, 2, 50

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, size: int, capstones: int, stones: int) -> None:
        self.size = size
        self.capstones = capstones
        self.stones = stones
        self.pieces = capstones + stones
        self.max_pieces = stones * 2 + 1
        self.carry_limit = size

        actions = []
        for column in range(0, self.size):
            for row in range(0, self.size):
                for type_ in Types:
                    actions.append((2, column, row, type_))
                for adjacent in self.get_adjacent_coordinates(column, row):
                    for pieces in range(1, self.carry_limit + 1):
                        actions.append((1, (column, row), adjacent, pieces))

        self.actions = actions

    @classmethod
    def get_default(cls) -> 'Presets':
        return cls.FIVE

    def get_adjacent_coordinates(self, column: int, row: int) -> List[Tuple[int, int]]:
        adjacent = []

        for offset in [-1, 1]:
            new_column = column + offset
            if 0 <= new_column < self.size:
                adjacent.append((new_column, row))

            new_row = row + offset
            if 0 <= new_row < self.size:
                adjacent.append((column, new_row))

        return adjacent
