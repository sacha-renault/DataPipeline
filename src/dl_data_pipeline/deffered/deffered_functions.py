from typing import Tuple

import numpy as np

from ..process_functions.any_process import rescale
from ..process_functions.process_1d import (
    rpad_rcut, lpad_lcut, center_pad_rcut
)
from ..process_functions.process_2d import (
    padding_2d,
    resize_with_max_distortion,
    open_rgb_image,
    image_to_channel_num,
    image_hwc_to_chw,
    image_chw_to_hwc
)
from . import deffered_execution

@deffered_execution
def deffered_rescale(data: np.ndarray, min_value: float = 0, max_value: float = 1):
    return rescale(data, min_value, max_value)

@deffered_execution
def deffered_rpad_rcut(data: np.ndarray, desired_audio_length: int):
    return rpad_rcut(data, desired_audio_length)

@deffered_execution
def deffered_lpad_lcut(data: np.ndarray, desired_audio_length: int):
    return lpad_lcut(data, desired_audio_length)

@deffered_execution
def deffered_center_pad_rcut(data: np.ndarray, desired_audio_length: int):
    return center_pad_rcut(data, desired_audio_length)

@deffered_execution
def deffered_padding_2d(data: np.ndarray, target_shape: Tuple[int, int], fill_value: float = 1):
    return padding_2d(data, target_shape, fill_value)

@deffered_execution
def deffered_resize_with_max_distortion(data: np.ndarray, 
                                        target_shape: Tuple[int, int], 
                                        max_ratio_distortion: float,
                                        fill_value: float = 1):
    return resize_with_max_distortion(data, target_shape, max_ratio_distortion, fill_value)

@deffered_execution
def deffered_resize_with_max_distortion(data: np.ndarray, 
                                        target_shape: Tuple[int, int], 
                                        max_ratio_distortion: float,
                                        fill_value: float = 1):
    return resize_with_max_distortion(data, target_shape, max_ratio_distortion, fill_value)

@deffered_execution
def deffered_open_rgb_image(path: str):
    return open_rgb_image(path)

@deffered_execution
def deffered_image_to_channel_num(image: np.ndarray, 
                                  channel_number_target: int = 3, 
                                  fill_value: float | int = 0):
    return image_to_channel_num(image, channel_number_target, fill_value)

@deffered_execution
def deffered_image_hwc_to_chw(data: np.ndarray):
    return image_hwc_to_chw(data)

@deffered_execution
def deffered_image_chw_to_hwc(data: np.ndarray):
    return image_chw_to_hwc(data)

# Dynamically construct __all__
__all__ = [name for name, obj in globals().items() if callable(obj) and name.startswith("deferred_")]