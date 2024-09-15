from typing import Any
from .base_validator import Validator
from .validation_error import ValidationError

class ShapeValidator(Validator):
    def __init__(self, accepted_shape: Any, shape_getter: str = "shape") -> None:
        self.__shape = accepted_shape
        self.__getter = shape_getter

    def validate(self, data: Any) -> None:
        if not hasattr(data, self.__getter):
            raise ValidationError(f"data must have an attribute {self.__getter}.")
        
        shape = getattr(data, self.__getter)
        if shape != self.__shape:
            raise ValidationError(f"Invalid shape, expected : {self.__shape}, received : {shape}.")