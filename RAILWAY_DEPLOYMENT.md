# Railway Deployment Guide for SmartSign

**Status:** ✅ Ready to Deploy
**Last Updated:** November 18, 2025

---

## Quick Start (5 minutes)

### Prerequisites
- Railway account at https://railway.app
- Railway CLI installed: `npm install -g @railway/cli`

### Deploy Steps

```bash
# 1. Login to Railway
railway login

# 2. Create/select project
railway init

# 3. Deploy
railway up

# 4. Get URL
railway open
```

That's it! Your app will be live at: `https://your-project.railway.app/`

---

## What Railway Will Do

When you run `railway up`, Railway automatically:

1. **Detects Python** - Reads `requirements.txt`
2. **Installs dependencies** - pandas, openpyxl
3. **Detects Procfile** - Knows to run `python server.py`
4. **Builds the app** - Creates Docker image
5. **Deploys** - Starts server on Railway infrastructure
6. **Assigns URL** - Your app becomes live online

**Total build time:** ~2-3 minutes

---

## Railway Configuration Files

### ✅ Procfile (Required)
```
web: python server.py
```
- Tells Railway how to start your app
- Listens on PORT environment variable (set by Railway)

### ✅ requirements.txt (Required)
```
pandas>=1.3.0
openpyxl>=3.0.0
```
- Python dependencies for your app
- Railway automatically installs before running

### ✅ start.sh (Optional)
```bash
#!/bin/bash
echo "Starting SmartSign server..."
python server.py
```
- Alternative to Procfile for starting app
- Not needed if Procfile is present

### ✅ .railwayignore (Optional)
```
# Files to exclude from Railway deployment
*.xlsx
*.xls
docs/
*.md
*.bat
...
```
- Reduces deployment size
- Excludes unnecessary files (Excel, docs, batch scripts)

---

## Server Configuration

**File:** `server.py`

Railway automatically:
1. Sets `PORT` environment variable (default: 8080)
2. Binds server to `0.0.0.0:PORT`
3. Exposes via HTTPS at your Railway domain

**Server serves:**
- `GET /` → `template_simple.html`
- `GET /seminarier.csv` → CSV data
- `GET /iml_logo.png` → Logo image
- `GET /iml_background.png` → Background image
- `GET /health` → Health check

---

## Step-by-Step Deployment

### Step 1: Verify Files Exist

```bash
# In smartsign directory
ls -la Procfile requirements.txt start.sh
ls -la server.py template_simple.html seminarier.csv
ls -la iml_background.png iml_logo.png
```

All should exist ✓

### Step 2: Install Railway CLI

```bash
npm install -g @railway/cli
```

Verify:
```bash
railway --version
```

### Step 3: Login to Railway

```bash
railway login
```

Opens browser for authentication.

### Step 4: Create Railway Project

```bash
railway init
```

Creates `railway.json` with project config.

### Step 5: Deploy

```bash
railway up
```

Output will show:
```
✓ Found Procfile
✓ Deployed to Railway
✓ Your app is live at: https://your-project-xxxxx.railway.app
```

### Step 6: Get Your URL

```bash
railway open
```

Or check Railway dashboard:
- https://railway.app
- View your project
- Copy domain name

**Format:** `https://[project-name]-[random-id].railway.app`

---

## Testing Railway Deployment

### Test 1: Load Template

Open in browser: `https://your-project.railway.app/`

Should see:
- "Seminars this week" header
- Logo on right side
- Seminar cards with data
- No errors

### Test 2: CSV Endpoint

Open: `https://your-project.railway.app/seminarier.csv`

Should download CSV file with seminar data.

### Test 3: Images

Open: `https://your-project.railway.app/iml_logo.png`

Should display logo image.

### Test 4: Health Check

Open: `https://your-project.railway.app/health`

Should display: "OK"

---

## Troubleshooting

### Problem: "Railpack could not determine how to build the app"

**Solution:** Make sure these files exist at repository root:
- [ ] `Procfile` - Must specify `web: python server.py`
- [ ] `requirements.txt` - Must list Python dependencies
- [ ] `start.sh` - Alternative to Procfile (optional)

Files should NOT be in a subdirectory.

### Problem: "ModuleNotFoundError: No module named 'pandas'"

**Solution:** Verify `requirements.txt` contains:
```
pandas>=1.3.0
openpyxl>=3.0.0
```

Railway will install these automatically.

### Problem: App builds but doesn't respond

**Solution:** Check Railway logs:
```bash
railway logs
```

Look for errors like:
- Port binding issues
- Missing files
- Import errors

### Problem: Images not loading (404 errors)

**Solution:** Verify image files exist:
- [ ] `iml_background.png` at root
- [ ] `iml_logo.png` at root
- [ ] `.railwayignore` includes `!iml_*.png` to keep them

### Problem: CSV file not found

**Solution:** Ensure:
- [ ] `seminarier.csv` exists at root
- [ ] `.railwayignore` includes `!seminarier.csv`

### Problem: "Port already in use" (local testing)

**Solution:** Railway assigns port automatically. For local testing:
```bash
python server.py
# Or specify port:
PORT=8080 python server.py
```

---

## Environment Variables

Railway automatically sets:

| Variable | Value | Used By |
|----------|-------|---------|
| PORT | 8080 | server.py (os.environ.get('PORT', 8080)) |
| RAILWAY_ENVIRONMENT_ID | UUID | Internal tracking |
| RAILWAY_PROJECT_ID | UUID | Internal tracking |

Your server automatically uses PORT from environment.

---

## Daily Updates with Railway

### Automated Daily Deployment

To deploy updated CSV daily:

**Option 1: Windows Task Scheduler (Local)**

Run `deploy_railway.bat` daily at 00:00:
```batch
cd C:\Users\chrwah28.KVA\Development\smartsign
deploy_railway.bat
```

**Option 2: GitHub Actions (CI/CD)**

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Railway
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python filter_seminarier.py
      - run: |
          npm install -g @railway/cli
          railway login --token ${{ secrets.RAILWAY_TOKEN }}
          railway up
```

**Option 3: Manual Deployment**

When you need to update:
```bash
python filter_seminarier.py  # Generate CSV
railway up                    # Deploy
```

---

## Railway Project Settings

### Recommended Configuration

**Environment Variables:** None required (server auto-detects PORT)

**Health Check:** `/health`
- Railway can use this to verify app is healthy

**Memory:** 512 MB (free tier default)
- Sufficient for Python HTTP server

**Region:** europe-west4 (closest to Sweden/IML)
- Lower latency
- Better performance

**Builds:** Automatic on `git push`
- If you connect GitHub repo to Railway
- Allows CI/CD integration

---

## Monitoring & Logs

### View Logs

```bash
# Live logs
railway logs -f

# Last N lines
railway logs --lines 50

# Tail for specific service
railway logs --service web
```

### View Metrics

Access Railway dashboard:
- https://railway.app
- Select your project
- View CPU, Memory, Network usage
- Check deployment history

### Set Up Alerts

Railway provides:
- Deployment status
- Health check failures
- Resource warnings

Check Railway docs for alert setup.

---

## Free Tier Limits

Railway free tier includes:
- ✅ 500 MB disk
- ✅ 512 MB RAM
- ✅ $5 credit/month
- ✅ Unlimited deployments
- ✅ HTTPS included
- ✅ Automatic SSL certificates

This is **MORE than sufficient** for SmartSign.

---

## Custom Domain (Optional)

To use your own domain (e.g., `smartsign.iml.se`):

1. In Railway dashboard → Project Settings
2. Add Custom Domain
3. Point DNS to Railway
4. Railway auto-provisions SSL

Documentation: https://docs.railway.app/configure/custom-domain

---

## Updating Code

### Deploy Updates

```bash
# Make changes locally
# Update template_simple.html, server.py, etc.

# Commit to Git
git add .
git commit -m "Update SmartSign"

# Deploy to Railway
railway up

# Or if connected to GitHub:
git push  # Automatic deploy via GitHub Actions
```

### Rollback

```bash
# View deployment history
railway logs

# Redeploy previous version
railway up --force
```

---

## Performance Tips

### 1. Cache Control
Server sets smart cache headers:
- CSV: 5 minutes (data changes daily)
- Images: 24 hours (assets stable)
- HTML: 5 minutes (template may update)

### 2. Auto-Refresh
Template auto-refreshes every 60 minutes to pick up data changes.

### 3. Database (Future)
When connecting database:
```python
import os
db_url = os.environ.get('DATABASE_URL')
```

---

## Getting Help

### Railway Docs
- https://docs.railway.app

### Railway Community
- Discord: https://discord.gg/railway
- GitHub: https://github.com/railwayapp

### SmartSign Support
- support@smartsign.com

### IML IT Team
- it@iml.se

---

## Summary

You now have:

✅ **Procfile** - Railway knows how to start your app
✅ **requirements.txt** - Dependencies installed automatically
✅ **start.sh** - Alternative startup script
✅ **.railwayignore** - Optimized deployment (no unnecessary files)
✅ **server.py** - Production-ready Python server
✅ **template_simple.html** - Dynamic template with CSV loading
✅ **Images & CSV** - All assets ready

**Next step:** Run `railway up` and your app will be live!

---

**Status:** ✅ Ready for Railway Deployment
**Date:** November 18, 2025
**Version:** 1.0
