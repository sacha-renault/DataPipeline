from typing import Any

import numpy as np

from .base_validator import Validator
from .validation_error import ValidationError

class MeanVarValidator(Validator):
    """
    Validator class that checks whether the mean and variance of a dataset 
    fall within specified ranges.

    This class extends the `Validator` base class to provide validation based 
    on statistical properties of the data. It checks if the mean and variance 
    of the input data are within user-defined acceptable ranges.

    Args:
        target_mean (float, optional): The target mean value that the data 
                                        should be close to. If `None`, mean 
                                        validation is not performed.
        max_mean_gap (float, optional): The maximum allowed deviation of the 
                                        mean from the target mean. Defaults 
                                        to 1.0.
        target_var (float, optional): The target variance value that the data 
                                       should be close to. If `None`, variance 
                                       validation is not performed.
        max_var_gap (float, optional): The maximum allowed deviation of the 
                                        variance from the target variance. 
                                        Defaults to 1.0.

    Raises:
        ValueError: If both `target_mean` and `target_var` are `None`.
        ValidationError: If the mean or variance of the data falls outside 
                          the acceptable range defined by `target_mean` and 
                          `max_mean_gap`, or `target_var` and `max_var_gap`.

    Examples:
        >>> validator = MeanVarValidator(target_mean=0.0, max_mean_gap=0.1, 
        >>>                                target_var=1.0, max_var_gap=0.1)
        >>> data = np.array([0.05, -0.02, 0.03])
        >>> validator.validate(data)  # This will pass if mean and variance are within the specified gaps
    """
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