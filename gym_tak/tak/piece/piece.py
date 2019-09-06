from typing import Any

from gym_tak.tak.piece import Types, Colors


class Piece:

    def __init__(self, color: Colors, type_: Types) -> None:
        self.color = color
        self.type = type_

    def flatten(self) -> None:
        if self.type is not Types.STANDING_STONE:
            raise TypeError("Can't flatten anything other than a standing stone")

        self.type = Types.FLAT_STONE
