import numpy as np

def padding_2d(data: np.ndarray, target_shape: tuple, fill_value: float = 1.0) -> np.ndarray:
    """
    Pads a 2D (or 3D) array to the target shape with the specified fill value.

    Args:
        data (np.ndarray): The input 2D (or 3D) array representing an image.
        target_shape (tuple): The desired shape of the output array.
        fill_value (float, optional): The value used for padding. Defaults to 1.0.

    Returns:
        np.ndarray: The padded array with the target shape.

    Raises:
        ValueError: If the input data shape is larger than the target shape.
                    If the input data is not a 2D or 3D array.
    """
    # Get data shape
    shape = data.shape

    # Assert data is an array representing an image
    if not (len(shape) == 2 or len(shape) == 3):
        raise ValueError("Input data must be 2D or 3D array")

    # Find final shape depending on 2D or 3D array
    if len(shape) == 3:  # Case of a non-BW image
        target_shape = (*target_shape, shape[2])  # Add number of channels in the final shape

    # Ensure input data is smaller than target shape
    if any(s > t for s, t in zip(shape, target_shape)):
        raise ValueError("Data shape must be smaller than target shape to add padding")

    # Create an array with fill value
    padded_data = np.full(target_shape, fill_value)

    # Find padding lengths (for centering)
    l_pad = (target_shape[0] - shape[0]) // 2
    t_pad = (target_shape[1] - shape[1]) // 2

    # Fill the array with the original image, centering it
    padded_data[l_pad:l_pad+shape[0], t_pad:t_pad+shape[1]] = data

    return padded_data
