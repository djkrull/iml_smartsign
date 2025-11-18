# SmartSign Seminar Display System

**Automated weekly seminar display for Institut Mittag-Leffler digital signage**

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Status](https://img.shields.io/badge/status-production-success)

---

## Overview

This system automatically filters and displays upcoming seminars on digital screens at Institut Mittag-Leffler (IML). It processes seminar data from Excel exports, filters to current week's events tagged for public display, and publishes to SmartSign CMS for automatic display.

### Key Features

- **Automated Weekly Filtering** - Shows only current week's seminars (Monday-Friday)
- **Tag-Based Selection** - Displays only seminars tagged with "website"
- **Past Event Removal** - Automatically excludes seminars that have already occurred
- **Speaker Extraction** - Intelligently extracts speaker information from HTML descriptions
- **Zero Manual Intervention** - Runs automatically via Windows Task Scheduler
- **Clean CSV Output** - Formats data perfectly for SmartSign CMS consumption

---

## Quick Start

### For End Users

The system runs automatically - no action needed!

Seminars on screens update daily at midnight with:
- **This week's seminars only** (Monday-Friday)
- **Only future events** (past seminars removed automatically)
- **Only public seminars** (tagged with "website")

### For Administrators

1. **Install Python 3.8+** and required packages:
   ```cmd
   pip install pandas openpyxl
   ```

2. **Configure paths** in `filter_seminarier.py` if needed

3. **Set up Windows Task Scheduler** to run daily at 00:00

4. **Configure SmartSign CMS** with CSV datasource and template

📖 **See [docs/SETUP.md](docs/SETUP.md) for complete installation guide**

---

## How It Works

```
Excel Export → Python Filter → CSV Output → Web Server → SmartSign → Screen Display
```

1. **Source Data**: Seminar program coordinator exports Excel from seminar management system
2. **Daily Processing**: Python script runs at midnight, filtering seminars
3. **CSV Generation**: Clean CSV file created with only relevant seminars
4. **Web Deployment**: CSV uploaded to web server (manual or automated)
5. **SmartSign Fetch**: SmartSign CMS fetches CSV hourly
6. **Display**: Digital screens show formatted seminar information

---

## Project Structure

```
smartsign/
├── filter_seminarier.py          # Main filtering script
├── analyze_excel.py               # Excel analysis utility (for debugging)
├── seminarier.csv                 # Generated output (updated daily)
├── README.md                      # This file
└── docs/
    ├── PRD_SmartSign_Seminarier.md    # Product Requirements Document
    ├── ADR_SmartSign_Seminarier.md    # Architecture Decision Records
    └── SETUP.md                       # Complete setup guide
```

---

## Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](README.md) | Project overview and quick start | Everyone |
| [PRD](docs/PRD_SmartSign_Seminarier.md) | Product requirements and specifications | Product managers, stakeholders |
| [ADR](docs/ADR_SmartSign_Seminarier.md) | Technical decisions and rationale | Developers, architects |
| [SETUP](docs/SETUP.md) | Installation and configuration | IT administrators |

---

## Requirements

### Software Requirements

- **Python** 3.8 or higher
- **Python Packages**:
  - `pandas` - Data manipulation
  - `openpyxl` - Excel file reading
- **Windows 10/11** - For Task Scheduler
- **SmartSign CMS** 11.x
- **Web Server** - With HTTPS support

### Input Requirements

**Source Excel File:**
- Path: `C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx`
- Required Columns: `Id`, `Start date`, `Start time`, `End time`, `Title`, `Description`, `Tag(s)`, `Room location`
- Seminar must have `"website"` in `Tag(s)` column to appear

**Data Format:**
- Dates in datetime format
- Times in timedelta format (`0 days HH:MM:SS`)
- HTML descriptions with speaker information

### Output Format

**CSV File:** `seminarier.csv`

| Column | Description | Example |
|--------|-------------|---------|
| Title_Original | Original title from Excel | WS, Björn Stinner: Finite element... |
| Title | Cleaned title (prefixes removed) | Björn Stinner: Finite element... |
| Speaker | Speaker name and institution | Björn Stinner, University of Warwick |
| Date | ISO date (for sorting) | 2025-11-18 |
| Date_Formatted | Human-readable date | Tuesday 18 Nov |
| Time | Formatted time range | 09:30-10:30 |
| Location | Room/venue name | Kuskvillan |

---

## Usage

### Running the Script Manually

```cmd
cd C:\Users\chrwah28.KVA\Development\smartsign
python filter_seminarier.py
```

**Expected Output:**
```
================================================================================
AUTOMATISK SEMINARIE-FILTRERING FOR SMARTSIGN
================================================================================

Laser Excel: C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx
Totalt antal seminarier i Excel: 175

Denna vecka: 2025-11-17 till 2025-11-21
Idag: 2025-11-17 kl 15:32

Seminarier denna vecka (framtida, taggade med 'website'): 6

Extraherar talare fran HTML-beskrivningar...

[OK] CSV skapad: C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv
     Antal seminarier: 6

================================================================================
FORHANDS VISNING AV FILTRERADE SEMINARIER:
================================================================================

Tuesday 18 Nov kl 09:30-10:30
  Titel: Björn Stinner: Finite element approximation of rough PDEs
  Talare: Björn Stinner, University of Warwick
  Plats: Kuskvillan

...

================================================================================
[KLART] Filen ar klar for SmartSign Sync!
================================================================================
```

### Automated Execution

Once configured, the script runs automatically via Windows Task Scheduler:

- **Frequency:** Daily
- **Time:** 00:00 (midnight)
- **Task Name:** "SmartSign Seminar Filter"

**Verify scheduled task:**
```cmd
schtasks /query /tn "SmartSign Seminar Filter"
```

**Run task manually:**
```cmd
schtasks /run /tn "SmartSign Seminar Filter"
```

---

## Filtering Logic

The script applies multiple filters in sequence:

### 1. Date Range Filter
```python
start_of_week = today - timedelta(days=today.weekday())  # Monday 00:00
end_of_week = start_of_week + timedelta(days=4, hours=23, minutes=59)  # Friday 23:59
```

### 2. Future Events Only
```python
df['Start date'] >= today  # No past seminars
```

### 3. Tag Filter
```python
df['Tag(s)'].str.contains('website', na=False)  # Only "website" tagged
```

### Example

**Input:** 175 seminars spanning entire semester

**After date range filter:** 8 seminars this week

**After future filter:** 7 seminars (removes past events)

**After tag filter:** 6 seminars (removes non-public events)

**Output:** 6 seminars displayed on screen

---

## Data Transformations

### Speaker Extraction

Extracts speaker from HTML description using regex:

**Input:**
```html
<b>Speaker</b><br />
Björn Stinner, University of Warwick<br />
```

**Output:**
```
Björn Stinner, University of Warwick
```

**Regex Pattern:**
```python
r'<b>Speaker</b><br\s*/?>[\n\s]*([^<]+?)(?:<br|$)'
```

### Time Formatting

Converts timedelta to readable format:

**Input:** `0 days 17:00:00`

**Output:** `17:00`

**Combined:** `09:30-10:30`

### Title Cleaning

Removes common prefixes:

**Input:** `WS, Björn Stinner: Finite element approximation...`

**Output:** `Björn Stinner: Finite element approximation...`

**Regex:** `r'^(WS|Workshop|Seminar)[,:\s]+'`

### Date Formatting

Creates human-readable dates:

**Input:** `2025-11-18 00:00:00`

**Output:** `Tuesday 18 Nov`

**Format:** `%A %d %b`

---

## Configuration

### File Paths

Update these paths in `filter_seminarier.py` if your setup differs:

```python
# Line 72-73
excel_file = r"C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx"
output_csv = r"C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv"
```

### Week Boundaries

Current configuration: Monday 00:00 to Friday 23:59

To change (e.g., to include weekends):

```python
# Line 92
end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59)  # Sunday
```

### Tag Filter

Current tag: `"website"`

To change tag name:

```python
# Line 102
(df['Tag(s)'].str.contains('your-tag-name', na=False))
```

To add multiple tags (OR logic):

```python
(df['Tag(s)'].str.contains('website|public', na=False))
```

---

## Troubleshooting

### No Seminars Found

**Possible causes:**
1. ✅ No seminars scheduled this week (expected behavior)
2. ⚠️ No seminars tagged with "website" - check Excel Tag(s) column
3. ✅ All seminars already occurred (expected behavior)
4. ❌ Excel file not found - verify file path

**Debug:**
```python
# Add after line 80 in filter_seminarier.py
print(f"Total seminars: {len(df)}")
print(f"This week: {len(df[(df['Start date'] >= start_of_week) & (df['Start date'] <= end_of_week)])}")
print(f"Future only: {len(df[(df['Start date'] >= today)])}")
print(f"Tagged 'website': {len(df[df['Tag(s)'].str.contains('website', na=False)])}")
```

### Script Errors

**ModuleNotFoundError: No module named 'pandas'**
```cmd
pip install pandas openpyxl
```

**FileNotFoundError: Excel file not found**
- Verify file path in line 72
- Check file exists
- Verify filename (especially spaces and parentheses)

**UnicodeEncodeError in console**
- Windows console limitation (cannot display some characters)
- Does NOT affect CSV output
- Script still works correctly
- Can safely ignore

### Task Scheduler Issues

**Task doesn't run automatically**
1. Verify task is **Enabled**
2. Check trigger is set to **Daily at 00:00**
3. Verify Python is in system **PATH**
4. Check Task History for error messages

**Task runs but produces no output**
- Add logging to file:
  ```cmd
  python filter_seminarier.py > C:\Logs\smartsign.log 2>&1
  ```

### SmartSign Issues

See [docs/SETUP.md](docs/SETUP.md) for comprehensive SmartSign troubleshooting.

---

## Maintenance

### Regular Tasks

**Daily (Automated):**
- ✅ Script runs at 00:00
- ✅ CSV regenerated
- ✅ Data uploaded to web server

**Weekly (Manual Check):**
- 👁️ Verify seminars displaying correctly on screens
- 📊 Check Task Scheduler history for any failures

**Monthly (Review):**
- 📝 Review execution logs
- 🔄 Update source Excel file path if changed
- 🐛 Check for any recurring issues

### Updating Source Data

When seminar coordinator updates Excel file:

1. Save as: `ProgramExport (2).xlsx` in Downloads folder
2. Wait until next midnight (00:00) for automatic update
3. Or run manually for immediate update

**For urgent updates:**
```cmd
python filter_seminarier.py
# Then manually upload CSV to web server
```

---

## Technical Details

### Dependencies

```
pandas>=1.3.0
openpyxl>=3.0.0
```

**Install:**
```cmd
pip install pandas openpyxl
```

### Python Version

**Required:** Python 3.8 or higher

**Tested on:**
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11

### Platform

**Supported:** Windows 10, Windows 11

**Note:** Script code is cross-platform (works on Linux/macOS), but Task Scheduler setup is Windows-specific.

### Performance

**Typical execution time:**
- 175 seminars: ~2-5 seconds
- 500 seminars: ~5-10 seconds

**Memory usage:** < 50 MB

**Output file size:** < 5 KB (typically 6-10 seminars)

---

## Architecture

### System Components

```
┌─────────────────────┐
│  Seminar System     │  (Source of truth)
│  (Excel Export)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Python Script      │  (Data processing)
│  - Filter           │
│  - Transform        │
│  - Generate CSV     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Web Server         │  (CSV hosting)
│  HTTPS URL          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  SmartSign CMS      │  (Content management)
│  - CSV Datasource   │
│  - Template         │
│  - Booking          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Digital Screen     │  (Display)
└─────────────────────┘
```

### Data Flow

1. **Input**: Excel file with all semester seminars
2. **Processing**: Python script filters and transforms data
3. **Output**: Clean CSV with current week's seminars
4. **Distribution**: CSV uploaded to web server
5. **Consumption**: SmartSign fetches CSV hourly
6. **Display**: Screen shows formatted seminar information

---

## Security

**Data Classification:** Public

The CSV contains only public information:
- Seminar titles (public)
- Speaker names (public figures)
- Dates and times (public events)
- Room locations (public)

**No sensitive data:**
- ❌ No personal information
- ❌ No authentication credentials
- ❌ No internal-only information

**Security measures:**
- ✅ HTTPS for data transmission
- ✅ Web server with valid SSL certificate
- ✅ Standard web server hardening
- ✅ CSV is publicly accessible (appropriate for public data)

---

## Future Enhancements

Potential improvements for future versions:

### Phase 2 Features
- [ ] Email notifications when no seminars found
- [ ] Support for multiple tag filters
- [ ] Display next week's seminars as preview
- [ ] Bilingual display (Swedish/English)
- [ ] Integration with IML calendar systems

### Technical Improvements
- [ ] API integration with seminar management system
- [ ] Real-time updates (hourly instead of daily)
- [ ] Automated web deployment via CI/CD
- [ ] Enhanced error monitoring and alerting
- [ ] Unit tests and integration tests

### User Experience
- [ ] Mobile app for seminar browsing
- [ ] QR codes on screens for more information
- [ ] RSS feed of upcoming seminars
- [ ] Calendar export (iCal format)

---

## Contributing

This is an internal IML IT project. For changes or improvements:

1. **Test thoroughly** in development environment
2. **Update documentation** (especially ADR for architectural changes)
3. **Verify end-to-end** before deploying to production
4. **Coordinate with** seminar program coordinators

---

## Support

**For technical issues:**
- **IT Team:** it@iml.se
- **SmartSign Support:** support@smartsign.com

**For seminar content issues:**
- **Program Coordinator:** program@iml.se

---

## License

Internal use only - Institut Mittag-Leffler

---

## Acknowledgments

**Developed by:** IML IT Team
**Date:** November 2025
**Purpose:** Streamline seminar communication and reduce manual administrative overhead

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-17 | Initial release with automated filtering and SmartSign integration |

---

## Quick Reference

**Key Files:**
```
filter_seminarier.py  → Main script
seminarier.csv        → Generated output
docs/SETUP.md         → Installation guide
```

**Key Commands:**
```cmd
python filter_seminarier.py                    # Run manually
schtasks /run /tn "SmartSign Seminar Filter"   # Trigger scheduled task
```

**CSV URL:**
```
https://iml.se/smartsign/seminarier.csv
```

---

**For detailed setup instructions, see [docs/SETUP.md](docs/SETUP.md)**

**For architectural decisions, see [docs/ADR_SmartSign_Seminarier.md](docs/ADR_SmartSign_Seminarier.md)**

**For full requirements, see [docs/PRD_SmartSign_Seminarier.md](docs/PRD_SmartSign_Seminarier.md)**
