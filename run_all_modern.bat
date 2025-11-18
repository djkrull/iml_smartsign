@echo off
REM SmartSign - Complete Workflow (Modern Hosting)
REM Filters seminars and deploys to Vercel or Railway

echo ================================================================================
echo SMARTSIGN SEMINAR DISPLAY - COMPLETE WORKFLOW (MODERN HOSTING)
echo ================================================================================
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
echo STEP 2: CHOOSE DEPLOYMENT PLATFORM
echo ================================================================================
echo.
echo Choose your deployment platform:
echo   [1] Vercel (recommended for static hosting)
echo   [2] Railway (alternative with web server)
echo   [3] Traditional FTP
echo   [4] Skip deployment (manual upload)
echo.

choice /C 1234 /N /M "Enter your choice (1-4): "
set DEPLOY_CHOICE=%ERRORLEVEL%

echo.

if %DEPLOY_CHOICE%==1 (
    echo [INFO] Deploying to Vercel...
    echo.
    call deploy_vercel.bat
) else if %DEPLOY_CHOICE%==2 (
    echo [INFO] Deploying to Railway...
    echo.
    call deploy_railway.bat
) else if %DEPLOY_CHOICE%==3 (
    echo [INFO] Deploying via FTP...
    echo.
    if exist deploy_to_web.bat (
        call deploy_to_web.bat
    ) else (
        echo [ERROR] deploy_to_web.bat not found
        echo Please configure FTP deployment first
    )
) else (
    echo [INFO] Skipping deployment
    echo.
    echo Please manually upload seminarier.csv to your web server.
    echo File location: C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv
)

echo.
echo ================================================================================
echo WORKFLOW COMPLETE
echo ================================================================================
echo.
echo Next steps:
echo   1. Copy your deployment URL
echo   2. Configure SmartSign CSV Datasource with this URL
echo   3. Verify data appears in SmartSign
echo   4. Check screen display
echo.
pause
