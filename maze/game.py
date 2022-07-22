import numpy as np

from .mazemap import Map
from .point import Point
from .random import Random
from .player import Player
from .mapvalue import MapValue
from .movestatus import MoveStatus
from .exceptions import *

from typing import Optional


class Game:
    def __init__(self, row: int, column: int, *, random: Random = None):
        self.map = Map(row, column, random=random)
        self.player = Player(self.map.st)
        self.move_list = np.empty(row * column, dtype=Point)
        self.move_step = 0
        self.is_move = False
        
    @property
    def row(self):
        return self.map.row
    
    @property
    def column(self):
        return self.map.column
    
    @property
    def random(self):
        return self.map.random

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
        if self.is_win:
            return False
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

        self.player.pos = self.move_list[step]

        self.is_move = True
        self.player.step += step
        self.player.move_times += 1
        return True
    
    def move_player(self, pos: Point):
        if self.map.is_overrange(pos):
            raise MapIndexError(pos)
        if self.map[pos] not in (MapValue.road, MapValue.st, MapValue.ed):
            return False
        self.player.pos = pos
        self.move_step = 0
        return True
    
    def solve(self, pos: Point = None):
        if pos is None:
            pos = self.player.pos
        solve_list = self.map.solve(pos)
        return solve_list

    def __bool__(self):
        return True

    @property
    def is_win(self):
        return self.map.ed == self.player.pos
