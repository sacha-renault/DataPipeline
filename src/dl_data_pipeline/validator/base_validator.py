from abc import ABC, abstractmethod
from typing import Any

from .validation_error import ValidationError

class Validator(ABC):
    """
    Abstract base class for data validation.

    This class provides a template for creating specific validators that 
    check the integrity or correctness of data. Implementations of this 
    class should define the `validate` method to perform the actual 
    validation logic.

    Subclasses must override the `validate` method to provide specific 
    validation rules. If the data does not meet the validation criteria, 
    the method should raise a `ValidationError`.

    Args:
        data (Any): The data to be validated.

    Raises:
        ValidationError: If the data fails to meet the validation criteria 
                          defined in the subclass implementation.
    """
    
    @abstractmethod
    def validate(self, data: Any) -> None:
        """base class for data validation

        Args:
            data (Any): data to be processed

        Raises:
            ValidationError: data didn't validate
        """