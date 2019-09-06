from enum import Enum

from gym_tak.read_only import read_only_enum


@read_only_enum('value', 'string')
class Colors(Enum):
    BLACK = 1, 'B'
    WHITE = -1, 'W'

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, value, string) -> None:
        self.value = value
        self.string = string
