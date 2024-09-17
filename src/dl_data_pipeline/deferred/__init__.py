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




from .deferred_wrapper import deferred_execution

def use_deferred_execution():
    import inspect
    from ..process_functions import (any_process, process_1d, process_2d)

    def _defers_execution_on_package(module):
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if not getattr(func, "is_deferred", False):
                wrapped_func = deferred_execution(func)
                setattr(wrapped_func, "is_deferred", True)
                setattr(module, name, wrapped_func)

    _defers_execution_on_package(any_process)
    _defers_execution_on_package(process_1d)
    _defers_execution_on_package(process_2d)