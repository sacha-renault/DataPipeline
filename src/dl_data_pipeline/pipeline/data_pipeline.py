from collections.abc import Callable
from typing import List, Any, Tuple, Dict
from .pipe_node import PipeNode

from ..validator import Validator

class Pipeline:
    """
    A class to manage a sequence of forward and backward processes with optional validation.

    The `Pipeline` class allows for adding functions to process data in a forward and backward manner.
    Each process can have associated arguments, keyword arguments, and validators to ensure the processed
    data meets certain criteria.

    Methods:
        add_forward_process(func, *args, **kwargs): Adds a function to the forward process list.
        add_forward_validator(validator): Adds a validator to the forward validators list.
        add_backward_process(func, *args, **kwargs): Adds a function to the backward process list.
        add_backward_validator(validator): Adds a validator to the backward validators list.
        forward(data): Processes the data through the forward functions and validators.
        backward(data): Processes the data through the backward functions and validators.
    """
    def __init__(self, inputs: PipeNode | list[PipeNode], outputs: PipeNode | list[PipeNode]) -> None:
        if not (isinstance(inputs, PipeNode) or (isinstance(inputs, list) and all(isinstance(x, PipeNode) for x in inputs))):
            raise ValueError("inputs must be a PipeNode or a list of PipeNode")

        if not (isinstance(outputs, PipeNode) or (isinstance(outputs, list) and all(isinstance(x, PipeNode) for x in outputs))):
            raise ValueError("outputs must be a PipeNode or a list of PipeNode")

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
