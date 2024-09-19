"""
This module provides the `deferred_execution` decorator, which is used to defer the execution
of functions until the necessary data is provided.

The `deferred_execution` decorator is particularly useful in scenarios where function execution
needs to be delayed and performed as part of a data processing pipeline or computation graph.
It wraps a function so that its execution is postponed until it receives data via `PipeNode`
objects, enabling flexible and modular data processing workflows.

Functions:
    deferred_execution(func): A decorator that defers the execution of a function until the
                              actual data is provided.

Usage Example:

    >>> from dl_data_pipeline.deferred_execution import deferred_execution
    >>> from dl_data_pipeline import PipeNode

    >>> @deferred_execution
    >>> def add(x, y):
    >>>     return x + y

    >>> input_node1 = PipeNode()
    >>> input_node2 = PipeNode()

    >>> add_node = add(input_node1, input_node2)

    >>> input_node1._set_value(5)
    >>> input_node2._set_value(3)

    >>> add_node.execute()
    >>> result = add_node.value  # result will be 8
"""


from .deferred_wrapper import deferred_execution, instant_excecution
