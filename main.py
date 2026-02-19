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
    QFrame,
    QSizePolicy,
    QSpacerItem,
    QGraphicsDropShadowEffect,
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette, QFontDatabase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import rcParams
import numpy as np

# Import custom modules
from signal_generator import generate_signal
from noise_module import add_noise
from filters import fir_filter, iir_filter
from fft_module import compute_fft
from embedded_sim import float_to_fixed, quantization_error

# ── Palette ──────────────────────────────────────────────────────────────────
C = {
    "bg": "#0d0f14",
    "surface": "#13161e",
    "panel": "#191d28",
    "border": "#252a38",
    "accent": "#00e5ff",
    "accent2": "#7b61ff",
    "muted": "#3d4560",
    "text": "#cdd6f4",
    "subtext": "#6c7a9c",
    "danger": "#f38ba8",
    "success": "#a6e3a1",
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {C['bg']};
    color: {C['text']};
    font-family: 'Courier New', monospace;
    font-size: 12px;
}}

/* ── Sidebar panel ── */
#sidebar {{
    background-color: {C['panel']};
    border-right: 1px solid {C['border']};
}}

/* ── Section labels ── */
QLabel#section {{
    color: {C['accent']};
    font-size: 9px;
    letter-spacing: 3px;
    font-weight: bold;
    padding: 0;
}}

/* ── Regular labels ── */
QLabel {{
    color: {C['subtext']};
    font-size: 11px;
    padding: 0;
}}

/* ── Inputs ── */
QLineEdit {{
    background-color: {C['surface']};
    border: 1px solid {C['border']};
    border-radius: 4px;
    color: {C['text']};
    padding: 6px 10px;
    selection-background-color: {C['accent2']};
    font-family: 'Courier New', monospace;
}}
QLineEdit:focus {{
    border: 1px solid {C['accent']};
}}

/* ── Dropdowns ── */
QComboBox {{
    background-color: {C['surface']};
    border: 1px solid {C['border']};
    border-radius: 4px;
    color: {C['text']};
    padding: 6px 10px;
    font-family: 'Courier New', monospace;
}}
QComboBox:focus {{
    border: 1px solid {C['accent']};
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox::down-arrow {{
    width: 8px;
    height: 8px;
    border-left: 2px solid {C['subtext']};
    border-bottom: 2px solid {C['subtext']};
    margin-right: 6px;
}}
QComboBox QAbstractItemView {{
    background-color: {C['panel']};
    border: 1px solid {C['border']};
    color: {C['text']};
    selection-background-color: {C['accent2']};
    outline: none;
}}

/* ── Checkboxes ── */
QCheckBox {{
    color: {C['text']};
    spacing: 8px;
    font-size: 11px;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 1px solid {C['muted']};
    background: {C['surface']};
}}
QCheckBox::indicator:checked {{
    background: {C['accent']};
    border: 1px solid {C['accent']};
}}

/* ── Primary button ── */
QPushButton#primary {{
    background-color: {C['accent']};
    color: {C['bg']};
    border: none;
    border-radius: 4px;
    padding: 9px 0;
    font-weight: bold;
    font-size: 11px;
    letter-spacing: 1px;
    font-family: 'Courier New', monospace;
}}
QPushButton#primary:hover {{
    background-color: #33eaff;
}}
QPushButton#primary:pressed {{
    background-color: #00b8cc;
}}

/* ── Secondary button ── */
QPushButton#secondary {{
    background-color: transparent;
    color: {C['accent2']};
    border: 1px solid {C['accent2']};
    border-radius: 4px;
    padding: 9px 0;
    font-size: 14px;
    letter-spacing: 1px;
    font-family: 'Courier New', monospace;
}}
QPushButton#secondary:hover {{
    background-color: {C['accent2']};
    color: white;
}}
QPushButton#secondary:pressed {{
    background-color: #5d47cc;
}}

/* ── Divider ── */
QFrame#divider {{
    color: {C['border']};
    background: {C['border']};
    max-height: 1px;
}}

/* ── Status bar ── */
QLabel#status {{
    color: {C['subtext']};
    font-size: 10px;
    padding: 4px 12px;
    background: {C['panel']};
    border-top: 1px solid {C['border']};
}}
"""

MPLSTYLE = {
    "axes.facecolor": C["surface"],
    "figure.facecolor": C["surface"],
    "axes.edgecolor": C["border"],
    "axes.labelcolor": C["subtext"],
    "xtick.color": C["subtext"],
    "ytick.color": C["subtext"],
    "grid.color": C["border"],
    "grid.linestyle": "--",
    "grid.linewidth": 0.5,
    "text.color": C["text"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "font.family": "monospace",
    "font.size": 9,
}
for k, v in MPLSTYLE.items():
    rcParams[k] = v


def make_label(text, is_section=False):
    lbl = QLabel(text.upper() if is_section else text)
    if is_section:
        lbl.setObjectName("section")
    return lbl


def make_divider():
    line = QFrame()
    line.setObjectName("divider")
    line.setFrameShape(QFrame.HLine)
    return line


class DSPToolkit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DSP Simulation Toolkit")
        self.setGeometry(100, 100, 1140, 680)
        self.setMinimumSize(900, 560)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(STYLESHEET)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(240)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 24, 20, 16)
        sidebar_layout.setSpacing(6)

        # App title
        title = QLabel("DSP TOOLKIT")
        title.setStyleSheet(
            f"color:{C['accent']}; font-size:15px; font-weight:bold; letter-spacing:4px;"
        )
        subtitle = QLabel("Signal Simulation Suite")
        subtitle.setStyleSheet(
            f"color:{C['subtext']}; font-size:10px; letter-spacing:1px;"
        )
        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(subtitle)
        sidebar_layout.addSpacing(16)
        sidebar_layout.addWidget(make_divider())
        sidebar_layout.addSpacing(10)

        # ── SIGNAL section ────────────────────────────────────────────────
        sidebar_layout.addWidget(make_label("Signal", is_section=True))
        sidebar_layout.addSpacing(4)

        sidebar_layout.addWidget(QLabel("Waveform Type"))
        self.signal_type = QComboBox()
        self.signal_type.addItems(["Sine", "Square", "Triangle"])
        sidebar_layout.addWidget(self.signal_type)
        sidebar_layout.addSpacing(4)

        sidebar_layout.addWidget(QLabel("Frequency (Hz)"))
        self.freq_input = QLineEdit("1000")
        self.freq_input.setPlaceholderText("e.g. 1000")
        sidebar_layout.addWidget(self.freq_input)
        sidebar_layout.addSpacing(4)

        sidebar_layout.addWidget(QLabel("Amplitude"))
        self.amp_input = QLineEdit("1")
        self.amp_input.setPlaceholderText("e.g. 1.0")
        sidebar_layout.addWidget(self.amp_input)

        sidebar_layout.addSpacing(14)
        sidebar_layout.addWidget(make_divider())
        sidebar_layout.addSpacing(10)

        # ── PROCESSING section ────────────────────────────────────────────
        sidebar_layout.addWidget(make_label("Processing", is_section=True))
        sidebar_layout.addSpacing(4)

        self.noise_check = QCheckBox("Add Gaussian Noise")
        sidebar_layout.addWidget(self.noise_check)
        sidebar_layout.addSpacing(4)

        sidebar_layout.addWidget(QLabel("Filter"))
        self.filter_type = QComboBox()
        self.filter_type.addItems(["None", "FIR Low-pass", "IIR High-pass"])
        sidebar_layout.addWidget(self.filter_type)

        sidebar_layout.addSpacing(14)
        sidebar_layout.addWidget(make_divider())
        sidebar_layout.addSpacing(10)

        # ── EMBEDDED section ──────────────────────────────────────────────
        sidebar_layout.addWidget(make_label("Embedded", is_section=True))
        sidebar_layout.addSpacing(4)

        self.embedded_check = QCheckBox("Fixed-Point Mode")
        sidebar_layout.addWidget(self.embedded_check)
        sidebar_layout.addSpacing(4)

        sidebar_layout.addWidget(QLabel("Bit Width"))
        self.bit_width = QComboBox()
        self.bit_width.addItems(["4", "8", "12", "16", "32"])
        self.bit_width.setCurrentText("16")
        sidebar_layout.addWidget(self.bit_width)

        sidebar_layout.addStretch()
        sidebar_layout.addWidget(make_divider())
        sidebar_layout.addSpacing(10)

        # ── Action buttons ────────────────────────────────────────────────
        self.generate_btn = QPushButton("▶  GENERATE SIGNAL")
        self.generate_btn.setObjectName("primary")
        self.generate_btn.setCursor(Qt.PointingHandCursor)
        sidebar_layout.addWidget(self.generate_btn)
        sidebar_layout.addSpacing(6)

        self.fft_btn = QPushButton("∿  COMPUTE FFT")
        self.fft_btn.setObjectName("secondary")
        self.fft_btn.setCursor(Qt.PointingHandCursor)
        sidebar_layout.addWidget(self.fft_btn)

        root.addWidget(sidebar)

        # ── Main plot area ────────────────────────────────────────────────
        right_panel = QVBoxLayout()
        right_panel.setContentsMargins(0, 0, 0, 0)
        right_panel.setSpacing(0)

        # Header bar
        header = QWidget()
        header.setFixedHeight(44)
        header.setStyleSheet(
            f"background:{C['panel']}; border-bottom: 1px solid {C['border']};"
        )
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        self.plot_title = QLabel("Time Domain")
        self.plot_title.setStyleSheet(
            f"color:{C['text']}; font-size:12px; letter-spacing:1px; background:transparent;"
        )
        self.plot_info = QLabel("Ready")
        self.plot_info.setStyleSheet(
            f"color:{C['subtext']}; font-size:10px; background:transparent;"
        )
        header_layout.addWidget(self.plot_title)
        header_layout.addStretch()
        header_layout.addWidget(self.plot_info)
        right_panel.addWidget(header)

        # Canvas
        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet(f"background-color:{C['surface']};")
        right_panel.addWidget(self.canvas, 1)

        # Status bar
        self.status_bar = QLabel("No signal generated.")
        self.status_bar.setObjectName("status")
        right_panel.addWidget(self.status_bar)

        right_container = QWidget()
        right_container.setLayout(right_panel)
        root.addWidget(right_container, 1)

        # Draw empty axes
        self._init_plot()

        # Connect
        self.generate_btn.clicked.connect(self.generate_signal)
        self.fft_btn.clicked.connect(self.compute_fft)
        self.embedded_check.toggled.connect(
            lambda checked: self.bit_width.setEnabled(checked)
        )
        self.bit_width.setEnabled(False)

    def _init_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor(C["surface"])
        ax.tick_params(colors=C["subtext"])
        for spine in ax.spines.values():
            spine.set_edgecolor(C["border"])
        ax.set_xlabel("Time (s)", color=C["subtext"])
        ax.set_ylabel("Amplitude", color=C["subtext"])
        ax.text(
            0.5,
            0.5,
            "Generate a signal to begin",
            transform=ax.transAxes,
            ha="center",
            va="center",
            color=C["muted"],
            fontsize=13,
            style="italic",
        )
        self.canvas.draw()

    def _update_header(self, title, info=""):
        self.plot_title.setText(title)
        self.plot_info.setText(info)

    def generate_signal(self):
        try:
            bits = int(self.bit_width.currentText())
            signal_type = self.signal_type.currentText()
            frequency = float(self.freq_input.text())
            amplitude = float(self.amp_input.text())
        except ValueError:
            self.status_bar.setText(
                "⚠  Invalid input — check Frequency and Amplitude fields."
            )
            return

        duration = 1
        sampling_rate = 44100

        t, original_signal = generate_signal(
            signal_type=signal_type,
            frequency=frequency,
            amplitude=amplitude,
            duration=duration,
            sampling_rate=sampling_rate,
        )
        signal = original_signal.copy()

        if self.noise_check.isChecked():
            signal = add_noise(
                signal,
                noise_type="Gaussian",
                noise_level=0.2,
                sampling_rate=sampling_rate,
            )

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

        fixed_signal = None
        mse_text = ""
        if self.embedded_check.isChecked():
            fixed_signal = float_to_fixed(signal, bits=bits)
            error, mse = quantization_error(signal, fixed_signal)
            mse_text = f"  ·  Quantization MSE ({bits}-bit): {mse:.2e}"

        # Plot
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Limit samples shown for performance
        max_pts = 4096
        step = max(1, len(t) // max_pts)
        ts, ss = t[::step], signal[::step]

        if self.embedded_check.isChecked():
            fs = fixed_signal[::step]
            ax.plot(ts, ss, color=C["accent"], linewidth=1.0, alpha=0.7, label="Float")
            ax.plot(
                ts,
                fs,
                color=C["accent2"],
                linewidth=0.9,
                linestyle="--",
                label=f"{bits}-bit Fixed",
            )
            ax.legend(facecolor=C["panel"], edgecolor=C["border"], labelcolor=C["text"])
            self._update_header(
                "Float vs Fixed-Point Comparison", f"{bits}-bit{mse_text}"
            )
        else:
            ax.plot(ts, ss, color=C["accent"], linewidth=1.0, label="Signal")
            filters_applied = (
                []
                + (["noise"] if self.noise_check.isChecked() else [])
                + ([filter_choice] if filter_choice != "None" else [])
            )
            info = " + ".join(filters_applied) if filters_applied else "clean"
            self._update_header(
                f"{signal_type} Wave — Time Domain", f"{frequency:.0f} Hz · {info}"
            )

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        self.canvas.draw()

        self.current_signal = (
            fixed_signal if self.embedded_check.isChecked() else signal
        )
        self.current_time = t
        self.status_bar.setText(
            f"✓  {signal_type} signal generated  ·  {frequency:.0f} Hz  ·  {sampling_rate} Sa/s  ·  {len(t):,} samples{mse_text}"
        )

    def compute_fft(self):
        if not hasattr(self, "current_signal"):
            self.status_bar.setText("⚠  No signal available — generate a signal first.")
            return

        sampling_rate = 44100
        freqs, magnitude = compute_fft(self.current_signal, sampling_rate)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        mask = freqs <= 5000
        ax.fill_between(freqs[mask], magnitude[mask], color=C["accent"], alpha=0.15)
        ax.plot(freqs[mask], magnitude[mask], color=C["accent"], linewidth=1.2)

        peak_idx = np.argmax(magnitude[mask])
        peak_f = freqs[mask][peak_idx]
        peak_m = magnitude[mask][peak_idx]
        ax.axvline(peak_f, color=C["accent2"], linewidth=0.8, linestyle=":")
        ax.annotate(
            f"{peak_f:.0f} Hz",
            xy=(peak_f, peak_m),
            xytext=(peak_f + 100, peak_m * 0.85),
            color=C["accent2"],
            fontsize=8,
            arrowprops=dict(arrowstyle="-", color=C["muted"]),
        )

        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("Magnitude")
        ax.set_xlim(0, 5000)
        self._update_header("Frequency-Domain Spectrum (FFT)", f"Peak: {peak_f:.0f} Hz")
        self.canvas.draw()
        self.status_bar.setText(
            f"✓  FFT computed  ·  {len(self.current_signal):,} samples  ·  Peak at {peak_f:.1f} Hz (magnitude {peak_m:.3f})"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Dark palette for native widgets
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(C["bg"]))
    palette.setColor(QPalette.WindowText, QColor(C["text"]))
    palette.setColor(QPalette.Base, QColor(C["surface"]))
    palette.setColor(QPalette.AlternateBase, QColor(C["panel"]))
    palette.setColor(QPalette.ToolTipBase, QColor(C["panel"]))
    palette.setColor(QPalette.ToolTipText, QColor(C["text"]))
    palette.setColor(QPalette.Text, QColor(C["text"]))
    palette.setColor(QPalette.Button, QColor(C["panel"]))
    palette.setColor(QPalette.ButtonText, QColor(C["text"]))
    palette.setColor(QPalette.Highlight, QColor(C["accent2"]))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    window = DSPToolkit()
    window.show()
    sys.exit(app.exec_())
