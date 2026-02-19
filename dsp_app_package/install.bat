@echo off
:: ============================================================
::  DSP Simulation Toolkit — Installer (Windows)
:: ============================================================
setlocal enabledelayedexpansion

echo.
echo ==============================
echo   Installing DSP Simulation Toolkit
echo ==============================
echo.

:: ── Check Python ─────────────────────────────────────────────────────────────
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please download Python 3.9+ from https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do echo Found: %%i

:: ── Set paths ─────────────────────────────────────────────────────────────────
set INSTALL_DIR=%LOCALAPPDATA%\DSPToolkit
set VENV_DIR=%INSTALL_DIR%\venv
set SHORTCUT_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs

:: ── Create virtual environment ─────────────────────────────────────────────────
echo.
echo Creating virtual environment...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
python -m venv "%VENV_DIR%"
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)
echo OK - Virtual environment created at %VENV_DIR%

:: ── Install dependencies ──────────────────────────────────────────────────────
echo.
echo Installing dependencies (this may take a moment)...
call "%VENV_DIR%\Scripts\pip.exe" install --upgrade pip --quiet
call "%VENV_DIR%\Scripts\pip.exe" install PyQt5 matplotlib numpy scipy --quiet
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo OK - Dependencies installed.

:: ── Install the package ───────────────────────────────────────────────────────
echo.
echo Installing DSP Toolkit...
call "%VENV_DIR%\Scripts\pip.exe" install "%~dp0." --quiet
if %ERRORLEVEL% neq 0 (
    echo ERROR: Package installation failed.
    pause
    exit /b 1
)
echo OK - Package installed.

:: ── Create launcher batch file ─────────────────────────────────────────────────
set LAUNCHER=%INSTALL_DIR%\DSP Toolkit.bat
(
    echo @echo off
    echo call "%VENV_DIR%\Scripts\activate.bat"
    echo start "" "%VENV_DIR%\Scripts\pythonw.exe" -m dsp_toolkit.main
) > "%LAUNCHER%"
echo OK - Launcher created.

:: ── Create Start Menu shortcut (using PowerShell) ─────────────────────────────
echo.
echo Creating Start Menu shortcut...
powershell -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $sc = $ws.CreateShortcut('%SHORTCUT_DIR%\DSP Toolkit.lnk'); ^
   $sc.TargetPath = '%LAUNCHER%'; ^
   $sc.Description = 'DSP Simulation Toolkit'; ^
   $sc.WorkingDirectory = '%INSTALL_DIR%'; ^
   $sc.Save()"
if %ERRORLEVEL% eq 0 (
    echo OK - Start Menu shortcut created.
) else (
    echo NOTE: Could not create Start Menu shortcut. You can run the app from: "%LAUNCHER%"
)

echo.
echo ==============================
echo   Installation complete!
echo ==============================
echo.
echo   Launch from: Start Menu > DSP Toolkit
echo   Or double-click: %LAUNCHER%
echo.
pause
