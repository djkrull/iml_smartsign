@echo off
REM SmartSign - Complete Workflow Script
REM This script runs the filter and deploys to web server in one step

echo ================================================================================
echo SMARTSIGN SEMINAR DISPLAY - COMPLETE WORKFLOW
echo ================================================================================
echo.
echo This script will:
echo   1. Filter seminars from Excel file
echo   2. Generate CSV file
echo   3. Upload CSV to web server
echo.

REM Step 1: Run filter script
echo ================================================================================
echo STEP 1: FILTERING SEMINARS
echo ================================================================================
echo.

cd /d C:\Users\chrwah28.KVA\Development\smartsign
python filter_seminarier.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Filter script failed!
    echo Please check Python installation and Excel file path.
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo STEP 2: DEPLOYING TO WEB SERVER
echo ================================================================================
echo.

REM Step 2: Deploy to web server (if configured)
if exist deploy_to_web.bat (
    REM Check if deployment is configured
    findstr /C:"your-ftp-username" deploy_to_web.bat >nul
    if %ERRORLEVEL% EQU 0 (
        echo [INFO] Web deployment not yet configured.
        echo Please edit deploy_to_web.bat with your FTP credentials.
        echo.
        echo For now, manually upload:
        echo   From: C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv
        echo   To: Your web server (e.g., https://iml.se/smartsign/seminarier.csv)
        echo.
    ) else (
        call deploy_to_web.bat
    )
) else (
    echo [INFO] deploy_to_web.bat not found.
    echo Please manually upload seminarier.csv to your web server.
    echo.
)

echo ================================================================================
echo WORKFLOW COMPLETE
echo ================================================================================
echo.
echo Next steps:
echo   1. Verify CSV file: C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv
echo   2. Upload to web server (if not automated)
echo   3. Check SmartSign datasource refreshes automatically
echo   4. Verify display on screens
echo.
pause
