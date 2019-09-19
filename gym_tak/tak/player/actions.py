from enum import Enum

from gym_tak.read_only import read_only_enum


@read_only_enum()
class Actions(Enum):
    MOVE = 1
    PLACE = 2

    def __new__(cls, value):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, value: int) -> None:
        self.int_value = value

    @classmethod
    def from_int(cls, value: int) -> 'Actions':
        for action in Actions:
            if action.value == value:
                return action
