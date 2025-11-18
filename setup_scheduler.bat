@echo off
REM SmartSign Seminar Filter - Task Scheduler Setup
REM This script creates a scheduled task to run the filter script daily at midnight

echo ================================================================================
echo SMARTSIGN SEMINAR FILTER - TASK SCHEDULER SETUP
echo ================================================================================
echo.

REM Delete existing task if it exists (suppress error if not found)
schtasks /delete /tn "SmartSign Seminar Filter" /f >nul 2>&1

echo Creating scheduled task...
echo.

REM Create the scheduled task
schtasks /create /tn "SmartSign Seminar Filter" /tr "python C:\Users\chrwah28.KVA\Development\smartsign\filter_seminarier.py" /sc daily /st 00:00 /ru SYSTEM /f

if %ERRORLEVEL% EQU 0 (
    echo [OK] Scheduled task created successfully!
    echo.
    echo Task Details:
    echo   Name: SmartSign Seminar Filter
    echo   Schedule: Daily at 00:00 (midnight)
    echo   Script: C:\Users\chrwah28.KVA\Development\smartsign\filter_seminarier.py
    echo   Run as: SYSTEM
    echo.
    echo To verify the task:
    echo   schtasks /query /tn "SmartSign Seminar Filter" /v
    echo.
    echo To run the task manually:
    echo   schtasks /run /tn "SmartSign Seminar Filter"
    echo.
) else (
    echo [ERROR] Failed to create scheduled task!
    echo Please run this script as Administrator.
    echo.
    exit /b 1
)

echo ================================================================================
echo SETUP COMPLETE
echo ================================================================================
pause
