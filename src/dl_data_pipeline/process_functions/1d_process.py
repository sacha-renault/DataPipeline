import numpy as np

def rpad_rcut(data : np.ndarray, desired_audio_length : int) -> np.ndarray:
    """ Pad or cut the audio array so that output has a length equal to desired_audio_length
    Args:
        data (np.ndarray): the input audio array
        desired_audio_length (int): the target length for the audio
    Return
        (np.ndarray): correctly shaped audio array
    """
    assert len(data.shape) == 2, "Audio should be 2D array, use reshape(1, -1) for 1D array"
    audio_length = data.shape[1]
    if audio_length < desired_audio_length:
        padding_array = np.zeros((data.shape[0], desired_audio_length - audio_length))
        return np.concatenate((data, padding_array), axis = 1)

    # Else
    return data[:,:desired_audio_length]

def lpad_lcut(data : np.ndarray, desired_audio_length : int) -> np.ndarray:
    """ Pad or cut the audio array so that output has a length equal to desired_audio_length
    Args:
        data (np.ndarray): the input audio array
        desired_audio_length (int): the target length for the audio
    Return
        (np.ndarray): correctly shaped audio array
    """
    assert len(data.shape) == 2, "Audio should be 2D array, use reshape(1, -1) for 1D array"
    audio_length = data.shape[1]
    if audio_length < desired_audio_length:
        padding_array = np.zeros((data.shape[0], desired_audio_length - audio_length))
        return np.concatenate((padding_array, data), axis = 1)

    # Else
    return data[:,desired_audio_length:]

def center_pad_rcut(data : np.ndarray, desired_audio_length : int) -> np.ndarray:
    """ Pad or cut the audio array so that output has a length equal to desired_audio_length
    Args:
        data (np.ndarray): the input audio array
        desired_audio_length (int): the target length for the audio
    Return
        (np.ndarray): correctly shaped audio array
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