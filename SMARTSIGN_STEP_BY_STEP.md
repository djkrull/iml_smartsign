# SmartSign Setup - Step-by-Step with Screenshots

**Your Production URL:** `https://imlsmartsign-production.up.railway.app`

---

## Step 1: Add Webpage

**Location:** Media Library → Bottom right button
**Click:** "+ Add webpage"

This opens the webpage configuration form.

---

## Step 2: Fill in Webpage Details

### Basic Information

**Name/Title:**
```
Seminar Display - IML Production
```

**Description (optional):**
```
Weekly seminars from Institut Mittag-Leffler (auto-updated)
```

### URL Configuration

**Webpage URL:**
```
https://imlsmartsign-production.up.railway.app/
```

⚠️ **Important:**
- Include `https://` (not http)
- End with `/` (trailing slash)
- Copy exactly as shown

### Display Mode

**Select:** "Live"
- Real-time display
- Auto-refreshes
- Works on all screens

**OR if you prefer "Snapshot" mode:**
- Snapshot Refresh: 3600 seconds (1 hour)
- Works on all players

---

## Step 3: Save the Webpage

1. **Fill in all fields above**
2. **Click "Save"** button
3. Webpage is created and added to Media Library

---

## Step 4: Create a Booking

**Navigation:** Publishing → Bookings → New Booking

### Booking Details

**Name:**
```
Seminar Display - Production
```

**Description:**
```
Weekly seminars for digital signage
```

**Content Type:** Select "Webpage"

**Webpage:** Select the webpage you just created
```
Seminar Display - IML Production
```

---

## Step 5: Configure Schedule

**Start Date:** Today's date (or future date)
**End Date:** Leave blank (for permanent display)

**Time:**
- Start: 00:00 (midnight)
- End: 23:59 (end of day)

**Recurrence:** Daily
**Days:** All days (Mon-Sun)

---

## Step 6: Assign to Channel

**Channel Assignment:**
1. Find your digital screen channel
2. **Priority:** Set to 80-90 (High)
3. **Status:** Active/Enabled

---

## Step 7: Publish

1. **Click "Save"**
2. **Click "Publish"**
3. Status should change to **"Active"**

---

## Step 8: Verify on Screen

**Wait 1-2 minutes, then check your digital screen:**

✅ Should show:
- "Seminars this week" header
- IML logo on right side
- Seminar cards with details
- Professional layout
- No errors

---

## What You'll See on the Screen

```
┌────────────────────────────────────────────┐
│                                            │
│   Seminars this week            [Logo]     │
│                                            │
├────────────────────────────────────────────┤
│ Tuesday 18 Nov • 09:30-10:30                │
│ Björn Stinner: Finite element...          │
│ Speaker: Björn Stinner, University...     │
│ Location: Kuskvillan                       │
│                                            │
├────────────────────────────────────────────┤
│ Tuesday 18 Nov • 11:00-12:00                │
│ Manuel Solano: The Transfer Path...       │
│ Speaker: Manuel Solano, Universidad...    │
│ Location: Kuskvillan                       │
└────────────────────────────────────────────┘
```

---

## Troubleshooting

### Display shows blank

1. **Check booking is Active**
   - Publishing → Bookings
   - Find "Seminar Display - Production"
   - Status should be "Active"

2. **Wait 1-2 minutes**
   - SmartSign needs time to fetch
   - Cache updates can take a moment

3. **Manually refresh**
   - Edit booking and click "Publish" again
   - Sometimes forces immediate update

### URL not loading

1. **Verify exact URL:**
   ```
   https://imlsmartsign-production.up.railway.app/
   ```
   - With `https://`
   - With trailing `/`
   - No typos

2. **Test in browser:**
   - Open URL in web browser
   - Should show seminars
   - If blank, check Railway server

3. **Check Railway status:**
   ```bash
   railway logs
   ```
   - Look for errors
   - Verify server is running

### Seminars not showing

1. **Check CSV has data**
   - Open: https://imlsmartsign-production.up.railway.app/seminarier.csv
   - Should download CSV file
   - File should have seminar rows

2. **Check Excel file**
   - Run: `python filter_seminarier.py`
   - Check for seminars this week
   - Verify "website" tag on seminars

3. **Deploy latest CSV**
   - Run: `deploy_railway.bat`
   - Wait 1-2 minutes
   - SmartSign will fetch updated data

---

## Next: Daily Updates

After setup is working, you have two options:

### Option 1: Manual Update
When you add seminars to Excel:
1. Tag with "website"
2. Run: `python filter_seminarier.py`
3. Run: `deploy_railway.bat`
4. SmartSign updates within 1 hour

### Option 2: Automatic Update (Recommended)
Set up Windows Task Scheduler to run daily:
- Task: `deploy_railway.bat`
- Time: 00:00 (midnight)
- Frequency: Daily
- Seminars update automatically every morning

---

## Success Checklist

- [ ] Webpage created in Media Library
- [ ] Booking created in Publishing → Bookings
- [ ] Booking is Active
- [ ] Digital screen displays seminars
- [ ] Logo is visible and aligned
- [ ] All seminar details showing
- [ ] No error messages
- [ ] Professional appearance

---

## Support

**If issues occur:**
1. Check SMARTSIGN_SETUP_GUIDE.md for troubleshooting
2. Verify Railway URL: https://imlsmartsign-production.up.railway.app
3. Check SmartSign logs in CMS
4. Contact: support@smartsign.com or it@iml.se

---

**You're all set!** Your seminar display is now live and automated. 🎉

Every day at midnight, new seminars will automatically appear on your screen.
