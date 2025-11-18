@echo off
REM SmartSign CSV Deployment Script
REM This script uploads the generated CSV file to the web server

echo ================================================================================
echo SMARTSIGN CSV DEPLOYMENT
echo ================================================================================
echo.

REM Configuration - UPDATE THESE VALUES
set LOCAL_CSV=C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv
set WEB_SERVER=ftp.iml.se
set WEB_USER=your-ftp-username
set WEB_PASS=your-ftp-password
set REMOTE_DIR=/public_html/smartsign
set REMOTE_FILE=seminarier.csv

REM Verify local file exists
if not exist "%LOCAL_CSV%" (
    echo [ERROR] Local CSV file not found: %LOCAL_CSV%
    echo Please run filter_seminarier.py first.
    pause
    exit /b 1
)

echo Local file: %LOCAL_CSV%
echo Remote server: %WEB_SERVER%
echo Remote directory: %REMOTE_DIR%
echo.
echo Creating FTP command file...

REM Create temporary FTP commands file
echo open %WEB_SERVER% > ftp_commands.tmp
echo %WEB_USER% >> ftp_commands.tmp
echo %WEB_PASS% >> ftp_commands.tmp
echo cd %REMOTE_DIR% >> ftp_commands.tmp
echo binary >> ftp_commands.tmp
echo put "%LOCAL_CSV%" %REMOTE_FILE% >> ftp_commands.tmp
echo bye >> ftp_commands.tmp

echo Uploading file via FTP...
echo.

REM Execute FTP upload
ftp -s:ftp_commands.tmp

REM Check if upload was successful
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] File uploaded successfully!
    echo.
    echo Verify at: https://iml.se/smartsign/seminarier.csv
    echo.
) else (
    echo.
    echo [ERROR] Upload failed!
    echo Check FTP credentials and server settings.
    echo.
)

REM Cleanup temporary file
if exist ftp_commands.tmp del ftp_commands.tmp

echo ================================================================================
echo DEPLOYMENT COMPLETE
echo ================================================================================
pause
