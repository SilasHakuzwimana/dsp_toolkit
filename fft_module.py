import numpy as np


def compute_fft(signal, sampling_rate):
    """
    Compute the Fast Fourier Transform (FFT) of a signal.

    Parameters:
    - signal (np.ndarray): Input time-domain signal
    - sampling_rate (int): Sampling rate in Hz

    Returns:
    - freqs (np.ndarray): Frequency axis
    - magnitude (np.ndarray): Magnitude spectrum
    """

    N = len(signal)

    # Compute FFT
    fft_values = np.fft.fft(signal)

    # Only take positive frequencies
    fft_values = fft_values[: N // 2]

    # Magnitude spectrum
    magnitude = np.abs(fft_values) * 2 / N

    # Frequency axis
    freqs = np.fft.fftfreq(N, 1 / sampling_rate)
    freqs = freqs[: N // 2]

    return freqs, magnitude
