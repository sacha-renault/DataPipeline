from collections.abc import Callable
from typing import List, Any, Tuple, Dict

from ..validator import Validator

class Pipeline:
    """
    A class to manage a sequence of forward and backward processes with optional validation.

    The `Pipeline` class allows for adding functions to process data in a forward and backward manner.
    Each process can have associated arguments, keyword arguments, and validators to ensure the processed
    data meets certain criteria.

    Methods:
        add_forward_process(func, *args, **kwargs): Adds a function to the forward process list.
        add_forward_validator(validator): Adds a validator to the forward validators list.
        add_backward_process(func, *args, **kwargs): Adds a function to the backward process list.
        add_backward_validator(validator): Adds a validator to the backward validators list.
        forward(data): Processes the data through the forward functions and validators.
        backward(data): Processes the data through the backward functions and validators.
    """
    def __init__(self) -> None:
        # forward 
        self.__forward: List[Callable] = []
        self.__forward_args: List[Tuple] = []
        self.__forward_kwargs: List[Dict] = []
        self.__forward_validators: List[Validator] = []

        # backward 
        self.__backward: List[Callable] = []
        self.__backward_args: List[Tuple] = []
        self.__backward_kwargs: List[Dict] = []
        self.__backward_validators: List[Validator] = []

    def add_forward_process(self, func: Callable, *args, **kwargs) -> None:
        if callable(func):
            self.__forward.append(func)
            self.__forward_args.append(args)
            self.__forward_kwargs.append(kwargs)
        else:
            raise TypeError(f"func must be a callable object")
        
    def add_forward_validator(self, validator: Validator) -> None:
        if isinstance(validator, Validator):
            self.__forward_validators.append(validator)
        else:
            raise TypeError(f"validator must be a Validator object")
        
    def add_backward_process(self, func: Callable, *args, **kwargs) -> None:
        if callable(func):
            self.__backward.append(func)
            self.__backward_args.append(args)
            self.__backward_kwargs.append(kwargs)
        else:
            raise TypeError(f"func must be a callable object")
        
    def add_backward_validator(self, validator: Validator) -> None:
        if isinstance(validator, Validator):
            self.__backward_validators.append(validator)
        else:
            raise TypeError(f"validator must be a Validator object")
    
    def forward(self, data: Any) -> Any:
        call_iterable = zip(self.__forward, self.__forward_args, self.__forward_kwargs)

        # Process data sequentially
        for func, args, kwargs in call_iterable:
            try:
                data = func(data, *args, **kwargs)
            except Exception as e:
                raise RuntimeError(f"Error in forward process {func.__name__}: {e}")


        # ensure data don't raise any error with validator
        for validator in self.__forward_validators:
            validator.validate(data)

        return data
    
    def backward(self, data: Any) -> Any:
        call_iterable = zip(self.__backward, self.__backward_args, self.__backward_kwargs)

        # process data sequentially
        for func, args, kwargs in call_iterable:
            try:
                data = func(data, *args, **kwargs)
            except Exception as e:
                raise RuntimeError(f"Error in backward process {func.__name__}: {e}")


        # ensure data don't raise any error with validator
        for validator in self.__backward_validators:
            validator.validate(data)
        return data
    
    def __repr__(self) -> str:
        return (f"Pipeline("
                f"forward_processes={len(self.__forward)}, "
                f"forward_validators={len(self.__forward_validators)}, "
                f"backward_processes={len(self.__backward)}, "
                f"backward_validators={len(self.__backward_validators)})")