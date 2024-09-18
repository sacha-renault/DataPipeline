try:
    from ._version import VERSION as __version__
except:
    __version__ = "Unknown"

from .pipeline.data_pipeline import Pipeline
from .pipeline.input_node import InputNode
from .process_functions import (process_1d, process_2d, any_process)
from .validator.base_validator import ValidationError
from .deferred import deferred_execution