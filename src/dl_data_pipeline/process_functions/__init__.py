"""
This module provides a collection of basic preprocessing functions, organized into three submodules.

The functions in this module are commonly used in data processing workflows, particularly in the contexts of
machine learning, data analysis, and image processing. These preprocessing steps are crucial for preparing data
before it is fed into models or further analyzed.

Submodules:
    any_process:
        Contains general-purpose preprocessing functions that can be applied to a variety of data types.

    process_1d:
        Focuses on preprocessing functions specifically designed for one-dimensional data, such as time series or
        signal data. The excepted shape for those data is (input_dim, channel_number).

    process_2d:
        Specializes in preprocessing functions for two-dimensional data, primarily images, including resizing, 
        padding, and cropping operations. The excepted shape for those data is (input_dim1, input_dim2, channel_number).

These submodules provide a comprehensive set of tools for handling different types of data, ensuring that they are
in the optimal format and condition for downstream tasks.
"""



from .any_process import rescale
from .process_1d import rpad_rcut
from .process_2d import (
    resize_with_max_distortion, 
    open_rgb_image,
    image_chw_to_hwc, image_hwc_to_chw)