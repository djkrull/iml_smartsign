@echo off
REM SmartSign System Verification Test
REM This script tests all components of the seminar display system

echo ================================================================================
echo SMARTSIGN SEMINAR DISPLAY - SYSTEM VERIFICATION TEST
echo ================================================================================
echo.

set PASS_COUNT=0
set FAIL_COUNT=0
set WARN_COUNT=0

REM Test 1: Python Installation
echo [TEST 1] Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [PASS] Python is installed
    for /f "tokens=*" %%i in ('python --version') do echo        %%i
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] Python is not installed or not in PATH
    echo        Please install Python 3.8+ from https://www.python.org/downloads/
    set /a FAIL_COUNT+=1
)
echo.

REM Test 2: Required Packages
echo [TEST 2] Checking Python packages...
python -c "import pandas; import openpyxl; print('OK')" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [PASS] Required packages installed (pandas, openpyxl)
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] Required packages missing
    echo        Please run: pip install pandas openpyxl
    set /a FAIL_COUNT+=1
)
echo.

REM Test 3: Script File Exists
echo [TEST 3] Checking filter script exists...
if exist "C:\Users\chrwah28.KVA\Development\smartsign\filter_seminarier.py" (
    echo [PASS] filter_seminarier.py found
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] filter_seminarier.py not found
    echo        Expected location: C:\Users\chrwah28.KVA\Development\smartsign\filter_seminarier.py
    set /a FAIL_COUNT+=1
)
echo.

REM Test 4: Excel File Exists
echo [TEST 4] Checking source Excel file...
if exist "C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx" (
    echo [PASS] Source Excel file found
    echo        C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx
    set /a PASS_COUNT+=1
) else (
    echo [WARN] Source Excel file not found
    echo        Expected: C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx
    echo        This is OK if file location is different - update script path
    set /a WARN_COUNT+=1
)
echo.

REM Test 5: Run Filter Script
echo [TEST 5] Running filter script...
echo        (This may take a few seconds...)
cd /d C:\Users\chrwah28.KVA\Development\smartsign
python filter_seminarier.py >test_output.tmp 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [PASS] Script executed successfully
    type test_output.tmp | findstr /C:"[OK] CSV skapad" >nul
    if %ERRORLEVEL% EQU 0 (
        echo [PASS] CSV file generated
        set /a PASS_COUNT+=2
    ) else (
        echo [FAIL] CSV generation unclear
        set /a FAIL_COUNT+=1
    )
) else (
    echo [FAIL] Script execution failed
    echo        Error output:
    type test_output.tmp
    set /a FAIL_COUNT+=2
)
del test_output.tmp >nul 2>&1
echo.

REM Test 6: Output CSV Exists
echo [TEST 6] Checking output CSV file...
if exist "C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv" (
    echo [PASS] Output CSV file exists
    echo        C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv
    for %%A in ("C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv") do (
        echo        Size: %%~zA bytes
        echo        Modified: %%~tA
    )
    set /a PASS_COUNT+=1
) else (
    echo [FAIL] Output CSV file not found
    set /a FAIL_COUNT+=1
)
echo.

REM Test 7: CSV File Format
echo [TEST 7] Validating CSV format...
if exist "C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv" (
    findstr /C:"Title,Speaker,Date" "C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo [PASS] CSV has correct header columns
        set /a PASS_COUNT+=1
    ) else (
        echo [FAIL] CSV header format incorrect
        set /a FAIL_COUNT+=1
    )
) else (
    echo [SKIP] CSV file not available
)
echo.

REM Test 8: Scheduled Task
echo [TEST 8] Checking scheduled task...
schtasks /query /tn "SmartSign Seminar Filter" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [PASS] Scheduled task exists
    echo        Task Name: SmartSign Seminar Filter
    for /f "tokens=2 delims=:" %%i in ('schtasks /query /tn "SmartSign Seminar Filter" /fo list ^| findstr /C:"Status"') do (
        echo        Status: %%i
    )
    set /a PASS_COUNT+=1
) else (
    echo [WARN] Scheduled task not configured
    echo        Run setup_scheduler.bat as Administrator to configure
    set /a WARN_COUNT+=1
)
echo.

REM Test 9: Deployment Script
echo [TEST 9] Checking deployment script...
if exist "C:\Users\chrwah28.KVA\Development\smartsign\deploy_to_web.bat" (
    findstr /C:"your-ftp-username" "C:\Users\chrwah28.KVA\Development\smartsign\deploy_to_web.bat" >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo [WARN] Deployment script not yet configured
        echo        Edit deploy_to_web.bat with your FTP credentials
        set /a WARN_COUNT+=1
    ) else (
        echo [PASS] Deployment script configured
        set /a PASS_COUNT+=1
    )
) else (
    echo [WARN] Deployment script not found
    set /a WARN_COUNT+=1
)
echo.

REM Test 10: Documentation
echo [TEST 10] Checking documentation...
set DOC_COUNT=0
if exist "README.md" set /a DOC_COUNT+=1
if exist "QUICKSTART.md" set /a DOC_COUNT+=1
if exist "docs\SETUP.md" set /a DOC_COUNT+=1
if exist "docs\SMARTSIGN_CONFIG.md" set /a DOC_COUNT+=1
if exist "docs\PRD_SmartSign_Seminarier.md" set /a DOC_COUNT+=1
if exist "docs\ADR_SmartSign_Seminarier.md" set /a DOC_COUNT+=1

if %DOC_COUNT% GEQ 5 (
    echo [PASS] Complete documentation available
    echo        %DOC_COUNT% documentation files found
    set /a PASS_COUNT+=1
) else (
    echo [WARN] Some documentation files missing
    echo        Found %DOC_COUNT% of 6 expected files
    set /a WARN_COUNT+=1
)
echo.

REM Summary
echo ================================================================================
echo TEST SUMMARY
echo ================================================================================
echo.
echo Passed:   %PASS_COUNT%
echo Failed:   %FAIL_COUNT%
echo Warnings: %WARN_COUNT%
echo.

if %FAIL_COUNT% EQU 0 (
    if %WARN_COUNT% EQU 0 (
        echo [SUCCESS] All tests passed! System is fully configured.
        echo.
        echo Next steps:
        echo   1. Configure FTP credentials in deploy_to_web.bat
        echo   2. Upload CSV to web server
        echo   3. Configure SmartSign CMS (see docs\SMARTSIGN_CONFIG.md)
        echo   4. Verify display on screens
    ) else (
        echo [SUCCESS] Core functionality working, minor warnings present.
        echo.
        echo Review warnings above and address as needed.
        echo See QUICKSTART.md or docs\SETUP.md for guidance.
    )
) else (
    echo [FAILURE] %FAIL_COUNT% tests failed. Please fix errors before proceeding.
    echo.
    echo See above for specific failures.
    echo Consult docs\SETUP.md for troubleshooting guidance.
)

echo.
echo ================================================================================
pause
