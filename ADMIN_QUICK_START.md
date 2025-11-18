# SmartSign Admin Tool - Quick Start Guide

**For non-technical users who just want to update seminars easily.**

---

## 🎯 The Simple Process

```
1. Run admin tool
2. Drag Excel file
3. Click "Update Seminars"
4. Done! Display updates automatically.
```

That's it! No command line, no technical knowledge needed.

---

## 📖 Step-by-Step Instructions

### Step 1: Open the Admin Tool

**Option A: Quick Click (Easiest)**
- Double-click: `run_admin.bat`
- Your browser opens automatically
- You see the upload page

**Option B: Using Command Prompt**
```
Open Command Prompt and type:
C:\Users\chrwah28.KVA\Development\smartsign\run_admin.bat
```

**Result:** You'll see this in your browser at `http://localhost:9000`:

```
┌─────────────────────────────────┐
│   SmartSign Admin               │
│  Update your seminar display    │
│                                 │
│   ┌───────────────────────┐    │
│   │      Drop file here   │    │
│   │   or click to browse  │    │
│   └───────────────────────┘    │
│                                 │
│ [Update Seminars]  [Clear]      │
│                                 │
└─────────────────────────────────┘
```

---

### Step 2: Prepare Your Excel File

**Before uploading, make sure:**

1. **File format:** Must be `.xlsx` (newer Excel)
   - Don't use `.xls` (old Excel)
   - Not CSV, not PDF - Excel only!

2. **Columns needed:**
   | Column | Example |
   |--------|---------|
   | **Title** | Machine Learning Basics |
   | **Speaker** | Dr. Jane Smith, MIT |
   | **Date** | 2025-11-20 |
   | **Time** | 14:00-15:00 |
   | **Location** | Main Hall |
   | **Tag(s)** | **website** ← Important! |

3. **Tag seminars with "website"**
   - This tag tells the system: "Show this on the digital display"
   - Without the tag, it won't appear on screen
   - Case doesn't matter ("website", "Website", "WEBSITE" all work)

4. **Save your file**
   - Make sure changes are saved
   - File size under 10MB

---

### Step 3: Drag and Drop

**Option A: Drag File (Easiest)**
1. Open your Excel file (or have file browser open)
2. Drag the Excel file from your file browser
3. Drop it into the upload box

**Option B: Click to Browse**
1. Click the upload box
2. File browser opens
3. Find your Excel file
4. Click "Open"

**You'll see:**
```
✓ your_file.xlsx
  150 KB

[Update Seminars]  [Clear]
```

---

### Step 4: Click "Update Seminars"

Click the big blue **"Update Seminars"** button.

**You'll see:**
- Loading spinner (few seconds)
- Green success message

**Success Message:**
```
✓ Success!
  CSV updated with 4 seminars successfully!
  Display will update via automatic deployment
```

---

### Step 5: Done! 🎉

The display updates automatically within:
- **Immediately:** If you click "Deploy Now" button
- **Within 1 hour:** Automatic refresh picks up changes
- **Within 24 hours:** Latest update for sure

You can close your browser. The system handles everything else.

---

## ❓ Frequently Asked Questions

### Q: Do I need to do anything technical?
**A:** No! Just drag, drop, and click. That's it.

### Q: What if something goes wrong?
**A:** The system shows an error message in plain English. Try uploading again. If it persists, contact IT: it@iml.se

### Q: Can I close the window after uploading?
**A:** Yes! The update is already being processed. You can close the browser.

### Q: Do I need to tag every seminar?
**A:** Only seminars tagged "website" show on the display. Other tags like "internal" or "external" are ignored.

### Q: What if I upload the wrong file?
**A:** No problem! Upload the correct file and it replaces the old one. Just click "Update Seminars" again.

### Q: Can I upload files larger than 10MB?
**A:** No. Excel files should always be under 5MB. If yours is bigger, delete old data or split into separate files.

### Q: What if the Excel file has errors?
**A:** The system shows a clear error message. Common issues:
- Missing "Date" column → Add it
- Wrong date format → Use YYYY-MM-DD (2025-11-20)
- Blank cells → Fill in all fields

### Q: Do I need to do anything else after uploading?
**A:** No! The system automatically:
- Filters seminars
- Generates the data file
- Updates the display
- All in 1-2 minutes

Just wait and check the screen.

---

## 🖼️ What You'll See on the Display

After upload, the digital screen shows:

```
┌──────────────────────────────────────┐
│ Upcoming Seminars           [Logo]   │
├──────────────────────────────────────┤
│ Wednesday 19 Nov • 09:30-11:30       │
│ Data Science Workshop                │
│ Speaker: Dr. Alice Johnson, Harvard  │
│ Location: Auditorium C               │
├──────────────────────────────────────┤
│ Thursday 20 Nov • 15:00-16:00        │
│ Web Development with Django          │
│ Speaker: Mr. Bob Wilson, Google      │
│ Location: Kuskvillan                 │
└──────────────────────────────────────┘
```

---

## ⚡ Quick Checklist Before Uploading

- [ ] File is Excel format (.xlsx)
- [ ] File is under 10MB
- [ ] All columns present: Title, Speaker, Date, Time, Location
- [ ] Seminars tagged with "website"
- [ ] Dates in YYYY-MM-DD format (2025-11-20)
- [ ] File saved

---

## 📞 Need Help?

**Common Issues:**

| Problem | Solution |
|---------|----------|
| "Page won't load" | Make sure you ran `run_admin.bat` |
| "File not accepted" | Must be `.xlsx` not `.xls` or `.csv` |
| "No seminars found" | Check if tagged with "website" |
| "Nothing on display" | Wait 1-2 minutes, then refresh screen |

**Contact IT:**
- Email: it@iml.se
- Include screenshot of error if possible

---

## 🎓 Behind the Scenes (For Curious Admins)

**What happens when you upload:**

1. System reads your Excel file
2. Finds seminars tagged "website"
3. Keeps only this week's seminars
4. Removes past events (before current time)
5. Generates data file
6. Updates display

**Filtering removes:**
- ❌ Seminars without "website" tag
- ❌ Seminars from last week
- ❌ Events already happened
- ❌ Empty rows

**Keeps only:**
- ✅ This week's seminars
- ✅ Future events (still to come)
- ✅ Tagged with "website"

---

## 💡 Tips for Success

1. **Keep it simple:** Use standard date format (2025-11-20)
2. **One file:** Upload the full Excel export, not split files
3. **Tag everything:** Always use "website" tag for display
4. **Check before:** Make sure Excel has no errors before uploading
5. **Wait a moment:** Give system 1-2 minutes to update display

---

## ✅ You're Ready!

Your admin tool is set up and ready to use. Just:

1. Double-click `run_admin.bat`
2. Drag your Excel file
3. Click "Update Seminars"
4. Done!

**Happy updating!** 🎉

---

**Questions?** Contact: it@iml.se
