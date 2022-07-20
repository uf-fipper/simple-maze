import enum

from .point import Point

from typing import Callable, TypeVar, Optional

_T_func = TypeVar('_T_func', bound=Callable[["MoveStatus", Point], Point])


class MoveStatus(enum.Enum):
    up = 0
    down = 1
    left = 2
    right = 3

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._next_func: Optional[_T_func] = None

    def get_next(self, p: Point) -> Point:
        if not self._next_func:
            raise NotImplementedError
        return self._next_func(p)

    def set_next(self, func: _T_func) -> _T_func:
        self._next_func = func
        return func


@MoveStatus.up.set_next
def _(self: MoveStatus, p: Point):
    return Point(p[0] - 1, p[1])


@MoveStatus.down.set_next
def _(self: MoveStatus, p: Point):
    return Point(p[0] + 1, p[1])


@MoveStatus.left.set_next
def _(self: MoveStatus, p: Point):
    return Point(p[0], p[1] - 1)


@MoveStatus.right.set_next
def _(self: MoveStatus, p: Point):
    return Point(p[0], p[1] + 1)
