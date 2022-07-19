import numpy as np

from .mazemap import Map
from .point import Point
from .random import Random
from .player import Player

from typing import Union


class Game:
    def __init__(self, row: int, column: int, *, random: Random = None):
        self.map = Map(row, column, random=random)
        self.player = Player(self.map.st)
        self.move_list = np.empty((row, column), dtype=Point)
        self.move_step = 0

    @property
    def is_move(self):
        return bool(self.move_step)
