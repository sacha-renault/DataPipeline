from typing import Any
from .base_validator import Validator
from .validation_error import ValidationError

class ShapeValidator(Validator):
    """
    Validator class that checks if the shape of the data matches the expected shape.

    This class extends the `Validator` base class to ensure that the shape of the 
    input data matches a specified shape. It uses a specified attribute getter 
    method to retrieve the shape of the data.

    Args:
        accepted_shape (Any): The shape that the data should match. This can be 
                              any value that represents the expected shape (e.g., 
                              a tuple for multidimensional arrays).
        shape_getter (str, optional): The name of the attribute to be used for 
                                       retrieving the shape of the data. Defaults 
                                       to "shape". This should be the name of an 
                                       attribute that returns the shape of the data 
                                       (e.g., 'shape' for NumPy arrays).

    Raises:
        ValidationError: If the data does not have the specified shape or if 
                          the shape attribute is not present.

    Examples:
        >>> validator = ShapeValidator((100, 200))
        >>> data = np.zeros((100, 200))
        >>> validator.validate(data)  # This will pass because the shape matches.

        >>> validator = ShapeValidator((100, 200))
        >>> data = np.zeros((100, 300))
        >>> validator.validate(data)  # This will raise a ValidationError because the shape does not match.
    """
    
    def __init__(self, accepted_shape: Any, shape_getter: str = "shape") -> None:
        self.__shape = accepted_shape
        self.__getter = shape_getter

    def validate(self, data: Any) -> None:
        if not hasattr(data, self.__getter):
            raise ValidationError(f"data must have an attribute {self.__getter}.")
        
        shape = getattr(data, self.__getter)
        if shape != self.__shape:
            raise ValidationError(f"Invalid shape, expected : {self.__shape}, received : {shape}.")