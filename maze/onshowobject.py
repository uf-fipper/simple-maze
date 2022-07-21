from typing import Callable, TypeVar, Optional, Generic

_T_result = TypeVar('_T_result')
_T_func = Callable[["OnShowObject"], _T_result]


class OnShowObject(Generic[_T_result]):
    def __init__(self):
        self._play_func: Optional[_T_func] = None

    def set_object(self, func: _T_func) -> _T_func:
        self._play_func = func
        return func

    def get_object(self) -> _T_result:
        if self._play_func:
            return self._play_func(self)
        raise NotImplementedError
