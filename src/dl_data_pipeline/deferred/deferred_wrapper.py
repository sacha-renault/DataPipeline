from functools import wraps
from contextlib import contextmanager
from ..pipeline.pipe_node import PipelineNode

_DEFERRED_EXECUTION_MODE = True

@contextmanager
def instant_excecution() -> None: # type: ignore
    """
    Context manager to temporarily disable deferred execution and execute functions immediately.

    This context manager allows the user to execute functions immediately even when they
    are decorated with `@deferred_function`, bypassing the default deferred execution mode.

    Upon entering the context (`with instant_execution():`), deferred execution is disabled.
    Once the block is exited, deferred execution is restored to its previous state, even if
    an exception occurs within the block.

    Note:
        This context manager ensures that deferred execution is always restored after the
        *with* block, even if an exception is raised.

    Example usage:

    >>> @deferred_function
    >>> def add(a, b):
    >>>     return a + b

    >>> # Deferred execution mode (default)
    >>> result_node = add(PipelineNode(), 5)

    >>> # Instant execution mode (within context)
    >>> with instant_execution():
    >>>     result = add(3, 5)
    >>>     # Executes immediately and returns 8
    """
    global _DEFERRED_EXECUTION_MODE
    _DEFERRED_EXECUTION_MODE = False
    try:
        yield  # Execute the block
    finally:
        _DEFERRED_EXECUTION_MODE = True  # Restore previous mode

def _create_pipeline_node(func, *args, **kwargs) -> PipelineNode:
    # Split args into Node / Non Node
    args_no_data = []
    parents = []

    for arg in args:
        if isinstance(arg, PipelineNode):
            parents.append(arg)
        else:
            args_no_data.append(arg)

    # ensure there is at least ONE PipeNode
    if len(parents) == 0:
        raise TypeError("Found no argument with type PipelineNode as positional argument"
                        "If you write a pipeline function, test it without `deferred_execution`"
                        "decorator") # TODO change to an other exception

    # kw_no_data = {k: v for k, v in kwargs.items() if not isinstance(v, PipeNode)}
    deferred_func = lambda *data: func(*data, *args_no_data, **kwargs)
    deferred_func.__name__ = func.__name__
    return PipelineNode(deferred_func, parents)

def deferred_execution(func):
    """
    A decorator that defers the execution of a function until the actual data is provided.

    The first argument of the function must be either DATA_PLACEHOLDER or None, indicating
    that the function execution should be deferred. When the function is eventually called
    with the actual data, the deferred execution is triggered.

    Args:
        func (callable): The function to be deferred.

    Returns:
        callable: A lambda function that takes the data as its first argument and executes
                  the original function with the deferred arguments.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check if execute_now in kwargs
        if _DEFERRED_EXECUTION_MODE:
            return _create_pipeline_node(func, *args, **kwargs)
        # check if any PipelineNode in args, else error
        elif any([isinstance(arg, PipelineNode) for arg in args]):
            raise TypeError(f"function `{func.__name__}` received PipelineNode argument"
                            "in a context where execution is non deferred"
                            "It's probably in incorrect usage of `with instant_excecution()`.")
        else:
            return func(*args, **kwargs)

    return wrapper
