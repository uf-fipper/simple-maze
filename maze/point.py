from collections import namedtuple
from typing import Generic, TypeVar

_T_p = TypeVar('_T_p', bound=int)


class Point(namedtuple('Point', 'x y'), Generic[_T_p]):
    def __new__(cls, x: _T_p, y: _T_p):
        return super().__new__(cls, x, y)

    def get_range(self):
        return [
            Point(self[0] - 1, self[1]),
            Point(self[0] + 1, self[1]),
            Point(self[0], self[1] - 1),
            Point(self[0], self[1] + 1),
        ]

    def __add__(self, other) -> "Point":
        if isinstance(other, (Point, tuple)):
            return Point(self[0] + other[0], self[1] + other[1])
        return NotImplemented
