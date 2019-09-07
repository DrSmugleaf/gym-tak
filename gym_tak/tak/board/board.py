import numpy as np

from gym_tak.tak.board import Presets


class Board:

    def __init__(self, preset: Presets) -> None:
        self.preset = preset
        self.rows = np.zeros((preset.size, preset.size), np.int8)
