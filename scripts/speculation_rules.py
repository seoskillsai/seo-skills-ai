#!/usr/bin/env python3
"""
SEO Skills AI — W3C Speculation Rules API & Back/Forward Cache (bfcache) Analyzer
Audits next-generation browser pre-rendering rules (<script type="speculationrules">) and bfcache eligibility.
"""
import os
import sys
import json
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.fetch_page import fetch_page

def analyze_speculation_and_bfcache(url: str) -> dict:
    res = fetch_page(url)
    if res["status_code"] != 200:
        return {"error": f"HTTP error {res['status_code']} fetching {url}"}

    html = res["html"]
    headers = res.get("headers", {})

    # 1. Speculation Rules Detection
    speculation_rules_raw = re.findall(
        r'<script\s+type=[\'"]speculationrules[\'"][^>]*>([\s\S]*?)</script>',
        html,
        re.IGNORECASE
    )

    speculation_rules_parsed = []
    has_prerender = False
    has_prefetch = False

    for block in speculation_rules_raw:
        try:
            data = json.loads(block.strip())
            speculation_rules_parsed.append(data)
            if "prerender" in data:
                has_prerender = True
            if "prefetch" in data:
                has_prefetch = True
        except Exception:
            pass

    # 2. bfcache Eligibility Inspection
    cache_control = headers.get("cache-control", "").lower()
    has_no_store = "no-store" in cache_control
    has_unload_handler = "window.onunload" in html or "addEventListener('unload'" in html or 'addEventListener("unload"' in html

    bfcache_eligible = not (has_no_store or has_unload_handler)
    bfcache_blockers = []
    if has_no_store:
        bfcache_blockers.append("Header 'Cache-Control: no-store' prevents Back/Forward Cache storage.")
    if has_unload_handler:
        bfcache_blockers.append("Deprecated 'unload' event listener detected in DOM, breaking bfcache transitions.")

    # Recommendations
    recommendations = []
    if not speculation_rules_parsed:
        recommendations.append("Add W3C Speculation Rules for high-probability internal navigation links to achieve 0ms render latency.")
    if not bfcache_eligible:
        recommendations.append("Remove bfcache blockers (switch 'no-store' to 'no-cache, must-revalidate' if suitable) to enable instant Back/Forward navigation.")

    return {
        "url": url,
        "speculation_rules": {
            "detected": len(speculation_rules_parsed) > 0,
            "rules_count": len(speculation_rules_parsed),
            "has_prerender": has_prerender,
            "has_prefetch": has_prefetch,
            "rules": speculation_rules_parsed
        },
        "bfcache": {
            "eligible": bfcache_eligible,
            "cache_control_header": cache_control,
            "blockers_count": len(bfcache_blockers),
            "blockers": bfcache_blockers
        },
        "recommendations": recommendations
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python speculation_rules.py <url>")
        sys.exit(1)
    target = sys.argv[1]
    res = analyze_speculation_and_bfcache(target)
    print(json.dumps(res, indent=2))
