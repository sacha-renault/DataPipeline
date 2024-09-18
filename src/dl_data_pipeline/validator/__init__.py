"""
This module provides various classes for data validation, extending the base `Validator` class.

The validators included in this module are designed to check different properties of data to ensure it meets specific criteria. They are useful for ensuring data integrity and quality in various data processing and analysis applications.

Classes:
- `TypeValidator`: Checks if the data is of one of the specified types.
- `ShapeValidator`: Validates that the data has a specific shape.
- `MinMaxValidator`: Ensures that the minimum and maximum values of the data fall within specified bounds.
- `MeanVarValidator`: Validates that the mean and variance of the data are within acceptable ranges.

Exceptions:
- `ValidationError`: Raised when data does not meet the validation criteria defined by any of the validators.

Usage Example:
    >>> from validators import TypeValidator, ShapeValidator, MinMaxValidator, MeanVarValidator, RangeValidator
    >>> validator = TypeValidator(int, float)
    >>> validator.validate(5)  # Passes as 5 is of type int
    >>> validator.validate("string")  # Raises ValidationError as "string" is not of type int or float

    >>> shape_validator = ShapeValidator((3, 3))
    >>> shape_validator.validate(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))  # Passes as shape is (3, 3)
    >>> shape_validator.validate(np.array([[1, 2, 3], [4, 5, 6]]))  # Raises ValidationError as shape is (2, 3)
    
    >>> min_max_validator = MinMaxValidator(min_value=0, max_value=10)
    >>> min_max_validator.validate(np.array([1, 5, 9]))  # Passes as min=1 and max=9 are within bounds
    >>> min_max_validator.validate(np.array([-1, 5, 12]))  # Raises ValidationError as min=-1 and max=12 are out of bounds
    
    >>> mean_var_validator = MeanVarValidator(target_mean=5.0, max_mean_gap=1.0, target_var=2.0, max_var_gap=0.5)
    >>> mean_var_validator.validate(np.array([4, 5, 6]))  # Passes as mean and variance are within acceptable ranges
    >>> mean_var_validator.validate(np.array([1, 2, 3]))  # Raises ValidationError as mean or variance are out of bounds
"""


from .base_validator import Validator
from .type_validator import TypeValidator
from .shape_validator import ShapeValidator
from .min_max_validator import MinMaxValidator
from .mean_var_validator import MeanVarValidator
from .validation_error import ValidationError