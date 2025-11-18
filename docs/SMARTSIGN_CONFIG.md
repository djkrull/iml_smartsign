# SmartSign CMS Configuration Guide

**Step-by-Step Configuration for Seminar Display**

---

## Prerequisites

Before starting, ensure you have:
- [ ] CSV file uploaded to web server and accessible via URL
- [ ] SmartSign CMS admin login credentials
- [ ] Screen/channel already set up in SmartSign

**Test your CSV URL:**
Open in browser: `https://your-domain.se/smartsign/seminarier.csv`

Should download a file that looks like:
```csv
Title_Original,Title,Speaker,Date,Date_Formatted,Time,Location
Björn Stinner: Finite element...,Björn Stinner: Finite element...,"Björn Stinner, University of Warwick",2025-11-18,Tuesday 18 Nov,09:30-10:30,Kuskvillan
```

---

## Part 1: Create CSV Datasource

### Step 1: Navigate to Datasources

1. Login to SmartSign CMS
2. Main menu → **Content** → **Datasources**
3. Click **"+ New Datasource"** button

### Step 2: Basic Configuration

**Field Values:**

| Field | Value | Notes |
|-------|-------|-------|
| **Type** | CSV Datasource | Select from dropdown |
| **Name** | `Seminarier` | Or "Weekly Seminars" |
| **Description** | `Current week's seminars for digital displays` | Optional but helpful |

### Step 3: Data Source Settings

**URL Configuration:**

| Field | Value | Example |
|-------|-------|---------|
| **Data Source URL** | Your CSV URL | `https://iml.se/smartsign/seminarier.csv` |
| **Fetch method** | Through Smartsign server | ✓ Recommended |
| **Update interval** | `3600` | Seconds (1 hour) |

**CSV Settings:**

| Field | Value | Notes |
|-------|-------|-------|
| **Encoding** | UTF-8 | Default, correct for Swedish characters |
| **First row is header** | ✓ Checked | CSV has header row |
| **Delimiter** | `,` (comma) | Default |

### Step 4: Column Mapping

SmartSign will auto-detect columns. Verify these are present:

1. `Title_Original` - Original title (not used in display)
2. `Title` - Cleaned title ✓ **Used**
3. `Speaker` - Speaker name and institution ✓ **Used**
4. `Date` - ISO date for sorting
5. `Date_Formatted` - Display date ✓ **Used**
6. `Time` - Time range ✓ **Used**
7. `Location` - Room name ✓ **Used**

### Step 5: Test Connection

1. Click **"Test"** or **"Fetch Data"** button
2. Should show: "Successfully fetched X rows" (where X = number of seminars)
3. Preview data should show correct seminar information

**Troubleshooting:**
- ❌ "Connection failed" → Check URL is publicly accessible
- ❌ "Invalid format" → Verify CSV encoding is UTF-8
- ❌ "0 rows" → Check CSV file has data

### Step 6: Save Datasource

1. Click **"Save"** button
2. Datasource appears in list with status "Active"

**Configuration Complete!** ✓

---

## Part 2: Create Smart Media Template

### Overview

We'll create a template that displays seminars in a clean, readable list format.

**Template Type:** Smart Media (data-bound template)
**Layout:** Vertical list with repeating rows
**Data Source:** Seminarier (CSV datasource created above)

### Step 1: Create New Template

1. Main menu → **Design** → **Template Creator**
2. Click **"+ New Template"**

**Basic Settings:**

| Field | Value | Notes |
|-------|-------|-------|
| **Name** | `Seminar Display` | Or "Weekly Seminars" |
| **Type** | Smart Media | Data-bound template |
| **Orientation** | Landscape | Match your screen |
| **Resolution** | 1920x1080 | Match your screen resolution |
| **Background color** | `#FFFFFF` (white) | Or your preference |

### Step 2: Template Layout Design

**Recommended Layout Structure:**

```
+-----------------------------------------------------------+
|                                                           |
|  SEMINARS THIS WEEK                          [IML Logo]  |
|                                                           |
+-----------------------------------------------------------+
|                                                           |
|  Tuesday 18 Nov • 09:30-10:30                            |
|  Björn Stinner: Finite element approximation of rough... |
|  Speaker: Björn Stinner, University of Warwick           |
|  Location: Kuskvillan                                     |
|                                                           |
+-----------------------------------------------------------+
|                                                           |
|  Tuesday 18 Nov • 11:00-12:00                            |
|  Manuel Solano: The Transfer Path Method...              |
|  Speaker: Manuel Solano, Universidad de Concepción       |
|  Location: Kuskvillan                                     |
|                                                           |
+-----------------------------------------------------------+
|  ... (more seminars)                                      |
+-----------------------------------------------------------+
```

### Step 3: Add Header Element

**Element: Static Text (Header)**

| Property | Value |
|----------|-------|
| **Type** | Text |
| **Content** | `SEMINARS THIS WEEK` |
| **Font** | Arial / Helvetica |
| **Size** | 60-80px |
| **Weight** | Bold |
| **Color** | `#000000` (black) or IML brand color |
| **Position** | Top: 50px, Left: 100px |
| **Width** | 1720px |
| **Height** | 100px |
| **Alignment** | Left |

### Step 4: Add Data-Bound Elements

For each seminar, you'll need these elements. SmartSign will repeat them for each row.

#### Element 1: Date & Time

| Property | Value |
|----------|-------|
| **Type** | Text |
| **Content** | `{{Date_Formatted}} • {{Time}}` |
| **Data Binding** | ✓ Enabled |
| **Datasource** | Seminarier |
| **Column (Date)** | `Date_Formatted` |
| **Column (Time)** | `Time` |
| **Font** | Arial / Helvetica |
| **Size** | 32px |
| **Weight** | Semi-bold |
| **Color** | `#666666` (gray) |
| **Position** | Top: 200px, Left: 100px |

**Binding Syntax:**
```
{{Date_Formatted}} • {{Time}}
```
or separate fields:
```
Date: {{Date_Formatted}}
Time: {{Time}}
```

#### Element 2: Seminar Title

| Property | Value |
|----------|-------|
| **Type** | Text |
| **Content** | `{{Title}}` |
| **Data Binding** | ✓ Enabled |
| **Datasource** | Seminarier |
| **Column** | `Title` |
| **Font** | Arial / Helvetica |
| **Size** | 44-48px |
| **Weight** | Bold |
| **Color** | `#000000` (black) |
| **Position** | Top: 250px, Left: 100px |
| **Width** | 1720px |
| **Max Lines** | 2 |
| **Text Overflow** | Ellipsis (...) |

**Binding Syntax:**
```
{{Title}}
```

#### Element 3: Speaker Information

| Property | Value |
|----------|-------|
| **Type** | Text |
| **Content** | `Speaker: {{Speaker}}` |
| **Data Binding** | ✓ Enabled |
| **Datasource** | Seminarier |
| **Column** | `Speaker` |
| **Font** | Arial / Helvetica |
| **Size** | 36px |
| **Weight** | Regular |
| **Color** | `#333333` (dark gray) |
| **Position** | Top: 350px, Left: 100px |

**Binding Syntax:**
```
Speaker: {{Speaker}}
```

or without prefix:
```
{{Speaker}}
```

#### Element 4: Location

| Property | Value |
|----------|-------|
| **Type** | Text |
| **Content** | `Location: {{Location}}` |
| **Data Binding** | ✓ Enabled |
| **Datasource** | Seminarier |
| **Column** | `Location` |
| **Font** | Arial / Helvetica |
| **Size** | 32px |
| **Weight** | Regular |
| **Color** | `#666666` (gray) |
| **Position** | Top: 400px, Left: 100px |

**Binding Syntax:**
```
Location: {{Location}}
```

or with icon:
```
📍 {{Location}}
```

### Step 5: Configure Repeating Behavior

**Important:** Configure how multiple seminars are displayed

**Option A: Scrolling List**
- Display: Vertical scroll
- Items per page: All
- Scroll speed: Slow/Medium
- Auto-scroll: ✓ Enabled
- Loop: ✓ Enabled

**Option B: Pagination**
- Display: Paginated
- Items per page: 3-4 seminars
- Duration per page: 15 seconds
- Transition: Fade or Slide
- Loop: ✓ Enabled

### Step 6: Preview Template

1. Click **"Preview"** button
2. Verify:
   - Data appears correctly
   - Formatting looks good
   - All seminars visible
   - Text fits within bounds
   - No truncation issues

**Common Issues:**
- Text too large → Reduce font size
- Text cut off → Increase element height/width
- Data not showing → Check datasource binding
- Wrong data → Verify column names

### Step 7: Save Template

1. Click **"Save"** button
2. Template appears in template list

**Template Complete!** ✓

---

## Part 3: Create Booking

### Step 1: Navigate to Bookings

1. Main menu → **Schedule** → **Bookings**
2. Click **"+ New Booking"** button

### Step 2: Configure Booking

**Basic Information:**

| Field | Value | Notes |
|-------|-------|-------|
| **Name** | `Seminar Display - Permanent` | Descriptive name |
| **Description** | `Automatically updated weekly seminars` | Optional |
| **Status** | Active | ✓ Enabled |

**Content Selection:**

| Field | Value | Notes |
|-------|-------|-------|
| **Content Type** | Template | Select template |
| **Template** | Seminar Display | Your template from Part 2 |
| **Datasource** | Seminarier | Auto-selected from template |

**Schedule:**

| Field | Value | Notes |
|-------|-------|-------|
| **Start Date** | Today's date | Or when you want it to start |
| **End Date** | (Leave blank) | For permanent booking |
| **Start Time** | 00:00 | All day |
| **End Time** | 23:59 | All day |
| **Recurrence** | Daily | Every day |
| **Days of Week** | All days | Mon-Sun |

**Channel Assignment:**

| Field | Value | Notes |
|-------|-------|-------|
| **Channel** | Your screen's channel | Select from dropdown |
| **Priority** | High (80-90) | Ensures display |

### Step 3: Advanced Settings (Optional)

**Playback Settings:**

| Field | Value | Notes |
|-------|-------|-------|
| **Duration** | Auto (based on content) | Or set specific duration |
| **Transitions** | Fade | Smooth transition |
| **Loop** | ✓ Enabled | Continuous display |

### Step 4: Save Booking

1. Click **"Save"** or **"Publish"** button
2. Booking appears in schedule
3. Status should show "Active"

**Booking Complete!** ✓

---

## Part 4: Verification

### Verify Datasource

1. Go to **Content** → **Datasources**
2. Find "Seminarier" datasource
3. Check:
   - Status: Active ✓
   - Last fetch: Recent timestamp
   - Row count: Matches expected seminars (6-10 typically)
   - No errors shown

**Manual refresh:**
- Click **"Refresh"** or **"Fetch Now"** button
- Should update row count immediately

### Verify Template

1. Go to **Design** → **Templates**
2. Find "Seminar Display" template
3. Click **"Preview"**
4. Verify:
   - All seminars display correctly
   - Formatting looks good
   - Data bindings work
   - No errors

### Verify Booking

1. Go to **Schedule** → **Bookings**
2. Find "Seminar Display - Permanent" booking
3. Check:
   - Status: Active ✓
   - Schedule: Today's date in range
   - Channel: Correct screen selected
   - Priority: High enough

### Verify Screen Display

**Live Screen Check:**

1. Go to your physical digital screen
2. Wait for booking to activate (may take 1-2 minutes)
3. Verify:
   - Template appears on screen
   - Seminars display correctly
   - All data visible and readable
   - Updates occur (if testing pagination)

**Remote Monitoring (if available):**

1. Go to **Devices** → **Screens**
2. Find your screen
3. Click **"Preview"** or **"Screenshot"**
4. Verify content is displaying

---

## Part 5: Testing Updates

### Test Data Update Flow

1. **Modify source Excel file**
   - Add a test seminar for this week
   - Ensure it has "website" tag

2. **Run filter script**
   ```cmd
   python filter_seminarier.py
   ```

3. **Upload CSV to web server**
   - Manual upload or run `deploy_to_web.bat`

4. **Wait for SmartSign to fetch**
   - Automatic fetch every hour
   - Or manually refresh datasource

5. **Verify on screen**
   - New seminar should appear within 1 hour
   - Or immediately if manually refreshed

---

## Troubleshooting

### Datasource Issues

**Problem:** "Error fetching data"

**Solutions:**
1. Verify URL is accessible from browser
2. Check firewall/network settings
3. Try "Direct" fetch method instead of "Through Smartsign server"
4. Verify CSV is UTF-8 encoded
5. Check SmartSign server logs

**Problem:** "0 rows fetched"

**Solutions:**
1. Verify CSV file has data (open in text editor)
2. Check "First row is header" is enabled
3. Verify CSV format is correct (no extra blank lines)
4. Check delimiter is comma

### Template Issues

**Problem:** No data displays

**Solutions:**
1. Verify datasource is fetching data (check row count)
2. Check data binding syntax: `{{ColumnName}}`
3. Verify column names match exactly (case-sensitive)
4. Preview template to see binding errors

**Problem:** Text truncated or cut off

**Solutions:**
1. Increase element width/height
2. Reduce font size
3. Enable text wrapping
4. Use ellipsis for overflow

### Booking Issues

**Problem:** Booking not showing on screen

**Solutions:**
1. Verify booking status is "Active"
2. Check schedule includes current date/time
3. Verify channel is correct
4. Increase priority if conflicting bookings
5. Check screen is online and connected

**Problem:** Old data still showing

**Solutions:**
1. Manually refresh datasource in CMS
2. Check datasource update interval (should be 3600 seconds)
3. Verify CSV file on web server is updated
4. Clear screen cache if available

---

## Configuration Checklist

Use this checklist to verify complete setup:

### Datasource Configuration
- [ ] CSV Datasource created and named "Seminarier"
- [ ] URL configured: `https://your-domain/smartsign/seminarier.csv`
- [ ] Fetch method: "Through Smartsign server"
- [ ] Update interval: 3600 seconds (1 hour)
- [ ] First row is header: ✓ Enabled
- [ ] Test connection successful
- [ ] Row count matches expected seminars
- [ ] Columns detected: Title, Speaker, Date_Formatted, Time, Location

### Template Configuration
- [ ] Smart Media template created and named "Seminar Display"
- [ ] Resolution matches screen (e.g., 1920x1080)
- [ ] Header element added ("SEMINARS THIS WEEK")
- [ ] Data-bound elements added for each field
- [ ] Data bindings use correct column names
- [ ] Repeating/scrolling configured
- [ ] Preview shows data correctly
- [ ] Template saved successfully

### Booking Configuration
- [ ] Booking created and named "Seminar Display - Permanent"
- [ ] Content set to "Seminar Display" template
- [ ] Schedule set to Daily, All day
- [ ] End date left blank (permanent)
- [ ] Channel assigned to correct screen
- [ ] Priority set to High (80-90)
- [ ] Status set to Active
- [ ] Booking saved/published successfully

### End-to-End Verification
- [ ] CSV file accessible from web browser
- [ ] Datasource fetches data successfully
- [ ] Template preview shows correct seminars
- [ ] Booking appears in schedule as Active
- [ ] Screen displays seminars correctly
- [ ] Data updates propagate within 1 hour
- [ ] Only current week's seminars shown
- [ ] Only "website" tagged seminars shown
- [ ] Past seminars not displayed

---

## Data Binding Reference

### Available Columns from CSV

| Column Name | Description | Example | Use In Display |
|-------------|-------------|---------|----------------|
| `Title_Original` | Original title with prefix | WS, Björn Stinner: Finite... | ❌ No (reference only) |
| `Title` | Cleaned title | Björn Stinner: Finite element... | ✅ Yes |
| `Speaker` | Name and institution | Björn Stinner, University of Warwick | ✅ Yes |
| `Date` | ISO date format | 2025-11-18 | ❌ No (for sorting only) |
| `Date_Formatted` | Human-readable date | Tuesday 18 Nov | ✅ Yes |
| `Time` | Time range | 09:30-10:30 | ✅ Yes |
| `Location` | Room/venue | Kuskvillan | ✅ Yes |

### Binding Syntax Examples

**Simple field:**
```
{{Title}}
```

**Multiple fields:**
```
{{Date_Formatted}} • {{Time}}
```

**With prefix text:**
```
Speaker: {{Speaker}}
Location: {{Location}}
```

**With formatting:**
```
📅 {{Date_Formatted}}
🕐 {{Time}}
📍 {{Location}}
```

---

## Quick Reference Card

**CSV Datasource Settings:**
```
Name: Seminarier
URL: https://your-domain/smartsign/seminarier.csv
Fetch: Through Smartsign server
Interval: 3600 seconds
Encoding: UTF-8
Header row: ✓ Yes
```

**Template Bindings:**
```
Header: SEMINARS THIS WEEK (static text)
Date/Time: {{Date_Formatted}} • {{Time}}
Title: {{Title}}
Speaker: Speaker: {{Speaker}}
Location: Location: {{Location}}
```

**Booking Settings:**
```
Name: Seminar Display - Permanent
Content: Seminar Display (template)
Schedule: Daily, 00:00-23:59
End date: (blank - permanent)
Priority: High (80-90)
```

---

## Support

**For configuration help:**
- SmartSign Documentation: https://support.smartsign.com
- SmartSign Support: support@smartsign.com

**For data/script issues:**
- See: `docs/SETUP.md` (Troubleshooting section)
- IML IT Team: it@iml.se

---

**Document Version:** 1.0
**Last Updated:** 2025-11-17
**Related Documents:**
- [SETUP.md](SETUP.md) - Installation guide
- [PRD_SmartSign_Seminarier.md](PRD_SmartSign_Seminarier.md) - Requirements
- [ADR_SmartSign_Seminarier.md](ADR_SmartSign_Seminarier.md) - Architecture decisions
