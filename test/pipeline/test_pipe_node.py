import numpy as np
import pytest

from src.dl_data_pipeline.pipeline import PipelineNode, Pipeline, InputNode
from src.dl_data_pipeline import deferred_execution

def test_pipe_node_getitem():
    input = PipelineNode()
    x = input[0]
    y = input[1]

    # assert x and y are nodes
    # and the parent is input
    assert isinstance(x, PipelineNode), "Type check failed"
    assert isinstance(y, PipelineNode), "Type check failed"
    assert input in x.parent
    assert input in y.parent

    # create a pipeline to test flow
    pipe = Pipeline(inputs=input, outputs=[x, y])
    result = pipe((10, 20))
    assert result == [10, 20]

    with pytest.raises(RuntimeError):
        pipe(10) # non subscriptable

def test_node_unwrap():
    @deferred_execution
    def dummy_func(v):
        return v + 1, v / 2

    inp = InputNode()
    x, y = dummy_func(inp).unwrap(2)
    pipe = Pipeline(inputs=inp, outputs=[x, y])
    o1, o2 = pipe(10)
    assert o1 == 11
    assert o2 == 5

def test_node_iter_no_unwrap():
    with pytest.raises(RuntimeError):
        x, y = PipelineNode()
