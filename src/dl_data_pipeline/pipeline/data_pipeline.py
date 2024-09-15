from collections.abc import Callable
from typing import List, Any

class Pipeline:
    def __init__(self) -> None:
        self.__forward :List[Callable] = []
        self.__backward :List[Callable] = []

    def add_forward(self, func: Callable) -> None:
        if callable(func):
            self.__forward.append(func)
        else:
            raise TypeError(f"func must be a callable object")
        
    def add_backward(self, func: Callable) -> None:
        if callable(func):
            self.__backward.append(func)
        else:
            raise TypeError(f"func must be a callable object")
    
    def forward(self, data: Any) -> Any:
        # TODO add pre processing validation

        for func in self.__forward:
            data = func(data)

        # TODO add post processing validation
        return data
    
    def backward(self, data: Any) -> Any:
        # TODO add pre processing validation

        for func in self.__backward:
            data = func(data)

        # TODO add post processing validation
        return data