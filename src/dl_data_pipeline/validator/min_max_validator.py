from typing import Any

import numpy as np

from .base_validator import Validator
from .validation_error import ValidationError

class MinMaxValidator(Validator):
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