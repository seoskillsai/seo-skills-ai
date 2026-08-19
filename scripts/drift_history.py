#!/usr/bin/env python3
"""
SEO Skills AI — SQLite Drift History Query Tool
"""
import sys
import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".config" / "seoskillsai" / "seo_drift.db"

def query_history(url: str = None):
    if not DB_PATH.exists():
        print("No database found.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    if url:
        cursor.execute("SELECT id, timestamp, url, status_code, title, word_count FROM baselines WHERE url = ? ORDER BY id DESC", (url,))
    else:
        cursor.execute("SELECT id, timestamp, url, status_code, title, word_count FROM baselines ORDER BY id DESC LIMIT 20")

    rows = cursor.fetchall()
    conn.close()

    print(f"{'ID':<5} | {'Timestamp':<25} | {'Status':<6} | {'Words':<6} | {'Title':<30} | {'URL'}")
    print("-" * 90)
    for r in rows:
        title = (r[4] or "")[:28]
        print(f"{r[0]:<5} | {r[1]:<25} | {r[3]:<6} | {r[5]:<6} | {title:<30} | {r[2]}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    query_history(target)
