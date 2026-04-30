@echo off
setlocal EnableDelayedExpansion
title Form Filler — Setup & Launch

echo.
echo  =========================================
echo   INFICON Form Filler
echo  =========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo  [!] Python is not installed or not in PATH.
    echo.
    echo  Please install Python 3.10 or newer from:
    echo    https://www.python.org/downloads/
    echo.
    echo.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo  [OK] Python %PY_VER% found.
echo.

echo  Installing required libraries (this may take a few minutes on first run)...
echo  Please wait — do not close this window.
echo.

python -m pip install --upgrade pip --quiet

python -m pip install ^
    sentence-transformers ^
    pandas ^
    numpy ^
    pymupdf ^
    pypdf ^
    python-docx ^
    scikit-learn ^
    torch ^
    Pillow ^
    --quiet

if errorlevel 1 (
    echo.
    echo  [!] Some packages failed to install.
    echo  Check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo  [OK] All libraries ready.
echo.

echo  Launching Form Filler...
echo.
cd /d "%~dp0"
python app.py

if errorlevel 1 (
    echo.
    echo  [!] The application exited with an error.
    echo  Press any key to close.
    pause
)

endlocal