# Modern Hosting Quick Start - Vercel & Railway

**The easiest way to deploy your SmartSign CSV**

---

## 🚀 Recommended: Vercel (3 Steps, 5 Minutes)

### Step 1: Install Vercel CLI
```cmd
npm install -g vercel
```

### Step 2: Login & Deploy
```cmd
cd C:\Users\chrwah28.KVA\Development\smartsign
vercel login
vercel
```
Answer the prompts, accept defaults.

### Step 3: Get Your URL
Vercel will give you a URL like:
```
https://smartsign-seminarier.vercel.app/seminarier.csv
```

**Use this URL in SmartSign CSV Datasource!**

---

## 📦 Daily Updates (Automatic)

### Option A: One-Click Script
```cmd
deploy_vercel.bat
```

### Option B: Integrated Workflow
```cmd
run_all_modern.bat
```
Choose option [1] for Vercel

### Option C: Task Scheduler (Fully Automated)

Update your scheduled task to run:
```cmd
python filter_seminarier.py && vercel --prod --yes
```

**Done!** Updates deploy automatically every night.

---

## 🎯 What You Get

✅ **Free hosting** - No cost for your use case
✅ **Auto HTTPS** - Secure by default
✅ **Global CDN** - Fast from anywhere
✅ **Simple deployment** - One command: `vercel --prod`
✅ **Version history** - Rollback anytime
✅ **Zero maintenance** - Just works

---

## 🔄 Complete Automated Flow

```
Excel File → Python Script → CSV Generated → Vercel Deploys → SmartSign Fetches → Screen Displays
    ↓             ↓              ↓                ↓                  ↓               ↓
  Manual     Daily 00:00    seminarier.csv   Automatic CDN      Every hour    Live display
                                              30 seconds
```

**Everything automatic after initial setup!**

---

## 📋 SmartSign Configuration

**CSV Datasource Settings:**
- URL: `https://your-project.vercel.app/seminarier.csv`
- Fetch method: Direct
- Update interval: 3600 seconds (1 hour)
- Encoding: UTF-8
- First row is header: ✓ Yes

---

## 🆘 Troubleshooting

### "vercel: command not found"
```cmd
npm install -g vercel
```

### "Not authenticated"
```cmd
vercel login
```

### CSV shows old data
```cmd
vercel --prod --yes
```
Wait 1-2 minutes for CDN propagation.

---

## 🔄 Alternative: Railway

**If you prefer Railway:**

```cmd
npm install -g @railway/cli
railway login
railway init
railway up
```

**Your URL:** `https://your-project.railway.app/seminarier.csv`

**See:** `docs\DEPLOYMENT_MODERN.md` for details

---

## ⚡ Why This Is Better Than FTP

| Feature | Vercel/Railway | Traditional FTP |
|---------|----------------|-----------------|
| **Setup time** | 5 minutes | 20+ minutes |
| **HTTPS** | Automatic | Manual config |
| **Speed** | Global CDN | Single server |
| **Cost** | Free | Varies |
| **Deployment** | One command | FTP client setup |
| **Rollback** | Easy | Manual |
| **Monitoring** | Built-in dashboard | Custom setup |

---

## 📁 Files Created

**Vercel:**
- `vercel.json` - Configuration
- `.vercelignore` - Deployment filter
- `deploy_vercel.bat` - Deployment script

**Railway:**
- `server.py` - Python web server
- `Procfile` - Railway start command
- `railway.json` - Configuration
- `.railwayignore` - Deployment filter
- `deploy_railway.bat` - Deployment script

**Unified:**
- `run_all_modern.bat` - Choose platform at runtime

---

## 🎓 Learning More

**Vercel Documentation:**
https://vercel.com/docs

**Railway Documentation:**
https://docs.railway.app

**Detailed Guide:**
`docs\DEPLOYMENT_MODERN.md` - Complete 20-page guide

---

## ✅ Checklist

- [ ] Node.js/npm installed
- [ ] Vercel CLI installed (`npm install -g vercel`)
- [ ] Logged in to Vercel (`vercel login`)
- [ ] Initial deployment done (`vercel`)
- [ ] Got deployment URL
- [ ] Tested URL in browser (CSV downloads)
- [ ] Updated SmartSign datasource with URL
- [ ] Verified data appears in SmartSign
- [ ] Updated Task Scheduler for automatic deployment

**Total time:** ~15 minutes

---

## 🎉 You're Done!

**Your system now:**
1. ✅ Filters seminars daily at midnight
2. ✅ Deploys to Vercel automatically
3. ✅ Serves CSV from global CDN
4. ✅ Updates SmartSign hourly
5. ✅ Displays on screens automatically

**Zero manual intervention needed!**

---

**Next:** Configure SmartSign CMS
**See:** `docs\SMARTSIGN_CONFIG.md`

**Version:** 1.0
**Last Updated:** 2025-11-17
