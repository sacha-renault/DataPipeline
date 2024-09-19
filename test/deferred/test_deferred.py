import numpy as np
import pytest

from src.dl_data_pipeline import deferred,InputNode
from src.dl_data_pipeline.process_functions import any_process

def test_instant_execute():
    with deferred.instant_excecution():
        val = any_process.rescale(np.random.randint(0,5, (10))) # choose a deferred function
    assert max(val) == 1
    assert min(val) == 0

def test_instant_execute_wrong():
    with pytest.raises(TypeError):
        with deferred.instant_excecution():
            any_process.rescale(InputNode())

def test_no_parents():
    with pytest.raises(TypeError):
        any_process.rescale(0)


