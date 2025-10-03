# Pre-Deployment Checklist for Render

## ✅ Code Preparation

- [x] `requirements.txt` - Updated with all dependencies including gunicorn
- [x] `runtime.txt` - Python version specified (3.11.0)
- [x] `render.yaml` - Render configuration file created
- [x] `.gitignore` - Excluding unnecessary files
- [x] `dashboard.py` - Updated to use PORT from environment and 0.0.0.0 binding
- [x] Health check endpoint added at `/health`
- [x] CORS enabled for API endpoints
- [x] README.md with documentation

## 📋 Before Deployment

### 1. Test Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
set START_URL=http://testphp.vulnweb.com

# Run locally
python dashboard.py

# Visit http://localhost:5050 to verify it works
```

### 2. Repository Setup
```bash
# Initialize git if needed
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Render deployment"

# Create repository on GitHub
# Then add remote and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### 3. Environment Variables to Set on Render

| Variable | Value | Required |
|----------|-------|----------|
| `PYTHON_VERSION` | `3.11.0` | Yes |
| `FLASK_ENV` | `production` | Yes |
| `START_URL` | `http://testphp.vulnweb.com` | No (has default) |
| `SECRET_KEY` | (generate random string) | Recommended |

To generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🚀 Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Login to Render**
   - Go to https://dashboard.render.com
   - Sign in with GitHub

2. **Create New Blueprint**
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select your repository
   - Render detects `render.yaml` automatically
   - Click "Apply"

3. **Monitor Deployment**
   - Watch build logs
   - Wait for "Live" status
   - Copy your app URL

### Option 2: Manual Web Service

1. **Login to Render**
   - Go to https://dashboard.render.com

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect repository

3. **Configure Service**
   - Name: `sql-scanner-dashboard`
   - Region: Oregon (or closest)
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn dashboard:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

4. **Add Environment Variables**
   ```
   PYTHON_VERSION=3.11.0
   FLASK_ENV=production
   START_URL=http://testphp.vulnweb.com
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 2-5 minutes for deployment

## ✅ Post-Deployment Verification

### 1. Check Health Endpoint
```bash
curl https://your-app-name.onrender.com/health
```
Expected response:
```json
{
  "status": "healthy",
  "service": "sql-scanner-dashboard",
  "timestamp": "2025-10-03T..."
}
```

### 2. Check Main Dashboard
Visit: `https://your-app-name.onrender.com/`
- Should see the dashboard interface
- "Scan Status" should show "Idle"

### 3. Test API Endpoints
```bash
# Status
curl https://your-app-name.onrender.com/api/status

# Results
curl https://your-app-name.onrender.com/api/results
```

### 4. Run a Test Scan
1. Open dashboard in browser
2. Enter a test URL: `http://testphp.vulnweb.com`
3. Set Max Depth: 1
4. Set Concurrency: 5
5. Click "Run Scan"
6. Watch progress in real-time

## 🔧 Troubleshooting

### Build Fails
**Problem**: Build fails with package errors
**Solution**: 
- Check `requirements.txt` syntax
- Verify all packages are available on PyPI
- Check Python version compatibility

### App Won't Start
**Problem**: Deployment shows "Failed" status
**Solution**:
- Check logs in Render dashboard
- Verify environment variables are set
- Ensure `PORT` is not hardcoded
- Check gunicorn is in requirements.txt

### 404 Errors
**Problem**: Main page shows 404
**Solution**:
- Verify start command uses `dashboard:app`
- Check Flask routes are correctly defined
- Review application logs

### Slow First Request (Free Tier)
**Problem**: First request takes 30+ seconds
**Solution**:
- This is normal on free tier (cold start)
- App spins down after 15 min inactivity
- Upgrade to paid tier for always-on service

### Scanner Fails
**Problem**: Scans don't complete
**Solution**:
- Check target URL is accessible from internet
- Reduce concurrency and increase delay
- Check if target blocks cloud IPs
- Review scanner logs

## 📊 Monitoring

### View Logs
```
Render Dashboard → Your Service → Logs
```

### Check Metrics
```
Render Dashboard → Your Service → Metrics
```

### Health Checks
Render automatically monitors `/health` endpoint
- Frequency: Every 30 seconds
- Timeout: 30 seconds
- Restarts service if unhealthy

## 🔒 Security Best Practices

1. **Never hardcode secrets**
   - Use environment variables for all sensitive data
   - Don't commit `.env` files

2. **Use HTTPS**
   - Render provides automatic SSL/TLS
   - Always access via `https://`

3. **Rate limiting**
   - Consider adding Flask-Limiter for production
   - Protect against abuse

4. **Authentication**
   - Add login for public deployments
   - Use Flask-Login or similar

5. **Input validation**
   - Already implemented in scanner
   - Validate user inputs on frontend

## 💰 Cost Management

### Free Tier Limits
- ✅ 750 hours/month free
- ✅ Automatic sleep after 15 min
- ✅ Good for testing/demos
- ❌ Cold starts (slow first request)

### Upgrade Recommendations
- Light usage: **Starter** ($7/month)
- Production: **Standard** ($25/month)
- High traffic: **Pro** ($85/month)

## 📚 Next Steps

After deployment:
1. ✅ Test all features
2. ✅ Configure custom domain (optional)
3. ✅ Set up monitoring/alerts
4. ✅ Add authentication if needed
5. ✅ Share with team
6. ✅ Document API endpoints
7. ✅ Plan backup strategy

## 🆘 Getting Help

- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Support**: support@render.com (paid plans)
- **GitHub Issues**: Your repository issues page

---

**Ready to deploy?** Follow the steps above and you'll be live in minutes! 🚀
