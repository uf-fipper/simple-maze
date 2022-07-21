from typing import Callable, TypeVar, Optional, Generic, Hashable

_T = TypeVar('_T', bound=Hashable)
_T_result = TypeVar('_T_result')
_T_func = Callable[[_T], _T_result]


class OnShowContainer(Generic[_T_result]):
    def __init__(self, obj_funcs: dict[_T, _T_func] = None):
        self.obj_funcs: dict[_T, _T_func] = obj_funcs or {}

    def __call__(self, source_obj: _T):
        def add(func: _T_func):
            self.obj_funcs[source_obj] = func

        return add

    def __getitem__(self, source_obj: _T) -> _T_result:
        return self.get_object(source_obj)

    def get_object(self, source_obj: _T) -> _T_result:
        if source_obj not in self.obj_funcs:
            raise TypeError('please set a function first')
        return self.obj_funcs[source_obj](source_obj)
