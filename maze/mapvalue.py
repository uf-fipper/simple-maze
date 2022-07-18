import enum

from typing import Callable, TypeVar, Any, Optional

_T_result = TypeVar('_T_result')
_T_func = TypeVar('_T_func', bound=Callable[..., _T_result])


class MapValue(enum.Enum):
    empty = '?'
    wall = 'O'
    road = ' '
    border = 'X'
    st = 'P'
    ed = 'E'

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._play_func: Optional[_T_func] = None

    def add_action(self, func: _T_func) -> _T_func:
        self._play_func = func
        return func

    def action(self, *args, **kwargs) -> Optional[_T_result]:
        res = None
        if self._play_func:
            res = self._play_func(self, *args, **kwargs)
        else:
            print(self.value, end='')
        return res


if __name__ == '__main__':
    a = MapValue.road

    @a.add_action
    def _(self: MapValue):
        print(self.value * 3)

    a.action()
