# 🔍 SQL Injection Vulnerability Scanner

A comprehensive, async web crawler and SQL injection vulnerability scanner with both Flask and Streamlit interfaces. Designed for security professionals and penetration testers to identify SQLi vulnerabilities in web applications.

## ⚠️ Legal Notice

**IMPORTANT:** Only use this tool on:
- Websites you own
- Systems you have explicit written permission to test
- Authorized penetration testing engagements

Unauthorized vulnerability scanning may violate laws including:
- Computer Fraud and Abuse Act (CFAA) - United States
- Computer Misuse Act - United Kingdom
- Similar cybercrime legislation worldwide

**You are solely responsible for ensuring you have authorization before scanning any system.**

## 🌟 Features

### Detection Capabilities
- ✅ **Error-based SQLi** - Detects SQL errors in responses
- ✅ **Boolean-based blind SQLi** - Multi-round differential analysis
- ✅ **UNION-based SQLi** - Column enumeration and confirmation
- ✅ **Time-based SQLi** (optional) - Delay-based detection for MySQL/MSSQL
- ✅ **WAF evasion** - Payload mutation with comment injection, case randomization
- ✅ **Multi-DBMS support** - SQLite, MySQL, PostgreSQL, MSSQL compatible patterns

### Crawler Features
- 🕷️ Async crawling with depth control
- 🔗 Link discovery (HTML anchors, forms, inline JS)
- 🤖 robots.txt compliance (configurable)
- 📄 Form parameter auto-discovery
- 🎭 Optional JavaScript rendering (Playwright)
- ⚡ Concurrent request handling with rate limiting

### Reporting
- 📊 JSON and CSV exports
- 🎨 PDF reports (optional, via reportlab)
- 📈 Risk scoring (CVSS-style 0-10)
- 🔧 Secure code snippets for remediation
- 📉 Live progress tracking

## 🚀 Quick Start

### Test Website
For safe testing without authorization concerns:
```
http://testphp.vulnweb.com
```

### Local Installation

```bash
# Clone repository
git clone https://github.com/Varunmathiazhagan/final_project_review.git
cd final_project_review

# Install dependencies
pip install -r requirements.txt

# Run Streamlit UI (recommended for beginners)
streamlit run streamlit_app.py

# OR run Flask dashboard
python dashboard.py

# OR run CLI scanner
python app.py --start-url http://testphp.vulnweb.com --max-depth 2
```

## ☁️ Streamlit Cloud Deployment

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Configure:
   - **Repository:** `Varunmathiazhagan/final_project_review`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
   - **App URL:** Choose your custom URL (e.g., `sqlscanner.streamlit.app`)
4. Click "Deploy"

Your app will be live in 2-5 minutes!

### Streamlit Cloud Notes
- **JS rendering disabled by default** (Playwright requires browser installation)
- **Recommended settings:** Max depth 1-2, concurrency 5-10
- **Timeout:** Streamlit Cloud may timeout for very long scans (>10 min)

### 🔄 Keeping Your App Active

Streamlit Cloud free tier apps sleep after 7 days of inactivity. To prevent this:

**Option 1: UptimeRobot (Recommended - Free)**
1. Sign up at [UptimeRobot.com](https://uptimerobot.com)
2. Add your app URL as a monitor
3. Set ping interval to 5 minutes
4. Your app stays awake 24/7!

**Option 2: GitHub Actions (Automated)**
- The included `.github/workflows/keep-alive.yml` pings your app every 6 hours
- Edit the file to add your Streamlit app URL
- Enable GitHub Actions in your repository

**Option 3: Manual Wake-Up**
- Visit your app at least once per week
- Click "Wake up" button if it goes to sleep

See `INACTIVITY_SOLUTIONS.md` for detailed troubleshooting.

## 🖥️ Alternative Deployment (Flask on Render/Railway)

### Render Deployment
1. Add `Procfile`:
   ```
   web: gunicorn dashboard:app
   ```
2. Add `gunicorn>=20.1` to `requirements.txt`
3. Connect repo to [Render](https://render.com)
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn dashboard:app`

### Railway Deployment
1. Connect repo to [Railway](https://railway.app)
2. Railway auto-detects Flask apps
3. Set environment variables if needed

## 📖 Usage Guide

### Streamlit Interface

1. **Enter Target URL**
   - Include protocol: `http://` or `https://`
   - Example: `http://testphp.vulnweb.com`

2. **Configure Scan Options**
   - **Max depth:** How many link levels to crawl (1-5)
     - Depth 1: Only scan starting page + immediate links
     - Depth 2: Recommended for most scans
     - Depth 3+: Thorough but slower
   
   - **Concurrency:** Parallel requests (1-20)
     - 5: Safe, respectful
     - 10: Balanced (default)
     - 15+: Aggressive (may trigger WAF/rate limits)
   
   - **Boolean rounds:** Confidence level (1-5)
     - 3: Recommended balance
     - 5: Higher confidence, slower

3. **Review Results**
   - Risk levels: Critical > High > Medium > Low
   - Filter by risk or technique
   - View remediation code snippets
   - Export JSON/CSV reports

### CLI Interface

```bash
# Basic scan
python app.py --start-url http://example.com

# Advanced scan with options
python app.py \
  --start-url http://testphp.vulnweb.com \
  --max-depth 3 \
  --concurrency 10 \
  --delay 0.3 \
  --boolean-rounds 3 \
  --time-based \
  --param-fuzz \
  --js-render

# Quick scan (fast)
python app.py -u http://example.com --max-depth 1 --concurrency 5

# Thorough scan (slow)
python app.py -u http://example.com --max-depth 4 --concurrency 15 --time-based --param-fuzz
```

### CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--start-url`, `-u` | Required | Target URL to scan |
| `--max-depth` | 2 | Maximum crawl depth |
| `--concurrency` | 5 | Parallel requests |
| `--delay` | 0.3 | Delay between requests (seconds) |
| `--timeout` | 10 | Request timeout (seconds) |
| `--retries` | 2 | Max retries per request |
| `--boolean-rounds` | 3 | Boolean-blind test iterations |
| `--union-max-columns` | 6 | Max columns for UNION tests |
| `--time-based` | Off | Enable time-delay tests |
| `--time-threshold` | 2.0 | Time delay threshold (seconds) |
| `--param-fuzz` | Off | Enable parameter fuzzing |
| `--crawler-ua` | Auto | Custom User-Agent |
| `--js-render` | Off | Enable Playwright JS rendering |
| `--no-robots` | Off | Ignore robots.txt |
| `--quiet` | Off | Suppress output |
| `--verbose` | Off | Extra logging |

## 🔧 Architecture

### Core Components

1. **AsyncSQLiScanner** (`app.py`)
   - Async crawling with aiohttp
   - Semaphore-based concurrency control
   - Exponential backoff retry logic
   - Pluggable progress/finding callbacks

2. **Payload Mutation** (`mutate_payload()`)
   - WAF evasion techniques:
     - Inline comment injection (`UN/**/ION`)
     - Versioned comments (`/*!SELECT*/`)
     - Case randomization
     - Whitespace tampering

3. **Detection Methods**
   - **Error-based:** Regex pattern matching for SQL errors
   - **Boolean-blind:** Multi-round differential response analysis
   - **UNION-based:** Column count enumeration + marker injection
   - **Time-based:** Delay measurement with jitter tolerance

4. **Interfaces**
   - **Streamlit UI:** Modern, interactive web interface
   - **Flask Dashboard:** RESTful API + SSE live updates
   - **CLI:** Command-line automation

### Supported Databases
- SQLite (primary target)
- MySQL / MariaDB
- PostgreSQL
- Microsoft SQL Server
- Oracle (partial)

## 📊 Output Format

### JSON Report
```json
[
  {
    "url": "http://example.com/page.php",
    "type": "GET",
    "param": "id",
    "technique": "error-based",
    "risk": "High",
    "score": 8.6,
    "payload": "'",
    "evidence": "SQLSTATE[42000] | status=200 | prox=45",
    "fix_snippet": "// PHP PDO example\n$stmt = $pdo->prepare('SELECT * FROM table WHERE id = ?');\n..."
  }
]
```

### CSV Report
Columns: `url`, `type`, `param`, `technique`, `risk`, `score`, `payload`, `evidence`

## 🛡️ Security Best Practices

### For Scanner Users
1. **Get authorization** before scanning
2. **Start with low concurrency** to avoid DoS
3. **Respect rate limits** and robots.txt
4. **Use VPN/authorization** if required
5. **Document findings** responsibly
6. **Follow disclosure** guidelines

### For Developers
1. **Use parameterized queries** (prepared statements)
2. **Validate input** with whitelists
3. **Escape output** properly
4. **Apply least privilege** DB permissions
5. **Disable detailed errors** in production
6. **Use WAF** as defense-in-depth
7. **Regular security audits**

## 🐛 Troubleshooting

### "This file does not exist" on Streamlit Cloud
- Ensure `streamlit_app.py` is at repo root
- Check branch is `main`
- Verify file is committed and pushed

### Scan Timeout / Slow Performance
- Reduce `max_depth` to 1-2
- Reduce `concurrency` to 5
- Disable `time_based` tests
- Increase `delay` to 0.5+

### No Vulnerabilities Found
- Try test site: `http://testphp.vulnweb.com`
- Increase `max_depth` to 3-4
- Enable `param_fuzz`
- Check if target has WAF (try different payloads)

### Playwright Not Working
- On Streamlit Cloud: Disable `js_render` (browsers not installed)
- Local: Run `python -m playwright install`

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

## 📚 References

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [OWASP Testing Guide - SQLi](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05-Testing_for_SQL_Injection)
- [PortSwigger SQLi Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
- [NIST 800-115 - Technical Guide to Information Security Testing](https://csrc.nist.gov/publications/detail/sp/800-115/final)

## 📄 License

This project is for educational and authorized security testing only. See `LICENSE` file for details.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 👨‍💻 Author

**Varun Mathiazhagan**
- GitHub: [@Varunmathiazhagan](https://github.com/Varunmathiazhagan)
- Repository: [final_project_review](https://github.com/Varunmathiazhagan/final_project_review)

## ⭐ Acknowledgments

- OWASP for vulnerability research
- Streamlit for amazing framework
- Security community for responsible disclosure practices

---

**Remember: With great power comes great responsibility. Use ethically and legally.**
