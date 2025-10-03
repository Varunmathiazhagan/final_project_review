# Deployment Guide for Render

## Prerequisites
1. A GitHub or GitLab account
2. A Render account (sign up at https://render.com)
3. Your code pushed to a Git repository

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure these files are in your repository:
- ✅ `requirements.txt` - Python dependencies
- ✅ `render.yaml` - Render configuration
- ✅ `runtime.txt` - Python version specification
- ✅ `dashboard.py` - Main application
- ✅ `app.py` - Scanner logic
- ✅ `.gitignore` - Files to exclude from Git

### 2. Push to GitHub/GitLab

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - SQL Scanner Dashboard"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/sql-scanner.git

# Push
git push -u origin main
```

### 3. Deploy on Render

#### Option A: Using render.yaml (Recommended)

1. Go to https://dashboard.render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub/GitLab repository
4. Select your repository
5. Render will automatically detect `render.yaml`
6. Click "Apply" to deploy

#### Option B: Manual Setup

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your repository
4. Configure:
   - **Name**: `sql-scanner-dashboard`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn dashboard:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Instance Type**: Free (or paid for better performance)

5. Add Environment Variables:
   ```
   PYTHON_VERSION=3.11.0
   FLASK_ENV=production
   START_URL=http://testphp.vulnweb.com
   ```

6. Click "Create Web Service"

### 4. Monitor Deployment

- Watch the build logs in Render dashboard
- Wait for "Live" status (usually 2-5 minutes)
- Your app will be available at: `https://your-app-name.onrender.com`

### 5. Test Your Deployment

Visit these URLs:
- `https://your-app-name.onrender.com/` - Main dashboard
- `https://your-app-name.onrender.com/health` - Health check
- `https://your-app-name.onrender.com/api/status` - API status

### 6. Configure Your Scanner

1. Open your dashboard URL
2. Enter a target URL (use only sites you have permission to test)
3. Adjust scan parameters:
   - Max Depth: 1-3 (start small)
   - Concurrency: 5-10
   - Delay: 0.5-1.0 seconds
4. Click "Run Scan"

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PORT` | Auto-set | 5050 | Server port (Render sets this) |
| `START_URL` | No | http://localhost:8000 | Default scan target |
| `FLASK_ENV` | No | production | Flask environment |
| `PYTHON_VERSION` | No | 3.11.0 | Python version |

## Troubleshooting

### Build Fails
- Check `requirements.txt` for syntax errors
- Verify Python version in `runtime.txt`
- Review build logs in Render dashboard

### App Crashes on Startup
- Check environment variables are set
- Review application logs
- Ensure `gunicorn` is in requirements.txt

### Slow Performance (Free Tier)
- Free tier spins down after 15 min of inactivity
- First request may be slow (cold start)
- Consider upgrading to paid tier for always-on service

### Scanner Not Working
- Verify target URL is accessible from internet
- Check if target has WAF blocking Render IPs
- Adjust delay and concurrency settings
- Review scan logs in dashboard

## Upgrading to Paid Plan

Benefits:
- ✅ No cold starts (always running)
- ✅ More CPU and memory
- ✅ Custom domains
- ✅ Better performance

To upgrade:
1. Go to your service in Render dashboard
2. Click "Settings"
3. Scroll to "Instance Type"
4. Select a paid plan
5. Click "Save Changes"

## Custom Domain Setup

1. Go to your service settings
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records as instructed
5. Wait for DNS propagation (5-30 minutes)

## Monitoring and Logs

- **Logs**: View real-time logs in Render dashboard
- **Metrics**: Check CPU, memory usage in dashboard
- **Health Check**: Render automatically monitors `/health` endpoint
- **Alerts**: Set up email alerts for service issues

## Security Recommendations

1. **Environment Variables**: Store sensitive data as environment variables
2. **HTTPS**: Render provides free SSL/TLS certificates
3. **Rate Limiting**: Consider adding rate limiting for production
4. **Authentication**: Add authentication for public deployments
5. **Firewall**: Render provides DDoS protection

## Updating Your Deployment

```bash
# Make changes to your code
git add .
git commit -m "Update features"
git push

# Render automatically redeploys on push
```

## Support

- Render Documentation: https://render.com/docs
- Community: https://community.render.com
- GitHub Issues: Create issue in your repository

## Cost Estimate

- **Free Tier**: $0/month (750 hours free)
  - Spins down after 15 min inactivity
  - Good for testing and demos

- **Starter**: $7/month
  - Always running
  - 512 MB RAM
  - Good for light usage

- **Standard**: $25/month
  - 2 GB RAM
  - Better performance
  - Good for production use

---

**Need Help?** Check the main README.md for more details about the application itself.
