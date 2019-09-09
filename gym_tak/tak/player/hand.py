from gym_tak.tak.board import Presets
from gym_tak.tak.piece import Colors, Types, Piece


class Hand:

    def __init__(self, preset: Presets, color: Colors) -> None:
        self.preset = preset
        self.color = color
        self.capstones = preset.capstones
        self.stones = preset.stones

    def get_amount(self, type_: Types) -> int:
        if type_ is Types.CAPSTONE:
            return self.capstones
        elif type_ in (Types.FLAT_STONE, Types.STANDING_STONE):
            return self.stones
        else:
            raise TypeError('Unrecognized type %s' % type_.name)

    def has(self, type_: Types) -> bool:
        return self.get_amount(type_) > 0

    def has_any(self) -> bool:
        for type_ in Types:
            if self.has(type_):
                return True
        return False

    def reset(self) -> None:
        self.capstones = self.preset.capstones
        self.stones = self.preset.stones

    def take_piece(self, type_: Types) -> Piece:
        assert self.has(type_)
        if type_ is Types.CAPSTONE:
            self.capstones -= 1
        elif type_ is Types.FLAT_STONE or type_ is Types.STANDING_STONE:
            self.stones -= 1
        else:
            raise TypeError('Unrecognized type %s' % type_.name)

        return Piece(self.color, type_)
