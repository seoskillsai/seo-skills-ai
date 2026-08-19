#!/usr/bin/env python3
"""
SEO Skills AI — SQLite On-Page Drift Baseline Engine
"""
import os
import sys
import json
import sqlite3
import datetime
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.fetch_page import fetch_page
from scripts.parse_html import parse_html_content

DB_DIR = Path.home() / ".config" / "seoskillsai"
DB_PATH = DB_DIR / "seo_drift.db"

def get_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS baselines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status_code INTEGER,
            title TEXT,
            meta_description TEXT,
            meta_robots TEXT,
            canonical TEXT,
            h1 TEXT,
            h2_list TEXT,
            word_count INTEGER,
            schemas TEXT,
            raw_html_hash TEXT
        )
    """)
    conn.commit()
    return conn

def capture_baseline(url: str) -> dict:
    conn = get_db()
    res = fetch_page(url)
    if res["status_code"] != 200:
        raise RuntimeError(f"Failed to fetch {url}: HTTP status {res['status_code']}")

    parsed = parse_html_content(res["html"], base_url=url)
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    h1_str = parsed["h1"][0] if parsed["h1"] else ""
    h2_json = json.dumps(parsed["h2"])
    schemas_json = json.dumps(parsed["schemas"])

    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO baselines (
            url, timestamp, status_code, title, meta_description, meta_robots,
            canonical, h1, h2_list, word_count, schemas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        url, now_iso, res["status_code"], parsed["title"], parsed["meta_description"],
        parsed["meta_robots"], parsed["canonical"], h1_str, h2_json,
        parsed["word_count"], schemas_json
    ))
    conn.commit()
    snapshot_id = cursor.lastrowid
    conn.close()

    return {
        "snapshot_id": snapshot_id,
        "url": url,
        "timestamp": now_iso,
        "title": parsed["title"],
        "word_count": parsed["word_count"],
        "h1": h1_str,
        "schemas_count": len(parsed["schemas"])
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python drift_baseline.py <url>")
        sys.exit(1)
    target = sys.argv[1]
    res = capture_baseline(target)
    print(f"[SUCCESS] Captured baseline #{res['snapshot_id']} for {target} at {res['timestamp']}")
