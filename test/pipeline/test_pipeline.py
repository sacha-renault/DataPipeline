import numpy as np
import pytest

from src.dl_data_pipeline.pipeline.data_pipeline import Pipeline
from src.dl_data_pipeline.validator import MinMaxValidator
from src.dl_data_pipeline.process_functions.any_process import rescale

def test_pipeline_basic():
    pipe = Pipeline()
    pipe.add_forward_process(rescale, 0, 2)
    pipe.add_backward_process(rescale, 0, 0.5)
    pipe.add_forward_validator(MinMaxValidator(0, 2))
    pipe.add_backward_validator(MinMaxValidator(0, 0.5))
    farr = pipe.forward(np.arange(10))
    barr = pipe.backward(np.arange(10))
    pipe.__repr__()
    assert np.max(farr) == 2
    assert np.max(barr) == 0.5

def test_pipeline_add_non_callable_forward():
    pipe = Pipeline()
    with pytest.raises(TypeError):
        pipe.add_forward_process(None, 0, 2)

def test_pipeline_add_non_callable_backward():
    pipe = Pipeline()
    with pytest.raises(TypeError):
        pipe.add_backward_process(None, 0, 2)

def test_pipeline_add_non_validator_forward():
    pipe = Pipeline()
    with pytest.raises(TypeError):
        pipe.add_forward_validator(None)

def test_pipeline_add_non_validator_backward():
    pipe = Pipeline()
    with pytest.raises(TypeError):
        pipe.add_backward_validator(None)

def test_pipeline_error_processing():
    pipe = Pipeline()
    pipe.add_forward_process(rescale, 0, 2)
    pipe.add_backward_process(rescale, 0, 0.5)
    flat_data = np.zeros(10)
    with pytest.raises(RuntimeError):
        pipe.forward(flat_data)
    with pytest.raises(RuntimeError):
        pipe.backward(flat_data)