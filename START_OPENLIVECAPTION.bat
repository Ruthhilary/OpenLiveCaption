@echo off
echo ========================================
echo   OpenLiveCaption v2.0.0
echo   Starting application...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies... This may take a few minutes.
    echo.
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies
        echo Please run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo Dependencies OK!
echo.
echo Starting OpenLiveCaption...
echo.
echo ========================================
echo   Application is running!
echo   Close this window to exit.
echo ========================================
echo.

REM Run the application
python Main.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   Application exited with an error
    echo ========================================
    echo.
    pause
)
