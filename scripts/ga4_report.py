#!/usr/bin/env python3
"""
GA4 Data API organic-search sessions.

Requires google_credentials.json with a refresh token and ga4_property_id.
Never invents session counts.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.google_oauth import load_google_credentials, refresh_google_bearer, unavailable
from scripts.http_json import json_request

GA4_REPORT = "https://analyticsdata.googleapis.com/v1beta/properties/{property_id}:runReport"


def fetch_ga4_organic_report(property_id: str | None = None, days: int = 30) -> dict:
    creds = load_google_credentials()
    if not creds:
        return unavailable({"date_range_days": days})

    pid = (property_id or creds.get("ga4_property_id") or "").strip()
    if not pid:
        return {
            "status": "UNAVAILABLE",
            "notice": "ga4_property_id is missing from ~/.config/seoskillsai/google_credentials.json",
            "date_range_days": days,
        }

    token = refresh_google_bearer(creds)
    if token.get("status") != "OK":
        return {"status": token.get("status", "ERROR"), "notice": token.get("notice"), "error": token.get("error")}

    body = {
        "dateRanges": [{"startDate": f"{max(1, days)}daysAgo", "endDate": "today"}],
        "dimensions": [{"name": "sessionDefaultChannelGroup"}],
        "metrics": [{"name": "sessions"}, {"name": "activeUsers"}],
        "dimensionFilter": {
            "filter": {
                "fieldName": "sessionDefaultChannelGroup",
                "stringFilter": {"matchType": "EXACT", "value": "Organic Search"},
            }
        },
    }
    result = json_request(
        GA4_REPORT.format(property_id=pid),
        method="POST",
        headers={"Authorization": f"Bearer {token['bearer']}"},
        body=body,
    )
    if result.get("status") == "ERROR":
        return {"status": "ERROR", "property_id": pid, "error": result.get("error"), "detail": result.get("detail")}

    rows = result.get("rows") or []
    sessions = 0
    users = 0
    if rows:
        values = rows[0].get("metricValues") or []
        if values:
            sessions = int(float(values[0].get("value") or 0))
        if len(values) > 1:
            users = int(float(values[1].get("value") or 0))

    return {
        "status": "OK",
        "property_id": pid,
        "date_range_days": days,
        "organic_sessions": sessions,
        "organic_users": users,
        "notice": "Organic Search row from the GA4 Data API for the local property_id only.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GA4 organic sessions")
    parser.add_argument("--property", dest="property_id", default=None)
    parser.add_argument("--days", type=int, default=30)
    args = parser.parse_args()
    print(json.dumps(fetch_ga4_organic_report(args.property_id, args.days), indent=2))
