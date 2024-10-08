import numpy as np
import pytest

from src.dl_data_pipeline import Pipeline, InputNode, deferred_execution
from src.dl_data_pipeline.validator import MinMaxValidator, ValidationError
from src.dl_data_pipeline.process_functions.any_process import rescale
from src.dl_data_pipeline.process_functions.process_2d import image_chw_to_hwc

def test_pipeline_basic():
    inp = InputNode()
    output = rescale(inp, 0, 2)

    pipe = Pipeline(inp, output)
    pipe.add_validator(MinMaxValidator(0, 2), 0)
    pipe.__repr__()
    data = pipe(np.random.rand(10))
    assert abs(np.max(data) - 2) < 1e-5

def test_pipeline_multi_in_out():
    @deferred_execution
    def add(a, b):
        return a + b

    @deferred_execution
    def sub(a, b):
        return a - b

    inp1= InputNode("Inp1")
    inp2= InputNode("Inp2")
    o1 = add(inp1, inp2)
    o2 = sub(inp1, inp2)
    pipe = Pipeline([inp1, inp2], [o1, o2])

    with pytest.raises(ValueError, match="Pipeline takes*"):
        pipe(np.random.rand(10))

    data1 = np.random.rand(10)
    data2 = np.random.rand(10)
    output = pipe(data1, data2)

    assert np.array_equal(output[0], data1 + data2)
    assert np.array_equal(output[1], data1 - data2)

def test_pipe_wrong_input():
    with pytest.raises(TypeError):
        Pipeline(1, InputNode())

def test_pipe_wrong_output():
    with pytest.raises(TypeError):
        Pipeline(InputNode(), 1)

def test_pipeline_add_non_validator():
    pipe = Pipeline(InputNode(), InputNode())
    with pytest.raises(TypeError):
        pipe.add_validator(1, 0)


def test_pipeline_add_validator_wrong_index():
    pipe = Pipeline(InputNode(), InputNode())
    with pytest.raises(IndexError):
        pipe.add_validator(MinMaxValidator(0, 1), -1)


def test_pipeline_trigger_validator():
    inp = InputNode()
    output = rescale(inp, 0, 5)
    pipe = Pipeline(inp, output)
    pipe.add_validator(MinMaxValidator(0, 2), 0)

    with pytest.raises(ValidationError):
        pipe(np.random.rand(10))

def test_sub_pipeline():
    inp = InputNode()
    inp2 = InputNode()
    output = rescale(inp, inp2, 5)
    subpipe = Pipeline([inp, inp2], output)

    n_input = InputNode()
    n_output = subpipe.as_deferred(n_input, 0)
    main_pipe = Pipeline(n_input, n_output)

    result = main_pipe(np.random.rand(10, 10) - 0.5)

    assert np.abs(np.min(result)) < 1e-9
    assert np.abs(np.max(result) - 5) < 1e-9

def test_sub_pipeline_no_node_execption():
    inp = InputNode()
    inp2 = InputNode()
    output = rescale(inp, inp2, 5)
    subpipe = Pipeline([inp, inp2], output)

    with pytest.raises(TypeError):
        subpipe.as_deferred(0, 0)