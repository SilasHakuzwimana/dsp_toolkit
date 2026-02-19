
# DSP Simulation Toolkit

## Academic Digital Signal Processing Teaching Tool

A Python-based interactive simulation toolkit for learning and teaching Digital Signal Processing (DSP) concepts without requiring physical hardware.

## Project Overview

The **DSP Simulation Toolkit** is a GUI-based educational software developed using:

* Python
* PyQt5
* NumPy
* Matplotlib

It allows students to:

* Generate different signals
* Add noise
* Apply FIR and IIR filters
* Compute FFT (frequency spectrum)
* Simulate fixed-point (embedded) DSP behavior

This project is designed for  **university-level DSP laboratories** .

## Educational Objectives

This toolkit helps students understand:

* Signal generation (Sine, Square, Triangle)
* Sampling and time-domain representation
* Noise modeling (Gaussian noise)
* FIR filtering concepts
* IIR filtering concepts
* FFT and frequency-domain analysis
* Quantization effects
* Fixed-point vs floating-point DSP systems

It bridges theoretical DSP concepts and practical simulation.

## Key Features

### 1. Signal Generator

Supports:

* Sine wave
* Square wave
* Triangle wave

Adjustable:

* Frequency
* Amplitude

### Noise Simulation

Optional Gaussian noise addition for:

* Signal-to-noise experiments
* Filter performance testing

### Digital Filters

#### FIR Low-Pass Filter

* Adjustable filter order
* Demonstrates convolution-based filtering

#### IIR High-Pass Filter

* Adjustable cutoff frequency
* Demonstrates recursive filtering

### FFT Spectrum Analyzer

* Computes magnitude spectrum
* Displays frequency-domain representation
* Demonstrates spectral peaks and bandwidth

### Embedded Mode (Fixed-Point Simulation)

Simulates behavior of real embedded DSP systems used in hardware platforms such as:

* Texas Instruments DSP processors
* ARM-based embedded systems

Features:

* Bit-width selection (4, 8, 12, 16, 32 bits)
* Floating vs Fixed comparison
* Quantization error calculation
* Mean Squared Error (MSE) display

This helps students understand:

* Quantization noise
* Precision loss
* Bit resolution trade-offs
* Embedded implementation constraints

## Project Structure

<pre class="overflow-visible! px-0!" data-start="2379" data-end="2730"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>DSP_Simulation_Toolkit/
│
├── _pycache_/
├── dsp_toolkit/
├── main.py                </span><span># Main GUI application</span><span>
├── signal_generator.py    </span><span># Signal generation module</span><span>
├── noise_module.py        </span><span># Noise addition functions</span><span>
├── filters.py             </span><span># FIR and IIR filters</span><span>
├── fft_module.py          </span><span># FFT computation</span><span>
├── embedded_sim.py        </span><span># Fixed-point simulation</span><span>
└── README.md
</span></span></code></div></div></pre>

## Installation

### 1️⃣ Install Python (3.8 or higher recommended)

Download from:

[https://www.python.org/](https://www.python.org/)

### Install Required Libraries

Run:

<pre class="overflow-visible! px-0!" data-start="2896" data-end="2942"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>pip install pyqt5 numpy matplotlib
</span></span></code></div></div></pre>

## Running the Application

From the project directory:

<pre class="overflow-visible! px-0!" data-start="3009" data-end="3035"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>python main.py
</span></span></code></div></div></pre>

The GUI window will open.

## Example Laboratory Exercises

### Lab 1 – Signal Generation

* Generate sine wave at different frequencies
* Observe time-domain changes

### Lab 2 – Noise and Filtering

* Add Gaussian noise
* Apply FIR Low-pass filter
* Compare before and after

### Lab 3 – FFT Analysis

* Generate 1000 Hz sine wave
* Compute FFT
* Identify frequency peak

### Lab 4 – Quantization Effects

* Enable Embedded Mode
* Compare 4-bit vs 16-bit
* Compute and analyze MSE
* Study distortion and quantization noise

## Learning Outcomes

After using this toolkit, students should be able to:

* Explain sampling theory
* Analyze signals in time and frequency domains
* Design basic FIR/IIR filters
* Understand quantization effects
* Compare floating-point and fixed-point DSP systems
* Relate simulation to real embedded hardware

## Future Development (Phase B – Research Level)

Planned enhancements:

* Real-time streaming simulation
* Filter design GUI
* Error signal visualization
* Performance benchmarking
* Multi-signal mixing
* Windowing techniques
* Spectrogram analysis
* Export results to CSV
* Save plots for lab reports

## Intended Use

* Undergraduate DSP laboratory courses
* Signal Processing demonstrations
* Embedded systems coursework
* Digital communications foundation courses

## License

This project is developed for educational purposes.

Open for academic use and modification.

## Author

Developed as a university academic project

DSP Simulation Toolkit – Educational Version (Phase A)

By Silas HAKUZWIMANA - 223001019 - Year III Computer Engineering Student - UR-CST (2025 - 2026)
