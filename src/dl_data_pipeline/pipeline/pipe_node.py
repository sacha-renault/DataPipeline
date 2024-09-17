from __future__ import annotations
from functools import wraps
from collections.abc import Callable
from typing import Any

class PipeNode:
    def __init__(self,
                 func: Callable = None,
                 parent: list[PipeNode] | None = None,
                 name: str | None = None,
                 ) -> None:
        self.__parent: list[PipeNode] = parent if parent is not None else []
        self.__name = name
        self.__func = func
        self.__value = None

    @property
    def value(self) -> Any:
        return self.__value

    @property
    def parent(self) -> list[PipeNode]:
        return self.__parent

    def __repr__(self) -> str:
        value = f"PipelineNode object <name : {self.__name}, parent number : {len(self.parent)}"
        if self.__func is not None:
            value += f", function : {self.__func.__name__}"
        value += ">"
        return value

    def execute(self) -> None:
        if len(self.__parent) != 0 and self.__func is not None:
            # get all value of previous parent
            data_list = [child.value for child in self.__parent]

            # perform operation
            self.__value = self.__func(*data_list)

    def _set_value(self, value: Any) -> None:
        self.__value = value

def deferred_execution(func):
    """
    A decorator that defers the execution of a function until the actual data is provided.

    The first argument of the function must be either DATA_PLACEHOLDER or None, indicating
    that the function execution should be deferred. When the function is eventually called
    with the actual data, the deferred execution is triggered.

    Args:
        func (callable): The function to be deferred.

    Returns:
        callable: A lambda function that takes the data as its first argument and executes
                  the original function with the deferred arguments.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Split args into Node / Non Node
        args_no_data = []
        parent = []
        for arg in args:
            if isinstance(arg, PipeNode):
                parent.append(arg)
            else:
                args_no_data.append(arg)

        # kw_no_data = {k: v for k, v in kwargs.items() if not isinstance(v, PipeNode)}
        deferred_func = lambda *data: func(*data, *args_no_data, **kwargs)
        deferred_func.__name__ = func.__name__
        return PipeNode(deferred_func, parent)
    return wrapper


