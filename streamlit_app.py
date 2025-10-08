#!/usr/bin/env python3
"""
Streamlit UI for Async SQLi Scanner

This wraps the AsyncSQLiScanner from app.py and provides a simple Streamlit
interface suitable for Streamlit Cloud deployment.

Notes:
- JS rendering (Playwright) is off by default because Streamlit Cloud
  environments typically don't have browsers installed. You can enable it if
  you've provisioned Playwright properly.
- Results are shown after the scan completes. For long scans, start with a low
  crawl depth and concurrency.
"""
import asyncio
import csv
import io
import json
import time
from typing import Any, Dict, List

import streamlit as st

from app import AsyncSQLiScanner


st.set_page_config(page_title="SQLi Vulnerability Scanner", layout="wide", page_icon="🔍")
st.title("🔍 SQL Injection Vulnerability Scanner")
st.caption("⚠️ **Legal Notice:** Only scan websites you own or have explicit written permission to test. Unauthorized scanning may be illegal.")


def sanitize_url(u: str) -> str:
    u = (u or "").strip()
    if not u:
        return u
    if not (u.startswith("http://") or u.startswith("https://")):
        u = "http://" + u
    return u


with st.form("scan_form"):
    st.markdown("### 🎯 Target Configuration")
    target_url = st.text_input(
        "Target URL", 
        placeholder="https://testphp.vulnweb.com or http://example.com",
        help="Enter the full URL including http:// or https://. For testing, try http://testphp.vulnweb.com"
    )

    with st.expander("⚙️ Advanced Scan Options", expanded=False):
        st.markdown("**Crawling Settings**")
        col1, col2, col3 = st.columns(3)
        with col1:
            max_depth = st.number_input("Max crawl depth", min_value=0, max_value=5, value=2, step=1,
                                       help="How many link levels deep to crawl (0-5). Start with 1-2 for faster scans.")
            delay = st.number_input("Delay between requests (s)", min_value=0.0, max_value=2.0, value=0.3, step=0.1,
                                   help="Delay to avoid overwhelming target server")
        with col2:
            concurrency = st.number_input("Concurrent requests", min_value=1, max_value=20, value=5, step=1,
                                         help="Number of parallel requests (1-20). Lower is safer.")
            respect_robots = st.checkbox("Respect robots.txt", value=True,
                                        help="Honor robots.txt exclusions")
        with col3:
            quiet = st.checkbox("Quiet mode", value=True,
                              help="Reduce console output during scan")
            union_max_cols = st.number_input("UNION max columns", min_value=3, max_value=10, value=6, step=1,
                                            help="Max columns to test for UNION-based SQLi")
        
        st.markdown("**Detection Settings**")
        col4, col5, col6 = st.columns(3)
        with col4:
            boolean_rounds = st.number_input("Boolean test rounds", min_value=1, max_value=5, value=3, step=1,
                                            help="More rounds = higher confidence but slower")
        with col5:
            time_based = st.checkbox("Time-based SQLi tests", value=False,
                                    help="Enable slow time-delay detection (adds scan time)")
            time_threshold = st.number_input("Time threshold (s)", min_value=1.0, max_value=5.0, value=2.0, step=0.5,
                                           help="Minimum delay to consider time-based SQLi", disabled=not time_based)
        with col6:
            param_fuzz = st.checkbox("Parameter fuzzing", value=False,
                                    help="Test multiple input variations per parameter")

        st.markdown("**Advanced Options**")
        crawler_ua = st.text_input("Custom User-Agent (optional)", 
                                   placeholder="Leave empty for default",
                                   help="Custom User-Agent string for requests")
        js_render = st.checkbox("JS rendering (Playwright)", value=False,
                                help="⚠️ Requires Playwright browser - usually not available on Streamlit Cloud")

    submitted = st.form_submit_button("🚀 Start Vulnerability Scan", use_container_width=True)


if submitted:
    start_url = sanitize_url(target_url)
    if not start_url:
        st.error("❌ Please enter a target URL.")
        st.stop()

    # Validate URL format
    try:
        from urllib.parse import urlparse
        parsed = urlparse(start_url)
        if not parsed.netloc:
            st.error("❌ Invalid URL format. Please include the domain (e.g., https://example.com)")
            st.stop()
    except Exception:
        st.error("❌ Invalid URL format.")
        st.stop()

    st.info("🔄 Starting vulnerability scan. This may take 2-10 minutes depending on site size and settings...")
    
    # Show recommended settings info
    with st.expander("ℹ️ Scan Progress Tips", expanded=True):
        st.markdown("""
        - **For quick tests:** Use max depth 1-2, concurrency 5
        - **For thorough scans:** Use max depth 3-4, concurrency 10
        - **If scan is slow:** Reduce depth or disable time-based tests
        - **Test sites:** Try `http://testphp.vulnweb.com` for safe testing
        """)

    # Create the scanner instance with options from the UI
    scanner = AsyncSQLiScanner(
        start_url=start_url,
        max_depth=int(max_depth),
        concurrency=int(concurrency),
        delay=float(delay),
        respect_robots=bool(respect_robots),
        boolean_rounds=int(boolean_rounds),
        union_max_columns=int(union_max_cols),
        verbose=not bool(quiet),
        quiet=bool(quiet),
        time_based=bool(time_based),
        time_threshold=float(time_threshold),
        param_fuzz=bool(param_fuzz),
        robots_user_agent=(crawler_ua or None),
        js_render=bool(js_render),
    )

    # Live progress tracking with better UX
    progress_container = st.container()
    with progress_container:
        col_a, col_b, col_c = st.columns(3)
        crawled_metric = col_a.empty()
        queue_metric = col_b.empty()
        findings_metric = col_c.empty()
    
    progress_bar = st.progress(0, text="Initializing scan...")

    def on_prog(p: Dict[str, Any]):
        try:
            crawled = int(p.get('crawled', 0))
            queue = int(p.get('queue', 0))
            findings = int(p.get('findings', 0))
            
            crawled_metric.metric("URLs Crawled", crawled)
            queue_metric.metric("Queue Remaining", queue)
            findings_metric.metric("Vulnerabilities", findings, delta=None if findings == 0 else f"+{findings}")
            
            # Update progress bar (estimate based on queue)
            total_est = max(crawled + queue, 1)
            progress = min(0.95, crawled / total_est)
            progress_bar.progress(progress, text=f"Scanning... {crawled} URLs processed")
        except Exception:
            pass

    def on_find(_entry: Dict[str, Any]):
        try:
            findings = len(scanner.results)
            findings_metric.metric("Vulnerabilities", findings, delta=f"+{findings}")
        except Exception:
            pass

    scanner.on_progress = on_prog
    scanner.on_finding = on_find

    # Run the async scanner
    try:
        asyncio.run(scanner.run())
        progress_bar.progress(1.0, text="✅ Scan complete!")
        st.success(f"✅ Scan complete! Analyzed {len(scanner.visited)} URLs and found {len(scanner.results)} potential vulnerabilities.")
    except Exception as e:
        progress_bar.empty()
        st.error(f"❌ Scan failed: {str(e)}")
        st.stop()

    # Show results
    results: List[Dict[str, Any]] = scanner.results
    
    # Summary metrics
    st.markdown("---")
    st.subheader(f"📊 Scan Results: {len(results)} Vulnerabilities Found")

    if results:
        # Risk breakdown
        risk_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        for r in results:
            risk = r.get("risk", "Medium")
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        col_r1.metric("🔴 Critical", risk_counts["Critical"])
        col_r2.metric("🟠 High", risk_counts["High"])
        col_r3.metric("🟡 Medium", risk_counts["Medium"])
        col_r4.metric("🟢 Low", risk_counts["Low"])
        
        st.markdown("---")
        
        # Filter controls
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            risk_filter = st.multiselect(
                "Filter by Risk Level",
                ["Critical", "High", "Medium", "Low"],
                default=["Critical", "High", "Medium", "Low"]
            )
        with filter_col2:
            technique_options = list(set(r.get("technique", "") for r in results))
            technique_filter = st.multiselect(
                "Filter by Technique",
                technique_options,
                default=technique_options
            )
        
        # Apply filters
        filtered_results = [
            r for r in results 
            if r.get("risk", "Medium") in risk_filter 
            and r.get("technique", "") in technique_filter
        ]
        
        st.info(f"Showing {len(filtered_results)} of {len(results)} findings")
        
        # Build a compact table with color coding
        display_cols = [
            "technique", "risk", "score", "url", "param", "payload", "evidence"
        ]
        
        # Create styled dataframe
        rows = []
        for r in filtered_results:
            row = {k: (str(r.get(k, "")) if r.get(k) is not None else "") for k in display_cols}
            rows.append(row)
        
        st.dataframe(
            rows, 
            use_container_width=True,
            column_config={
                "risk": st.column_config.TextColumn("Risk", help="Vulnerability severity"),
                "score": st.column_config.NumberColumn("Score", help="CVSS-style score (0-10)", format="%.1f"),
                "url": st.column_config.TextColumn("URL", help="Vulnerable endpoint"),
                "param": st.column_config.TextColumn("Parameter", help="Vulnerable parameter name"),
                "technique": st.column_config.TextColumn("Technique", help="SQLi detection method"),
            },
            height=400
        )

        # Detailed findings with expandable sections
        st.markdown("### 🔍 Detailed Findings")
        for idx, r in enumerate(filtered_results, 1):
            risk = r.get("risk", "Medium")
            risk_emoji = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(risk, "⚪")
            technique = r.get('technique', 'Unknown')
            
            with st.expander(
                f"{risk_emoji} #{idx}: {technique} on `{r.get('param', 'N/A')}` [{risk}]",
                expanded=False
            ):
                col_detail1, col_detail2 = st.columns([2, 1])
                with col_detail1:
                    st.markdown(f"**URL:** `{r.get('url', '')}`")
                    st.markdown(f"**Parameter:** `{r.get('param', '')}`")
                    st.markdown(f"**Payload:** `{r.get('payload', '')}`")
                    st.markdown(f"**Evidence:** {r.get('evidence', 'N/A')}")
                with col_detail2:
                    st.markdown(f"**Risk Level:** {risk}")
                    st.markdown(f"**Score:** {r.get('score', 'N/A')}")
                    st.markdown(f"**Type:** {r.get('type', 'GET')}")
                    st.markdown(f"**Technique:** {technique}")
                
                # Show technique-specific explanation
                st.markdown("---")
                st.markdown("**📖 Vulnerability Explanation:**")
                
                tech_lower = technique.lower()
                if "error" in tech_lower:
                    st.info(
                        "**Error-Based SQLi:** The application reveals database errors containing sensitive "
                        "information when invalid SQL syntax is injected. Attackers can extract database "
                        "structure and data by analyzing error messages."
                    )
                elif "boolean" in tech_lower:
                    st.info(
                        "**Boolean-Based Blind SQLi:** The application responds differently to TRUE vs FALSE "
                        "SQL conditions, allowing attackers to extract data bit-by-bit by asking yes/no questions "
                        "to the database through conditional logic."
                    )
                elif "time" in tech_lower:
                    st.info(
                        "**Time-Based Blind SQLi:** The application can be forced to delay responses using "
                        "SQL time functions (e.g., SLEEP, WAITFOR). Attackers infer data by measuring response times, "
                        "extracting information when no visible differences exist in page content."
                    )
                elif "union" in tech_lower:
                    st.info(
                        "**UNION-Based SQLi:** The application allows injecting additional SELECT statements "
                        "using UNION operators, enabling direct extraction of data from other tables or columns "
                        "by combining results with the original query."
                    )
                
                # Show fix snippet
                fs = r.get("fix_snippet") or "Use parameterized queries to prevent SQLi."
                st.markdown("**🔧 Remediation (Secure Code Example):**")
                st.code(fs, language="php")
                
                # Add security best practices
                st.markdown("**✅ Additional Security Best Practices:**")
                best_practices = []
                if "error" in tech_lower:
                    best_practices = [
                        "Disable detailed error messages in production",
                        "Implement custom error pages",
                        "Log errors securely server-side only",
                        "Use try-catch blocks to handle exceptions gracefully"
                    ]
                elif "boolean" in tech_lower:
                    best_practices = [
                        "Always use parameterized queries/prepared statements",
                        "Never concatenate user input into SQL strings",
                        "Implement strict input validation",
                        "Use ORM frameworks when possible (e.g., SQLAlchemy, Entity Framework)"
                    ]
                elif "time" in tech_lower:
                    best_practices = [
                        "Use parameterized queries to prevent injection",
                        "Implement rate limiting on endpoints",
                        "Set database query timeouts",
                        "Monitor for unusual response time patterns"
                    ]
                elif "union" in tech_lower:
                    best_practices = [
                        "Use parameterized queries exclusively",
                        "Whitelist allowed column names for dynamic queries",
                        "Validate and sanitize all user inputs",
                        "Apply principle of least privilege to database accounts"
                    ]
                else:
                    best_practices = [
                        "Use parameterized queries/prepared statements",
                        "Apply input validation and sanitization",
                        "Follow principle of least privilege",
                        "Regular security audits and penetration testing"
                    ]
                
                for bp in best_practices:
                    st.markdown(f"- {bp}")


        # Downloads (JSON and CSV)
        st.markdown("---")
        st.markdown("### 📥 Export Results")
        dl_col1, dl_col2 = st.columns(2)
        
        with dl_col1:
            json_bytes = json.dumps(results, indent=2).encode("utf-8")
            st.download_button(
                "⬇️ Download JSON Report", 
                data=json_bytes, 
                file_name=f"sqli_scan_{int(time.time())}.json", 
                mime="application/json",
                use_container_width=True
            )
        
        with dl_col2:
            # Build CSV
            csv_buf = io.StringIO()
            fieldnames = ["url", "type", "param", "technique", "risk", "score", "payload", "evidence"]
            writer = csv.DictWriter(csv_buf, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow({k: r.get(k, "") for k in fieldnames})
            st.download_button(
                "⬇️ Download CSV Report", 
                data=csv_buf.getvalue().encode("utf-8"),
                file_name=f"sqli_scan_{int(time.time())}.csv", 
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.success("✅ No SQL injection vulnerabilities detected!")
        st.info("This doesn't guarantee the site is secure - it means no common SQLi patterns were found with the current scan settings.")

st.markdown("---")
st.markdown("""
### ⚖️ Legal & Ethical Notice
- **Authorization Required:** Only scan websites you own or have explicit written permission to test
- **Legal Compliance:** Unauthorized vulnerability scanning may violate laws including CFAA (US), Computer Misuse Act (UK), and similar statutes worldwide
- **Responsible Disclosure:** If you find vulnerabilities, follow responsible disclosure practices
- **No Warranty:** This tool is provided as-is for educational and authorized security testing only

### 💡 Quick Start Guide
1. **For testing:** Try `http://testphp.vulnweb.com` (a safe test site)
2. **Start small:** Use depth 1-2 and concurrency 5 for initial scans
3. **Review results:** Check the risk level and remediation code for each finding
4. **Export reports:** Download JSON/CSV for documentation

### 🔗 Resources
- [OWASP SQLi Guide](https://owasp.org/www-community/attacks/SQL_Injection)
- [Responsible Disclosure](https://cheatsheetseries.owasp.org/cheatsheets/Vulnerability_Disclosure_Cheat_Sheet.html)
""")
