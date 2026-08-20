#!/usr/bin/env python3
"""
First-party Firecrawl scrape client.

Uses FIRECRAWL_API_KEY. Optional beside scripts/site_crawler.py.
User-supplied URLs still pass url_safety.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.http_json import json_request
from scripts.url_safety import normalize_user_url, validate_url

SCRAPE_URL = "https://api.firecrawl.dev/v1/scrape"


def scrape_url(url: str, formats: list[str] | None = None) -> dict:
    target = normalize_user_url(url)
    try:
        validate_url(target)
    except (ValueError, PermissionError) as exc:
        return {"url": url, "status": "BLOCKED", "error": str(exc)}

    key = (os.environ.get("FIRECRAWL_API_KEY") or "").strip()
    if not key:
        return {
            "url": target,
            "status": "UNAVAILABLE",
            "notice": "FIRECRAWL_API_KEY is required. No sample markdown is invented. Use scripts/site_crawler.py for local crawls.",
        }

    result = json_request(
        SCRAPE_URL,
        method="POST",
        headers={"Authorization": f"Bearer {key}"},
        body={"url": target, "formats": formats or ["markdown"]},
    )
    if result.get("status") == "ERROR":
        return {"url": target, "status": "ERROR", "error": result.get("error"), "detail": result.get("detail")}
    data = result.get("data") or {}
    return {
        "url": target,
        "status": "OK",
        "title": (data.get("metadata") or {}).get("title"),
        "markdown": data.get("markdown"),
        "notice": "Firecrawl scrape. This is vendor HTML-to-markdown, not a local crawl.",
    }


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    print(json.dumps(scrape_url(target), indent=2))
