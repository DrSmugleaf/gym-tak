from __future__ import annotations
from enum import Enum

from gym_tak.read_only import read_only_enum
from gym_tak.tak.board import Board
from gym_tak.tak.piece import Types
from gym_tak.tak.player.actions import Actions


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
        self.carry_limit = size

        actions = []
        board = Board(self)
        for column in range(0, self.size):
            for row in range(0, self.size):
                for type_ in Types:
                    actions.append((Actions.PLACE.value, column, row, type_))
                for adjacent in board.get_adjacent_coordinates(column, row):
                    for pieces in range(1, self.carry_limit + 1):
                        actions.append((Actions.MOVE.value, (column, row), adjacent, pieces))

        self.actions = actions

    @classmethod
    def get_default(cls) -> Presets:
        return cls.FIVE
