@echo off
REM SmartSign Admin Server Launcher
REM This script starts the admin upload interface

cls
echo.
echo ================================================================================
echo SMARTSIGN ADMIN SERVER
echo ================================================================================
echo.
echo Starting admin interface...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Flask is not installed. Installing dependencies...
    pip install -r admin_requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Railway CLI not found. You can still update CSV locally.
    echo Install Railway CLI with: npm install -g @railway/cli
    echo.
)

echo.
echo ================================================================================
echo Admin Server Starting...
echo ================================================================================
echo.
echo Your browser should open automatically.
echo If not, open: http://localhost:9000
echo.
echo Instructions:
echo 1. Drag and drop your Excel file into the upload area
echo 2. Click "Update & Deploy"
echo 3. Wait for confirmation
echo 4. Your display updates automatically!
echo.
echo Press Ctrl+C to stop the server.
echo.
echo ================================================================================
echo.

python admin_server.py
