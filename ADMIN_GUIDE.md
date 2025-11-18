# SmartSign Admin Guide - Excel Upload Tool

**Version:** 1.0
**Date:** November 18, 2025

---

## 🚀 Quick Start (30 seconds)

### Step 1: Start Admin Server

Double-click:
```
C:\Users\chrwah28.KVA\Development\smartsign\run_admin.bat
```

Or open Command Prompt and run:
```bash
cd C:\Users\chrwah28.KVA\Development\smartsign
python admin_server.py
```

### Step 2: Upload Excel File

1. Your browser opens automatically to `http://localhost:9000`
2. Drag your Excel file into the upload area
3. Click **"Update & Deploy"**
4. Wait for success message
5. **Done!** Display updates automatically within 1-2 minutes

---

## 📋 How It Works

```
Admin Workflow:
   Your Excel File
          ↓
   [Drag & Drop to Admin Page]
          ↓
   [Click "Update & Deploy"]
          ↓
   Admin Server Processes File
   - Extracts seminars tagged "website"
   - Filters to current week only
   - Removes past events
          ↓
   Generates seminarier.csv
          ↓
   Deploys to Railway
          ↓
   SmartSign Fetches New Data
          ↓
   Display Updates Automatically ✅
```

---

## 📊 What Gets Uploaded

### Your Excel File Should Have

| Column | Required | Example |
|--------|----------|---------|
| **Title** | Yes | Finite element methods for PDEs |
| **Speaker** | Yes | Björn Stinner, University of Warwick |
| **Date** | Yes | 2025-11-18 |
| **Time** | Yes | 09:30-10:30 |
| **Location** | Yes | Kuskvillan |
| **Tag(s)** | Yes | website |

⚠️ **CRITICAL:** Seminar must have **"website"** tag!
- Other tags like "internal" or "external" are ignored
- Without "website" tag, seminar won't display

### What the System Does

✅ **Automatically filters:**
- Only seminars tagged "website"
- Only this week's seminars (Monday-Sunday)
- Only future events (removes past seminars)
- Sorts by date/time

❌ **Excludes:**
- Seminars without "website" tag
- Seminars from past weeks
- Events that already happened

---

## 🎯 Admin Workflow Examples

### Scenario 1: Add New Seminar

**What admin does:**
1. Open Excel file
2. Add new seminar row:
   - Title: "Machine Learning Applications"
   - Speaker: "Dr. Jane Smith"
   - Date: 2025-11-20 (this week)
   - Time: 14:00-15:00
   - Location: Main Hall
   - Tag: **website** ← Important!
3. Save Excel
4. Go to http://localhost:9000
5. Drag Excel file → Click "Update & Deploy"
6. Done!

**Result:** Seminar appears on display within 2 minutes

---

### Scenario 2: Update Existing Seminar

**What admin does:**
1. Find seminar in Excel
2. Update details (speaker, time, location, etc.)
3. Make sure tag is still "website"
4. Save Excel
5. Upload via admin tool

**Result:** Display updates with new information

---

### Scenario 3: Remove Seminar

**What admin does:**
1. Find seminar in Excel
2. Delete entire row
3. Save Excel
4. Upload via admin tool

**Result:** Seminar disappears from display

---

### Scenario 4: Tag-Based Publishing

**What admin does:**
1. Add multiple seminars to Excel
2. Tag seminars with:
   - "website" → Shows on digital display
   - "internal" → Shows only internally
   - "hidden" → Doesn't show anywhere
3. Save Excel
4. Upload via admin tool

**Result:** Only "website" tagged seminars show on digital display

---

## ⚙️ Installation & Setup

### First Time Setup

#### Step 1: Install Admin Dependencies

Open Command Prompt in smartsign directory:
```bash
cd C:\Users\chrwah28.KVA\Development\smartsign
pip install -r admin_requirements.txt
```

This installs:
- Flask (web server)
- Flask-CORS (allows file uploads)
- pandas (Excel processing)
- openpyxl (Excel reading)

#### Step 2: Verify Railway CLI

Make sure Railway CLI is installed:
```bash
railway --version
```

If not installed:
```bash
npm install -g @railway/cli
```

And login to Railway:
```bash
railway login
```

#### Step 3: Test Admin Server

Run the admin server:
```bash
python admin_server.py
```

You should see:
```
================================================================================
SMARTSIGN ADMIN SERVER
================================================================================
Starting admin interface...
Open your browser and go to: http://localhost:9000
```

Browser should open automatically. If not, manually go to `http://localhost:9000`

---

## 🖥️ Using the Admin Interface

### The Upload Page

```
┌─────────────────────────────────────────────────────┐
│                 SmartSign Admin                      │
│          Update your seminar display in one click    │
│                                                      │
│     ┌─────────────────────────────────────────┐    │
│     │                 📁                        │    │
│     │   Drop your Excel file here             │    │
│     │        or click to browse               │    │
│     └─────────────────────────────────────────┘    │
│                                                      │
│   [Update & Deploy]  [Clear]                        │
│                                                      │
│   ℹ️ How it works:                                  │
│   ✓ Drag your Excel file here                       │
│   ✓ Click "Update & Deploy"                         │
│   ✓ System converts to CSV                          │
│   ✓ Deploys to production                           │
│   ✓ Display updates automatically                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Step-by-Step

1. **Open Admin Tool**
   - Double-click `run_admin.bat` OR
   - Run `python admin_server.py`

2. **Select Excel File**
   - Drag Excel file onto the drop zone, OR
   - Click the zone to browse and select

3. **See Confirmation**
   - File name and size appear
   - "Update & Deploy" button becomes active

4. **Click "Update & Deploy"**
   - Shows loading spinner
   - Progress bar animates

5. **Wait for Result**
   - **Success**: Green message with confirmation
   - **Error**: Red message with details
   - Explains what went wrong if needed

6. **Done!**
   - Form clears automatically
   - Display updates within 1-2 minutes

---

## ❓ Troubleshooting

### Problem: Page doesn't load

**Solution:**
1. Make sure `admin_server.py` is running
2. Check for error messages in Command Prompt
3. Try manually opening `http://localhost:9000`

### Problem: File upload fails

**Possible reasons:**

| Error | Solution |
|-------|----------|
| "Invalid file type" | Must upload Excel (.xlsx or .xls) |
| "File is too large" | File exceeds 10MB. Reduce file size. |
| "Railway CLI not found" | Install: `npm install -g @railway/cli` |
| "Connection error" | Ensure admin server is running |

### Problem: Seminars don't appear on display

**Checklist:**

- [ ] Did you tag seminars with "website"? (Case insensitive)
- [ ] Is the seminar this week? (Monday-Sunday of current week)
- [ ] Is the seminar in the future? (Not a past event)
- [ ] Did upload complete successfully? (Green success message)
- [ ] Did you wait 1-2 minutes for display to update?

**Debug:**

1. Check the CSV file was created:
   ```bash
   cat seminarier.csv
   ```
   Should show your seminars with data

2. Verify Railway deployment:
   ```bash
   railway logs --lines 20
   ```
   Should show "SMARTSIGN TEMPLATE & DATA SERVER" running

3. Test production URL in browser:
   ```
   https://imlsmartsign-production.up.railway.app/
   ```
   Should show seminars or be blank (not error)

### Problem: Admin server crashes

**Solution:**

1. Check for Python errors in the Command Prompt window
2. Restart admin server
3. If repeated, check that all dependencies installed:
   ```bash
   pip install -r admin_requirements.txt --upgrade
   ```

### Problem: Excel file format issues

**Make sure Excel file:**
- ✅ Is saved as `.xlsx` (modern Excel format)
- ✅ Has header row with column names
- ✅ Has data in expected columns
- ✅ Is not locked or protected
- ✅ Is under 10MB in size

**Supported Excel formats:**
- `.xlsx` (Excel 2007+) ← Preferred
- `.xls` (Excel 97-2003) ← Works but older

---

## 🔧 Advanced Options

### Manual CSV Update (If Admin Tool Fails)

If the admin tool has issues, you can still update manually:

1. Process locally:
   ```bash
   python filter_seminarier.py
   ```

2. Deploy to Railway:
   ```bash
   railway up
   ```

### Offline Mode (If Railway Unavailable)

If Railway is down, you can still generate CSV locally:

1. Run admin tool to generate CSV
2. Even if deployment fails, CSV is created locally
3. When Railway is back, run:
   ```bash
   railway up
   ```

---

## 📞 Support

### Issues with Admin Tool

Check:
1. Is `admin_server.py` running?
2. Is file in correct Excel format?
3. Are all column headers present?
4. Are seminars tagged with "website"?

### Issues with Railway Deployment

Check:
1. Is Railway CLI installed? `railway --version`
2. Are you logged in? `railway login`
3. Is project linked? Check `railway.json` exists
4. Check logs: `railway logs --lines 50`

### Contact

- **Admin Tool Issues:** Check Python/Flask installation
- **Railway Issues:** Check Railway account and CLI
- **SmartSign Issues:** Contact support@smartsign.com
- **IML IT:** it@iml.se

---

## 📚 File Locations

| File | Location | Purpose |
|------|----------|---------|
| Excel Data | C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx | Admin's seminar data |
| Admin Tool | C:\Users\chrwah28.KVA\Development\smartsign\run_admin.bat | Shortcut to start admin |
| Admin Server | C:\Users\chrwah28.KVA\Development\smartsign\admin_server.py | Upload processor |
| Generated CSV | C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv | What gets deployed |
| Production URL | https://imlsmartsign-production.up.railway.app/ | What displays on screen |

---

## ✅ Quick Checklist

**Before using admin tool:**
- [ ] Python 3.8+ installed
- [ ] Admin dependencies installed: `pip install -r admin_requirements.txt`
- [ ] Railway CLI installed: `npm install -g @railway/cli`
- [ ] Railway CLI logged in: `railway login`

**When uploading Excel:**
- [ ] File is `.xlsx` format
- [ ] Seminars have "website" tag
- [ ] Dates are in YYYY-MM-DD format
- [ ] File is under 10MB

**After upload:**
- [ ] See green success message
- [ ] Wait 1-2 minutes
- [ ] Check display for new seminars

---

## 🎓 How the System Works (Technical)

### Admin Server Flow

```
1. Admin uploads Excel
        ↓
2. Admin server receives file
        ↓
3. Python reads Excel with pandas
        ↓
4. System filters:
   - Only "website" tagged seminars
   - Only this week's dates
   - Only future events
        ↓
5. Generates seminarier.csv
        ↓
6. Commits to git
        ↓
7. Runs "railway up" deployment
        ↓
8. Railway builds and deploys
        ↓
9. Server.py starts on Railway
        ↓
10. SmartSign fetches CSV (auto-refresh every 60 minutes)
        ↓
11. Display updates with new seminars
```

### Key Features

- **Automatic Filtering:** Only displays relevant seminars
- **Weekly Window:** Only shows this week's events
- **Time Aware:** Removes past events automatically
- **Tag-Based:** Control what displays via tagging
- **One-Click Deploy:** No command line needed
- **Real-Time:** Updates within 1-2 minutes

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Nov 18, 2025 | Initial release with admin tool |

---

## 🎉 You're Ready!

Your SmartSign admin system is fully set up. Just:

1. Run `run_admin.bat`
2. Drop Excel file
3. Click "Update & Deploy"
4. Done!

**No more command line. No more scripts. Just drag, drop, and deploy.**

---

**Happy updating!** 🚀
