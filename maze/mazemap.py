import numpy as np

from .random import Random
from .mapvalue import MapValue
from .exceptions import SolveException
from .point import Point

from queue import Queue
from collections import namedtuple
from typing import List, Tuple, TypeVar
try:
    from numpy.typing import NDArray
except ImportError:
    raise ImportError('请保证numpy版本大于1.21')


class Map:
    _random: Random
    """随机数种子"""
    map: NDArray[MapValue]
    """地图"""
    inst_st: Point
    """初始化地图用的点"""
    st: Point
    """玩家初始位置"""
    ed: Point
    """终点位置"""

    def is_overrange(self, p: Point) -> bool:
        i, j = p
        if i < 0 or j < 0:
            return True
        if i >= self.row or j >= self.column:
            return True
        return False

    def _init_get_walls(self, p: Point, lp: Point):
        """
        获取一个点周围所有的墙
        :param p: 这个点
        :param lp: 上一个点
        """
        res_temp: List[Point] = [
            Point(p[0] + 1, p[1]),
            Point(p[0] - 1, p[1]),
            Point(p[0], p[1] + 1),
            Point(p[0], p[1] - 1),
        ]
        res: List[Point] = []
        for point in res_temp:
            if self.is_overrange(point):
                continue
            if point == lp:
                continue
            res.append(point)
        return res

    def _init_check_wall(self, p: Point, lp: Point) -> bool:
        """
        检查这个墙是否能生成道路
        :param p: 这个点
        :param lp: 上一个点
        :return:
        """
        temp = self._init_get_walls(p, lp)
        if not temp:
            return False
        for t in temp:
            if self.map[t] != MapValue.wall:
                return False
        return True

    def _init_map(self):
        """
        初始化地图

        inst_st: Point
        "初始化地图用的点"
        st: Point
        "玩家初始位置"
        ed: Point
        "终点位置"
        """
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
            if not self._init_check_wall(p, lp):
                continue
            self.map[p] = MapValue.road
            around_walls = self._init_get_walls(p, lp)
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
                    self.st = Point(i, j)
                    st_get = True
                ed_idx = Point(self.row - 1 - i, self.column - 1 - j)
                if not ed_get and self.map[ed_idx] == MapValue.road:
                    self.ed = ed_idx
                    ed_get = True

    def __init__(self, row: int, column: int, *, random: Random = None):
        """
        实例化地图对象
        :param row: 地图宽
        :param column: 地图长
        :param random: 随机数种子
        """
        self._random = random or Random()
        self.map = np.zeros((row, column), dtype=MapValue)
        self._init_map()

    def _solve_get_roads(self, map_temp: NDArray[Point], p: Point):
        """
        获取一个点周围所有没被遍历过的路
        :param map_temp:
        :param p:
        :return:
        """
        res_temp: List[Point] = [
            Point(p[0] + 1, p[1]),
            Point(p[0] - 1, p[1]),
            Point(p[0], p[1] + 1),
            Point(p[0], p[1] - 1),
        ]
        res: List[Point] = []

        for _p in res_temp:
            if self.is_overrange(_p):
                continue
            idx = map_temp[_p]
            if idx != Point(-1, -1):
                continue
            if self.map[_p] != MapValue.road:
                continue
            res.append(_p)

        return res

    def solve(self, pos: Point = None) -> NDArray[Point]:
        """
        求解迷宫
        :param pos: 从某个点开始求解，不指定则从起始点求解
        :return:
        """
        pos = pos or self.st
        if self.row <= 1 or self.column <= 1:
            return np.array([])
        queue: Queue[Tuple[Point, Point, int]] = Queue(maxsize=self.row * self.column)
        map_temp = np.empty((self.row, self.column), dtype=Point)
        """
        map_temp 用于记录遍历到某个点时的上一个点是什么
        如果没有遍历过，则是 Point(-1, -1)
        
        例如：
        map_temp[1, 2] = Point(0, 2)
        则 (1, 2) 的前一个点是 (0, 2)
        """
        for i in range(self.row):
            for j in range(self.column):
                map_temp[i, j] = Point(-1, -1)

        p = pos
        lp = Point(-2, -2)
        step = 0
        queue.put((p, lp, step))
        while p != self.ed:
            p, lp, step = queue.get()
            map_temp[p] = lp
            roads = self._solve_get_roads(map_temp, p)
            for road in roads:
                queue.put((road, p, step + 1))

        rp = map_temp[self.ed]
        res = np.empty(step + 1, dtype=Point)
        res[step] = self.ed
        for i in range(step - 1, -1, -1):
            res[i] = rp
            rp = map_temp[rp]
        if res[0] != pos:
            raise SolveException('居然不是从pos开始？？？')

        return res

    @property
    def row(self):
        return self.map.shape[0]

    @property
    def column(self):
        return self.map.shape[1]

    def __repr__(self):
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
