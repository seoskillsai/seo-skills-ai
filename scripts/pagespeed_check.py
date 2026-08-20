#!/usr/bin/env python3
"""
SEO Skills AI — Google PageSpeed Insights v5 & Lighthouse Runner
User URL is validated before it is sent to Google's API. Failures are returned
as errors — scores are never invented.
"""
import os
import sys
import json
import urllib.request
from urllib.parse import quote

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.url_safety import validate_url


def run_pagespeed_check(url: str, strategy: str = "mobile", api_key: str = None) -> dict:
    try:
        validate_url(url)
    except (ValueError, PermissionError) as exc:
        return {"url": url, "strategy": strategy, "status": "BLOCKED", "error": str(exc)}

    encoded_url = quote(url, safe="")
    endpoint = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={encoded_url}&strategy={strategy}"
    if api_key:
        endpoint += f"&key={api_key}"

    try:
        req = urllib.request.Request(endpoint, headers={"User-Agent": "SEOSkillsAI/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            lighthouse = data.get("lighthouseResult", {})
            categories = lighthouse.get("categories", {})
            audits = lighthouse.get("audits", {})

            return {
                "url": url,
                "strategy": strategy,
                "status": "SUCCESS",
                "scores": {
                    "performance": int(categories.get("performance", {}).get("score", 0) * 100),
                    "accessibility": int(categories.get("accessibility", {}).get("score", 0) * 100),
                    "best_practices": int(categories.get("best-practices", {}).get("score", 0) * 100),
                    "seo": int(categories.get("seo", {}).get("score", 0) * 100)
                },
                "core_web_vitals": {
                    "lcp": audits.get("largest-contentful-paint", {}).get("displayValue", "N/A"),
                    "cls": audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A"),
                    "inp": audits.get("interaction-to-next-paint", {}).get("displayValue", "N/A"),
                    "fcp": audits.get("first-contentful-paint", {}).get("displayValue", "N/A"),
                    "speed_index": audits.get("speed-index", {}).get("displayValue", "N/A"),
                    "total_blocking_time": audits.get("total-blocking-time", {}).get("displayValue", "N/A")
                }
            }
    except Exception as e:
        return {
            "url": url,
            "strategy": strategy,
            "status": "UNAVAILABLE",
            "error": str(e),
            "notice": "PageSpeed Insights did not return live scores. No heuristic fallback is used."
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pagespeed_check.py <url> [mobile|desktop]")
        sys.exit(1)
    target = sys.argv[1]
    strat = sys.argv[2] if len(sys.argv) > 2 else "mobile"
    res = run_pagespeed_check(target, strategy=strat)
    print(json.dumps(res, indent=2))
    if res.get("status") != "SUCCESS":
        sys.exit(1)
