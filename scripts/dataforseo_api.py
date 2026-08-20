#!/usr/bin/env python3
"""
SEO Skills AI — DataForSEO Live SERP & Keyword Data Client
"""
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def fetch_live_serp(query: str, location_name: str = "United States", language_code: str = "en") -> dict:
    login = os.environ.get("DATAFORSEO_LOGIN")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not password:
        return {
            "query": query,
            "location": location_name,
            "language": language_code,
            "status": "UNAVAILABLE",
            "notice": "DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD are required. No sample SERP rows are invented.",
        }
    return {
        "query": query,
        "location": location_name,
        "language": language_code,
        "status": "UNAVAILABLE",
        "notice": "Use the DataForSEO MCP extension with your own credentials for live SERP data.",
    }

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "ai seo skills"
    res = fetch_live_serp(q)
    print(json.dumps(res, indent=2))
