import numpy as np

from ..deferred import deferred_execution

@deferred_execution
def rescale(data: np.ndarray, min_value: float = 0.0, max_value: float = 1.0) -> np.ndarray:
    """
    Rescales the input data array to a specified range [min_value, max_value].

    This function takes a NumPy array and rescales its values to fit within the specified
    minimum and maximum values. The rescaling is done by first shifting the data so that
    the minimum value becomes zero, then scaling it to the target range, and finally
    shifting it to start from the specified minimum value.

    Args:
        data (np.ndarray): The input data array to be rescaled.
        min_value (float, optional): The minimum value of the target range. Defaults to 0.0.
        max_value (float, optional): The maximum value of the target range. Defaults to 1.0.

    Returns:
        np.ndarray: The rescaled data array, with values in the range [min_value, max_value].

    Raises:
        ValueError: If data contains constant values (e.g., all elements are the same),
                    which would lead to division by zero during rescaling.

    Examples:
        >>> import numpy as np
        >>> data = np.array([10, 20, 30, 40, 50])
        >>> rescaled_data = rescale(data, min_value=-1, max_value=1)
        >>> print(rescaled_data)
        [-1.  -0.5  0.   0.5  1. ]
    """
    # calculate ranges
    data_min = np.min(data)
    data_max = np.max(data)
    data_range = data_max - data_min
    target_range = max_value - min_value

    # throw error (anyway it would throw /0 err later)
    if data_range == 0:
        raise ValueError("Data range is zero, cannot rescale a constant array.")

    # Translate data to start from 0
    data = data - data_min

    # Scale data to the target range
    data = data * (target_range / data_range)

    # Translate data to start from min_value
    data = data + min_value

    return data