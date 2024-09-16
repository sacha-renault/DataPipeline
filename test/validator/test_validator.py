import pytest
import numpy as np
from . import DummyData, CustomShapeData, CustomClass
from src.dl_data_pipeline.validator import (
    MeanVarValidator,
    MinMaxValidator,
    ShapeValidator,
    TypeValidator,
    ValidationError
)

def test_validate_with_mean_within_gap():
    data = np.array([1.0, 2.0, 3.0])
    validator = MeanVarValidator(target_mean=2.0, max_mean_gap=1.0)
    # This should pass as the mean is exactly 2.0, within the allowed gap
    validator.validate(data)

def test_validate_with_mean_outside_gap():
    data = np.array([1.0, 2.0, 3.0])
    validator = MeanVarValidator(target_mean=4.0, max_mean_gap=0.5)
    with pytest.raises(ValidationError, match=r"Mean of data is.*out of interval.*"):
        validator.validate(data)

def test_validate_with_var_within_gap():
    data = np.array([1.0, 2.0, 3.0])
    validator = MeanVarValidator(target_var=0.5, max_var_gap=1.0)
    # This should pass as the variance is within the allowed gap
    validator.validate(data)

def test_validate_with_var_outside_gap():
    data = np.array([1.0, 2.0, 3.0])
    validator = MeanVarValidator(target_var=2.0, max_var_gap=0.5)
    with pytest.raises(ValidationError, match=r"Var of data is.*out of interval.*"):
        validator.validate(data)

def test_validate_with_both_mean_and_var_within_gap():
    data = np.array([1.0, 2.0, 3.0])
    validator = MeanVarValidator(target_mean=2.0, max_mean_gap=1.0, target_var=0.6667, max_var_gap=0.5)
    # Both mean and variance are within the allowed gap
    validator.validate(data)

def test_validate_with_mean_within_var_outside():
    data = np.array([1.0, 2.0, 3.0])
    validator = MeanVarValidator(target_mean=2.0, max_mean_gap=1.0, target_var=1, max_var_gap=0.1)
    with pytest.raises(ValidationError, match=r"Var of data is.*out of interval.*"):
        validator.validate(data)

def test_validate_with_var_within_mean_outside():
    data = np.array([1.0, 2.0, 3.0])
    validator = MeanVarValidator(target_mean=3.0, max_mean_gap=0.5, target_var=0.6667, max_var_gap=0.5)
    with pytest.raises(ValidationError, match=r"Mean of data is.*out of interval.*"):
        validator.validate(data)

def test_validate_with_neither_mean_nor_var_set():
    with pytest.raises(ValueError, match=r"Both target_mean and target_var cannot be None"):
        MeanVarValidator()

def test_validate_with_single_value_data():
    data = np.array([2.0])
    validator = MeanVarValidator(target_mean=2.0, max_mean_gap=0.1, target_var=0.0, max_var_gap=0.1)
    # Single value data should pass for both mean and variance
    validator.validate(data)

def test_min_max_validator_within_bounds():
    data = np.array([1.0, 2.0, 3.0])
    validator = MinMaxValidator(min_value=1.0, max_value=3.0)
    # This should pass as all data is within the specified min and max bounds
    validator.validate(data)

def test_min_max_validator_min_violation():
    data = np.array([0.5, 1.0, 2.0])
    validator = MinMaxValidator(min_value=1.0)
    with pytest.raises(ValidationError, match=r"Min of data is.*less than.*"):
        validator.validate(data)

def test_min_max_validator_max_violation():
    data = np.array([2.0, 3.0, 4.0])
    validator = MinMaxValidator(max_value=3.0)
    with pytest.raises(ValidationError, match=r"Max of data is.*more than.*"):
        validator.validate(data)

def test_min_max_validator_no_min_or_max_raises_error():
    with pytest.raises(ValueError, match=r"Both min_value and max_value cannot be None"):
        MinMaxValidator()

def test_min_max_validator_min_only():
    data = np.array([1.5, 2.0, 3.0])
    validator = MinMaxValidator(min_value=1.0)
    # This should pass as all data is above the min bound
    validator.validate(data)

def test_min_max_validator_max_only():
    data = np.array([1.0, 2.0, 2.5])
    validator = MinMaxValidator(max_value=3.0)
    # This should pass as all data is below the max bound
    validator.validate(data)

def test_shape_validator_correct_shape():
    data = DummyData((2, 3))
    validator = ShapeValidator(accepted_shape=(2, 3))
    # This should pass as the shape matches the accepted shape
    validator.validate(data)

def test_shape_validator_incorrect_shape():
    data = DummyData((2, 4))
    validator = ShapeValidator(accepted_shape=(2, 3))
    with pytest.raises(ValidationError, match=r"Invalid shape, expected :.*received :.*"):
        validator.validate(data)

def test_shape_validator_missing_attribute():
    class NoShapeAttribute:
        pass

    data = NoShapeAttribute()
    validator = ShapeValidator(accepted_shape=(2, 3))
    with pytest.raises(ValidationError, match=r"data must have an attribute shape."):
        validator.validate(data)

def test_shape_validator_custom_getter():
    data = CustomShapeData(custom_shape=(2, 3))
    validator = ShapeValidator(accepted_shape=(2, 3), shape_getter="custom_shape_attr")
    # This should pass as the shape matches using the custom getter
    validator.validate(data)

def test_shape_validator_custom_getter_wrong_shape():
    data = CustomShapeData(custom_shape=(2, 4))
    validator = ShapeValidator(accepted_shape=(2, 3), shape_getter="custom_shape_attr")
    with pytest.raises(ValidationError, match=r"Invalid shape, expected :.*received :.*"):
        validator.validate(data)

def test_type_validator_single_type():
    validator = TypeValidator(int)
    data = 42
    # This should pass as data is of type int
    validator.validate(data)

def test_type_validator_multiple_types():
    validator = TypeValidator(int, float)
    data = 3.14
    # This should pass as data is of type float
    validator.validate(data)

def test_type_validator_invalid_type():
    validator = TypeValidator(int, float)
    data = "a string"
    with pytest.raises(ValidationError, match=r"data must be type :.*not <class 'str'>"):
        validator.validate(data)

def test_type_validator_with_custom_class():
    validator = TypeValidator(CustomClass)
    data = CustomClass()
    # This should pass as data is of type CustomClass
    validator.validate(data)

def test_type_validator_invalid_custom_class():
    validator = TypeValidator(CustomClass)
    data = 42
    with pytest.raises(ValidationError, match=r"data must be type :.*not <class 'int'>"):
        validator.validate(data)
