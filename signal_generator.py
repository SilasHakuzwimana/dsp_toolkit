import numpy as np


def generate_signal(
    signal_type="Sine", frequency=1000, amplitude=1, duration=1, sampling_rate=44100
):
    """
    Generate a digital signal.

    Parameters:
    - signal_type (str): "Sine", "Square", or "Triangle"
    - frequency (float): Frequency of the signal in Hz
    - amplitude (float): Amplitude of the signal
    - duration (float): Duration in seconds
    - sampling_rate (int): Number of samples per second

    Returns:
    - t (np.ndarray): Time vector
    - signal (np.ndarray): Generated signal samples
    """
    t = np.arange(0, duration, 1 / sampling_rate)

    if signal_type.lower() == "sine":
        signal = amplitude * np.sin(2 * np.pi * frequency * t)
    elif signal_type.lower() == "square":
        signal = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    elif signal_type.lower() == "triangle":
        signal = amplitude * (2 * np.arcsin(np.sin(2 * np.pi * frequency * t)) / np.pi)
    else:
        raise ValueError(
            "Unsupported signal type. Choose 'Sine', 'Square', or 'Triangle'."
        )

    return t, signal
