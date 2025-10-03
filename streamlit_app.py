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


st.set_page_config(page_title="SQLi Scanner", layout="wide")
st.title("SQL Injection Scanner (Streamlit)")
st.caption("Scan only targets you own or have explicit permission to test.")


def sanitize_url(u: str) -> str:
    u = (u or "").strip()
    if not u:
        return u
    if not (u.startswith("http://") or u.startswith("https://")):
        u = "http://" + u
    return u


with st.form("scan_form"):
    target_url = st.text_input("Target URL", placeholder="https://example.com")

    with st.expander("Scan options", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            max_depth = st.number_input("Max depth", min_value=0, value=2, step=1)
            delay = st.number_input("Delay (s)", min_value=0.0, value=0.2, step=0.1)
            respect_robots = st.checkbox("Respect robots.txt", value=True)
        with col2:
            concurrency = st.number_input("Concurrency", min_value=1, value=10, step=1)
            boolean_rounds = st.number_input("Boolean rounds", min_value=1, value=3, step=1)
            quiet = st.checkbox("Quiet output", value=False)
        with col3:
            time_based = st.checkbox("Time-based SQLi", value=False)
            time_threshold = st.number_input("Time threshold (s)", min_value=1.0, value=2.0, step=0.5)
            param_fuzz = st.checkbox("Param fuzzing", value=False)

        crawler_ua = st.text_input("Crawler User-Agent (optional)")
        js_render = st.checkbox("JS rendering (Playwright)", value=False,
                                help="Requires Playwright and a browser in the environment.")

    submitted = st.form_submit_button("Run Scan")


if submitted:
    start_url = sanitize_url(target_url)
    if not start_url:
        st.error("Please enter a target URL.")
        st.stop()

    st.info("Starting scan. This can take a few minutes depending on site size and options.")

    # Create the scanner instance with options from the UI
    scanner = AsyncSQLiScanner(
        start_url=start_url,
        max_depth=int(max_depth),
        concurrency=int(concurrency),
        delay=float(delay),
        respect_robots=bool(respect_robots),
        boolean_rounds=int(boolean_rounds),
        verbose=not bool(quiet),
        quiet=bool(quiet),
        time_based=bool(time_based),
        time_threshold=float(time_threshold),
        param_fuzz=bool(param_fuzz),
        robots_user_agent=(crawler_ua or None),
        js_render=bool(js_render),
    )

    # Optional progress placeholders (they will render after completion in Streamlit)
    progress_ph = st.empty()
    findings_ph = st.empty()

    def on_prog(p: Dict[str, Any]):
        try:
            progress_ph.write(
                f"Crawled: {int(p.get('crawled', 0))} | Queue: {int(p.get('queue', 0))} | Findings: {int(p.get('findings', 0))}"
            )
        except Exception:
            pass

    def on_find(_entry: Dict[str, Any]):
        try:
            findings_ph.write(f"Findings: {len(scanner.results)}")
        except Exception:
            pass

    scanner.on_progress = on_prog
    scanner.on_finding = on_find

    with st.spinner("Scanning..."):
        # Run the async scanner synchronously
        asyncio.run(scanner.run())

    st.success("Scan complete.")

    # Show results
    results: List[Dict[str, Any]] = scanner.results
    st.subheader(f"Findings ({len(results)})")

    if results:
        # Build a compact table
        display_cols = [
            "technique", "risk", "score", "url", "param", "payload", "evidence"
        ]
        # Defensive copy with default strings
        rows = [
            {k: (str(r.get(k, "")) if r.get(k) is not None else "") for k in display_cols}
            for r in results
        ]
        st.dataframe(rows, use_container_width=True)

        # Optional secure code snippet toggle
        if st.checkbox("Show secure query snippet", value=False):
            for r in results:
                fs = r.get("fix_snippet") or "Use parameterized queries."
                with st.expander(f"Fix for {r.get('param', 'param')} ({r.get('technique', '')})", expanded=False):
                    st.code(fs, language="php")

        # Downloads (JSON and CSV)
        json_bytes = json.dumps(results, indent=2).encode("utf-8")
        st.download_button("Download JSON", data=json_bytes, file_name="latest_scan.json", mime="application/json")

        # Build CSV
        csv_buf = io.StringIO()
        fieldnames = ["url", "type", "param", "technique", "risk", "score", "payload", "evidence"]
        writer = csv.DictWriter(csv_buf, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k, "") for k in fieldnames})
        st.download_button("Download CSV", data=csv_buf.getvalue().encode("utf-8"),
                           file_name="latest_scan.csv", mime="text/csv")
    else:
        st.info("No findings.")

st.markdown("---")
st.write("Legal notice: Only scan systems you own or have permission to test.")
