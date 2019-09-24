import numpy as np

from gym_tak.tak.piece import Types, Colors


class Piece:

    def __init__(self, color: Colors, type_: Types) -> None:
        self.color = color
        self.type = type_

    @classmethod
    def from_int(cls, value: int) -> 'Piece':
        color = Colors.from_int(value)
        type_ = Types.from_int(value)
        return cls(color, type_)

    def flatten(self) -> None:
        if self.type is not Types.STANDING_STONE:
            raise TypeError("Can't flatten anything other than a standing stone. Type: %s" % self.type)
        self.type = Types.FLAT_STONE

    def to_int(self) -> int:
        return self.color.int_value * self.type.int_value

    def to_string(self) -> str:
        return self.color.string + self.type.string

    def move(self, to: np.ndarray, pieces: int):
        if pieces == 1 and self is Types.CAPSTONE and len(to) > 0:
            to_top_index = to.nonzero()[-1]
            to_top_value = to[to_top_index]
            to_top_piece = Piece.from_int(to_top_value)
            if to_top_piece is Types.STANDING_STONE:
                to_top_piece.type = Types.FLAT_STONE
                to[to_top_index] = to_top_piece.to_int()
