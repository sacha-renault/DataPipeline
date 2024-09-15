from typing import Any

import numpy as np

from .base_validator import Validator
from .validation_error import ValidationError

class MeanVarValidator(Validator):
    def __init__(self, 
                target_mean: float | None = None,
                max_mean_gap: float = 1.0,
                target_var: float | None = None,
                max_var_gap: float = 1.0,
                ) -> None:
        super().__init__()
        if target_mean is None and target_var is None:
            raise ValueError("Both target_mean and target_var cannot be None")
        self.__target_mean = target_mean
        self.__max_mean_gap = max_mean_gap
        self.__target_var = target_var
        self.__max_var_gap = max_var_gap

    def validate(self, data: Any) -> None:
        # check only if mean is set
        if self.__target_mean is not None:
            data_mean = np.mean(data)
            mean_gap = np.abs(data_mean - self.__target_mean)
            if self.__max_mean_gap < mean_gap:
                raise ValidationError(f"Mean of data is {data_mean}, this is out of interval "
                    f"[{self.__target_mean - self.__max_mean_gap}, {self.__target_mean + self.__max_mean_gap}], "
                    "defined by user.")
        
        # check only if var is set
        if self.__target_var is not None:
            data_var = np.var(data)
            var_gap = np.abs(data_var - self.__target_var)
            if self.__max_var_gap < var_gap:
                raise ValidationError(f"Var of data is {data_var}, this is out of interval "
                    f"[{self.__target_var - self.__max_var_gap}, {self.__target_var + self.__max_var_gap}], "
                    "defined by user.")