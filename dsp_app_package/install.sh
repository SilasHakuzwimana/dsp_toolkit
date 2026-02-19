#!/usr/bin/env bash
# ============================================================
#  DSP Simulation Toolkit — Installer (Linux / macOS)
# ============================================================
set -e

PYTHON=python3
PIP=pip3
APP_NAME="DSP Simulation Toolkit"
VENV_DIR="$HOME/.local/share/dsp-toolkit/venv"
INSTALL_DIR="$HOME/.local/share/dsp-toolkit"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

echo ""
echo "=============================="
echo "  Installing $APP_NAME"
echo "=============================="
echo ""

# ── Check Python ──────────────────────────────────────────────────────────────
if ! command -v $PYTHON &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.9 or later."
    exit 1
fi

PY_VER=$($PYTHON -c "import sys; print(sys.version_info[:2])")
echo "✓ Found Python: $($PYTHON --version)"

# ── Create virtual environment ────────────────────────────────────────────────
echo "→ Creating virtual environment at $VENV_DIR ..."
mkdir -p "$INSTALL_DIR"
$PYTHON -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# ── Install dependencies ──────────────────────────────────────────────────────
echo "→ Installing dependencies ..."
pip install --upgrade pip --quiet
pip install PyQt5 matplotlib numpy scipy --quiet
echo "✓ Dependencies installed."

# ── Install the package ───────────────────────────────────────────────────────
echo "→ Installing DSP Toolkit ..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pip install "$SCRIPT_DIR" --quiet
echo "✓ Package installed."

# ── Create launcher script ────────────────────────────────────────────────────
mkdir -p "$BIN_DIR"
LAUNCHER="$BIN_DIR/dsp-toolkit"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env bash
source "$VENV_DIR/bin/activate"
exec dsp-toolkit "\$@"
EOF
chmod +x "$LAUNCHER"
echo "✓ Launcher created at $LAUNCHER"

# ── Create .desktop entry (Linux only) ───────────────────────────────────────
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    mkdir -p "$DESKTOP_DIR"
    cat > "$DESKTOP_DIR/dsp-toolkit.desktop" <<EOF
[Desktop Entry]
Version=1.0
Name=DSP Simulation Toolkit
Comment=Signal generation, filtering, FFT analysis, and embedded simulation
Exec=$LAUNCHER
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=Science;Education;Engineering;
EOF
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
    echo "✓ Desktop entry created."
fi

# ── macOS .command launcher ───────────────────────────────────────────────────
if [[ "$OSTYPE" == "darwin"* ]]; then
    APPS_DIR="$HOME/Applications"
    mkdir -p "$APPS_DIR"
    MACOS_LAUNCHER="$APPS_DIR/DSP Toolkit.command"
    cp "$LAUNCHER" "$MACOS_LAUNCHER"
    chmod +x "$MACOS_LAUNCHER"
    echo "✓ macOS launcher created at $MACOS_LAUNCHER"
fi

echo ""
echo "=============================="
echo "  Installation complete!"
echo "=============================="
echo ""
echo "  Run anytime with:"
echo "    dsp-toolkit"
echo ""
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "  NOTE: Add $BIN_DIR to your PATH if the command is not found:"
    echo "    echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc && source ~/.bashrc"
    echo ""
fi
