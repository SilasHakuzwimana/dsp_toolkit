import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        # Placeholder: integrate signal_generator.py
        print("Generate signal clicked")
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot([0,1,2,3,4],[0,1,0,-1,0])  # Demo waveform
        ax.set_title("Time-Domain Signal")
        self.canvas.draw()
    
    def compute_fft(self):
        # Placeholder: integrate fft_module.py
        print("Compute FFT clicked")
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot([0,1,2,3,4],[0,0.5,1,0.5,0])  # Demo spectrum
        ax.set_title("Frequency-Domain Spectrum")
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DSPToolkit()
    window.show()
    sys.exit(app.exec_())
