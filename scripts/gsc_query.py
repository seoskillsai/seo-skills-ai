#!/usr/bin/env python3
"""
Google Search Console Search Analytics.

Requires ~/.config/seoskillsai/google_credentials.json from google_oauth.py.
Never invents clicks or impressions.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, timedelta
from urllib.parse import quote

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.google_oauth import load_google_credentials, refresh_access_token, unavailable
from scripts.http_json import json_request
from scripts.url_safety import normalize_user_url, validate_url

GSC_QUERY = "https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GSC Search Analytics")
    parser.add_argument("site_url", nargs="?", default=None)
    parser.add_argument("--site", dest="site_flag")
    parser.add_argument("--filter", dest="filter_type", default="striking-distance")
    parser.add_argument("--days", type=int, default=28)
    return parser.parse_args(argv)


def _validate_gsc_property(site_url: str) -> str:
    text = (site_url or "").strip()
    if text.lower().startswith("sc-domain:"):
        domain = text.split(":", 1)[1].strip().rstrip("/")
        validate_url("https://" + domain)
        return "sc-domain:" + domain
    url = normalize_user_url(text)
    validate_url(url)
    return url


def query_gsc(site_url: str, filter_type: str = "all", days: int = 28) -> dict:
    try:
        url = _validate_gsc_property(site_url)
    except (ValueError, PermissionError) as exc:
        return {"site_url": site_url, "status": "BLOCKED", "error": str(exc)}

    creds = load_google_credentials()
    if not creds:
        return unavailable({"site_url": url, "date_range_days": days})

    token = refresh_access_token(creds)
    if token.get("status") != "OK":
        return {"site_url": url, "status": token.get("status", "ERROR"), "notice": token.get("notice"), "error": token.get("error")}

    end = date.today()
    start = end - timedelta(days=max(1, days))
    encoded_site = quote(url, safe="")
    endpoint = GSC_QUERY.format(site=encoded_site)
    payload = {
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "dimensions": ["query"],
        "rowLimit": 25000,
    }
    result = json_request(
        endpoint,
        method="POST",
        headers={"Authorization": f"Bearer {token['access_token']}"},
        body=payload,
    )
    if result.get("status") == "ERROR":
        return {"site_url": url, "status": "ERROR", "error": result.get("error"), "detail": result.get("detail")}

    rows = result.get("rows") or []
    keywords = []
    for row in rows:
        keys = row.get("keys") or []
        query = keys[0] if keys else ""
        position = float(row.get("position") or 0)
        item = {
            "query": query,
            "clicks": row.get("clicks"),
            "impressions": row.get("impressions"),
            "ctr": row.get("ctr"),
            "position": position,
        }
        if filter_type == "striking-distance" and not (8.0 <= position <= 20.0):
            continue
        keywords.append(item)

    return {
        "site_url": url,
        "status": "OK",
        "date_range_days": days,
        "filter": filter_type,
        "row_count": len(keywords),
        "keywords": keywords,
        "notice": "Values come from Search Console Search Analytics for the authenticated Google account.",
    }


if __name__ == "__main__":
    args = _parse_args(sys.argv[1:])
    target = args.site_flag or args.site_url or "https://example.com"
    print(json.dumps(query_gsc(target, filter_type=args.filter_type, days=args.days), indent=2))
