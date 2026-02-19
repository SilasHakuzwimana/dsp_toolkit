"""
DSP Simulation Toolkit - setup.py
Installs the app and its dependencies via pip.
Run: pip install .
Then launch with: dsp-toolkit
"""
from setuptools import setup, find_packages
import os

# Read the README if it exists
here = os.path.abspath(os.path.dirname(__file__))
long_description = ""
readme_path = os.path.join(here, "README.md")
if os.path.exists(readme_path):
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="dsp-simulation-toolkit",
    version="1.0.0",
    description="A desktop DSP simulation tool for signal generation, filtering, FFT analysis, and embedded fixed-point simulation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="you@example.com",
    url="https://github.com/yourname/dsp-simulation-toolkit",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "PyQt5>=5.15",
        "matplotlib>=3.5",
        "numpy>=1.22",
        "scipy>=1.8",
    ],
    entry_points={
        "console_scripts": [
            # Launch without a terminal window on Windows via pythonw
            "dsp-toolkit=dsp_toolkit.main:main",
        ],
        "gui_scripts": [
            "dsp-toolkit-gui=dsp_toolkit.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "dsp_toolkit": ["assets/*", "*.ico", "*.png"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Environment :: X11 Applications :: Qt",
    ],
    keywords="dsp signal processing fft filter embedded fixed-point simulation",
)
