# SmartSign Hybrid Deployment - Railway Setup Guide

**Status:** Ready for deployment
**Date:** 2025-11-18
**Approach:** HTML template hosted on Railway with dynamic CSV loading

---

## Overview

This hybrid approach combines:
- **HTML Template** (`template_simple.html`) - Dynamic seminar display
- **Python Server** (`server.py`) - Railway-hosted web server
- **CSV Data** (`seminarier.csv`) - Auto-generated daily from Excel
- **SmartSign Webpage** - Displays the template URL directly

**Result:** Admin only uploads CSV - all updates are fully automated!

---

## Architecture

```
┌─────────────────────────────────┐
│   Excel Seminar Data            │
│   (Source of Truth)             │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Python Filter Script          │
│   (filter_seminarier.py)        │ ← Runs daily at 00:00
│   - Filters current week        │
│   - Removes past seminars       │
│   - Extracts speakers           │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   seminarier.csv                │
│   (Generated data file)         │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Railway Server                │
│   - Serves HTML template        │
│   - Serves CSV data             │
│   - Serves background & logo    │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   template_simple.html          │
│   - Fetches CSV via JavaScript  │
│   - Parses data dynamically     │
│   - Renders seminar cards       │
│   - Auto-refreshes hourly       │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   SmartSign CMS                 │
│   - Displays webpage at URL     │
│   - Shows rendered template     │
│   - Updates hourly              │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│   Digital Screen                │
│   Displays seminars             │
└─────────────────────────────────┘
```

---

## Phase 1: Local Testing

### Step 1: Verify Files Exist

Check that all required files are present:

```bash
# Navigate to smartsign directory
cd C:\Users\chrwah28.KVA\Development\smartsign

# Verify files
dir /B
```

Required files:
- ✅ `template_simple.html` - HTML template with JavaScript
- ✅ `server.py` - Python web server
- ✅ `seminarier.csv` - CSV data (or run filter_seminarier.py to generate)
- ✅ `iml_background.png` - Background image
- ✅ `iml_logo.png` - Logo image

### Step 2: Run Filter Script

Generate sample CSV data from Excel:

```bash
python filter_seminarier.py
```

Expected output:
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
     Antal seminarier: 6
```

### Step 3: Start Local Server

Run the Python server locally:

```bash
python server.py
```

Expected output:
```
================================================================================
SMARTSIGN TEMPLATE & DATA SERVER
================================================================================
Server running on port 8080
Access template at: http://localhost:8080/
Access CSV data at: http://localhost:8080/seminarier.csv
Health check at: http://localhost:8080/health
Press Ctrl+C to stop
================================================================================
```

### Step 4: Test in Browser

**Test 1: Load template**
- Open: `http://localhost:8080/`
- Should see: "Seminars this week" header with logo
- Should see: Seminar cards loading and populating from CSV
- Wait for JavaScript to parse CSV and render seminars

**Test 2: Access CSV directly**
- Open: `http://localhost:8080/seminarier.csv`
- Should download: CSV file with seminar data
- Verify columns: Title_Original, Title, Speaker, Date, Date_Formatted, Time, Location

**Test 3: Check assets**
- Open: `http://localhost:8080/iml_logo.png`
- Should display: IML logo image
- Open: `http://localhost:8080/iml_background.png`
- Should display: Background image (if available)

**Test 4: Health check**
- Open: `http://localhost:8080/health`
- Should return: "OK"

**Test 5: Auto-refresh**
- Open template at: `http://localhost:8080/`
- Modify `seminarier.csv` (add/remove a seminar)
- Wait up to 60 minutes OR open browser dev tools and check console
- Template should reload automatically

### Troubleshooting Local Testing

**Problem: "Cannot find module"**
```
ModuleNotFoundError: No module named 'pandas'
```
**Solution:** Install dependencies
```bash
pip install pandas openpyxl
```

**Problem: Port 8080 already in use**
```
Address already in use
```
**Solution:** Use different port
```bash
python server.py  # Will try 8080
# Or modify to use different port (edit server.py line 71)
```

**Problem: CSV file not found**
```
FileNotFoundError: CSV file not found: seminarier.csv
```
**Solution:** Run filter script first
```bash
python filter_seminarier.py
```

**Problem: Background/logo images not loading**
- Verify image files exist: `iml_background.png`, `iml_logo.png`
- Check browser console for 404 errors
- Images should be in same directory as `template_simple.html`

---

## Phase 2: Deploy to Railway

### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

Verify installation:
```bash
railway --version
```

### Step 2: Login to Railway

```bash
railway login
```

This opens a browser window. Authenticate with your Railway account.

### Step 3: Create Railway Project (First Time Only)

```bash
railway init
```

Follow prompts to create new project. Creates `railway.json`.

### Step 4: Run Deployment Script

```bash
deploy_railway.bat
```

This script automatically:
1. Runs `filter_seminarier.py` to generate CSV
2. Verifies all required files exist
3. Deploys to Railway via `railway up`

**Expected output:**
```
[INFO] Step 1: Generating CSV from Excel...
... (filter script output) ...
[INFO] Step 2: Verifying required files...
[OK] template_simple.html found
[OK] seminarier.csv found
[OK] server.py found
[OK] iml_background.png found
[OK] iml_logo.png found

[INFO] Step 3: Deploying to Railway...
... (railway deployment output) ...

[SUCCESS] Deployment complete!
```

### Step 5: Get Railway URL

View your Railway project:
```bash
railway open
```

Or check dashboard at https://railway.app

Your URL will be: `https://your-project-name.railway.app`

### Step 6: Test Railway Deployment

**Test 1: Load template from Railway**
- Open: `https://your-project.railway.app/`
- Should see: Seminars displaying (same as local)

**Test 2: Access CSV from Railway**
- Open: `https://your-project.railway.app/seminarier.csv`
- Should download: CSV file

**Test 3: Health check**
- Open: `https://your-project.railway.app/health`
- Should return: "OK"

---

## Phase 3: SmartSign Configuration

### Step 1: Access SmartSign CMS

1. Login to SmartSign CMS admin
2. Navigate to: **Publishing → Channels**

### Step 2: Create Webpage Booking

1. Click **"+ New Booking"** button
2. Fill in details:

| Field | Value | Example |
|-------|-------|---------|
| Name | Seminar Display | Seminar Display |
| Description | Weekly seminars (auto-updated) | Weekly seminars (auto-updated) |
| Start Date | Today or future | 2025-11-18 |
| End Date | (Leave blank) | Permanent |
| Start Time | 00:00 | 00:00 |
| End Time | 23:59 | 23:59 |
| Recurrence | Daily | Daily |
| Days | All days | Mon-Sun |

### Step 3: Add Webpage Content

1. **Content Type:** Select "Webpage"
2. **Webpage URL:** Enter your Railway URL
   - Example: `https://your-project.railway.app/`
3. **Playback Mode:** Select **"Live"**
4. **Snapshot Refresh:** 3600 seconds (1 hour)
   - Matches HTML auto-refresh interval

### Step 4: Assign to Screen

1. **Channel:** Select your digital screen channel
2. **Priority:** Set to High (80-90)
3. **Status:** Enabled/Active

### Step 5: Save & Publish

1. Click **"Save"** button
2. Click **"Publish"** button
3. Booking should appear in schedule with status "Active"

### Step 6: Verify on Screen

1. Go to your digital screen
2. Wait 1-2 minutes for content to appear
3. Verify:
   - Header "Seminars this week" displays
   - Logo shows in correct position (right side, aligned with header)
   - Seminar cards display with all details
   - No errors or blank areas

---

## Phase 4: Set Up Daily Automation

### Windows Task Scheduler Configuration

**Schedule the deployment script to run daily:**

1. Open **Task Scheduler** (Windows key → "Task Scheduler")
2. Click **Create Task**
3. Fill in details:

| Field | Value |
|-------|-------|
| Name | SmartSign Railway Deploy |
| Description | Daily deployment of seminars to Railway |
| Run with highest privileges | ✓ Checked |

4. Go to **Triggers** tab
   - Click **New**
   - Begin task: On a schedule
   - Daily
   - Start time: 00:00 (midnight)
   - Repeat: Daily

5. Go to **Actions** tab
   - Click **New**
   - Program: `C:\Users\chrwah28.KVA\Development\smartsign\deploy_railway.bat`
   - Start in: `C:\Users\chrwah28.KVA\Development\smartsign`

6. Click **OK** to save

### Verify Task Runs

Check Task Scheduler History:
1. Right-click task → Properties
2. Go to **History** tab
3. Should show daily executions with status "The task completed with an exit code of (0)."

---

## Daily Workflow

### Admin Updates Seminars

1. Open Excel seminar export
2. Add new seminars for this week
3. Tag seminars with "website" for public display
4. Save file as: `ProgramExport (2).xlsx` in Downloads folder

### Automated Deployment

At midnight (00:00) every day:
1. Windows Task Scheduler runs `deploy_railway.bat`
2. Script automatically:
   - Filters seminars from Excel
   - Generates CSV with current week only
   - Removes past seminars
   - Deploys to Railway
3. SmartSign fetches updated content within 1 hour
4. Digital screen displays new seminars

**No manual intervention needed!** 🎉

---

## Troubleshooting

### Template not appearing on SmartSign

1. **Check Railway deployment**
   ```bash
   railway logs
   ```
   - Should show "Server running on port {PORT}"

2. **Verify URL is accessible**
   - Open Railway URL in browser
   - Should load template successfully

3. **Check SmartSign booking**
   - Go to Publishing → Bookings
   - Verify URL is correct
   - Verify Mode is "Live"
   - Verify Status is "Active"

4. **Wait for cache expiry**
   - SmartSign caches content
   - Changes appear within 5-10 minutes
   - Force refresh by editing booking

### Seminars not showing on screen

1. **Verify CSV has data**
   ```bash
   type seminarier.csv
   ```
   - Should show seminar rows (not just header)

2. **Test CSV endpoint**
   - Open: `https://your-project.railway.app/seminarier.csv`
   - Should download CSV with data

3. **Check screen connectivity**
   - Verify screen is online
   - Check screen's internet connection
   - Try rebooting screen

4. **Check filtering logic**
   - Run filter script manually: `python filter_seminarier.py`
   - Check output shows expected seminars
   - Verify Excel has "website" tag on seminars

### JavaScript errors in template

1. Open browser console (F12)
2. Check for JavaScript errors
3. Common issues:
   - CSV not found → Verify CSV path in template
   - Parse error → Check CSV format (UTF-8 encoding)
   - Missing assets → Verify images are uploaded

---

## Files Summary

| File | Purpose | Deployed |
|------|---------|----------|
| `template_simple.html` | HTML template with JavaScript CSV loader | ✅ To Railway |
| `server.py` | Python web server | ✅ To Railway |
| `seminarier.csv` | Generated seminar data | ✅ To Railway |
| `iml_background.png` | Background image | ✅ To Railway |
| `iml_logo.png` | Logo image | ✅ To Railway |
| `filter_seminarier.py` | Excel filter script | ✅ Local only (runs daily) |
| `deploy_railway.bat` | Deployment automation | ✅ Local only (runs daily) |

---

## Support & Contacts

**Railway Issues:**
- Railway Docs: https://docs.railway.app
- Railway Support: https://railway.app/support

**SmartSign Issues:**
- SmartSign Docs: https://support.smartsign.com
- SmartSign Support: support@smartsign.com

**IML Issues:**
- IML IT Team: it@iml.se

---

## Checklist

### Pre-Deployment
- [ ] All files present locally
- [ ] Filter script runs successfully
- [ ] Local server test passed
- [ ] Template loads in browser
- [ ] CSV displays correctly

### Railway Deployment
- [ ] Railway CLI installed
- [ ] Railway project created
- [ ] Deployment script runs successfully
- [ ] Railway URL accessible
- [ ] Template displays on Railway

### SmartSign Setup
- [ ] Webpage booking created
- [ ] URL configured correctly
- [ ] Playback mode set to "Live"
- [ ] Channel assigned
- [ ] Status is "Active"

### Field Testing
- [ ] Screen displays template
- [ ] Seminars visible
- [ ] Logo aligned correctly
- [ ] Background image loads
- [ ] No errors on screen

### Automation
- [ ] Task Scheduler task created
- [ ] Task runs daily at 00:00
- [ ] Task history shows successful runs
- [ ] Screen updates show new seminars

---

**Setup Complete!** Your SmartSign display is now fully automated. 🎉

---

**Document Version:** 1.0
**Last Updated:** 2025-11-18
**Status:** Production Ready
