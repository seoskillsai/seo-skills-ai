#!/usr/bin/env python3
"""
SEO Skills AI — CrUX 25-Week Performance History Analyzer
"""
import sys
import json
import urllib.request

def fetch_crux_history(url: str, api_key: str = None) -> dict:
    endpoint = "https://chromeuxreport.googleapis.com/v1/records:queryHistoryRecord"
    body = json.dumps({"url": url}).encode("utf-8")
    req = urllib.request.Request(endpoint, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {"status": "SUCCESS", "record": data.get("record", {})}
    except Exception as e:
        return {"status": "UNAVAILABLE", "message": "CrUX history requires minimum traffic threshold or API key.", "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crux_history.py <url>")
        sys.exit(1)
    res = fetch_crux_history(sys.argv[1])
    print(json.dumps(res, indent=2))
