#!/usr/bin/env python3
"""
Bing Webmaster Tools query stats.

Requires BING_WEBMASTER_API_KEY or BING_API_KEY.
Does not invent impressions. IndexNow stays in indexing_notify.py.
"""
from __future__ import annotations

import json
import os
import sys
from urllib.parse import urlencode

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.http_json import json_request
from scripts.url_safety import normalize_user_url, validate_url

QUERY_STATS = "https://ssl.bing.com/webmaster/api.svc/json/GetQueryStats"
TRAFFIC_STATS = "https://ssl.bing.com/webmaster/api.svc/json/GetRankAndTrafficStats"


def _api_key(explicit: str | None = None) -> str:
    return (
        (explicit or "").strip()
        or (os.environ.get("BING_WEBMASTER_API_KEY") or "").strip()
        or (os.environ.get("BING_API_KEY") or "").strip()
    )


def fetch_bing_metrics(site_url: str, api_key: str | None = None) -> dict:
    url = normalize_user_url(site_url)
    try:
        validate_url(url)
    except (ValueError, PermissionError) as exc:
        return {"site_url": site_url, "status": "BLOCKED", "error": str(exc)}

    key = _api_key(api_key)
    if not key:
        return {
            "site_url": url,
            "engine": "Bing Webmaster Tools",
            "status": "UNAVAILABLE",
            "notice": "BING_WEBMASTER_API_KEY (or BING_API_KEY) was not provided. No estimated impressions are returned.",
        }

    qs = urlencode({"apikey": key, "siteUrl": url})
    queries = json_request(f"{QUERY_STATS}?{qs}", method="GET")
    traffic = json_request(f"{TRAFFIC_STATS}?{qs}", method="GET")
    if queries.get("status") == "ERROR" and traffic.get("status") == "ERROR":
        return {
            "site_url": url,
            "engine": "Bing Webmaster Tools",
            "status": "ERROR",
            "error": queries.get("error") or traffic.get("error"),
            "detail": queries.get("detail") or traffic.get("detail"),
        }
    return {
        "site_url": url,
        "engine": "Bing Webmaster Tools",
        "status": "OK",
        "query_stats": queries.get("d") or queries,
        "traffic_stats": traffic.get("d") or traffic,
        "notice": "Live Bing Webmaster JSON. Values are vendor data for the authenticated site.",
    }


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    print(json.dumps(fetch_bing_metrics(t), indent=2))
