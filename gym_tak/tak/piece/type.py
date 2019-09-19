from enum import Enum

from gym_tak.read_only import read_only_enum


@read_only_enum('blocks', 'ignores_block', 'forms_road', 'value', 'string')
class Types(Enum):
    CAPSTONE = True, True, True, 1, 'C'
    FLAT_STONE = False, False, True, 2, 'F'
    STANDING_STONE = True, False, False, 3, 'S'

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, blocks: bool, ignores_block: bool, forms_road: bool, value: int, string: str) -> None:
        self.blocks = blocks
        self.ignores_block = ignores_block
        self.forms_road = forms_road
        self.int_value = value
        self.string = string

    @classmethod
    def from_int(cls, value: int) -> 'Types':
        value = abs(value)

        for type_ in cls:
            if type_.value == value:
                return type_

    def can_move(self, to_top_piece_type: 'Types') -> bool:
        if self is self.CAPSTONE:
            return to_top_piece_type is not self.CAPSTONE
        return self.ignores_block or not to_top_piece_type.blocks

