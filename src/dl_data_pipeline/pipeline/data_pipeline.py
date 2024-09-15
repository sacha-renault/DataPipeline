from collections.abc import Callable
from typing import List, Any

class Pipeline:
    def __init__(self) -> None:
        self.__forward: List[Callable] = []
        self.__forward_args: list = []
        self.__forward_kwargs: list = []
        self.__backward: List[Callable] = []
        self.__backward_args: list = []
        self.__backward_kwargs: list = []

    def add_forward(self, func: Callable, *args, **kwargs) -> None:
        if callable(func):
            self.__forward.append(func)
            self.__forward_args.append(args)
            self.__forward_kwargs.append(kwargs)
        else:
            raise TypeError(f"func must be a callable object")
        
    def add_backward(self, func: Callable, *args, **kwargs) -> None:
        if callable(func):
            self.__backward.append(func)
            self.__backward_args.append(args)
            self.__backward_kwargs.append(kwargs)
        else:
            raise TypeError(f"func must be a callable object")
    
    def forward(self, data: Any) -> Any:
        # TODO add pre processing validation

        call_iterable = zip(self.__forward, self.__forward_args, self.__forward_kwargs)
        for func, args, kwargs in call_iterable:
            data = func(data, *args, **kwargs)

        # TODO add post processing validation
        return data
    
    def backward(self, data: Any) -> Any:
        # TODO add pre processing validation

        call_iterable = zip(self.__backward, self.__backward_args, self.__backward_kwargs)
        for func, args, kwargs in call_iterable:
            data = func(data, *args, **kwargs)

        # TODO add post processing validation
        return data