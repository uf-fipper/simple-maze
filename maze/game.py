import numpy as np

from .mazemap import Map
from .point import Point
from .random import Random
from .player import Player
from .mapvalue import MapValue
from .movestatus import MoveStatus

from typing import Optional


class Game:
    def __init__(self, row: int, column: int, *, random: Random = None):
        self.map = Map(row, column, random=random)
        self.source_map = Map(row, column, random=self.map.random)
        self.source_map.map = self.map.map.copy()
        self.player = Player(self.map.st)
        self.move_list = np.empty(row * column, dtype=Point)
        self.move_step = 0
        self.is_move = False

    def _move_find_road(self, p: Point, lp: Point) -> Optional[Point]:
        """
        该点附近存在岔路或者无路可走，返回 None
        :param p:
        :param lp:
        :return:
        """
        res = None
        for _p in p.get_range():
            if self.map.is_overrange(_p):
                continue
            if _p == lp:
                continue
            if self.map[_p] in (MapValue.wall,):
                continue
            if res is not None:
                return None
            res = _p

        return res

    def move(self, move: MoveStatus):
        lp = self.player.pos
        p = move.get_next(lp)

        if self.map[p] == MapValue.wall:
            return False

        self.move_list[0] = lp
        self.move_list[1] = p
        step = 1
        next_road = self._move_find_road(p, lp)
        while next_road is not None and p != self.map.ed:
            step += 1
            lp = p
            p = next_road
            self.move_list[step] = p
            next_road = self._move_find_road(p, lp)

        self.move_step = step
        self.map[self.player.pos] = self.source_map[self.player.pos]
        self.player.pos = self.move_list[step]
        # move_list
        for p in self.move_list[:step]:
            self.map[p] = MapValue.move
        self.map[self.player.pos] = self.player
        self.is_move = True
        self.player.step += step
        self.player.move_times += 1
        return True

    def __bool__(self):
        return True

    def is_win(self):
        return self.map.ed == self.player.pos
