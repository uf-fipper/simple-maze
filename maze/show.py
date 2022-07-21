import numpy as np
from colorama import Fore, Back

from .game import Game
from .mazemap import Map
from .point import Point
from .onshowcontainer import OnShowContainer
from .mapvalue import MapValue

from typing import TypeVar, Generic, Any

_T_result = TypeVar('_T_result')


class GameShow(Generic[_T_result]):
    def __init__(self, game: Game, container: OnShowContainer, *, dtype=object):
        self.game = game
        self.container = container
        self._result = np.empty(((self.row + 2), (self.column + 2)), dtype=dtype)

    @property
    def map(self):
        return self.game.map

    @property
    def row(self):
        return self.map.row

    @property
    def column(self):
        return self.map.column

    def __getitem__(self, p: Point) -> Any:
        if p[0] < 0 or p[0] >= self.row:
            raise IndexError
        if p[1] < 0 or p[1] >= self.column:
            raise IndexError
        return self._result[p + (1, 1)]

    def __setitem__(self, p: Point, value: Any):
        if p[0] < 0 or p[0] >= self.row:
            raise IndexError
        if p[1] < 0 or p[1] >= self.column:
            raise IndexError
        self._result[p + (1, 1)] = value

    def init_result(self):
        for i in range(self.column + 2):
            self._result[0, i] = self.container[MapValue.border]

        for i in range(self.row):
            self._result[Point(i + 1, 0)] = self.container[MapValue.border]
            for j in range(self.column):
                self[Point(i, j)] = self.container[self.map[Point(i, j)]]
            self._result[i + 1, self.column + 1] = self.container[MapValue.border]

        for i in range(self.column + 2):
            self._result[self.row + 1, i] = self.container[MapValue.border]

    def get_result(self):
        self.init_result()
        return self._result

    def format(self) -> _T_result:
        raise NotImplementedError


class StrGameShow(GameShow[str]):
    def __init__(self, game: Game, container: OnShowContainer[str] = None):
        container = container or OnShowContainer(obj_funcs={
            MapValue.border: lambda x: f'{Back.RED} {Back.RESET}',
            MapValue.wall: lambda x: f'{Back.YELLOW} {Back.RESET}',
            MapValue.road: lambda x: ' ',
            MapValue.move: lambda x: '.',
            MapValue.st: lambda x: f'{Fore.GREEN}S{Fore.RESET}',
            MapValue.ed: lambda x: f'{Fore.BLUE}E{Fore.RESET}',
            game.player: lambda x: f'{Fore.GREEN}P{Fore.RESET}',
        })
        super().__init__(game, container, dtype=object)

    def format(self) -> str:
        return '\n'.join((''.join(row) for row in self.get_result()))
