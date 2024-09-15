from abc import ABC, abstractmethod
from typing import Any

from .validation_error import ValidationError

class Validator(ABC):
    @abstractmethod
    def validate(self, data: Any) -> None:
        """base class for data validation

        Args:
            data (Any): data to be processed

        Raises:
            ValidationError: data didn't validate
        """