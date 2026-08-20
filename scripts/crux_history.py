#!/usr/bin/env python3
"""
SEO Skills AI — CrUX 25-Week Performance History Analyzer
"""
import os
import sys
import json
import urllib.request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.url_safety import validate_url


def fetch_crux_history(url: str, api_key: str = None) -> dict:
    try:
        validate_url(url)
    except (ValueError, PermissionError) as exc:
        return {"status": "BLOCKED", "error": str(exc)}

    endpoint = "https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord"
    body = json.dumps({"url": url}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        endpoint += f"?key={api_key}"
    req = urllib.request.Request(endpoint, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {"status": "SUCCESS", "record": data.get("record", {})}
    except Exception as e:
        return {
            "status": "UNAVAILABLE",
            "message": "CrUX history requires a traffic threshold and/or API key.",
            "error": str(e),
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crux_history.py <url>")
        sys.exit(1)
    res = fetch_crux_history(sys.argv[1])
    print(json.dumps(res, indent=2))
