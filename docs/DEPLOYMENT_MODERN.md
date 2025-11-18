# Modern Hosting Deployment Guide - Vercel & Railway

**Deploy SmartSign CSV to modern hosting platforms**

---

## Overview

Instead of traditional FTP, you can deploy your `seminarier.csv` file to modern hosting platforms:

- **Vercel** - Best for static file hosting (recommended)
- **Railway** - Alternative with web server
- **Both platforms offer:**
  - ✅ Free tier available
  - ✅ Automatic HTTPS
  - ✅ Global CDN
  - ✅ CLI deployment
  - ✅ Git integration
  - ✅ One-command deployment

---

## Option 1: Vercel (Recommended)

### Why Vercel?

**Pros:**
- ✅ Perfect for static CSV hosting
- ✅ Extremely fast global CDN
- ✅ Simple deployment (one command)
- ✅ Free tier is generous
- ✅ Automatic HTTPS
- ✅ CORS configured automatically

**Cons:**
- ⚠️ Requires Node.js/npm
- ⚠️ CSV file is immutable per deployment (good for caching)

### Setup Vercel (One-Time)

#### Step 1: Install Vercel CLI

```cmd
npm install -g vercel
```

**Verify installation:**
```cmd
vercel --version
```

#### Step 2: Login to Vercel

```cmd
vercel login
```

- Opens browser for authentication
- Login with your Vercel account
- Or GitHub/GitLab/Bitbucket

#### Step 3: Initial Deployment

```cmd
cd C:\Users\chrwah28.KVA\Development\smartsign
vercel
```

- Answer setup questions:
  - **Set up and deploy:** Yes
  - **Which scope?** Your account
  - **Link to existing project?** No
  - **Project name:** `smartsign-seminarier` (or your choice)
  - **Directory:** `.` (current directory)
  - **Settings correct?** Yes

**First deployment complete!**

Vercel will give you a URL like:
```
https://smartsign-seminarier.vercel.app
```

Your CSV is available at:
```
https://smartsign-seminarier.vercel.app/seminarier.csv
```

### Daily Deployment (Automated)

#### Manual Method:

Run the deployment script:
```cmd
deploy_vercel.bat
```

This runs `vercel --prod --yes` automatically.

#### Automated Method:

Update your Windows Task Scheduler to run:
```cmd
cd C:\Users\chrwah28.KVA\Development\smartsign
python filter_seminarier.py && vercel --prod --yes
```

Or use the unified script:
```cmd
run_all_modern.bat
```
Choose option [1] for Vercel.

### Files Created for Vercel

**`vercel.json`** - Configuration
```json
{
  "version": 2,
  "name": "smartsign-seminarier",
  "routes": [
    {
      "src": "/seminarier.csv",
      "headers": {
        "Cache-Control": "public, max-age=300",
        "Content-Type": "text/csv; charset=utf-8",
        "Access-Control-Allow-Origin": "*"
      }
    }
  ]
}
```

**`.vercelignore`** - Excludes unnecessary files

### SmartSign Configuration

**CSV Datasource URL:**
```
https://your-project.vercel.app/seminarier.csv
```

**Settings:**
- Fetch method: Direct (Vercel CDN is very fast)
- Update interval: 3600 seconds (1 hour)
- Encoding: UTF-8

---

## Option 2: Railway

### Why Railway?

**Pros:**
- ✅ Full web server (more flexible)
- ✅ Can run Python scripts on server
- ✅ Free tier with $5/month credit
- ✅ Simple deployment
- ✅ Automatic HTTPS
- ✅ Good for future enhancements

**Cons:**
- ⚠️ Slightly more complex than Vercel
- ⚠️ Requires running Python server
- ⚠️ Free tier has sleep mode (500 hours/month)

### Setup Railway (One-Time)

#### Step 1: Install Railway CLI

```cmd
npm install -g @railway/cli
```

**Verify installation:**
```cmd
railway --version
```

#### Step 2: Login to Railway

```cmd
railway login
```

- Opens browser for authentication
- Login with your Railway account
- Or GitHub authentication

#### Step 3: Create Project

Via CLI:
```cmd
cd C:\Users\chrwah28.KVA\Development\smartsign
railway init
```

- **Project name:** `smartsign-seminarier`
- Creates new Railway project

Or via web dashboard:
1. Go to https://railway.app
2. Click "New Project"
3. Choose "Empty Project"
4. Name it "smartsign-seminarier"

#### Step 4: Link Local Directory

```cmd
railway link
```

Choose your project from the list.

#### Step 5: Initial Deployment

```cmd
railway up
```

Railway will:
- Detect Python application
- Install dependencies
- Start `server.py`
- Give you a deployment URL

**Get your URL:**
```cmd
railway open
```

Or check Railway dashboard.

Your CSV is available at:
```
https://your-project.railway.app/seminarier.csv
```

### Daily Deployment (Automated)

#### Manual Method:

Run the deployment script:
```cmd
deploy_railway.bat
```

This runs `railway up` automatically.

#### Automated Method:

Update your Windows Task Scheduler to run:
```cmd
cd C:\Users\chrwah28.KVA\Development\smartsign
python filter_seminarier.py && railway up
```

Or use the unified script:
```cmd
run_all_modern.bat
```
Choose option [2] for Railway.

### Files Created for Railway

**`server.py`** - Simple Python web server
```python
# Serves CSV file with CORS headers
# Runs on port 8080 (or PORT env variable)
```

**`Procfile`** - Tells Railway how to start
```
web: python server.py
```

**`railway.json`** - Configuration (optional)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python server.py"
  }
}
```

**`.railwayignore`** - Excludes unnecessary files

### SmartSign Configuration

**CSV Datasource URL:**
```
https://your-project.railway.app/seminarier.csv
```

**Settings:**
- Fetch method: Through Smartsign server (Railway can handle it)
- Update interval: 3600 seconds (1 hour)
- Encoding: UTF-8

---

## Comparison: Vercel vs Railway

| Feature | Vercel | Railway |
|---------|--------|---------|
| **Best for** | Static files | Web applications |
| **Deployment** | `vercel --prod` | `railway up` |
| **Free tier** | Generous, no limits | $5/month credit |
| **Speed** | Very fast CDN | Fast, no CDN |
| **Setup complexity** | Very simple | Simple |
| **Server required** | No | Yes (included) |
| **HTTPS** | Automatic | Automatic |
| **Custom domain** | Easy | Easy |
| **CSV updates** | Redeploy file | Redeploy or restart |
| **Cold starts** | None | Possible on free tier |

**Recommendation:** **Vercel** for simplicity and speed

---

## Complete Automated Workflow

### Option A: Vercel Automation

**1. Update filter script path (if needed)**

Edit line 72 in `filter_seminarier.py`:
```python
excel_file = r"C:\Users\chrwah28.KVA\Downloads\ProgramExport (2).xlsx"
```

**2. Test manual workflow**

```cmd
cd C:\Users\chrwah28.KVA\Development\smartsign
python filter_seminarier.py
vercel --prod --yes
```

**3. Create automated batch file**

Create `automated_vercel.bat`:
```batch
@echo off
cd C:\Users\chrwah28.KVA\Development\smartsign
python filter_seminarier.py
if %ERRORLEVEL% EQU 0 (
    vercel --prod --yes
)
```

**4. Update Task Scheduler**

- Task Name: SmartSign Seminar Filter
- Action: Run `automated_vercel.bat`
- Schedule: Daily at 00:00
- Run as: SYSTEM

**5. Done!**

Fully automated: Excel → Python → CSV → Vercel → SmartSign → Screen

### Option B: Railway Automation

Same steps as Vercel, but use `railway up` instead of `vercel --prod`

---

## Unified Deployment Script

**Use the modern deployment script:**

```cmd
run_all_modern.bat
```

**Menu options:**
1. Vercel (recommended)
2. Railway (alternative)
3. Traditional FTP (old method)
4. Skip deployment (manual)

**Workflow:**
1. Filters seminars automatically
2. Generates CSV
3. Deploys to your chosen platform
4. Gives you the URL for SmartSign

---

## Testing Your Deployment

### Test 1: CSV File Accessibility

Open browser and navigate to:
```
https://your-deployment-url.vercel.app/seminarier.csv
```
or
```
https://your-deployment-url.railway.app/seminarier.csv
```

**Expected:** CSV file downloads or displays in browser

### Test 2: CSV Content

Open the downloaded CSV and verify:
- ✅ Header row: `Title_Original,Title,Speaker,Date,Date_Formatted,Time,Location`
- ✅ Seminars for current week only
- ✅ Only future events
- ✅ Only "website" tagged seminars
- ✅ UTF-8 encoding (Swedish characters display correctly)

### Test 3: SmartSign Datasource

In SmartSign CMS:
1. Create CSV Datasource with your deployment URL
2. Click "Test" or "Fetch Data"
3. Verify row count matches expected seminars
4. Preview shows correct data

### Test 4: Automatic Updates

1. Update source Excel file
2. Wait until midnight (or run script manually)
3. Check deployment URL in browser (should show new data)
4. Wait 1 hour for SmartSign to refresh
5. Verify screen shows updated seminars

---

## Troubleshooting

### Vercel Issues

**Problem:** `vercel: command not found`

**Solution:**
```cmd
npm install -g vercel
vercel login
```

**Problem:** "Not authorized"

**Solution:**
```cmd
vercel login
```
Complete authentication in browser.

**Problem:** "File size too large"

**Solution:**
CSV file should be < 5 KB. If larger, check for issues in filtering.

### Railway Issues

**Problem:** `railway: command not found`

**Solution:**
```cmd
npm install -g @railway/cli
railway login
```

**Problem:** "No project linked"

**Solution:**
```cmd
railway link
```
Choose your project from list.

**Problem:** "Server not responding"

**Solution:**
- Check `server.py` is running
- View logs: `railway logs`
- Restart: `railway restart`

### General Issues

**Problem:** CSV shows old data on deployment

**Solution:**
1. Verify `seminarier.csv` is updated locally
2. Redeploy: `vercel --prod --yes` or `railway up`
3. Clear browser cache
4. Wait a few minutes for CDN propagation

**Problem:** SmartSign can't fetch CSV

**Solution:**
1. Test URL directly in browser
2. Verify URL is publicly accessible
3. Check CORS headers (should be `Access-Control-Allow-Origin: *`)
4. Try "Through Smartsign server" fetch method

---

## Cost Comparison

### Vercel Free Tier

**Includes:**
- Unlimited deployments
- 100 GB bandwidth/month
- Automatic SSL
- Global CDN

**Cost:** $0/month (free tier is sufficient)

### Railway Free Tier

**Includes:**
- $5 credit/month
- 500 hours execution time/month
- Unlimited deployments
- Automatic SSL

**Cost:** $0/month (free tier is sufficient)

**Both platforms:** Your CSV file usage will easily fit in free tier

---

## Advanced: GitHub Actions Automation

For fully automated deployment without Task Scheduler:

### 1. Create GitHub Repository

```cmd
cd C:\Users\chrwah28.KVA\Development\smartsign
git init
git add .
git commit -m "Initial commit"
```

### 2. Create `.github/workflows/deploy.yml`

```yaml
name: Deploy SmartSign CSV

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:  # Manual trigger

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install pandas openpyxl

      - name: Run filter script
        run: python filter_seminarier.py

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

**Note:** Excel file would need to be in repo or fetched from another source

---

## Migration from FTP

**If you're currently using FTP:**

1. **Test Vercel/Railway first**
   ```cmd
   deploy_vercel.bat
   ```

2. **Update SmartSign datasource URL**
   - Old: `https://ftp-server.com/path/seminarier.csv`
   - New: `https://your-project.vercel.app/seminarier.csv`

3. **Verify data appears correctly**

4. **Update Task Scheduler**
   - Change from FTP upload to Vercel/Railway deployment

5. **Decommission FTP** (after confirming new method works)

---

## Summary

**Recommended Setup: Vercel**

**One-time setup (10 minutes):**
```cmd
npm install -g vercel
vercel login
cd C:\Users\chrwah28.KVA\Development\smartsign
vercel
```

**Daily automation:**
- Task Scheduler runs `python filter_seminarier.py && vercel --prod --yes`
- Or run `deploy_vercel.bat` manually

**Result:**
- CSV automatically deployed to global CDN
- HTTPS enabled
- Fast access from anywhere
- Free hosting
- Zero maintenance

**SmartSign URL:**
```
https://your-project.vercel.app/seminarier.csv
```

---

**Questions?**
- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- See `QUICKSTART.md` for other setup options

**Version:** 1.0
**Last Updated:** 2025-11-17
