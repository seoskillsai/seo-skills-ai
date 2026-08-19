#!/usr/bin/env python3
"""
SEO Skills AI — Google API 4-Tier Credential Wizard
"""
import os
import sys
import json
from pathlib import Path

CRED_PATH = Path.home() / ".config" / "seoskillsai" / "google_credentials.json"

def get_tier_status():
    if not CRED_PATH.exists():
        return {"tier": 0, "status": "Tier 0 (Public API / Zero Key Mode)", "unlocked": ["PSI v5", "CrUX History"]}
    try:
        with open(CRED_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "service_account" in data or "oauth" in data:
            return {"tier": 1, "status": "Tier 1 (Search Console & Indexing API Active)", "unlocked": ["GSC", "Indexing API"]}
    except Exception:
        pass
    return {"tier": 0, "status": "Tier 0 (Public API)", "unlocked": ["PSI v5", "CrUX"]}

if __name__ == "__main__":
    status = get_tier_status()
    print(f"Active Google Tier: {status['tier']} ({status['status']})")
    print(f"Unlocked Capabilities: {', '.join(status['unlocked'])}")
