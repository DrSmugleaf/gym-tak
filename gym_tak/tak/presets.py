from enum import Enum

from gym_tak.frozen_enum import freeze
from gym_tak.read_only_properties import read_only_properties


@freeze
@read_only_properties('size', 'capstones', 'stones')
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

    def __init__(self, size, capstones, stones) -> None:
        self.size = size
        self.capstones = capstones
        self.stones = stones
