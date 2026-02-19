# DSP Simulation Toolkit

A desktop application for generating, processing, and analysing digital signals — featuring waveform synthesis, noise injection, digital filtering, FFT spectrum analysis, and fixed-point embedded system simulation.

## Quick Install

### Windows
Double-click `install.bat`

### Linux / macOS
```bash
chmod +x install.sh
./install.sh
```

### Manual (any OS)
```bash
pip install .
dsp-toolkit
```

## Requirements

- Python 3.9+
- PyQt5, Matplotlib, NumPy, SciPy (installed automatically)

## Features

- **Waveform generation**: Sine, Square, Triangle
- **Signal processing**: Gaussian noise, FIR low-pass, IIR high-pass filters
- **FFT analysis**: Frequency-domain spectrum with peak detection
- **Embedded simulation**: Fixed-point quantisation (4–32 bit) with MSE reporting
- **Dark UI**: Industrial-grade dark theme optimised for signal readability

## Project Structure

```
dsp-simulation-toolkit/
├── setup.py
├── install.sh          # Linux/macOS installer
├── install.bat         # Windows installer
├── README.md
└── src/
    └── dsp_toolkit/
        ├── __init__.py
        ├── main.py          # Entry point
        ├── app.py           # Main window (DSPToolkit class)
        ├── signal_generator.py
        ├── noise_module.py
        ├── filters.py
        ├── fft_module.py
        └── embedded_sim.py
```

## Licence

MIT
