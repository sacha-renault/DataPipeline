import pytest
import numpy as np

from src.dl_data_pipeline.process_functions import any_process

def test_rescale_basic():
    data = np.array([1, 2, 3, 4, 5])
    rescaled_data = any_process.rescale(data, 0, 1)
    expected_data = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    assert np.allclose(rescaled_data, expected_data), "Basic rescaling failed"

def test_rescale_error_0_range():
    data = np.array([0,0,0,0,0])    
    with pytest.raises(ValueError):
        rescaled_data = any_process.rescale(data, 0, 1)