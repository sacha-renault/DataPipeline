from typing import Any
from .base_validator import Validator
from .validation_error import ValidationError

class TypeValidator(Validator):
    def __init__(self, *accepted_types: type) -> None:
        super().__init__()
        self.__types = accepted_types

    def validate(self, data: Any) -> None:
        if not isinstance(data, self.__types):
            raise ValidationError(f"data must be type : {self.__types}, not {type(data)}")