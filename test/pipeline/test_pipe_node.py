import numpy as np
import pytest

from src.dl_data_pipeline.pipeline import PipelineNode, Pipeline

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