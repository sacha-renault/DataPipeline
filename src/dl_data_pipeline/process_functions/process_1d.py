import numpy as np
from ..deferred import deferred_execution

@deferred_execution
def rpad_rcut(data : np.ndarray, desired_audio_length : int) -> np.ndarray:
    """ Pad or cut the audio array so that output has a length equal to desired_audio_length
    Args:
        data (np.ndarray): the input audio array
        desired_audio_length (int): the target length for the audio
    Return
        (np.ndarray): correctly shaped audio array

    Examples:
        >>> data = np.array([[1, 2, 3], [4, 5, 6]])
        >>> rpad_rcut(data, 5)
        array([[1., 2., 3., 0., 0.],
               [4., 5., 6., 0., 0.]])
        >>> rpad_rcut(data, 2)
        array([[1, 2],
               [4, 5]])
    """
    assert len(data.shape) == 2, "Audio should be 2D array, use reshape(1, -1) for 1D array"
    audio_length = data.shape[1]
    if audio_length < desired_audio_length:
        padding_array = np.zeros((data.shape[0], desired_audio_length - audio_length))
        return np.concatenate((data, padding_array), axis = 1)

    # Else
    return data[:,:desired_audio_length]

@deferred_execution
def lpad_lcut(data : np.ndarray, desired_audio_length : int) -> np.ndarray:
    """ Pad or cut the audio array so that output has a length equal to desired_audio_length
    Args:
        data (np.ndarray): the input audio array
        desired_audio_length (int): the target length for the audio
    Return
        (np.ndarray): correctly shaped audio array

    Examples:
        >>> data = np.array([[1, 2, 3], [4, 5, 6]])
        >>> lpad_lcut(data, 5)
        array([[0., 0., 1., 2., 3.],
               [0., 0., 4., 5., 6.]])
        >>> lpad_lcut(data, 2)
        array([[2, 3],
               [5, 6]])
    """
    assert len(data.shape) == 2, "Audio should be 2D array, use reshape(1, -1) for 1D array"
    audio_length = data.shape[1]
    if audio_length < desired_audio_length:
        padding_array = np.zeros((data.shape[0], desired_audio_length - audio_length))
        return np.concatenate((padding_array, data), axis = 1)

    # Else
    return data[:,desired_audio_length:]

@deferred_execution
def center_pad_rcut(data : np.ndarray, desired_audio_length : int) -> np.ndarray:
    """ Pad or cut the audio array so that output has a length equal to desired_audio_length
    Args:
        data (np.ndarray): the input audio array
        desired_audio_length (int): the target length for the audio
    Return
        (np.ndarray): correctly shaped audio array

    Examples:
        >>> data = np.array([[1, 2, 3], [4, 5, 6]])
        >>> center_pad_rcut(data, 5)
        array([[0., 1., 2., 3., 0.],
               [0., 4., 5., 6., 0.]])
        >>> center_pad_rcut(data, 2)
        array([[2, 3],
               [5, 6]])
    """
    assert len(data.shape) == 2, "Audio should be 2D array, use reshape(1, -1) for 1D array"
    audio_length = data.shape[1]
    if audio_length < desired_audio_length:
        l_pad_length = (desired_audio_length - audio_length) // 2
        r_pad_length = l_pad_length + (desired_audio_length - audio_length) % 2
        l_padding_array = np.zeros((data.shape[0], l_pad_length))
        r_padding_array = np.zeros((data.shape[0], r_pad_length))
        return np.concatenate((l_padding_array, data, r_padding_array), axis = 1)

    # Else
    return data[:,:desired_audio_length]