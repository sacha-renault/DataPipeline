import pytest
import numpy as np

from src.dl_data_pipeline.process_functions import process_1d 

def test_rpad_rcut_exception():
    with pytest.raises(AssertionError):
        process_1d.rpad_rcut(np.random.rand(1000), 5000)

def test_rpad_rcut_normal():
    array = np.random.rand(2, 1000)
    result = process_1d.rpad_rcut(array, 5000)
    assert result.shape == (2, 5000)
    assert np.array_equal(array, result[:, :1000])

def test_lpad_lcut_exception():
    with pytest.raises(AssertionError):
        process_1d.lpad_lcut(np.random.rand(1000), 5000)

def test_lpad_lcut_normal():
    array = np.random.rand(2, 1000)
    result = process_1d.lpad_lcut(array, 5000)
    assert result.shape == (2, 5000)
    assert np.array_equal(array, result[:, -1000:])

def test_center_pad_rcut_exception():
    with pytest.raises(AssertionError):
        process_1d.center_pad_rcut(np.random.rand(1000), 5000)

def test_center_pad_rcut_normal():
    array = np.random.rand(2, 1000)
    result = process_1d.center_pad_rcut(array, 5000)
    assert result.shape == (2, 5000)
    assert np.array_equal(array, result[:, 2000:3000])

def test_center_pad_rcut_many():
    array = np.random.rand(2, 1000)
    for i in range(200):
        result = process_1d.center_pad_rcut(array, 5000 + i)
        assert result.shape == (2, 5000 + i)

def test_rpad_rcut_normal_smaller():
    array = np.random.rand(2, 1000)
    result = process_1d.rpad_rcut(array, 500)
    assert result.shape == (2, 500)
    assert np.array_equal(array[:, :500], result)

def test_lpad_lcut_normal_smaller():
    array = np.random.rand(2, 1000)
    result = process_1d.lpad_lcut(array, 500)
    assert result.shape == (2, 500)
    assert np.array_equal(array[:, -500:], result)

def test_center_pad_rcut_normal_smaller():
    array = np.random.rand(2, 1000)
    result = process_1d.center_pad_rcut(array, 500)
    assert result.shape == (2, 500)
    assert np.array_equal(array[:, :500], result)