# SmartSign Seminar Display - Quick Start Guide

**Get up and running in 30 minutes**

---

## For System Administrators

### Step 1: Install Python (5 minutes)

```cmd
# Check if Python is installed
python --version

# If not installed, download from: https://www.python.org/downloads/
# During installation, CHECK "Add Python to PATH"

# Install required packages
pip install pandas openpyxl
```

### Step 2: Configure File Paths (2 minutes)

Open `filter_seminarier.py` and verify these paths (lines 72-73):

```python
excel_file = r"C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx"
output_csv = r"C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv"
```

**Update if your files are in different locations.**

### Step 3: Test the Script (3 minutes)

```cmd
cd C:\Users\chrwah28.KVA\Development\smartsign
python filter_seminarier.py
```

**Expected output:** "CSV skapad" with count of seminars

**Verify:** File `seminarier.csv` is created

### Step 4: Set Up Automation (5 minutes)

**Right-click** `setup_scheduler.bat` → **Run as Administrator**

This creates a Windows scheduled task to run daily at midnight.

**Verify:**
```cmd
schtasks /query /tn "SmartSign Seminar Filter"
```

### Step 5: Configure Web Deployment (10 minutes)

**Option A: Manual FTP (for testing)**
1. Upload `seminarier.csv` to your web server
2. Verify accessible at: `https://your-domain/smartsign/seminarier.csv`

**Option B: Automated FTP**
1. Edit `deploy_to_web.bat`
2. Update FTP credentials (lines 12-16)
3. Run: `deploy_to_web.bat`

### Step 6: Configure SmartSign CMS (15 minutes)

See detailed guide: **[docs/SMARTSIGN_CONFIG.md](docs/SMARTSIGN_CONFIG.md)**

**Quick steps:**
1. **Datasource:** Create CSV datasource with your web URL
2. **Template:** Create Smart Media template with data bindings
3. **Booking:** Create permanent booking on your screen channel

---

## For Seminar Program Coordinators

### Adding Seminars to Display

**Your seminars will automatically appear on screens if:**

1. ✅ Seminar is scheduled for **current week** (Monday-Friday)
2. ✅ Seminar has **"website"** tag in the Tag(s) column
3. ✅ Seminar **start time is in the future**

### Excel File Requirements

**File Location:** `C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx`

**Required Columns:**
- Start date
- Start time / End time
- Title
- Description (with speaker information)
- Tag(s) ← **Must include "website"** for public display
- Room location

**Speaker Format in Description:**
```html
<b>Speaker</b><br />
Name, Institution<br />
```

### What Gets Displayed

**On screen you'll see:**
- Seminar title
- Speaker name and institution
- Date (e.g., "Tuesday 18 Nov")
- Time (e.g., "09:30-10:30")
- Location (room name)

**NOT displayed:**
- Abstracts
- Full descriptions
- Internal notes

### Update Schedule

**When you update the Excel file:**
1. Save as usual to Downloads folder
2. **Wait until next day** (updates run at midnight)
3. Changes appear on screens the next morning

**For urgent updates:**
Ask IT to run: `python filter_seminarier.py` manually

---

## For End Users (Visitors)

### What You'll See

Digital screens in IML lobby show **this week's upcoming seminars**:

- Only **current week** (Monday-Friday)
- Only **future** seminars (past events removed automatically)
- Only **public** seminars (tagged for display)

**Updates:** Automatically every day at midnight

---

## Troubleshooting

### "No seminars found this week"

**Possible reasons:**
1. ✅ No seminars scheduled this week (expected)
2. ⚠️ Seminars not tagged with "website" in Excel
3. ✅ All seminars already occurred (expected)

**Fix:** Add "website" to Tag(s) column in Excel file

### Script fails with "FileNotFoundError"

**Reason:** Excel file not found

**Fix:** Verify file path in `filter_seminarier.py` line 72

### Scheduled task not running

**Fix:** Run `setup_scheduler.bat` as Administrator

### Screen shows old data

**Possible reasons:**
1. CSV file not uploaded to web server
2. SmartSign not refreshing datasource
3. Web server caching

**Fix:**
1. Manually refresh datasource in SmartSign CMS
2. Check CSV file on web server is updated

---

## File Structure

```
smartsign/
├── filter_seminarier.py          ← Main script (run daily)
├── seminarier.csv                 ← Output file (generated)
├── setup_scheduler.bat            ← Run as Admin to set up automation
├── deploy_to_web.bat              ← Upload CSV to web server
├── run_all.bat                    ← Run filter + deploy in one step
├── README.md                      ← Full documentation
├── QUICKSTART.md                  ← This file
└── docs/
    ├── SETUP.md                   ← Detailed installation guide
    ├── SMARTSIGN_CONFIG.md        ← SmartSign CMS configuration
    ├── PRD_SmartSign_Seminarier.md    ← Product requirements
    └── ADR_SmartSign_Seminarier.md    ← Technical decisions
```

---

## Key Commands

```cmd
# Run filter manually
python filter_seminarier.py

# Upload to web server (after configuring)
deploy_to_web.bat

# Run everything (filter + deploy)
run_all.bat

# Check scheduled task
schtasks /query /tn "SmartSign Seminar Filter"

# Run scheduled task manually
schtasks /run /tn "SmartSign Seminar Filter"
```

---

## Configuration Checklist

**Installation:**
- [ ] Python 3.8+ installed
- [ ] pandas and openpyxl packages installed
- [ ] File paths configured in script
- [ ] Script runs successfully manually

**Automation:**
- [ ] Windows Task Scheduler configured
- [ ] Task runs daily at 00:00
- [ ] Task tested manually

**Web Deployment:**
- [ ] FTP credentials configured
- [ ] CSV uploads successfully
- [ ] CSV accessible via web URL

**SmartSign:**
- [ ] CSV Datasource created
- [ ] Smart Media Template created
- [ ] Booking created and active
- [ ] Screen displays seminars

---

## Support Contacts

**Technical Issues (IT):**
- Email: it@iml.se
- Script errors, automation issues, web server problems

**Content Issues (Program):**
- Email: program@iml.se
- Seminar tagging, Excel file questions

**SmartSign Issues:**
- SmartSign Support: support@smartsign.com
- CMS configuration, template design, screen connectivity

---

## Next Steps After Setup

1. **Monitor for first week** - Check screens daily to verify automation
2. **Document actual web URL** - Update in SmartSign datasource
3. **Train program coordinators** - Explain "website" tag requirement
4. **Set up monitoring** - Consider email alerts for failures (future)

---

**Questions?** See full documentation in [README.md](README.md) or [docs/SETUP.md](docs/SETUP.md)

**Version:** 1.0
**Last Updated:** 2025-11-17
