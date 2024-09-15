from typing import Any
from .base_validator import Validator
from .validation_error import ValidationError

class NameValidator(Validator):
    def validate(self, data: Any) -> None:
        pass
        # TODO