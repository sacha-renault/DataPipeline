from typing import Tuple

import pytest
import numpy as np

from src.dl_data_pipeline.process_functions import process_2d

def test_padding_2d_rgb():
    original_image = np.random.rand(256,256, 3)
    padded = process_2d.padding_2d(original_image, (512, 512), 0)
    assert np.array_equal(original_image, padded[128:384,128:384,:]), "RGB padding test failed."
    assert padded.dtype == original_image.dtype

def test_padding_2d_error_not_accepted_dim():
    original_image = np.random.rand(256)
    with pytest.raises(ValueError):
        padded = process_2d.padding_2d(original_image, (512, 512), 0)
    original_image = np.random.rand(2,2,2,2)
    with pytest.raises(ValueError):
        padded = process_2d.padding_2d(original_image, (512, 512), 0)

def test_padding_2d_error_too_big():
    original_image = np.random.rand(256, 256)
    with pytest.raises(ValueError):
        padded = process_2d.padding_2d(original_image, (128, 128), 0)

def test_padding_2d_bw():
    original_image = np.random.rand(256,256)
    padded = process_2d.padding_2d(original_image, (512, 512), 1.0)
    assert np.array_equal(original_image, padded[128:384,128:384]), "BW padding test failed."
    assert padded.dtype == original_image.dtype

def test_image_to_channel_num_2d():
    original_image = np.random.rand(256,256)
    extended = process_2d.image_to_channel_num(original_image, 1)
    assert np.array_equal(extended, original_image[:,:, np.newaxis])
    assert extended.dtype == original_image.dtype

def test_image_to_channel_num_3d1():
    original_image = np.random.rand(256,256, 1)
    extended = process_2d.image_to_channel_num(original_image, 4)
    assert np.array_equal(extended, np.repeat(original_image, 4, -1))
    assert extended.dtype == original_image.dtype

def test_image_to_channel_num_3d2():
    original_image = np.random.rand(256,256, 3)
    extended = process_2d.image_to_channel_num(original_image, 5)
    assert np.array_equal(extended[:,:,:3], original_image)
    assert np.array_equal(extended[:,:,3:], np.zeros((256,256,2)))
    assert extended.dtype == original_image.dtype

def test_image_to_channel_num_3d3():
    original_image = np.random.rand(256,256, 5)
    truncated = process_2d.image_to_channel_num(original_image, 3)
    assert np.array_equal(truncated, original_image[:,:,:3])
    assert truncated.dtype == original_image.dtype


def test_resize_with_max_distortion_no_distortion():
    data = np.random.rand(256, 128, 3)
    target_shape = (512, 256)
    max_ratio_distortion = 0.0

    resized_image = process_2d.resize_with_max_distortion(data, target_shape, max_ratio_distortion)
    
    # Aspect ratio should be preserved
    assert resized_image.shape == (512, 256, 3)

def test_resize_with_max_distortion_with_distortion():
    data = np.random.rand(256, 256, 3)
    target_shape = (512, 256)
    max_ratio_distortion = 0.2

    resized_image = process_2d.resize_with_max_distortion(data, target_shape, max_ratio_distortion)
    
    # With distortion, the image may not preserve the exact aspect ratio but should still fit within the target shape
    assert resized_image.shape == (512, 256, 3)

def test_resize_with_max_distortion_padding():
    data = np.random.rand(256, 256, 3)
    target_shape = (512, 512)
    max_ratio_distortion = 0.0
    fill_value = 0.5

    resized_image = process_2d.resize_with_max_distortion(data, target_shape, max_ratio_distortion, fill_value)
    assert resized_image.shape == (512, 512, 3)
    assert np.all(resized_image[:128, :, :] == fill_value)      # Top padding
    assert np.all(resized_image[-128:, :, :] == fill_value)     # Bottom padding
    assert np.all(resized_image[:, :128, :] == fill_value)      # Left padding
    assert np.all(resized_image[:, -128:, :] == fill_value)     # Right padding

def test_resize_with_max_distortion_invalid_input_shape():
    data = np.random.rand(256, 256, 256, 3)  # Invalid shape (4D)
    target_shape = (512, 512)
    max_ratio_distortion = 0.0

    with pytest.raises(ValueError, match=r"Input data is not a 2D or 3D array"):
        process_2d.resize_with_max_distortion(data, target_shape, max_ratio_distortion)

def test_resize_with_max_distortion_non_image():
    data = np.random.rand(256, 256)
    target_shape = (512, 512)
    max_ratio_distortion = 10
    resized_image = process_2d.resize_with_max_distortion(data, target_shape, max_ratio_distortion)
    assert resized_image.shape == (512, 512)

def test_resize_with_max_distortion_adjust_width_then_height():
    data = np.random.rand(125, 100, 3)  # Original aspect ratio = 2.0
    target_shape = (100, 100)  # Target aspect ratio = 1.0
    max_ratio_distortion = 5

    resized_image = process_2d.resize_with_max_distortion(data, target_shape, max_ratio_distortion)
    assert resized_image.shape == (*target_shape, 3)

    
def test_resize_with_max_distortion_adjust_height_then_width():
    data = np.random.rand(200, 100, 3)  # Original aspect ratio = 2.0
    target_shape = (150, 150)  # Target aspect ratio = 1.0
    max_ratio_distortion = 0

    resized_image = process_2d.resize_with_max_distortion(data, target_shape, max_ratio_distortion)
    assert resized_image.shape == (*target_shape, 3) 