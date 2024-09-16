from functools import wraps

DATA_PLACEHOLDER = object()
""" An object to be put instead of data before pipeline is called.
"""

def deffered_execution(func):
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
        if len(args) == 0:
            raise ValueError(f"cannot differe execution of with 0 argument")
        elif args[0] is not DATA_PLACEHOLDER and args[0] is not None:
            raise ValueError(f"args[0] must be either DATA_PLACEHOLDER or None, not : {args[0]}")
        
        # Remove the placeholder and prepare the deferred function
        args_no_data = args[1:]
        deferred_func = lambda data: func(data, *args_no_data, **kwargs)
        deferred_func.__name__ = func.__name__
        return deferred_func
    return wrapper
            