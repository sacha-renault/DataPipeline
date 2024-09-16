from typing import Any

import numpy as np

from .base_validator import Validator
from .validation_error import ValidationError

class MinMaxValidator(Validator):
    """
    Validator class that checks whether the values in a dataset fall within
    specified minimum and maximum bounds.

    This class extends the `Validator` base class to provide validation based 
    on the minimum and maximum values of the data. It ensures that all values 
    in the input data are within the defined range.

    Args:
        min_value (float, optional): The minimum allowable value for the data. 
                                     If `None`, the minimum value is not validated.
        max_value (float, optional): The maximum allowable value for the data. 
                                     If `None`, the maximum value is not validated.

    Raises:
        ValueError: If both `min_value` and `max_value` are `None`.
        ValidationError: If any value in the data is outside the range defined 
                          by `min_value` and `max_value`.

    Examples:
        >>> validator = MinMaxValidator(min_value=0.0, max_value=1.0)
        >>> data = np.array([0.5, 0.8, 1.2])
        >>> validator.validate(data)  # This will raise a ValidationError because 1.2 > 1.0
    """
    
    def __init__(self, min_value: float | None = None, max_value: float | None = None) -> None:
        super().__init__()

        if min_value is None and max_value is None:
            raise ValueError("Both min_value and max_value cannot be None")
        
        self.__max = max_value
        self.__min = min_value

    def validate(self, data: Any) -> None:
        if self.__min is not None:
            data_min = np.min(data)
            if data_min < self.__min:
                raise ValidationError(f"Min of data is {data_min}, "
                    f"this is less than {self.__min}, "
                    f"defined by user.")
        
        if self.__max is not None:
            data_max = np.max(data)
            if data_max > self.__max:
                raise ValidationError(f"Max of data is {data_max}, "
                    f"this is more than {self.__max}, defined by user.")