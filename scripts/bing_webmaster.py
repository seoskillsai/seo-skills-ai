#!/usr/bin/env python3
"""
SEO Skills AI — Bing Webmaster Tools & IndexNow API Client
"""
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.url_safety import normalize_user_url, validate_url


def fetch_bing_metrics(site_url: str, api_key: str = None) -> dict:
    url = normalize_user_url(site_url)
    try:
        validate_url(url)
    except (ValueError, PermissionError) as exc:
        return {"site_url": site_url, "status": "BLOCKED", "error": str(exc)}

    if not api_key:
        return {
            "site_url": url,
            "engine": "Bing Webmaster Tools",
            "status": "UNAVAILABLE",
            "notice": "Bing Webmaster API key was not provided. No estimated impressions or link counts are returned.",
        }
    return {
        "site_url": url,
        "engine": "Bing Webmaster Tools",
        "status": "UNAVAILABLE",
        "notice": "Bing Webmaster live queries are not wired in this runtime beyond IndexNow submission.",
    }

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "https://seoskillsai.com"
    res = fetch_bing_metrics(t)
    print(json.dumps(res, indent=2))
