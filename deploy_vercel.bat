@echo off
REM SmartSign - Vercel Deployment Script
REM Deploys CSV file to Vercel for SmartSign consumption

echo ================================================================================
echo SMARTSIGN CSV DEPLOYMENT TO VERCEL
echo ================================================================================
echo.

REM Check if Vercel CLI is installed
where vercel >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Vercel CLI not installed
    echo.
    echo Please install Vercel CLI:
    echo   npm install -g vercel
    echo.
    echo Or use the web interface: https://vercel.com
    pause
    exit /b 1
)

REM Verify CSV file exists
if not exist "seminarier.csv" (
    echo [ERROR] seminarier.csv not found
    echo Please run filter_seminarier.py first
    pause
    exit /b 1
)

echo [INFO] CSV file found
for %%A in ("seminarier.csv") do (
    echo        Size: %%~zA bytes
    echo        Modified: %%~tA
)
echo.

REM Deploy to Vercel
echo [INFO] Deploying to Vercel...
echo.

vercel --prod --yes

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================================
    echo [SUCCESS] Deployment complete!
    echo ================================================================================
    echo.
    echo Your CSV is now available at your Vercel URL.
    echo.
    echo Next steps:
    echo   1. Copy your Vercel URL from above
    echo   2. Add /seminarier.csv to the URL
    echo   3. Use this URL in SmartSign CSV Datasource
    echo.
    echo Example URL: https://your-project.vercel.app/seminarier.csv
    echo.
) else (
    echo.
    echo [ERROR] Deployment failed
    echo.
    echo Troubleshooting:
    echo   1. Run 'vercel login' to authenticate
    echo   2. Check your Vercel account status
    echo   3. Verify vercel.json configuration
    echo.
)

echo ================================================================================
pause
