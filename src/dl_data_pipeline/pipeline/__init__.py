"""
This package provides the core components for building and managing data processing pipelines.

The package includes the following classes:

Classes:
    Pipeline: Manages the flow of data from input `PipeNode` objects through a series of operations to produce output `PipeNode` objects. Supports validation and execution of the pipeline.
    PipeNode: A node in a pipeline that can execute a function based on the values of its parent nodes, allowing for deferred execution and modular data processing.
    InputNode: A specialized `PipeNode` that represents the entry point of data into the pipeline, holding initial input values without performing any computation.

Usage Example:

>>> # Import lib
>>> from dl_data_pipeline import Pipeline, InputNode, deferred_execution

>>> # Create input nodes
>>> input_node1 = InputNode(name="1")   # InputNode base name is input, it then concatenate
>>> input_node2 = InputNode(name="2")   # Any subname passed by user   

>>> # use any function, you can also create one
>>> @deferred_execution
>>> def sum(v1, v2):
>>>     return v1 + v2

>>> # create a functional PipelineNode with this function
>>> add_node = sum(input_node1, input_node2)

>>> # Create a pipeline
>>> pipeline = Pipeline(inputs=[input_node1, input_node2], outputs=add_node)

>>> # Compute pipe
>>> result = pipeline(20, 10) # will be 30

Modules:
    data_pipeline: Contains the `Pipeline` class for managing the data flow in a pipeline.
    pipe_node: Contains the `PipeNode` class, the basic building block for creating data processing graphs.
    input_node: Contains the `InputNode` class, a specialized node for inputting data into the pipeline.
"""

from .data_pipeline import Pipeline
from .input_node import InputNode
from .pipe_node import PipelineNode