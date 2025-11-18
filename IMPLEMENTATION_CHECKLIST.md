# SmartSign Railway Implementation Checklist

**Quick Start Guide for Full Deployment**

---

## ✅ Pre-Implementation (Complete)

- [x] Enhanced `template_simple.html` with JavaScript CSV loader
- [x] Updated `server.py` to serve HTML, assets, and CSV
- [x] Updated `deploy_railway.bat` with automation
- [x] Created comprehensive setup guide (`RAILWAY_HYBRID_SETUP.md`)

**All components are ready!**

---

## 🚀 Phase 1: Local Testing (15 minutes)

1. **Open Command Prompt**
   ```cmd
   cd C:\Users\chrwah28.KVA\Development\smartsign
   ```

2. **Generate CSV from Excel**
   ```cmd
   python filter_seminarier.py
   ```
   - [ ] Script completes successfully
   - [ ] `seminarier.csv` created/updated

3. **Start Local Server**
   ```cmd
   python server.py
   ```
   - [ ] Server shows "running on port 8080"
   - [ ] Terminal shows "Press Ctrl+C to stop"

4. **Test in Browser**
   - [ ] Open `http://localhost:8080/`
   - [ ] "Seminars this week" header appears
   - [ ] Logo visible on right side
   - [ ] Seminar cards loading from CSV
   - [ ] All seminar details display correctly

5. **Test CSV Endpoint**
   - [ ] Open `http://localhost:8080/seminarier.csv`
   - [ ] CSV file downloads with data

6. **Stop Server**
   - [ ] Press `Ctrl+C` in command prompt
   - [ ] Server stops cleanly

**Status: Ready to deploy to Railway ✓**

---

## 🌐 Phase 2: Deploy to Railway (20 minutes)

1. **Install Railway CLI** (if not already installed)
   ```cmd
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```cmd
   railway login
   ```
   - [ ] Browser opens for authentication
   - [ ] Login successful

3. **Create Railway Project** (first time only)
   ```cmd
   railway init
   ```
   - [ ] `railway.json` created
   - [ ] Project ID displayed

4. **Deploy Automatically**
   ```cmd
   deploy_railway.bat
   ```
   - [ ] Filter script runs successfully
   - [ ] Files verified
   - [ ] Deployment to Railway completes
   - [ ] Success message shown

5. **Get Railway URL**
   ```cmd
   railway open
   ```
   - [ ] Railway dashboard opens
   - [ ] Copy your project domain
   - [ ] Format: `https://your-project-xxxxx.railway.app`

6. **Test Railway Deployment**
   - [ ] Open Railway URL in browser
   - [ ] Template loads (same as localhost)
   - [ ] Seminars display correctly
   - [ ] Logo and images load

**Status: Deployed to Railway ✓**

---

## 📺 Phase 3: Configure SmartSign (15 minutes)

1. **Open SmartSign CMS Admin**
   - [ ] Login to SmartSign
   - [ ] Navigate to **Publishing → Channels**

2. **Create New Webpage Booking**
   - [ ] Click **"+ New Booking"**
   - [ ] Name: `Seminar Display`
   - [ ] Description: `Weekly seminars (auto-updated)`

3. **Configure Booking Details**
   - [ ] Start Date: Today's date
   - [ ] End Date: (leave blank for permanent)
   - [ ] Start Time: 00:00
   - [ ] End Time: 23:59
   - [ ] Recurrence: Daily
   - [ ] Days: All days (Mon-Sun)

4. **Add Webpage Content**
   - [ ] Content Type: **Webpage**
   - [ ] URL: `https://your-project-xxxxx.railway.app/`
   - [ ] Playback Mode: **Live**
   - [ ] Snapshot Refresh: 3600 seconds (1 hour)

5. **Assign to Screen**
   - [ ] Channel: Select your digital screen
   - [ ] Priority: 80-90 (High)
   - [ ] Status: Active/Enabled

6. **Save & Publish**
   - [ ] Click **Save**
   - [ ] Click **Publish**
   - [ ] Booking appears in schedule as "Active"

**Status: SmartSign configured ✓**

---

## 🖥️ Phase 4: Verify on Screen (10 minutes)

1. **Check Digital Screen**
   - [ ] Screen is powered on
   - [ ] Screen is connected to network
   - [ ] Wait 1-2 minutes for content

2. **Verify Display**
   - [ ] Header "Seminars this week" visible
   - [ ] Logo appears on right side
   - [ ] Logo vertically aligned with header
   - [ ] Seminar cards display with:
     - [ ] Date (e.g., "Tuesday 18 Nov")
     - [ ] Time (e.g., "09:30-10:30")
     - [ ] Seminar title
     - [ ] Speaker name and institution
     - [ ] Location (e.g., "Kuskvillan")

3. **Troubleshoot if Needed**
   - [ ] See "RAILWAY_HYBRID_SETUP.md" troubleshooting section
   - [ ] Check SmartSign logs
   - [ ] Verify Railway URL is accessible

**Status: Display verified ✓**

---

## ⏰ Phase 5: Set Up Daily Automation (15 minutes)

1. **Open Windows Task Scheduler**
   - [ ] Windows key → Type "Task Scheduler"
   - [ ] Click "Task Scheduler"

2. **Create New Task**
   - [ ] Right-click **Task Scheduler Library**
   - [ ] Click **Create Task**
   - [ ] Name: `SmartSign Railway Deploy`
   - [ ] Description: `Daily deployment of seminars to Railway`
   - [ ] Check: **Run with highest privileges**

3. **Configure Trigger**
   - [ ] Go to **Triggers** tab
   - [ ] Click **New**
   - [ ] Begin task: **On a schedule**
   - [ ] Daily, Start time: **00:00** (midnight)
   - [ ] Check: **Repeat task every 1 day**

4. **Configure Action**
   - [ ] Go to **Actions** tab
   - [ ] Click **New**
   - [ ] Program: `C:\Users\chrwah28.KVA\Development\smartsign\deploy_railway.bat`
   - [ ] Start in: `C:\Users\chrwah28.KVA\Development\smartsign`

5. **Verify Task**
   - [ ] Click **OK** to save
   - [ ] Task appears in list
   - [ ] Check **History** tab for previous runs

**Status: Automation set up ✓**

---

## 📝 Daily Workflow (Going Forward)

**Every Day (Admin):**
1. [ ] Update Excel seminar file with new seminars
2. [ ] Tag seminars with "website" for public display
3. [ ] Save as `ProgramExport (2).xlsx` in Downloads
4. **That's it!** The rest is automatic.

**Automatic (Every Night at Midnight):**
1. Windows Task Scheduler runs `deploy_railway.bat`
2. Filter script processes Excel
3. CSV is generated with current week's seminars
4. Deployment to Railway
5. SmartSign updates within 1 hour
6. Display shows new seminars next morning

---

## 🎯 Success Criteria

✅ **Implementation Complete When:**
- [ ] Template loads locally
- [ ] Template loads from Railway URL
- [ ] SmartSign booking is Active
- [ ] Digital screen displays seminars
- [ ] Logo is properly positioned
- [ ] All seminar details visible
- [ ] No errors on screen or in logs
- [ ] Task Scheduler automation is set

---

## 📞 Need Help?

### Testing Issues
See: `RAILWAY_HYBRID_SETUP.md` → Troubleshooting section

### SmartSign Questions
Contact: SmartSign Support (support@smartsign.com)

### Railway Issues
Docs: https://docs.railway.app

### IML IT Support
Email: it@iml.se

---

## 📊 Project Summary

| Component | Status | Location |
|-----------|--------|----------|
| HTML Template | ✅ Enhanced | `template_simple.html` |
| Python Server | ✅ Updated | `server.py` |
| CSV Loader | ✅ Implemented | JavaScript in template |
| Deployment Script | ✅ Updated | `deploy_railway.bat` |
| Setup Guide | ✅ Complete | `RAILWAY_HYBRID_SETUP.md` |
| This Checklist | ✅ Complete | `IMPLEMENTATION_CHECKLIST.md` |

---

**All components are ready for deployment!** 🚀

Next step: Follow the checklist phases above to deploy to your environment.

---

**Document Version:** 1.0
**Date:** 2025-11-18
**Status:** Ready for Implementation
