import numpy as np

from .random import Random
from .mapvalue import MapValue

from typing import List, Tuple, TypeVar

Point = Tuple[int, int]


class Map:
    def is_overrange(self, p: Point) -> bool:
        i, j = p
        if i < 0 or j < 0:
            return True
        if i >= self.row or j >= self.column:
            return True
        return False

    def _get_walls(self, p: Point, lp: Point):
        """
        获取一个点周围所有的墙
        :param p:
        :param lp:
        :return:
        """
        res_temp: List[Point] = [
            (p[0] + 1, p[1]),
            (p[0] - 1, p[1]),
            (p[0], p[1] + 1),
            (p[0], p[1] - 1),
        ]
        res: List[Point] = []
        for point in res_temp:
            if self.is_overrange(point):
                continue
            if point == lp:
                continue
            res.append(point)
        return res

    def _check_wall(self, p: Point, lp: Point) -> bool:
        """
        检查这个墙是否能生成道路
        :param p: 这个墙
        :param lp: 上一个墙
        :return:
        """
        temp = self._get_walls(p, lp)
        if not temp:
            return False
        for t in temp:
            if self.map[t] != MapValue.wall:
                return False
        return True

    def _init_map(self):
        for i in range(self.row):
            for j in range(self.column):
                self.map[i, j] = MapValue.wall

        "初始化地图时所用的初始点"
        inst_st = self.inst_st = (self._random.randint(0, self.row - 1), self._random.randint(0, self.column - 1))

        stack: List[Tuple[Point, Point, int]] = []
        p = inst_st
        lp = (-1, -1)
        step = 0
        stack.append((p, lp, step))
        while stack:
            p, lp, step = stack.pop()
            if not self._check_wall(p, lp):
                continue
            self.map[p] = MapValue.road
            around_walls = self._get_walls(p, lp)
            if not around_walls:
                continue
            around_walls = self._random.randarray(around_walls)
            for wall in around_walls:
                stack.append((wall, p, step + 1))

        "是否获取了 st 和 ed"
        st_get = False
        ed_get = False
        for i in range(self.row):
            for j in range(self.column):
                if st_get and ed_get:
                    return
                if not st_get and self.map[i, j] == MapValue.road:
                    self.st = i, j
                    st_get = True
                ed_idx = self.row - 1 - i, self.column - 1 - j
                if not ed_get and self.map[ed_idx] == MapValue.road:
                    self.ed = ed_idx
                    ed_get = True

    def __init__(self, row: int, column: int, *, seed: int = None):
        self._random = Random(seed)
        self.map = np.zeros((row, column), dtype=MapValue)
        self.solve_list = np.zeros(row * column)
        self._init_map()

    @property
    def row(self):
        return self.map.shape[0]

    @property
    def column(self):
        return self.map.shape[1]

    def __str__(self):
        temp_res = np.zeros(((self.row + 2), (self.column + 3)), dtype=str)

        for i in range(self.column + 2):
            temp_res[0, i] = MapValue.border.value
        temp_res[0, self.column + 2] = '\n'

        for i in range(1, self.row + 1):
            temp_res[i, 0] = MapValue.border.value
            for j in range(1, self.column + 1):
                temp_res[i, j] = self.map[i - 1, j - 1].value
            temp_res[i, self.column + 1] = MapValue.border.value
            temp_res[i, self.column + 2] = '\n'

        for i in range(self.column + 2):
            temp_res[self.row + 1, i] = MapValue.border.value

        temp_res[self.row + 1, self.column + 2] = '\0'

        temp_res[self.st[0] + 1, self.st[1] + 1] = MapValue.st.value
        temp_res[self.ed[0] + 1, self.ed[1] + 1] = MapValue.ed.value

        return ''.join([''.join(each) for each in temp_res])

    def __repr__(self):
        return self.__str__()
