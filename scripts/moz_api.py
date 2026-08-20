#!/usr/bin/env python3
"""
SEO Skills AI — Moz Link Explorer API Client
Returns live data only when Moz credentials are provided.
"""
import os
import sys
import json
from urllib.parse import urlparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.url_safety import normalize_user_url, validate_url


def query_moz_api(target_url: str, access_id: str = None, secret_key: str = None) -> dict:
    url = normalize_user_url(target_url)
    try:
        validate_url(url)
    except (ValueError, PermissionError) as exc:
        return {"target": target_url, "status": "BLOCKED", "error": str(exc)}

    domain = urlparse(url).netloc or target_url
    if not access_id or not secret_key:
        return {
            "target": url,
            "domain": domain,
            "status": "UNAVAILABLE",
            "notice": "Moz API credentials were not provided. No estimated DA/PA values are returned.",
        }
    return {
        "target": url,
        "domain": domain,
        "status": "UNAVAILABLE",
        "notice": "Moz signed requests are not implemented in this open runtime. Use the official Moz API client with your own credentials.",
    }

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "https://seoskillsai.com"
    res = query_moz_api(t)
    print(json.dumps(res, indent=2))
