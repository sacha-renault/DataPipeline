import pytest
import numpy as np

from src.dl_data_pipeline.process_functions import process_1d
from src.dl_data_pipeline.pipeline.pipe_node import PipelineNode

def test_rpad_rcut_exception():
    node = PipelineNode()
    node._set_value(np.random.rand(1000))
    with pytest.raises(AssertionError):
        result_node = process_1d.rpad_rcut(node, 5000)
        result_node.execute()

def test_rpad_rcut_normal():
    array = np.random.rand(2, 1000)
    node = PipelineNode()
    node._set_value(array)
    result_node = process_1d.rpad_rcut(node, 5000)
    result_node.execute()
    result = result_node.value
    assert result.shape == (2, 5000)
    assert np.array_equal(array, result[:, :1000])

def test_lpad_lcut_exception():
    node = PipelineNode()
    node._set_value(np.random.rand(1000))
    with pytest.raises(AssertionError):
        result_node = process_1d.lpad_lcut(node, 5000)
        result_node.execute()

def test_lpad_lcut_normal():
    array = np.random.rand(2, 1000)
    node = PipelineNode()
    node._set_value(array)
    result_node = process_1d.lpad_lcut(node, 5000)
    result_node.execute()
    result = result_node.value
    assert result.shape == (2, 5000)
    assert np.array_equal(array, result[:, -1000:])

def test_center_pad_rcut_exception():
    node = PipelineNode()
    node._set_value(np.random.rand(1000))
    with pytest.raises(AssertionError):
        result_node = process_1d.center_pad_rcut(node, 5000)
        result_node.execute()

def test_center_pad_rcut_normal():
    array = np.random.rand(2, 1000)
    node = PipelineNode()
    node._set_value(array)
    result_node = process_1d.center_pad_rcut(node, 5000)
    result_node.execute()
    result = result_node.value
    assert result.shape == (2, 5000)
    assert np.array_equal(array, result[:, 2000:3000])

def test_center_pad_rcut_many():
    array = np.random.rand(2, 1000)
    node = PipelineNode()
    node._set_value(array)
    for i in range(200):
        result_node = process_1d.center_pad_rcut(node, 5000 + i)
        result_node.execute()
        result = result_node.value
        assert result.shape == (2, 5000 + i)

def test_rpad_rcut_normal_smaller():
    array = np.random.rand(2, 1000)
    node = PipelineNode()
    node._set_value(array)
    result_node = process_1d.rpad_rcut(node, 500)
    result_node.execute()
    result = result_node.value
    assert result.shape == (2, 500)
    assert np.array_equal(array[:, :500], result)

def test_lpad_lcut_normal_smaller():
    array = np.random.rand(2, 1000)
    node = PipelineNode()
    node._set_value(array)
    result_node = process_1d.lpad_lcut(node, 500)
    result_node.execute()
    result = result_node.value
    assert result.shape == (2, 500)
    assert np.array_equal(array[:, -500:], result)

def test_center_pad_rcut_normal_smaller():
    array = np.random.rand(2, 1000)
    node = PipelineNode()
    node._set_value(array)
    result_node = process_1d.center_pad_rcut(node, 500)
    result_node.execute()
    result = result_node.value
    assert result.shape == (2, 500)
    assert np.array_equal(array[:, :500], result)
