@echo off
REM Windows Startup Script for Handwriting Recognition System

title Handwriting Recognition System

echo ================================================
echo Handwriting Recognition System - FastAPI
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo [*] Python is installed
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo [*] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [!] No virtual environment found
    echo [*] Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo [*] Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
    
    if errorlevel 1 (
        echo [!] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo [*] Creating necessary directories...
if not exist "models" mkdir models
if not exist "data\uploaded\images" mkdir data\uploaded\images
if not exist "data\exports" mkdir data\exports
if not exist "logs" mkdir logs

echo.
echo [*] Starting server...
echo [*] The server will start on http://localhost:8000
echo [*] Press Ctrl+C to stop the server
echo.
echo ================================================
echo.

python server.py

if errorlevel 1 (
    echo.
    echo [!] Server stopped with error
    pause
    exit /b 1
)

pause
