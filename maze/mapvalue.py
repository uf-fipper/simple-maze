import enum

from .onshowobject import OnShowObject, _T_func, _T_result

from typing import Callable, TypeVar, Any, Optional


class MapValue(OnShowObject, enum.Enum):
    def __init__(self, *args):
        super().__init__()

    empty = '?'
    wall = 'O'
    road = ' '
    border = 'X'
    st = 'P'
    ed = 'E'
