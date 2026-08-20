#!/usr/bin/env python3
"""
SEO Skills AI — Google Indexing API & IndexNow Batch Notifier
Each submitted URL is checked against the network-target policy. Failures are
not reported as success.
"""
import os
import sys
import json
import urllib.request

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.url_safety import validate_url


def notify_indexnow(host: str, key: str, url_list: list) -> dict:
    if not key or key == "seoskillsai-key":
        return {
            "engine": "IndexNow",
            "status": "SKIPPED",
            "error": "IndexNow key is required. Pass a real key; dummy placeholders are rejected.",
        }

    checked = []
    for item in url_list:
        try:
            validate_url(item)
            checked.append(item)
        except (ValueError, PermissionError) as exc:
            return {
                "engine": "IndexNow",
                "status": "BLOCKED",
                "error": str(exc),
                "rejected_url": item,
            }

    endpoint = "https://api.indexnow.org/indexnow"
    payload = {
        "host": host,
        "key": key,
        "urlList": checked
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(endpoint, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return {
                "engine": "IndexNow (Bing/Yandex/Seznam)",
                "status_code": resp.status,
                "urls_submitted": len(checked),
                "status": "SUCCESS"
            }
    except Exception as e:
        return {
            "engine": "IndexNow",
            "status_code": 0,
            "error": str(e),
            "status": "FAILED",
            "urls_submitted": 0
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python indexing_notify.py <host> <key> <url1> [url2...]")
        sys.exit(1)
    h = sys.argv[1]
    k = sys.argv[2] if len(sys.argv) > 2 else ""
    urls = sys.argv[3:] if len(sys.argv) > 3 else [f"https://{h}/"]
    res = notify_indexnow(h, k, urls)
    print(json.dumps(res, indent=2))
    if res.get("status") != "SUCCESS":
        sys.exit(1)
