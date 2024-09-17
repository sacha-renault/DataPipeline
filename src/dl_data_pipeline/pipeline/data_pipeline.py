"""
data_pipeline.py

This module defines the `Pipeline` class, which is used to create and manage data processing pipelines.

A `Pipeline` consists of interconnected `PipeNode` objects that define a sequence of operations, allowing
for the execution of complex data processing flows. The `Pipeline` class supports validation of the processed
data through user-defined `Validator` objects and ensures that the data flows correctly from inputs to outputs.

Classes:
    Pipeline: Manages the flow of data from input `PipeNode` objects through a series of operations
              to produce output `PipeNode` objects. Supports validation and execution of the pipeline.

Usage Example:
    from pipeline import Pipeline
    from my_nodes import PipeNode
    from my_validators import MyValidator

    input_node = PipeNode()
    output_node = PipeNode(parent=input_node)
    pipeline = Pipeline(inputs=input_node, outputs=output_node)

    # Add a validator to the output
    validator = MyValidator()
    pipeline.add_validator(validator, output_index=0)

    # Execute the pipeline with input data
    result = pipeline(input_data)
"""

from collections.abc import Callable
from typing import List, Any, Tuple, Dict
from .pipe_node import PipeNode

from ..validator import Validator

class Pipeline:
    """
    A class that represents a data processing pipeline consisting of interconnected `PipeNode` objects.

    The `Pipeline` class manages the flow of data from input nodes through a series of operations
    to produce output nodes. It supports validation of output data through user-defined `Validator` objects.

    Args:
        inputs (PipeNode | list[PipeNode]): A single `PipeNode` or a list of `PipeNode` objects
            that serve as the inputs to the pipeline.
        outputs (PipeNode | list[PipeNode]): A single `PipeNode` or a list of `PipeNode` objects
            that serve as the outputs of the pipeline.

    Raises:
        ValueError: If `inputs` or `outputs` is not a `PipeNode` or a list of `PipeNode`.

    Methods:
        add_validator(validator: Validator, output_index: int) -> None:
            Adds a `Validator` to validate the output at the specified index.

        __call__(*args: Any) -> Any:
            Executes the pipeline with the provided inputs and returns the output(s).

    Example:
        # Create a simple pipeline
        input_node = PipeNode()
        output_node = PipeNode(parent=input_node)
        pipeline = Pipeline(inputs=input_node, outputs=output_node)

        # Add a validator to the output
        validator = MyValidator()
        pipeline.add_validator(validator, output_index=0)

        # Execute the pipeline
        result = pipeline(input_data)
    """
    def __init__(self, inputs: PipeNode | list[PipeNode], outputs: PipeNode | list[PipeNode]) -> None:
        if not (isinstance(inputs, PipeNode) or (isinstance(inputs, list) and all(isinstance(x, PipeNode) for x in inputs))):
            raise TypeError("inputs must be a PipeNode or a list of PipeNode")

        if not (isinstance(outputs, PipeNode) or (isinstance(outputs, list) and all(isinstance(x, PipeNode) for x in outputs))):
            raise TypeError("outputs must be a PipeNode or a list of PipeNode")

        self.__inputs = inputs if isinstance(inputs, list) else [inputs]
        self.__outputs = outputs if isinstance(outputs, list) else [outputs]
        self.__validators: list[list[Validator]] = [[] for _ in range(len(self.__outputs))]

        # init an exec graph
        exec_graph: list[PipeNode] = []
        visited = set()
        virtual_node = PipeNode(parent = self.__outputs)

        # lambda func to get ordered in topological order
        def build_topo(v: PipeNode):
            if v not in visited:
                visited.add(v)
                for child in v.parent:
                    build_topo(child)
                exec_graph.append(v)

        # build the actual graph
        build_topo(virtual_node)
        self.__exec_graph = exec_graph[:-1] # remove the last ghost node

    def add_validator(self, validator: Validator, output_index: int) -> None:
        if not isinstance(validator, Validator):
            raise TypeError(f"validator must be Validator type, not {type(validator)}")
        if output_index >= len(self.__outputs) or output_index < 0:
            raise IndexError(f"output_index isn't included in [0, len(outputs)[")

        self.__validators[output_index].append(validator)



    def __call__(self, *args: Any) -> Any:
        if len(args) != len(self.__inputs):
            raise ValueError(f"Pipeline takes {len(self.__inputs)} positional(s) argument(s), "
                             f"but {len(args)} were(was) provided")

        # set value in inputs node
        for node, arg in zip(self.__inputs, args):
            node._set_value(arg)

        # excecute
        for node in self.__exec_graph:
            node.execute()

        # return the output node value
        output = [node.value for node in self.__outputs]

        # validate data
        for output_data, validators in zip(output, self.__validators):
            for validator in validators:
                validator.validate(output_data)

        if len(output) == 1:
            return output[0]
        return output

    def __repr__(self) -> str:
        return (f"{self.__class__.__name__}("
                f"num_inputs = {len(self.__inputs)}, "
                f"num_outputs = {len(self.__outputs)}, "
                f"num_validators = {len(self.__validators)})")
