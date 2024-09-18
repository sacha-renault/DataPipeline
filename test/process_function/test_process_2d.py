from typing import Tuple
from unittest.mock import patch

import pytest
import numpy as np
import cv2

from src.dl_data_pipeline.process_functions import process_2d
from src.dl_data_pipeline.pipeline.pipe_node import PipelineNode

def test_padding_2d_rgb():
    original_image = np.random.rand(256, 256, 3)
    node = PipelineNode()
    node._set_value(original_image)
    padded_node = process_2d.padding_2d(node, (512, 512), 0)
    padded_node.execute()
    padded = padded_node.value
    assert np.array_equal(original_image, padded[128:384, 128:384, :]), "RGB padding test failed."
    assert padded.dtype == original_image.dtype

def test_padding_2d_error_not_accepted_dim():
    original_image = np.random.rand(256)
    node = PipelineNode()
    node._set_value(original_image)
    with pytest.raises(ValueError):
        padded_node = process_2d.padding_2d(node, (512, 512), 0)
        padded_node.execute()

    original_image = np.random.rand(2, 2, 2, 2)
    node._set_value(original_image)
    with pytest.raises(ValueError):
        padded_node = process_2d.padding_2d(node, (512, 512), 0)
        padded_node.execute()

def test_padding_2d_error_too_big():
    original_image = np.random.rand(256, 256)
    node = PipelineNode()
    node._set_value(original_image)
    with pytest.raises(ValueError):
        padded_node = process_2d.padding_2d(node, (128, 128), 0)
        padded_node.execute()

def test_padding_2d_bw():
    original_image = np.random.rand(256, 256)
    node = PipelineNode()
    node._set_value(original_image)
    padded_node = process_2d.padding_2d(node, (512, 512), 1.0)
    padded_node.execute()
    padded = padded_node.value
    assert np.array_equal(original_image, padded[128:384, 128:384]), "BW padding test failed."
    assert padded.dtype == original_image.dtype

def test_image_to_channel_num_2d():
    original_image = np.random.rand(256, 256)
    node = PipelineNode()
    node._set_value(original_image)
    extended_node = process_2d.image_to_channel_num(node, 1)
    extended_node.execute()
    extended = extended_node.value
    assert np.array_equal(extended, original_image[:, :, np.newaxis])
    assert extended.dtype == original_image.dtype

def test_image_to_channel_num_3d1():
    original_image = np.random.rand(256, 256, 1)
    node = PipelineNode()
    node._set_value(original_image)
    extended_node = process_2d.image_to_channel_num(node, 4)
    extended_node.execute()
    extended = extended_node.value
    assert np.array_equal(extended, np.repeat(original_image, 4, -1))
    assert extended.dtype == original_image.dtype

def test_image_to_channel_num_3d2():
    original_image = np.random.rand(256, 256, 3)
    node = PipelineNode()
    node._set_value(original_image)
    extended_node = process_2d.image_to_channel_num(node, 5)
    extended_node.execute()
    extended = extended_node.value
    assert np.array_equal(extended[:, :, :3], original_image)
    assert np.array_equal(extended[:, :, 3:], np.zeros((256, 256, 2)))
    assert extended.dtype == original_image.dtype

def test_image_to_channel_num_3d3():
    original_image = np.random.rand(256, 256, 5)
    node = PipelineNode()
    node._set_value(original_image)
    truncated_node = process_2d.image_to_channel_num(node, 3)
    truncated_node.execute()
    truncated = truncated_node.value
    assert np.array_equal(truncated, original_image[:, :, :3])
    assert truncated.dtype == original_image.dtype

def test_resize_with_max_distortion_no_distortion():
    data = np.random.rand(256, 128, 3)
    node = PipelineNode()
    node._set_value(data)
    resized_node = process_2d.resize_with_max_distortion(node, (512, 256), 100.0)
    resized_node.execute()
    resized_image = resized_node.value
    assert resized_image.shape == (512, 256, 3)

def test_resize_with_max_distortion_with_distortion():
    data = np.random.rand(256, 256, 3)
    node = PipelineNode()
    node._set_value(data)
    resized_node = process_2d.resize_with_max_distortion(node, (512, 256), 100.0)
    resized_node.execute()
    resized_image = resized_node.value
    assert resized_image.shape == (512, 256, 3)

def test_resize_with_max_distortion_invalid_input_shape():
    data = np.random.rand(256, 256, 256, 3)  # Invalid shape
    node = PipelineNode()
    node._set_value(data)
    with pytest.raises(ValueError, match=r"Input data is not a 2D or 3D array"):
        resized_node = process_2d.resize_with_max_distortion(node, (512, 512), 0.0)
        resized_node.execute()

def test_resize_with_max_distortion_non_image():
    data = np.random.rand(256, 256)
    node = PipelineNode()
    node._set_value(data)
    resized_node = process_2d.resize_with_max_distortion(node, (512, 512), 10)
    resized_node.execute()
    resized_image = resized_node.value
    assert resized_image.shape == (512, 512)

def test_resize_with_max_distortion_adjust_width_then_height():
    data = np.random.rand(125, 100, 3)
    node = PipelineNode()
    node._set_value(data)
    resized_node = process_2d.resize_with_max_distortion(node, (100, 100), 5)
    resized_node.execute()
    resized_image = resized_node.value
    assert resized_image.shape == (100, 100, 3)

def test_hwc_to_chw():
    shape = (10, 5, 2)
    data = np.random.rand(*shape)
    node = PipelineNode()
    node._set_value(data)
    ndata_node = process_2d.image_hwc_to_chw(node)
    ndata_node.execute()
    ndata = ndata_node.value
    assert ndata.shape == (data.shape[2], data.shape[0], data.shape[1])

def test_chw_to_hwc():
    shape = (10, 5, 2)
    data = np.random.rand(*shape)
    node = PipelineNode()
    node._set_value(data)
    ndata_node = process_2d.image_chw_to_hwc(node)
    ndata_node.execute()
    ndata = ndata_node.value
    assert ndata.shape == (data.shape[1], data.shape[2], data.shape[0])

def test_hwc_to_chw_wrong_dim():
    shape = (10, 5)
    data = np.random.rand(*shape)
    node = PipelineNode()
    node._set_value(data)
    with pytest.raises(ValueError):
        ndata_node = process_2d.image_hwc_to_chw(node)
        ndata_node.execute()

def test_chw_to_hwc_wrong_dim():
    shape = (10, 5, 2, 5)
    data = np.random.rand(*shape)
    node = PipelineNode()
    node._set_value(data)
    with pytest.raises(ValueError):
        ndata_node = process_2d.image_chw_to_hwc(node)
        ndata_node.execute()

@patch('cv2.cvtColor')
@patch('cv2.imread')
def test_open_rgb_image(mock_imread, mock_cvtColor):
    # Mocked return value for cv2.imread
    mock_img = np.ones((100, 100, 3), dtype=np.uint8)  # Mocked image in BGR format
    mock_imread.return_value = mock_img

    # Mocked return value for cv2.cvtColor
    mock_img_rgb = np.ones((100, 100, 3), dtype=np.uint8) * 255  # Mocked image in RGB format
    mock_cvtColor.return_value = mock_img_rgb

    # Call the function
    node = PipelineNode()
    node._set_value("dummy/path/to/image.jpg")
    result_node = process_2d.open_rgb_image(node)
    result_node.execute()
    result = result_node.value

    # Assertions
    mock_imread.assert_called_once_with("dummy/path/to/image.jpg")
    mock_cvtColor.assert_called_once_with(mock_img, cv2.COLOR_BGR2RGB)
    np.testing.assert_array_equal(result, mock_img_rgb)

