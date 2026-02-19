import numpy as np


def float_to_fixed(signal, bits=16):
    """
    Convert floating-point signal to fixed-point representation.

    Parameters:
    - signal (np.ndarray): Input floating signal (-1 to 1 recommended)
    - bits (int): Bit width (8, 16, etc.)

    Returns:
    - fixed_signal (np.ndarray): Quantized fixed-point signal
    """

    max_int = 2 ** (bits - 1) - 1

    # Clip to avoid overflow
    clipped = np.clip(signal, -1, 1)

    # Scale and round
    fixed_signal = np.round(clipped * max_int)

    # Convert back to float representation
    fixed_signal = fixed_signal / max_int

    return fixed_signal


def quantization_error(original, quantized):
    """
    Compute quantization error.

    Returns:
    - error signal
    - mean squared error (MSE)
    """
    error = original - quantized
    mse = np.mean(error**2)

    return error, mse
