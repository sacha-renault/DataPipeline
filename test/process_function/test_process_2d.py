import pytest
import numpy as np

from src.dl_data_pipeline.process_functions import process_2d

def test_padding_2d_rgb():
    original_image = np.random.rand(256,256, 3)
    padded = process_2d.padding_2d(original_image, (512, 512), 0)
    assert np.array_equal(original_image, padded[128:384,128:384,:]), "RGB padding test failed."
    assert padded.dtype == original_image.dtype

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