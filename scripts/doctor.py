#!/usr/bin/env python3
"""
SEO Skills AI — Environment & Runtime Health Diagnostic (/seo doctor)
"""
import os
import sys
import sqlite3
import importlib.util

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def check_env():
    print("==> [SEO Skills AI Doctor] Running System Diagnostics...")
    all_ok = True

    py_ver = sys.version_info
    if py_ver >= (3, 10):
        print(f"  [PASS] Python Runtime: {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
    else:
        print(f"  [FAIL] Python Runtime: {py_ver.major}.{py_ver.minor}.{py_ver.micro} (Python 3.10+ required)")
        all_ok = False

    libs = ["urllib.request", "sqlite3", "json", "re", "xml.etree.ElementTree"]
    for lib in libs:
        if importlib.util.find_spec(lib) is not None or lib in sys.modules:
            print(f"  [PASS] Module '{lib}': Available")
        else:
            print(f"  [FAIL] Module '{lib}': Missing")
            all_ok = False

    db_dir = os.path.expanduser("~/.config/seoskillsai")
    db_path = os.path.join(db_dir, "seo_drift.db")
    try:
        os.makedirs(db_dir, exist_ok=True)
        conn = sqlite3.connect(db_path)
        conn.close()
        print(f"  [PASS] SQLite Drift Storage: Ready ({db_path})")
    except Exception as e:
        print(f"  [FAIL] SQLite Drift Storage Error: {e}")
        all_ok = False

    skills_dir = os.path.abspath("skills")
    if os.path.exists(skills_dir):
        total_skills = len([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))])
        print(f"  [PASS] Agent Skills Directory: {total_skills} skills discovered")
    else:
        print(f"  [FAIL] Agent Skills Directory: Missing {skills_dir}")
        all_ok = False

    if importlib.util.find_spec("playwright") is not None:
        print("  [PASS] Playwright: Installed (optional headless Chromium)")
    else:
        print("  [WARN] Playwright: Not installed. Screenshots stay unavailable until you run install.sh / install.ps1.")

    if all_ok:
        print("\n[SUCCESS] [SEO Skills AI Doctor] Core environment is ready. Optional Playwright is reported separately.")
        return 0
    print("\n[FAILED] [SEO Skills AI Doctor] Some required checks failed.")
    return 1


if __name__ == "__main__":
    sys.exit(check_env())
