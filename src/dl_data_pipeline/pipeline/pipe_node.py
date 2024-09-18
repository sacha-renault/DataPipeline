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
from collections.abc import Callable, Generator
from typing import Any

class PipelineNode:
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
                 parent: list[PipelineNode] | None = None,
                 name: str | None = None,
                 ) -> None:
        self.__parent: list[PipelineNode] = parent if parent is not None else []
        self.__name = name
        self.__func = func
        self.__value = None
        self.__n_iter = None

    @property
    def value(self) -> Any:
        """Current value of the node.

        Returns:
            Any: value of the node.
        """
        return self.__value

    @property
    def parent(self) -> list[PipelineNode]:
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
    
    def __getitem__(self, key : int | str | Any) -> PipelineNode:
        """Access an item in a subscriptable value of the node.

        This method creates a new `PipelineNode` that represents 
        the key-th or key-named item from the current node's value 
        if the value is subscriptable (supports indexing). If the 
        value is not subscriptable, a `TypeError` is raised.

        Args:
            key (int | str | Any): The key to access the item from the subscriptable value. 
                             Can be an integer (for index-based access) or a string (for key-based access).

        Raises:
            TypeError: If the node's value is not subscriptable.

        Returns:
            PipelineNode: A new node representing the accessed item from the subscriptable object.

        Example:\n
        >>> # create a node
        >>> node = PipeNode()

        >>> # execute a function on the node that could result in a subscriptable object
        >>> # for example, a function that reads some columns from a CSV row and returns 
        >>> # an iterable of values
        >>> x = read_cols_in_csv(node, "name", "path")
        
        >>> # get the results in separate nodes
        >>> name = x[0]  # node representing the 'name'
        >>> path = x[1]  # node representing the 'path'
        """      
        # define the lambda
        def get_item(*_):
            if hasattr(self.value, '__getitem__'):
                return self.value[key]
            else:
                raise TypeError(f"value of this node of type {type(self.value)} "
                                "cannot be accessed with [] "
                                "ensure graph construction is made properly")
        
        # make it named like the __get_item__ function
        get_item.__name__ = "__getitem__"
        
        # create a Functional Node that will dynamically get the keyth result
        # in the parent Node
        return PipelineNode(get_item, parent=[self], name = "__getitem__")
            

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

    def __iter__(self) -> Generator[PipelineNode, None, None]:
        if self.__n_iter is None:
            raise RuntimeError("Must call `unwrap` method before iterating")

        for i in range(self.__n_iter):
            yield self[i]

    def unwrap(self, num: int) -> PipelineNode:
        """Prepare the node for iteration with a specified number of outputs.

        This method sets the number of iterations (`num`) that the node should 
        be unwrapped into. It allows the node to be used in a context where 
        multiple outputs are expected, like tuple unpacking.

        Args:
            num (int): The number of outputs expected from the node.

        Returns:
            PipelineNode: The node itself, ready to be iterated over the specified 
                        number of outputs.

        Example:

        >>> # Define a function that returns a subscriptable object (e.g., a tuple)
        >>> @deferred_execution
        >>> def min_max(v1, v2):
        >>>     return np.min(v1), np.max(v2)

        >>> # Define the pipeline
        >>> input_node = InputNode(name="1")
        >>> x = ...  # Add some processing functions here ...
        >>> min_node, max_node = min_max(x).unwrap(2)
        >>> pipeline = Pipeline(inputs=[input_node], outputs=[min_node, max_node])

        >>> # Unwrap allows you to get multiple nodes from a single node when the value 
        >>> # is a subscriptable object, like a tuple.
        >>> min_value, max_value = pipeline(data)  # 'data' must be defined with the expected input.
        """
        self.__n_iter = num
        return self
