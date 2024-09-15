from typing import Tuple, Callable
import math

import numpy as np

import numpy as np
from typing import Tuple

def padding_2d(data: np.ndarray, target_shape: Tuple[int, int], fill_value: float = 1.0) -> np.ndarray:
    """
    Pads a 2D (or 3D) array to the target shape with the specified fill value.

    Args:
        data (np.ndarray): The input 2D (or 3D) array representing an image.
        target_shape (tuple): The desired shape of the output array (height, width).
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
    if len(shape) not in [2, 3]:
        raise ValueError("Input data must be 2D or 3D array")

    # Determine the final shape
    if len(shape) == 3:  # Case of a 3D image
        target_shape = (*target_shape, shape[2])

    # Ensure input data is smaller than target shape
    if any(s > t for s, t in zip(shape, target_shape)):
        raise ValueError("Data shape must be smaller than target shape to add padding")

    # Create an array with the fill value
    padded_data = np.full(target_shape, fill_value, dtype=data.dtype)

    # Find padding lengths (for centering)
    l_pad = (target_shape[0] - shape[0]) // 2
    t_pad = (target_shape[1] - shape[1]) // 2

    # Fill the array with the original image, centering it
    if len(shape) == 2:
        padded_data[l_pad:l_pad+shape[0], t_pad:t_pad+shape[1]] = data
    else:
        padded_data[l_pad:l_pad+shape[0], t_pad:t_pad+shape[1], :] = data

    return padded_data


def resize_with_max_distortion(data: np.ndarray, 
           target_shape: Tuple[float, float], 
           max_stretch_distortion: float, 
           fill_value: float | int = 1.0,
           resize_function: Callable[[np.ndarray, tuple], np.ndarray] | None = None
           ) -> np.ndarray:
    """
    Resizes the input 2D or 3D array (image) to the target shape with a constraint on maximum allowable distortion.

    This function resizes an image (or any 2D/3D array) to a specified target shape while controlling the amount 
    of distortion (change in aspect ratio) allowed during the resizing process. If the distortion exceeds the 
    specified `max_stretch_distortion`, the function adjusts the stretch ratios accordingly to minimize distortion.
    After resizing, the image may be padded with the specified `fill_value` to ensure the final output matches the 
    target shape exactly.

    Args:
        data (np.ndarray): The input 2D or 3D array to be resized. Typically, this represents an image.
        target_shape (Tuple[float, float]): The desired target shape (height, width) for the output array.
        max_stretch_distortion (float): The maximum allowable difference between the horizontal and vertical 
                                        stretch ratios. This controls how much the aspect ratio can change during 
                                        resizing.
        fill_value (float, optional): The value used for padding the image if the resized image does not perfectly 
                                      match the target shape. Defaults to 1.0.
        resize_function (Callable[[np.ndarray, tuple], np.ndarray], optional): A custom function to handle resizing. 
                                                                              If None, a simple default method will 
                                                                              be used. Defaults to None.

    Returns:
        np.ndarray: The resized and possibly padded array with the specified target shape.

    Raises:
        ValueError: If the input data shape is larger than the target shape.
                    If the input data is not a 2D or 3D array.
    """
    # Assert data is an array representing an image
    if not (len(data.shape) == 2 or len(data.shape) == 3):
        raise ValueError("Input data must be 2D or 3D array")

    # get shapes
    target_height, target_width = target_shape
    height, width, *_ = data.shape    

    # calculate distortion for current values
    hratio = target_height / height
    wratio =  target_width / width

    # Calculate the distortion
    distortion = abs(hratio - wratio)

    # Ensure the distortion is within the allowed limit
    if distortion > max_stretch_distortion:
        # Adjust both ratios proportionally to reduce distortion
        if hratio < wratio:
            wratio = hratio + min(max_stretch_distortion, wratio - hratio)
        else:
            hratio = wratio + min(max_stretch_distortion, hratio - wratio)
    
    # Calculate new dimensions
    new_height = math.floor(height * hratio)
    new_width = math.floor(width * wratio)

    # Resize the image
    if resize_function is None:
        resized_image = np.resize(data, (new_height, new_width))
    else:
        resized_image = resize_function(data, (new_height, new_width))

    # padd the image if needed to fit the target shape
    if (new_height, new_width) != (target_height, target_width):
        padded_image = padding_2d(resized_image, target_shape, fill_value)
        return padded_image
    else:
        return resized_image