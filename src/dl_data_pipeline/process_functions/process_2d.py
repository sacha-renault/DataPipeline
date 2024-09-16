from typing import Tuple

import cv2
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
           max_ratio_distortion: float, 
           fill_value: float | int = 1.0,
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
        max_ratio_distortion (float): The maximum allowable difference between the horizontal and vertical 
                                        stretch ratios. This controls how much the aspect ratio can change during 
                                        resizing. 0 as max distortion ensure aspect ratio is kept
        fill_value (float, optional): The value used for padding the image if the resized image does not perfectly 
                                      match the target shape. Defaults to 1.0.

    Returns:
        np.ndarray: The resized and possibly padded array with the specified target shape.

    Raises:
        ValueError: If the input data shape is larger than the target shape.
                    If the input data is not a 2D or 3D array.
    """
    # test valid range for dim
    if len(data.shape) not in [2, 3]:
        raise ValueError("Input data is not a 2D or 3D array")

    # Get original dimensions
    height, width = data.shape[:2]
    target_height, target_width = target_shape

    # Calculate aspect ratios
    original_aspect_ratio = width / height
    target_aspect_ratio = target_width / target_height

    # Calculate allowable aspect ratio range
    allowed_aspect_ratio_min = original_aspect_ratio * (1 - max_ratio_distortion)
    allowed_aspect_ratio_max = original_aspect_ratio * (1 + max_ratio_distortion)

    # Adjust target aspect ratio to be within allowable range
    adjusted_aspect_ratio = min(max(target_aspect_ratio, allowed_aspect_ratio_min), allowed_aspect_ratio_max)

    # Determine new dimensions based on adjusted aspect ratio
    if adjusted_aspect_ratio > original_aspect_ratio:
        # Adjust width based on adjusted aspect ratio
        new_height = min(target_height, height * (1 + max_ratio_distortion))
        new_width = int(new_height * adjusted_aspect_ratio)

    else:
        # Adjust height based on adjusted aspect ratio
        new_width = min(target_width, width * (1 + max_ratio_distortion))
        new_height = int(new_width / adjusted_aspect_ratio)
        if new_height > target_height:
            new_height = target_height
            new_width = int(new_height * adjusted_aspect_ratio)

    # Ensure new dimensions are integers
    new_height = int(new_height)
    new_width = int(new_width)

    # Resize the image
    resized_image = cv2.resize(data, (new_width, new_height))

    # Pad the image to target dimensions
    padded_image = padding_2d(resized_image, (target_height, target_width), fill_value)
    return padded_image

def open_rgb_image(path: str) -> np.ndarray:
    """Open an image using cv2 and convert back to RGB.

    Args:
        path (str): path of the image

    Returns:
        np.ndarray: array representing the image
    """
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_array = np.array(img_rgb)
    return img_array

def image_to_channel_num(image: np.ndarray, 
                         channel_number_target: int = 3, 
                         fill_value: float | int = 0.0) -> np.ndarray:
    """
    Convert an image to the specified number of channels.

    Args:
        image (np.ndarray): Input image array, which can be grayscale (2D), 
                            single-channel (3D), or multi-channel (3D).
        channel_number_target (int, optional): Target number of channels. Defaults to 3.
        fill_value (float | int, optional): Value used to fill new channels if needed. Defaults to 1.0.

    Returns:
        np.ndarray: Image array with the specified number of channels.
    """
    # if image is BW
    if len(image.shape) == 2:
        image_3d = np.repeat(image[:,:, np.newaxis], channel_number_target, -1)
    
    # if image is a BW 3d with single channel
    elif len(image.shape) == 3 and image.shape[2] == 1:
        image_3d = np.repeat(image, channel_number_target, -1)
    
    # If the image has fewer channels than the target
    elif len(image.shape) == 3 and image.shape[2] < channel_number_target:
        image_3d = np.full((*image.shape[:2], channel_number_target), fill_value, dtype=image.dtype)
        image_3d[:,:,:image.shape[2]] = image
    
    # image has more channels than the target => truncate 
    else:
        image_3d = image[:,:,:channel_number_target]

    return image_3d

def image_hwc_to_chw(data: np.ndarray) -> np.ndarray:
    """
    Converts an image from HWC (Height-Width-Channel) format to CHW (Channel-Height-Width) format.

    Args:
        data (np.ndarray): The input image array in HWC format. 
                           The shape should be (height, width, channels).

    Returns:
        np.ndarray: The image array in CHW format.
                    The shape will be (channels, height, width).
    """
    if len(data.shape) != 3:
        raise ValueError("input data must be dim 3")
    return np.transpose(data, [2, 0, 1])

def image_chw_to_hwc(data: np.ndarray) -> np.ndarray:
    """
    Converts an image from CHW (Channel-Height-Width) format to HWC (Height-Width-Channel) format.

    Args:
        data (np.ndarray): The input image array in CHW format. 
                           The shape should be (channels, height, width).

    Returns:
        np.ndarray: The image array in HWC format.
                    The shape will be (height, width, channels).
    """
    if len(data.shape) != 3:
        raise ValueError("input data must be dim 3")
    return np.transpose(data, [1, 2, 0])
