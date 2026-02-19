import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
    QCheckBox,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


# Import custom modules
from signal_generator import generate_signal
from noise_module import add_noise
from filters import fir_filter, iir_filter
from fft_module import compute_fft
from embedded_sim import float_to_fixed, quantization_error


class DSPToolkit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DSP Simulation Toolkit")
        self.setGeometry(100, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Control panel (left)
        control_panel = QVBoxLayout()

        # Signal selection
        control_panel.addWidget(QLabel("Signal Type"))
        self.signal_type = QComboBox()
        self.signal_type.addItems(["Sine", "Square", "Triangle"])
        control_panel.addWidget(self.signal_type)

        # Frequency input
        control_panel.addWidget(QLabel("Frequency (Hz)"))
        self.freq_input = QLineEdit("1000")
        control_panel.addWidget(self.freq_input)

        # Amplitude input
        control_panel.addWidget(QLabel("Amplitude"))
        self.amp_input = QLineEdit("1")
        control_panel.addWidget(self.amp_input)

        # Bit width selection
        control_panel.addWidget(QLabel("Bit Width"))
        self.bit_width = QComboBox()
        self.bit_width.addItems(["4", "8", "12", "16", "32"])
        control_panel.addWidget(self.bit_width)

        # Noise checkbox
        self.noise_check = QCheckBox("Add Noise")
        control_panel.addWidget(self.noise_check)

        # Filter selection placeholder
        control_panel.addWidget(QLabel("Filter Type"))
        self.filter_type = QComboBox()
        self.filter_type.addItems(["None", "FIR Low-pass", "IIR High-pass"])
        control_panel.addWidget(self.filter_type)

        # Embedded mode toggle
        self.embedded_check = QCheckBox("Embedded Mode (Fixed-Point)")
        control_panel.addWidget(self.embedded_check)

        # Action buttons
        self.generate_btn = QPushButton("Generate Signal")
        control_panel.addWidget(self.generate_btn)

        self.fft_btn = QPushButton("Compute FFT")
        control_panel.addWidget(self.fft_btn)

        main_layout.addLayout(control_panel, 1)

        # Plot area (right)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas, 3)

        # Connect buttons
        self.generate_btn.clicked.connect(self.generate_signal)
        self.fft_btn.clicked.connect(self.compute_fft)

    def generate_signal(self):

        bits = int(self.bit_width.currentText())
        signal_type = self.signal_type.currentText()
        frequency = float(self.freq_input.text())
        amplitude = float(self.amp_input.text())

        duration = 1
        sampling_rate = 44100

        # Generate clean signal
        t, original_signal = generate_signal(
            signal_type=signal_type,
            frequency=frequency,
            amplitude=amplitude,
            duration=duration,
            sampling_rate=sampling_rate,
        )

        signal = original_signal.copy()

        # Add noise if checked
        if self.noise_check.isChecked():
            signal = add_noise(
                signal,
                noise_type="Gaussian",
                noise_level=0.2,
                sampling_rate=sampling_rate,
            )

        # Apply filter
        filter_choice = self.filter_type.currentText()
        if filter_choice == "FIR Low-pass":
            signal = fir_filter(signal, filter_type="lowpass", order=5)
        elif filter_choice == "IIR High-pass":
            signal = iir_filter(
                signal,
                filter_type="highpass",
                cutoff_freq=1000,
                sampling_rate=sampling_rate,
                order=4,
            )

        # Embedded Mode (Fixed-Point)
        fixed_signal = None
        if self.embedded_check.isChecked():
            fixed_signal = float_to_fixed(signal, bits=bits)
            error, mse = quantization_error(signal, fixed_signal)
            print(f"Quantization MSE ({bits}-bit):   {mse:.8f}")

        # Plot
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if self.embedded_check.isChecked():
            ax.plot(t, signal, label="Floating-Point", alpha=0.7)
            ax.plot(t, fixed_signal, label=f"{bits}-bit Fixed-Point", linestyle="--")
            ax.set_title("Floating vs Fixed-Point Comparison")
        else:
            ax.plot(t, signal, label="Signal", alpha=0.8)
            ax.set_title(f"{signal_type} Signal - Time Domain")

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.legend()
        self.canvas.draw()

        # Store correct signal for FFT
        self.current_signal = (
            fixed_signal if self.embedded_check.isChecked() else signal
        )
        self.current_time = t

    def compute_fft(self):
        if not hasattr(self, "current_signal"):
            print("No signal generated yet. Please generate a signal first.")
            return
        sampling_rate = 44100
        freqs, magnitude = compute_fft(self.current_signal, sampling_rate)

        # Plot frequency-domain spectrum
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title("Frequency-Domain Spectrum (FFT)")
        ax.plot(freqs, magnitude)
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.set_xlim(0, 5000)  # limit view for clarity
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DSPToolkit()
    window.show()
    sys.exit(app.exec_())
