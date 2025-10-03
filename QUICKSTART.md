# SQL Scanner Dashboard - Quick Reference

## 🚀 Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python dashboard.py

# Access at: http://localhost:5050
```

## 🌐 Deploy to Render (5 Minutes)

**No environment variables needed!** Users enter target URLs directly in the web UI.

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```

### Step 2: Deploy on Render
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Click **"Apply"**
5. Wait 2-5 minutes ✨

### Step 3: Access Your App
Your app will be live at: `https://your-app-name.onrender.com`

**Enter any website URL to scan - no configuration needed!**

## 📋 Important Files

| File | Purpose |
|------|---------|
| `render.yaml` | Render deployment config |
| `requirements.txt` | Python dependencies |
| `runtime.txt` | Python version (3.11.0) |
| `dashboard.py` | Main Flask application |
| `app.py` | Scanner logic |
| `.gitignore` | Files to exclude from Git |

## 🔧 Configuration

### Environment Variables (Set in Render - Minimal!)
```
PYTHON_VERSION=3.11.0
FLASK_ENV=production
```

**That's it!** No START_URL needed - users enter URLs in the web interface.

### Scanner Parameters (Adjustable in UI)
- **Max Depth**: 1-3 (crawl depth)
- **Concurrency**: 5-10 (parallel requests)
- **Delay**: 0.5-1.0 seconds (between requests)

## 🎯 Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Main dashboard |
| `/health` | Health check (for monitoring) |
| `/api/status` | Scan status |
| `/api/results` | Get results (JSON/CSV) |
| `/scan` | Trigger new scan |

## ⚠️ Important Notes

1. **Legal Use Only**: Only scan sites you own or have permission to test
2. **Free Tier Limits**: App sleeps after 15min inactivity (cold starts)
3. **Performance**: Start with low concurrency, increase gradually
4. **Target Sites**: Some sites may block cloud IPs

## 🆘 Troubleshooting

### Build Fails
- Check `requirements.txt` syntax
- Verify Python version in `runtime.txt`

### App Won't Start
- Check Render logs
- Verify environment variables
- Ensure using `PORT` from environment

### Scanner Issues
- Test target URL manually first
- Reduce concurrency
- Increase delay between requests
- Check if site blocks automated tools

## 📚 Documentation

- **Full Docs**: See `README.md`
- **Deployment Guide**: See `DEPLOYMENT.md`
- **Checklist**: See `CHECKLIST.md`

## 💡 Tips

1. **Test Locally First**: Always test before deploying
2. **Start Small**: Begin with depth=1, concurrency=5
3. **Monitor Resources**: Check Render metrics
4. **Upgrade When Needed**: Free tier great for testing

## 🔗 Useful Links

- Render Dashboard: https://dashboard.render.com
- Render Docs: https://render.com/docs
- Test Site: http://testphp.vulnweb.com

---

**Need more help?** Check the detailed documentation files or create an issue!
