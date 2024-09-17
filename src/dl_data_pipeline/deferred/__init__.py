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