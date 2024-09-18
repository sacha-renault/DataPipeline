"""
input_node.py

This module defines the `InputNode` class, a specialized subclass of `PipeNode` that represents an input node
in a data processing pipeline.

An `InputNode` is used to provide initial data into a pipeline, serving as the starting point for data flow.
It does not perform any computation itself but instead holds a value that can be used by other nodes in the
pipeline.

Classes:
    InputNode: A subclass of `PipeNode` designed to serve as an input node in a pipeline.
"""

from collections.abc import Callable
from .pipe_node import PipelineNode

class InputNode(PipelineNode):
    """
    A class representing an input node in a data processing pipeline.

    The `InputNode` class is a specialized subclass of `PipeNode` that is designed to hold initial input data
    for a pipeline. Unlike other nodes, `InputNode` does not perform any computation; it simply stores a value
    that can be accessed by other nodes in the pipeline.

    Args:
        name (str, optional): An optional name for the input node. Defaults to an empty string.
    """
    def __init__(self, name: str = "") -> None:
        super().__init__(None, None, f"Input {name}")