from typing import Any
from .base_validator import Validator
from .validation_error import ValidationError

class TypeValidator(Validator):
    """
    Validator class that checks if the data is of one of the accepted types.

    This class extends the `Validator` base class to ensure that the type of the 
    input data matches one of the specified acceptable types.

    Args:
        *accepted_types (type): A variable number of type arguments representing the 
                                acceptable types for the data. The data must be an 
                                instance of at least one of these types.

    Raises:
        ValidationError: If the data is not an instance of any of the accepted types.

    Examples:
        >>> validator = TypeValidator(int, float)
        >>> validator.validate(42)  # This will pass because 42 is an int.

        >>> validator = TypeValidator(int, float)
        >>> validator.validate("string")  # This will raise a ValidationError because "string" is not an int or float.
    """
    
    def __init__(self, *accepted_types: type) -> None:
        super().__init__()
        self.__types = accepted_types

    def validate(self, data: Any) -> None:
        if not isinstance(data, self.__types):
            raise ValidationError(f"data must be type : {self.__types}, not {type(data)}")