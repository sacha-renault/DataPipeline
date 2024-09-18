import pytest
import numpy as np

from src.dl_data_pipeline.process_functions import any_process
from src.dl_data_pipeline.pipeline.pipe_node import PipelineNode

def test_rescale_basic():
    data = np.array([1, 2, 3, 4, 5])
    node = PipelineNode()
    node._set_value(data)
    rescaled_data_node = any_process.rescale(node, 0, 1)
    rescaled_data_node.execute()
    expected_data = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    assert np.allclose(rescaled_data_node.value, expected_data), "Basic rescaling failed"

def test_rescale_error_0_range():
    data = np.array([0,0,0,0,0])
    with pytest.raises(ValueError):
        node = PipelineNode()
        node._set_value(data)
        any_process.rescale(node, 0, 1).execute()