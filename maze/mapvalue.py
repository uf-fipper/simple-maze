import enum

from typing import Callable, TypeVar, Any, Optional
from colorama import Fore, Back, Style

_T_result = TypeVar('_T_result')
_T_func = Callable[["MapValue"], _T_result]


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

    def set_object(self, func: _T_func) -> _T_func:
        self._play_func = func
        return func

    def get_object(self) -> Optional[_T_result]:
        if self._play_func:
            return self._play_func(self)
        else:
            return self.value


if __name__ == '__main__':
    @MapValue.road.set_object
    def _(self: MapValue) -> str:
        return f' '

    @MapValue.wall.set_object
    def _(self: MapValue) -> str:
        return f'{Back.YELLOW} {Style.RESET_ALL}'
