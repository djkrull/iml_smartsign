# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

SmartSign Seminar Display System - An automated solution that filters and displays Institut Mittag-Leffler's weekly seminars on digital signage screens. The system consists of:

- **Core script** (`filter_seminarier.py`) - Standalone Python utility that filters seminars from Excel exports
- **Flask server** (`server.py`) - Production display server with admin upload interface (Railway-optimized)
- **Admin server** (`admin_server.py`) - Dedicated admin upload interface with deployment integration
- **Data analyzer** (`analyze_excel.py`) - Excel debugging utility

## Common Development Commands

### Running the Core Filter Script

```bash
# Manual execution
python filter_seminarier.py

# Automated (via Windows Task Scheduler)
schtasks /query /tn "SmartSign Seminar Filter"
schtasks /run /tn "SmartSign Seminar Filter"
```

### Running the Servers (Flask)

```bash
# Production display server (port 8080 or PORT env var)
python server.py

# Admin upload server (port 5000)
python admin_server.py

# Development mode with environment variable
set PORT=8080
python server.py
```

### Utilities

```bash
# Analyze Excel structure and data
python analyze_excel.py

# Install dependencies
pip install -r requirements.txt
pip install -r admin_requirements.txt
```

### Deployment Scripts

```bash
# Windows batch scripts available
run_admin.bat                 # Run admin server
deploy_railway.bat            # Deploy to Railway
setup_scheduler.bat           # Configure Task Scheduler
```

## High-Level Architecture

### Data Flow

```
Excel Export → Python Filter → CSV Output → Web Server → SmartSign → Screen Display
```

1. **Source Data**: `C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx`
   - Excel file with all semester seminars (typically 175+ seminars)
   - Required columns: `Id`, `Start date`, `Start time`, `End time`, `Title`, `Description`, `Tag(s)`, `Room location`

2. **Processing**: `filter_seminarier.py` filters seminars daily
   - Date filter: Monday-Friday of current week (Mon-Thu) OR next week (Fri-Sun)
   - Future events only (excludes past seminars)
   - Tag filter: Only seminars tagged with "website" appear
   - Speaker extraction: Parses HTML descriptions for speaker info
   - Title cleaning: Removes prefixes like "WS,", "Workshop"

3. **Output**: `seminarier.csv` generated with clean data
   - Columns: `Title_Original`, `Title`, `Speaker`, `Date`, `Date_Formatted`, `Time`, `Location`

4. **Distribution**: Flask server (`server.py`) serves:
   - Display template at `/`
   - CSV data at `/seminarier.csv`
   - Admin upload interface at `/admin`

5. **SmartSign CMS**: Fetches CSV hourly and displays on screens

### File Structure

```
smartsign/
├── filter_seminarier.py          # Core filtering script (standalone)
├── server.py                     # Production Flask server (display + CSV)
├── admin_server.py               # Admin upload server
├── analyze_excel.py              # Excel debugging utility
├── admin.html                    # Admin upload interface
├── template_simple.html          # Display template
├── seminarier.csv                # Generated output (updated daily)
├── requirements.txt              # Flask server dependencies
├── admin_requirements.txt        # Admin server dependencies
├── docs/
│   ├── PRD_SmartSign_Seminarier.md
│   ├── ADR_SmartSign_Seminarier.md
│   ├── SETUP.md
│   ├── SMARTSIGN_CONFIG.md
│   └── TEMPLATE_CONFIGURATION.md
└── [batch scripts and deployment files]
```

## Critical Implementation Details

### Excel Processing

Both `server.py` and `admin_server.py` support two Excel formats:

1. **ProjectPlace Export Format** (detected by columns: `Start date`, `Start time`)
   - Dates: datetime format
   - Times: timedelta format (`0 days HH:MM:SS`)
   - Descriptions: HTML with speaker embedded

2. **Simple Format**
   - Dates: `Date` column
   - Times: `Time` column (already formatted HH:MM or HH:MM-HH:MM)
   - Speakers: Direct `Speaker` column

### Speaker Extraction Logic

The system uses smart parsing to extract speaker information:

1. **Primary**: Regex from HTML description: `<b>Speaker</b><br/>Name, Institution`
2. **Fallback**: If description empty, parses title for "Name: Title" pattern
   - Only applies if left side looks like a person's name (< 60 chars, not starting with number, no course keywords)
   - Example: "Genming Bai: TBA" → Speaker="Genming Bai", Title="TBA"

### Time Conversion

Timedelta (ProjectPlace format) → HH:MM string:

```python
# Input: timedelta(0, 64800)  # 18 hours of seconds
# Output: "18:00"
total_seconds = int(timedelta_obj.total_seconds())
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
return f"{hours:02d}:{minutes:02d}"
```

### Filtering Logic (Order Matters)

1. Check for "website" tag (case-insensitive)
2. Parse date (supports multiple formats)
3. Verify date falls within current week (Mon-Fri)
4. Parse time and check if event is future (not past)
5. Build output row with cleaned title and extracted speaker

## Configuration & Constants

### File Paths (in `filter_seminarier.py`)

```python
excel_file = r"C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx"
output_csv = r"C:\Users\chrwah28.KVA\Development\smartsign\seminarier.csv"
```

### Week Boundaries

**Default behavior:**
- **Mon-Thu**: Show current week (Monday-Friday)
- **Fri-Sun**: Show next week (Monday-Friday)

This allows users to see upcoming seminars at the end of the current week.

Customize by modifying the week calculation:

```python
# In filter_seminarier.py, server.py, admin_server.py
start_of_week = today - timedelta(days=today.weekday())
if today.weekday() >= 4:  # Friday or later
    start_of_week = start_of_week + timedelta(days=7)
end_of_week = start_of_week + timedelta(days=4, hours=23, minutes=59, seconds=59)
```

To always show current week regardless of day:
```python
# Remove the "if today.weekday() >= 4" condition
```

### Tag Filter

Default: `"website"` (case-insensitive). Change with:

```python
df['Tag(s)'].str.contains('your-tag-name', na=False)  # Single tag
df['Tag(s)'].str.contains('website|public', na=False) # Multiple tags
```

## Environment Variables

### Flask Server

```env
PORT=8080              # Server port (default: 8080)
FLASK_DEBUG=0          # Debug mode (0=off, 1=on)
```

### Windows Task Scheduler Setup

The filter script runs daily at 00:00 via Task Scheduler:

```cmd
# Task name: "SmartSign Seminar Filter"
# Program: C:\Users\chrwah28.KVA\AppData\Local\Programs\Python\Python3.x\python.exe
# Arguments: C:\Users\chrwah28.KVA\Development\smartsign\filter_seminarier.py
```

## API Endpoints (server.py)

- `GET /` → Display template (HTML)
- `GET /seminarier.csv` → CSV data
- `GET /admin` → Admin upload interface
- `POST /api/upload` → Excel file upload handler
- `GET /health` → Health check
- `GET /<filename>` → Static files (images)

## Testing & Debugging

### Verify Excel Structure

```bash
python analyze_excel.py
```

Outputs:
- Sheet names and count
- Column names and data types
- Date range (min/max)
- Preview CSV for inspection

### Manual Script Execution

```bash
python filter_seminarier.py
```

Expected output shows:
- Total seminars in Excel
- Week range and current date
- Number of filtered seminars
- Preview of each seminar with speaker and location

### Common Issues

**No seminars found:**
- No seminars scheduled this week (expected)
- No seminars tagged "website" (check Excel Tag(s) column)
- All seminars already occurred (expected)
- Excel file not found (verify path, file exists, check special characters)

**Speaker extraction fails:**
- Description format doesn't match expected HTML pattern
- Title doesn't contain "Name: Title" pattern
- Check with `analyze_excel.py` to see actual format

**UnicodeEncodeError in console:**
- Windows console limitation, not a code error
- CSV output is correct despite console warnings
- Can safely ignore

## Key Functions & Modules

### filter_seminarier.py

- `extract_speaker(html_description)` - Regex extraction with HTML parsing
- `format_time(timedelta_obj)` - Converts seconds to HH:MM
- `clean_title(title)` - Removes common prefixes (WS, Workshop, Seminar)
- `main()` - Orchestrates filtering and CSV generation

### server.py

- `get_current_week_start()` / `get_current_week_end()` - Week boundary calculation
- `parse_date(date_value)` - Multi-format date parser
- `convert_timedelta_to_time_str(td_value)` - Timedelta to HH:MM conversion
- `extract_speaker_from_description(desc_html)` - HTML speaker extraction
- `process_excel_to_csv(excel_file)` - Core processing logic (supports both Excel formats)
- `upload_file()` - POST endpoint for admin uploads

### admin_server.py

Similar structure to `server.py` with additional Railway deployment integration.

## Dependencies

### Core (requirements.txt)

```
Flask>=2.3.0           # Web framework
pandas>=1.3.0          # Data processing
openpyxl>=3.0.0       # Excel reading
```

### Admin (admin_requirements.txt)

```
Flask>=2.3.0           # Web framework
flask-cors>=4.0.0      # CORS support
pandas>=1.3.0          # Data processing
openpyxl>=3.0.0       # Excel reading
```

Note: No additional packages needed for `filter_seminarier.py` beyond core requirements.

## Windows-Specific Considerations

- File paths use backslashes: `C:\Users\chrwah28.KVA\...`
- Task Scheduler configuration requires full Python path
- Script is fully compatible but uses Windows paths
- Can be deployed on Linux/macOS but would need path adjustments

## Important Notes

- The CSV contains only public information (seminar titles, speaker names, dates, locations)
- SmartSign CMS fetches CSV hourly (refreshing displays)
- Production server optimized for Railway deployment
- HTML descriptions may vary in format - use `analyze_excel.py` to debug
- Date/time parsing is defensive with fallbacks for multiple formats
