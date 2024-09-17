"""
pipe_node.py

This module defines the `PipeNode` class, which is a fundamental component for building and managing
data processing pipelines.

A `PipeNode` represents a node in a directed acyclic graph (DAG) that performs an operation on its parent nodes.
The `PipeNode` class supports deferred execution, where data processing operations are only executed when
explicitly called. It allows for building complex data processing workflows in a modular and flexible manner.

Classes:
    PipeNode: A node in a pipeline that can execute a function based on the values of its parent nodes.

Usage Example:

>>> from dl_data_pipeline import PipeNode
>>> def add(x, y):
>>>     return x + y

>>> # Create nodes
>>> node1 = PipeNode(name="input1")
>>> node2 = PipeNode(name="input2")
>>> node3 = PipeNode(func=add, parent=[node1, node2], name="sum")

>>> # Set values for input nodes
>>> node1._set_value(3)
>>> node2._set_value(4)

>>> # Execute the node with the function
>>> node3.execute()

>>> # Get the result
>>> result = node3.value  # result should be 7
"""


from __future__ import annotations
from functools import wraps
from collections.abc import Callable
from typing import Any

class PipeNode:
    """
    A class representing a node in a data processing pipeline.

    The `PipeNode` class is used to build directed acyclic graphs (DAGs) where each node can execute a function
    based on the values of its parent nodes. This allows for deferred execution of data processing steps, enabling
    the construction of complex and modular data pipelines.

    Args:
        func (Callable, optional): A function that takes the values from the parent nodes as inputs and returns
            the computed result. Defaults to None.
        parent (list[PipeNode], optional): A list of parent `PipeNode` objects whose values are used as inputs
            to the function. Defaults to None.
        name (str | None, optional): An optional name for the node. Defaults to None.
    """
    def __init__(self,
                 func: Callable = None,
                 parent: list[PipeNode] | None = None,
                 name: str | None = None,
                 ) -> None:
        self.__parent: list[PipeNode] = parent if parent is not None else []
        self.__name = name
        self.__func = func
        self.__value = None

    @property
    def value(self) -> Any:
        """Current value of the node.

        Returns:
            Any: value of the node.
        """
        return self.__value

    @property
    def parent(self) -> list[PipeNode]:
        """Parents of the node

        Returns:
            list[PipeNode]: a list of the parents of this node.
        """
        return self.__parent

    def __repr__(self) -> str:
        value = f"PipelineNode object <name : {self.__name}, parent number : {len(self.parent)}"
        if self.__func is not None:
            value += f", function : {self.__func.__name__}"
        value += ">"
        return value

    def execute(self) -> None:
        """Excecute the function stored in the node with 
        parent values as argument.
        """
        if len(self.__parent) != 0 and self.__func is not None:
            # get all value of previous parent
            data_list = [child.value for child in self.__parent]

            # perform operation
            self.__value = self.__func(*data_list)

    def _set_value(self, value: Any) -> None:
        """Set the value of the current node.

        Args:
            value (Any): value to be stored in the node.
        """
        self.__value = value
