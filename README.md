# SQL Injection Scanner Dashboard

A comprehensive asynchronous SQL injection vulnerability scanner with a Flask-based dashboard for visualization and reporting.

## 🌐 Universal Scanner - Works with ANY Website!

**No configuration needed!** Just deploy to Render and users can scan any website directly from the web interface. No environment variables required for different targets.

## Features

- **Universal Target Selection**: Scan any website by entering URL in the UI
- **Async Web Crawler**: Intelligent crawling with depth control and same-domain filtering
- **Multi-Technique SQLi Detection**: 
  - Error-based injection
  - Boolean-based blind injection
  - Union-based injection
  - Time-based blind injection (optional)
- **WAF Evasion**: Payload mutation with inline comments, case toggling, and keyword splitting
- **Real-time Dashboard**: Live progress tracking and vulnerability visualization
- **Detailed Reporting**: JSON and CSV export with remediation suggestions
- **Configurable Scanning**: Adjustable concurrency, depth, delays, and detection parameters
- **No Configuration Required**: Deploy once, scan any site

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd SQL_CRAWLER

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
# Start the dashboard
python dashboard.py

# Access the dashboard at:
# http://localhost:5050

# Enter any website URL in the interface to scan
```

### Command Line Scanner

You can also run scans directly from the command line:

```bash
python app.py --start-url http://target-site.com --max-depth 2 --concurrency 10
```

**Options:**
- `--start-url`: Target URL to scan (required)
- `--max-depth`: Maximum crawl depth (default: 2)
- `--concurrency`: Number of concurrent requests (default: 10)
- `--delay`: Delay between requests in seconds (default: 0.2)
- `--quiet`: Suppress verbose output
- `--no-robots`: Ignore robots.txt
- `--time-based`: Enable time-based SQLi detection
- `--param-fuzzing`: Enable parameter value fuzzing

## Deploying to Render

### Quick Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Deployment

1. **Create a Render Account**: Sign up at [render.com](https://render.com)

2. **Connect Your Repository**:
   - Push this code to GitHub/GitLab
   - In Render dashboard, click "New +" → "Web Service"
   - Connect your repository

3. **Configure the Service**:
   - **Name**: `sql-scanner-dashboard`
   - **Region**: Choose your preferred region
   - **Branch**: `main` (or your default branch)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn dashboard:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
   - **Plan**: Free or paid plan

4. **Set Environment Variables**:
   ```
   PYTHON_VERSION=3.11.0
   FLASK_ENV=production
   ```
   
   **Note:** No `START_URL` needed! Users enter target URLs directly in the web interface.

5. **Deploy**: Click "Create Web Service"

6. **Start Scanning**: Visit your app URL and enter any website to scan!

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `PORT` | Server port (auto-set by Render) | Auto | 5050 |
| `FLASK_ENV` | Flask environment (development/production) | Yes | production |
| `PYTHON_VERSION` | Python version to use | Yes | 3.11.0 |
| `START_URL` | Optional default URL (users can override) | No | (empty) |

## Configuration

The dashboard provides extensive configuration options:

- **Max Depth**: Control crawl depth (0-10)
- **Concurrency**: Number of parallel requests (1-50)
- **Delay**: Time between requests to avoid overwhelming targets
- **Boolean Rounds**: Number of verification rounds for blind injection
- **Respect robots.txt**: Honor site crawl restrictions
- **Time-based SQLi**: Enable slower but thorough time-based detection
- **Parameter Fuzzing**: Test parameter value variations

## Security Considerations

⚠️ **IMPORTANT**: This tool is designed for:
- **Authorized security testing** only
- **Educational purposes**
- **Testing your own applications**

**Never use this tool on systems you don't own or have explicit permission to test.**

### Best Practices:
1. Always get written authorization before scanning
2. Use appropriate delay settings to avoid DoS
3. Respect rate limits and robots.txt
4. Run scans during maintenance windows when possible
5. Review and validate all findings manually

## Output Formats

### JSON Export
Detailed vulnerability information with metadata, payloads, and evidence.

### CSV Export
Tabular format suitable for reporting and spreadsheet analysis.

### Dashboard View
Real-time web interface with:
- Live scan progress
- Vulnerability severity indicators
- Remediation suggestions
- Error tracking
- Technique breakdown

## Troubleshooting

### Common Issues

**Scanner not finding vulnerabilities:**
- Ensure target is accessible
- Check if WAF/firewall is blocking requests
- Adjust delay and concurrency settings
- Verify target has actual SQL injection vulnerabilities

**Dashboard shows "Running" but no progress:**
- Check browser console for errors
- Verify target URL is accessible from server
- Check server logs for error messages

**Timeout errors:**
- Increase timeout threshold in settings
- Reduce concurrency
- Increase delay between requests

## Architecture

### Components

1. **app.py**: Core async scanner with crawling and injection testing logic
2. **dashboard.py**: Flask web application with REST API and SSE support
3. **Scanner Engine**: Multi-threaded async execution with semaphore-based concurrency control

### Technology Stack

- **Backend**: Flask (Python 3.11+)
- **Async I/O**: aiohttp, asyncio
- **Parsing**: BeautifulSoup4
- **Reporting**: ReportLab (PDF), JSON, CSV
- **Deployment**: Gunicorn WSGI server

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## License

This project is provided for educational and authorized security testing purposes only.

## Disclaimer

The authors are not responsible for misuse of this tool. Use responsibly and ethically.
