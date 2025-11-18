# SmartSign Seminar Display System - Setup Guide

**Version:** 1.0
**Last Updated:** 2025-11-17
**Target Audience:** IT Administrators, System Integrators

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [SmartSign CMS Setup](#smartsign-cms-setup)
6. [Testing and Verification](#testing-and-verification)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance](#maintenance)

---

## Overview

This guide walks through complete setup of the automated SmartSign seminar display system, from Python installation to SmartSign CMS configuration.

**System Components:**
1. Python filtering script (`filter_seminarier.py`)
2. Windows Task Scheduler (daily automation)
3. Web server (CSV hosting)
4. SmartSign CMS (datasource + template + booking)

**Expected Setup Time:** 1-2 hours

---

## Prerequisites

### Required Software

| Software | Version | Download | Notes |
|----------|---------|----------|-------|
| Python | 3.8 or higher | https://www.python.org/downloads/ | Check "Add to PATH" during install |
| SmartSign CMS | 11.x | (Existing installation) | Must have admin access |
| Web Server | Any with HTTPS | (Existing IML server) | Need FTP/SSH access |

### Required Access

- [ ] Windows administrator privileges (for Task Scheduler)
- [ ] Access to source Excel file location
- [ ] Web server FTP/SSH credentials
- [ ] SmartSign CMS admin login
- [ ] Network access from SmartSign to web server

### Required Knowledge

- Basic Python environment setup
- Windows Task Scheduler configuration
- FTP/SSH file transfer
- SmartSign CMS administration

---

## Installation Steps

### Step 1: Verify Python Installation

Open Command Prompt and verify Python is installed:

```cmd
python --version
```

**Expected output:** `Python 3.8.x` or higher

If Python is not installed:
1. Download from https://www.python.org/downloads/
2. Run installer
3. **Important:** Check "Add Python to PATH" option
4. Verify installation with `python --version`

### Step 2: Install Required Python Packages

Install pandas and openpyxl libraries:

```cmd
pip install pandas openpyxl
```

**Expected output:**
```
Successfully installed pandas-x.x.x openpyxl-x.x.x
```

**Verification:**
```cmd
python -c "import pandas; import openpyxl; print('OK')"
```

Should print: `OK`

### Step 3: Verify Script Location

Ensure the script is in the correct location:

```
C:\Users\chrwah28.KVA\Development\smartsign\filter_seminarier.py
```

### Step 4: Update File Paths in Script

Open `filter_seminarier.py` and verify/update these paths:

```python
# Line 72-73
excel_file = r"C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx"
output_csv = r"C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv"
```

**Adjust these paths if:**
- Excel file is in a different location
- You want output CSV elsewhere

### Step 5: Test Manual Execution

Run the script manually to verify it works:

```cmd
cd C:\Users\chrwah28.KVA\Development\smartsign
python filter_seminarier.py
```

**Expected output:**
```
================================================================================
AUTOMATISK SEMINARIE-FILTRERING FOR SMARTSIGN
================================================================================

Laser Excel: C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx
Totalt antal seminarier i Excel: 175

Denna vecka: 2025-11-17 till 2025-11-21
Idag: 2025-11-17 kl 15:32

Seminarier denna vecka (framtida, taggade med 'website'): 6

[OK] CSV skapad: C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv
```

**Verify output file exists:**
```cmd
dir C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv
```

---

## Configuration

### Configure Windows Task Scheduler

#### Option 1: Using Task Scheduler GUI

1. **Open Task Scheduler:**
   - Press `Win + R`
   - Type `taskschd.msc`
   - Press Enter

2. **Create New Task:**
   - Click "Create Basic Task" in right panel
   - Name: `SmartSign Seminar Filter`
   - Description: `Daily filtering of seminars for SmartSign display`

3. **Set Trigger:**
   - Trigger type: **Daily**
   - Start date: **Today**
   - Start time: **00:00:00** (midnight)
   - Recur every: **1 days**

4. **Set Action:**
   - Action: **Start a program**
   - Program/script: `python`
   - Add arguments: `C:\Users\chrwah28.KVA\Development\smartsign\filter_seminarier.py`
   - Start in: `C:\Users\chrwah28.KVA\Development\smartsign`

5. **Advanced Settings:**
   - Check: "Run whether user is logged on or not"
   - Check: "Run with highest privileges"
   - Configure for: **Windows 10**

6. **Save Task:**
   - Enter your Windows password when prompted
   - Click OK

#### Option 2: Using Command Line

Run this command in **Administrator Command Prompt**:

```cmd
schtasks /create /tn "SmartSign Seminar Filter" /tr "python C:\Users\chrwah28.KVA\Development\smartsign\filter_seminarier.py" /sc daily /st 00:00 /ru SYSTEM
```

**Verify task created:**
```cmd
schtasks /query /tn "SmartSign Seminar Filter"
```

#### Test the Scheduled Task

Run the task manually to verify it works:

```cmd
schtasks /run /tn "SmartSign Seminar Filter"
```

**Check execution in Task Scheduler:**
1. Open Task Scheduler
2. Find "SmartSign Seminar Filter"
3. View "History" tab (enable if needed)
4. Verify successful execution

---

### Configure Web Server Deployment

The CSV file must be uploaded to a web server for SmartSign to access.

#### Option 1: Manual FTP Upload (for testing)

1. **Connect to web server via FTP:**
   ```
   Host: ftp.iml.se (example)
   Username: [your-username]
   Password: [your-password]
   ```

2. **Upload file:**
   - Local file: `C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv`
   - Remote path: `/public_html/smartsign/seminarier.csv` (example)

3. **Verify URL access:**
   - Open browser
   - Navigate to: `https://iml.se/smartsign/seminarier.csv` (example)
   - Should download CSV file

#### Option 2: Automated FTP Upload (recommended)

Create a batch script for automated upload: `upload_csv.bat`

```batch
@echo off
REM FTP Upload Script for SmartSign CSV

set LOCAL_FILE=C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv
set FTP_HOST=ftp.iml.se
set FTP_USER=your-username
set FTP_PASS=your-password
set REMOTE_DIR=/public_html/smartsign

REM Create FTP command file
echo open %FTP_HOST% > ftp_commands.txt
echo %FTP_USER% >> ftp_commands.txt
echo %FTP_PASS% >> ftp_commands.txt
echo cd %REMOTE_DIR% >> ftp_commands.txt
echo binary >> ftp_commands.txt
echo put %LOCAL_FILE% >> ftp_commands.txt
echo bye >> ftp_commands.txt

REM Execute FTP upload
ftp -s:ftp_commands.txt

REM Cleanup
del ftp_commands.txt

echo Upload complete!
```

**Update Task Scheduler to run both scripts:**

Change the scheduled task action to run a wrapper batch file:

`run_filter_and_upload.bat`:
```batch
@echo off
cd C:\Users\chrwah28.KVA\Development\smartsign
python filter_seminarier.py
call upload_csv.bat
```

#### Option 3: Using WinSCP/rsync (recommended for production)

If using WinSCP for automation:

```batch
"C:\Program Files (x86)\WinSCP\WinSCP.com" /script=upload_script.txt
```

`upload_script.txt`:
```
open sftp://username:password@iml.se/
cd /public_html/smartsign
put C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv
exit
```

---

## SmartSign CMS Setup

### Step 1: Create CSV Datasource

1. **Login to SmartSign CMS:**
   - Navigate to SmartSign admin URL
   - Login with admin credentials

2. **Navigate to Datasources:**
   - Main menu → **Content** → **Datasources**

3. **Create New Datasource:**
   - Click **"+ New Datasource"**
   - Type: **CSV Datasource**
   - Name: `Seminarier`
   - Description: `Weekly seminar data for digital displays`

4. **Configure Datasource:**
   - **Data Source URL:** `https://iml.se/smartsign/seminarier.csv` (your actual URL)
   - **Fetch method:** `Through Smartsign server` (recommended)
   - **Update interval:** `3600` seconds (1 hour)
   - **Encoding:** `UTF-8`
   - **First row is header:** ✓ (checked)

5. **Map Columns:**
   - Column 1: `Title_Original` (not used in template, for reference)
   - Column 2: `Title`
   - Column 3: `Speaker`
   - Column 4: `Date` (ISO format, for sorting)
   - Column 5: `Date_Formatted`
   - Column 6: `Time`
   - Column 7: `Location`

6. **Test Connection:**
   - Click **"Test"** button
   - Should show: "Successfully fetched X rows"

7. **Save Datasource**

### Step 2: Create Smart Media Template

1. **Navigate to Template Creator:**
   - Main menu → **Design** → **Template Creator**

2. **Create New Template:**
   - Click **"+ New Template"**
   - Name: `Seminar Display`
   - Type: **Smart Media**
   - Orientation: **Landscape** (or match your screen)
   - Resolution: **1920x1080** (or match your screen)

3. **Design Template Layout:**

   Use the template designer to create layout. Example structure:

   ```
   +--------------------------------------------------+
   |  SEMINARS THIS WEEK                              |
   +--------------------------------------------------+
   |                                                  |
   |  {{Date_Formatted}} • {{Time}}                   |
   |  {{Title}}                                       |
   |  Speaker: {{Speaker}}                            |
   |  Location: {{Location}}                          |
   |                                                  |
   +--------------------------------------------------+
   ```

4. **Add Text Elements:**

   For each seminar row, add text elements with these bindings:

   **Element 1: Header**
   - Text: "SEMINARS THIS WEEK"
   - Font: Large, bold
   - Position: Top of screen

   **Element 2: Date & Time**
   - Text: `{{Date_Formatted}} • {{Time}}`
   - Data binding: **CSV Value**
   - Datasource: `Seminarier`
   - Column: `Date_Formatted` and `Time`
   - Font: Medium, semi-bold

   **Element 3: Title**
   - Text: `{{Title}}`
   - Data binding: **CSV Value**
   - Datasource: `Seminarier`
   - Column: `Title`
   - Font: Large, bold

   **Element 4: Speaker**
   - Text: `Speaker: {{Speaker}}`
   - Data binding: **CSV Value**
   - Datasource: `Seminarier`
   - Column: `Speaker`
   - Font: Medium, regular

   **Element 5: Location**
   - Text: `Location: {{Location}}`
   - Data binding: **CSV Value**
   - Datasource: `Seminarier`
   - Column: `Location`
   - Font: Medium, regular

5. **Configure Repeating/Scrolling:**

   - Set template to **scroll** or **paginate** through all seminar rows
   - Display duration: **15 seconds** per seminar
   - Transition: **Fade** or **Slide**

6. **Preview Template:**
   - Click **"Preview"**
   - Verify data appears correctly
   - Check formatting and layout

7. **Save Template**

### Step 3: Create Booking

1. **Navigate to Bookings:**
   - Main menu → **Schedule** → **Bookings**

2. **Create New Booking:**
   - Click **"+ New Booking"**
   - Name: `Seminar Display - Permanent`

3. **Configure Booking:**
   - **Content:** Select `Seminar Display` template
   - **Channel:** Select your screen's channel
   - **Start date:** Today
   - **End date:** (Leave blank for permanent, or set far future date)
   - **Schedule:** All day, every day
   - **Priority:** High

4. **Save Booking**

5. **Verify Booking Active:**
   - Check booking appears in schedule
   - Verify it's marked as "Active"

---

## Testing and Verification

### End-to-End Test

1. **Modify Source Excel:**
   - Open `ProgramExport (2).xlsx`
   - Add a test seminar for this week with "website" tag
   - Save

2. **Run Filter Script:**
   ```cmd
   python filter_seminarier.py
   ```

3. **Verify CSV Output:**
   - Open `seminarier.csv`
   - Confirm test seminar appears

4. **Upload to Web Server:**
   - Upload `seminarier.csv` to web server
   - Verify accessible via browser

5. **Trigger SmartSign Update:**
   - In SmartSign CMS, go to Datasources
   - Click "Refresh" on `Seminarier` datasource
   - Verify row count updates

6. **Check Screen Display:**
   - View your SmartSign screen
   - Confirm test seminar appears
   - Verify formatting is correct

### Automated Test Checklist

- [ ] Script runs successfully manually
- [ ] CSV file is generated with correct data
- [ ] File uploads to web server successfully
- [ ] URL is accessible from browser
- [ ] SmartSign datasource fetches data
- [ ] Template displays data correctly
- [ ] Booking is active on screen
- [ ] Scheduled task runs at midnight
- [ ] Updates propagate within 24 hours

---

## Troubleshooting

### Script Execution Issues

#### Problem: `ModuleNotFoundError: No module named 'pandas'`

**Solution:**
```cmd
pip install pandas openpyxl
```

#### Problem: `FileNotFoundError: Excel file not found`

**Solution:**
- Verify Excel file path in script (line 72)
- Check file exists at specified location
- Verify file permissions

#### Problem: `UnicodeEncodeError` in console output

**Solution:**
- This is a Windows console limitation (emoji characters)
- Does NOT affect CSV output
- Script still works correctly
- Can ignore or redirect output to file

#### Problem: Script returns 0 seminars

**Possible causes:**
1. No seminars scheduled this week → **Expected behavior**
2. No seminars tagged with "website" → Check Excel Tag(s) column
3. All seminars in the past → **Expected behavior**
4. Wrong week calculation → Check system date/time

**Debug:**
```python
# Add print statements to script
print(f"Total seminars: {len(df)}")
print(f"This week: {len(df_week)}")
print(f"Tagged 'website': {len(df_tagged)}")
```

### Task Scheduler Issues

#### Problem: Task shows "Ready" but never runs

**Solution:**
1. Check task trigger is configured correctly
2. Verify start time is correct
3. Ensure task is enabled
4. Check "History" tab for errors

#### Problem: Task runs but fails

**Solution:**
1. Check Task History for error codes
2. Verify Python is in system PATH
3. Run task manually with "Run" button to see errors
4. Check user account has permissions

#### Problem: Task runs but no output

**Solution:**
- Redirect output to log file:
  ```cmd
  python filter_seminarier.py > C:\Logs\smartsign.log 2>&1
  ```

### Web Server Issues

#### Problem: CSV file not accessible via URL

**Solution:**
1. Verify FTP upload succeeded
2. Check file permissions (should be readable)
3. Verify correct path and filename
4. Test URL in browser
5. Check web server logs

#### Problem: SmartSign can't fetch CSV

**Solution:**
1. Verify URL is publicly accessible
2. Check firewall rules
3. Verify HTTPS certificate is valid
4. Test with "Through Smartsign server" fetch method
5. Check SmartSign CMS logs

### SmartSign CMS Issues

#### Problem: Datasource shows "Error fetching data"

**Solution:**
1. Test URL manually in browser
2. Check datasource URL configuration
3. Try "Direct" vs "Through Smartsign server"
4. Verify CSV encoding (UTF-8)
5. Check first row is header row

#### Problem: Template shows no data

**Solution:**
1. Verify datasource is fetching data (check row count)
2. Check data bindings in template
3. Verify column names match exactly
4. Preview template to see errors
5. Check template is using correct datasource

#### Problem: Screen shows old data

**Solution:**
1. Check datasource update interval (should be 3600 seconds)
2. Manually refresh datasource
3. Verify booking is active
4. Check screen is online and connected
5. Verify booking priority is high enough

---

## Maintenance

### Regular Maintenance Tasks

#### Daily (Automated)
- Script runs at 00:00 via Task Scheduler
- CSV file generated and uploaded
- SmartSign fetches updated data

#### Weekly (Manual)
- [ ] Verify seminars displaying correctly
- [ ] Check Task Scheduler history for failures
- [ ] Verify web server access logs show SmartSign fetches

#### Monthly (Manual)
- [ ] Review script execution logs
- [ ] Update source Excel file location if changed
- [ ] Verify all system components functioning
- [ ] Check for Python/library updates

### Updating the Source Excel File

When seminar program coordinator updates the Excel file:

1. **Save file to standard location:**
   ```
   C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx
   ```

2. **Changes propagate automatically:**
   - Next midnight (00:00): Script runs
   - CSV regenerated with new data
   - Uploaded to web server
   - SmartSign fetches within 1 hour

3. **For urgent updates:**
   - Run script manually: `python filter_seminarier.py`
   - Upload CSV manually via FTP
   - Refresh datasource in SmartSign CMS

### Updating the Script

If you need to modify `filter_seminarier.py`:

1. **Make changes to script**
2. **Test manually:**
   ```cmd
   python filter_seminarier.py
   ```
3. **Verify output CSV is correct**
4. **No need to update Task Scheduler** (uses same script path)

### Logs and Monitoring

**Enable logging to file:**

Modify Task Scheduler action:
```cmd
python filter_seminarier.py >> C:\Logs\smartsign_filter.log 2>&1
```

Create log directory:
```cmd
mkdir C:\Logs
```

**Log rotation:**
- Use Windows built-in log rotation or third-party tool
- Archive logs monthly
- Keep last 12 months

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    SEMINAR PROGRAM COORDINATOR              │
│              (Updates Excel file with seminars)             │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
               ┌──────────────────────────┐
               │  ProgramExport (2).xlsx  │
               │  (Master seminar data)   │
               └─────────────┬────────────┘
                             │
                             ▼
               ┌──────────────────────────┐
               │ Windows Task Scheduler   │
               │  (Daily at 00:00)        │
               └─────────────┬────────────┘
                             │
                             ▼
               ┌──────────────────────────┐
               │  filter_seminarier.py    │
               │  - Filter current week   │
               │  - Filter "website" tag  │
               │  - Extract speaker       │
               │  - Format data           │
               └─────────────┬────────────┘
                             │
                             ▼
               ┌──────────────────────────┐
               │   seminarier.csv         │
               │  (Filtered output)       │
               └─────────────┬────────────┘
                             │
                             ▼
               ┌──────────────────────────┐
               │  FTP/SFTP Upload         │
               └─────────────┬────────────┘
                             │
                             ▼
               ┌──────────────────────────┐
               │     Web Server           │
               │  https://iml.se/...      │
               └─────────────┬────────────┘
                             │
                             ▼
               ┌──────────────────────────┐
               │   SmartSign CMS          │
               │  - CSV Datasource        │
               │  - Updates hourly        │
               └─────────────┬────────────┘
                             │
                             ▼
               ┌──────────────────────────┐
               │  Smart Media Template    │
               │  (Seminar Display)       │
               └─────────────┬────────────┘
                             │
                             ▼
               ┌──────────────────────────┐
               │   Booking/Schedule       │
               │  (Permanent)             │
               └─────────────┬────────────┘
                             │
                             ▼
               ┌──────────────────────────┐
               │   Digital Screen         │
               │  (Displays seminars)     │
               └──────────────────────────┘
```

---

## Security Considerations

### Sensitive Information

**CSV file contains:**
- Public seminar information
- Speaker names (public figures)
- No sensitive or personal data

**Security measures:**
- CSV hosted on public web server (appropriate for public data)
- No authentication required for CSV access
- HTTPS encrypts data in transit

### Task Scheduler Security

**Run as:** SYSTEM or dedicated service account
**Permissions needed:**
- Read access to Excel file
- Write access to output directory
- Network access for FTP/upload

### Web Server Security

**Recommendations:**
- Use HTTPS (required for SmartSign)
- Valid SSL certificate
- Standard web server hardening
- Monitor access logs

---

## Support and Contact

**For technical issues:**
- IML IT Team: it@iml.se
- SmartSign Support: support@smartsign.com

**Documentation:**
- PRD: `docs/PRD_SmartSign_Seminarier.md`
- ADR: `docs/ADR_SmartSign_Seminarier.md`
- This file: `docs/SETUP.md`

**Version Control:**
- Script location: `C:\Users\chrwah28.KVA\Development\smartsign\`
- Backup recommended before changes

---

## Appendix: Quick Reference

### File Paths

| File | Path |
|------|------|
| Filter script | `C:\Users\chrwah28.KVA\Development\smartsign\filter_seminarier.py` |
| Source Excel | `C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx` |
| Output CSV | `C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv` |
| Documentation | `C:\Users\chrwah28.KVA\Development\smartsign\docs\` |

### Key Commands

```cmd
# Run script manually
python filter_seminarier.py

# Check Python version
python --version

# Install dependencies
pip install pandas openpyxl

# Run scheduled task manually
schtasks /run /tn "SmartSign Seminar Filter"

# View task details
schtasks /query /tn "SmartSign Seminar Filter" /v
```

### SmartSign URLs (Example)

- **CSV URL:** `https://iml.se/smartsign/seminarier.csv`
- **SmartSign CMS:** `https://cms.smartsign.com/`
- **Screen URL:** (Your screen's SmartSign URL)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-17
**Maintained By:** IML IT Team
