#!/usr/bin/env python3
"""
SEO Skills AI — 17-Rule SEO Drift Comparison Engine
"""
import os
import sys
import json
import sqlite3
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.fetch_page import fetch_page
from scripts.parse_html import parse_html_content

DB_PATH = Path.home() / ".config" / "seoskillsai" / "seo_drift.db"

def compare_drift(url: str) -> dict:
    if not DB_PATH.exists():
        return {"error": "No baseline database found. Run 'python scripts/drift_baseline.py <url>' first."}

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, title, meta_description, meta_robots, canonical, h1, h2_list, word_count, schemas
        FROM baselines
        WHERE url = ?
        ORDER BY id DESC LIMIT 1
    """, (url,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": f"No baseline snapshot found for URL '{url}'."}

    baseline = {
        "id": row[0],
        "timestamp": row[1],
        "title": row[2],
        "meta_description": row[3],
        "meta_robots": row[4],
        "canonical": row[5],
        "h1": row[6],
        "h2_list": json.loads(row[7]) if row[7] else [],
        "word_count": row[8],
        "schemas": json.loads(row[9]) if row[9] else []
    }

    # Fetch live
    res = fetch_page(url)
    live = parse_html_content(res["html"], base_url=url)
    live_h1 = live["h1"][0] if live["h1"] else ""

    diffs = []
    # 17 Drift Rules Evaluation
    if not live["title"] and baseline["title"]:
        diffs.append({"rule": 1, "severity": "P0", "msg": "Title tag was completely removed!"})
    elif live["title"] != baseline["title"]:
        diffs.append({"rule": 1, "severity": "P1", "msg": f"Title changed: '{baseline['title']}' -> '{live['title']}'"})

    if live["meta_robots"] != baseline["meta_robots"]:
        severity = "P0" if "noindex" in live["meta_robots"].lower() else "P1"
        diffs.append({"rule": 2, "severity": severity, "msg": f"Meta robots changed: '{baseline['meta_robots']}' -> '{live['meta_robots']}'"})

    if live["canonical"] != baseline["canonical"]:
        diffs.append({"rule": 3, "severity": "P0", "msg": f"Canonical tag modified: '{baseline['canonical']}' -> '{live['canonical']}'"})

    if live_h1 != baseline["h1"]:
        diffs.append({"rule": 4, "severity": "P1", "msg": f"Primary H1 changed: '{baseline['h1']}' -> '{live_h1}'"})

    if baseline["word_count"] > 0:
        ratio = live["word_count"] / baseline["word_count"]
        if ratio < 0.8:
            diffs.append({"rule": 6, "severity": "P1", "msg": f"Significant word count drop: {baseline['word_count']} -> {live['word_count']} (down {round((1-ratio)*100)}%)"})

    if len(live["schemas"]) < len(baseline["schemas"]):
        diffs.append({"rule": 5, "severity": "P0", "msg": f"JSON-LD Schema count decreased: {len(baseline['schemas'])} -> {len(live['schemas'])}"})

    return {
        "url": url,
        "baseline_id": baseline["id"],
        "baseline_timestamp": baseline["timestamp"],
        "total_drifts_detected": len(diffs),
        "drift_details": diffs,
        "status": "DRIFT_DETECTED" if diffs else "CLEAN"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python drift_compare.py <url>")
        sys.exit(1)
    target = sys.argv[1]
    res = compare_drift(target)
    print(json.dumps(res, indent=2))
