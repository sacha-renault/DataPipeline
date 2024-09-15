from typing import Any

import numpy as np

from .base_validator import Validator
from .validation_error import ValidationError

class MinMaxValidator(Validator):
    def __init__(self, min: float, max: float) -> None:
        super().__init__()
        self.__max = max
        self.__min = min

    def validate(self, data: Any) -> None:
        data_min = np.min(data)
        if np.min(data) < self.__min:
            raise ValidationError(f"Min of data is {data_min}, this is less than {self.__min}, defined by user.")
        
        data_max = np.max(data)
        if data_max > self.__max:
            raise ValidationError(f"Max of data is {data_max}, this is more than {self.__max}, defined by user.")