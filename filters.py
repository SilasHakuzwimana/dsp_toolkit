import numpy as np
from scipy.signal import lfilter, butter


# -------------------------------
# FIR Filter (Moving Average)
# -------------------------------
def fir_filter(signal, filter_type="lowpass", order=5):
    """
    Apply a simple FIR filter (moving average)

    Parameters:
    - signal: input signal (numpy array)
    - filter_type: "lowpass" or "highpass"
    - order: filter order (number of taps)

    Returns:
    - filtered_signal: output signal after FIR filtering
    """
    if order < 1:
        order = 1

    if filter_type.lower() == "lowpass":
        # Simple moving average
        kernel = np.ones(order) / order
    elif filter_type.lower() == "highpass":
        # Subtract moving average to get high-pass effect
        kernel = -np.ones(order) / order
        kernel[order // 2] += 1
    else:
        raise ValueError("Unsupported FIR filter type. Use 'lowpass' or 'highpass'.")

    filtered_signal = np.convolve(signal, kernel, mode="same")
    return filtered_signal


# -------------------------------
# IIR Filter (Butterworth)
# -------------------------------
def iir_filter(
    signal, filter_type="lowpass", cutoff_freq=1000, sampling_rate=44100, order=4
):
    """
    Apply an IIR Butterworth filter

    Parameters:
    - signal: input signal (numpy array)
    - filter_type: "lowpass" or "highpass"
    - cutoff_freq: cutoff frequency in Hz
    - sampling_rate: sampling rate in Hz
    - order: filter order

    Returns:
    - filtered_signal: output signal after IIR filtering
    """
    nyquist = 0.5 * sampling_rate
    normal_cutoff = cutoff_freq / nyquist
    b, a = butter(order, normal_cutoff, btype=filter_type, analog=False)
    filtered_signal = lfilter(b, a, signal)
    return filtered_signal
