import numpy as np


def add_noise(signal, noise_type="Gaussian", noise_level=0.1, sampling_rate=44100):
    """
    Add noise to a signal.

    Parameters:
    - signal (np.ndarray): Original signal
    - noise_type (str): "Gaussian" or "50Hz"
    - noise_level (float): Amplitude of noise relative to signal
    - sampling_rate (int): Sampling rate in Hz

    Returns:
    - noisy_signal (np.ndarray): Signal with added noise
    """
    noisy_signal = signal.copy()

    if noise_type.lower() == "gaussian":
        noise = noise_level * np.random.randn(len(signal))
        noisy_signal += noise

    elif noise_type.lower() == "50hz":
        t = np.arange(len(signal)) / sampling_rate
        interference = noise_level * np.sin(2 * np.pi * 50 * t)
        noisy_signal += interference

    else:
        raise ValueError("Unsupported noise type. Choose 'Gaussian' or '50Hz'.")

    return noisy_signal
