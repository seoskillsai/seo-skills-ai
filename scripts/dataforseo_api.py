#!/usr/bin/env python3
"""
DataForSEO live SERP and Google Ads search volume.

Uses DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD from the environment.
Does not invent SERP rows when credentials are missing.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.http_json import json_request
from scripts.url_safety import normalize_user_url, validate_url

SERP_URL = "https://api.dataforseo.com/v3/serp/google/organic/live/regular"
VOLUME_URL = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"


def _creds() -> tuple[str, str] | None:
    login = (os.environ.get("DATAFORSEO_LOGIN") or "").strip()
    password = (os.environ.get("DATAFORSEO_PASSWORD") or "").strip()
    if not login or not password:
        return None
    return login, password


def fetch_live_serp(query: str, location_name: str = "United States", language_code: str = "en") -> dict:
    creds = _creds()
    if not creds:
        return {
            "query": query,
            "location": location_name,
            "language": language_code,
            "status": "UNAVAILABLE",
            "notice": "DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD are required. No sample SERP rows are invented.",
        }
    result = json_request(
        SERP_URL,
        method="POST",
        body=[
            {
                "keyword": query,
                "location_name": location_name,
                "language_code": language_code,
            }
        ],
        basic_auth=creds,
    )
    if result.get("status") == "ERROR":
        return {"query": query, "status": "ERROR", "error": result.get("error"), "detail": result.get("detail")}

    items = []
    for task in result.get("tasks") or []:
        for block in task.get("result") or []:
            for row in block.get("items") or []:
                if row.get("type") and row.get("type") not in ("organic", "featured_snippet"):
                    continue
                items.append(
                    {
                        "type": row.get("type"),
                        "rank": row.get("rank_group") or row.get("rank_absolute"),
                        "url": row.get("url"),
                        "title": row.get("title"),
                        "description": row.get("description"),
                    }
                )
    return {
        "query": query,
        "location": location_name,
        "language": language_code,
        "status": "OK",
        "items": items,
        "notice": "Live DataForSEO SERP response. Items are vendor data, not estimates.",
    }


def fetch_search_volume(keywords: list[str], location_code: int = 2840, language_code: str = "en") -> dict:
    creds = _creds()
    if not creds:
        return {
            "keywords": keywords,
            "status": "UNAVAILABLE",
            "notice": "DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD are required. No sample volumes are invented.",
        }
    result = json_request(
        VOLUME_URL,
        method="POST",
        body=[{"keywords": keywords, "location_code": location_code, "language_code": language_code}],
        basic_auth=creds,
    )
    if result.get("status") == "ERROR":
        return {"keywords": keywords, "status": "ERROR", "error": result.get("error"), "detail": result.get("detail")}
    rows = []
    for task in result.get("tasks") or []:
        rows.extend(task.get("result") or [])
    return {"keywords": keywords, "status": "OK", "result": rows}


def fetch_url_serp_context(url: str) -> dict:
    target = normalize_user_url(url)
    try:
        validate_url(target)
    except (ValueError, PermissionError) as exc:
        return {"url": url, "status": "BLOCKED", "error": str(exc)}
    return fetch_live_serp(target)


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "ai seo skills"
    print(json.dumps(fetch_live_serp(q), indent=2))
