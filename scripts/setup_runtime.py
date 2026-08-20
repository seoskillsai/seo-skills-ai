#!/usr/bin/env python3
"""
SEO Skills AI — Runtime Provisioner (/seo setup)
"""
import os
import sys
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def setup():
    print("==> [SEO Skills AI Setup] Provisioning local config (SQLite drift DB).")
    print("    Python venv + Playwright Chromium are installed by install.sh / install.ps1, not this script.")
    config_dir = Path.home() / ".config" / "seoskillsai"
    config_dir.mkdir(parents=True, exist_ok=True)

    # Initialize sqlite baseline table
    db_path = config_dir / "seo_drift.db"
    import sqlite3
    conn = sqlite3.connect(str(db_path))
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
    conn.close()
    print(f"  [PASS] Initialized drift tracking database at {db_path}")

    print("\n[SUCCESS] [SEO Skills AI Setup] Setup completed successfully!")

if __name__ == "__main__":
    setup()
