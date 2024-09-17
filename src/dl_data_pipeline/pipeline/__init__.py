"""
This package provides the core components for building and managing data processing pipelines.

The package includes the following classes:

Classes:
    Pipeline: Manages the flow of data from input `PipeNode` objects through a series of operations to produce output `PipeNode` objects. Supports validation and execution of the pipeline.
    PipeNode: A node in a pipeline that can execute a function based on the values of its parent nodes, allowing for deferred execution and modular data processing.
    InputNode: A specialized `PipeNode` that represents the entry point of data into the pipeline, holding initial input values without performing any computation.

Usage Example:
    from my_pipeline_package import Pipeline, PipeNode, InputNode

    # Create input nodes
    input_node1 = InputNode(name="input1")
    input_node2 = InputNode(name="input2")

    # Create a processing node that adds the values from the two input nodes
    add_node = PipeNode(func=lambda x, y: x + y, parent=[input_node1, input_node2], name="sum")

    # Create a pipeline
    pipeline = Pipeline(inputs=[input_node1, input_node2], outputs=add_node)

    # Set input values
    input_node1._set_value(10)
    input_node2._set_value(20)

    # Execute the pipeline
    result = pipeline()  # result will be 30

Modules:
    pipeline: Contains the `Pipeline` class for managing the data flow in a pipeline.
    pipe_node: Contains the `PipeNode` class, the basic building block for creating data processing graphs.
    input_node: Contains the `InputNode` class, a specialized node for inputting data into the pipeline.
"""

from .data_pipeline import Pipeline
from .input_node import InputNode
from .pipe_node import PipeNode