#!/usr/bin/env python3
"""
SEO Skills AI — Live Backlink Verification Crawler
"""
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.fetch_page import fetch_page
from scripts.parse_html import parse_html_content

def verify_single_backlink(referring_url: str, target_domain: str) -> dict:
    page = fetch_page(referring_url)
    if page["status_code"] != 200:
        return {
            "referring_url": referring_url,
            "target_domain": target_domain,
            "status": "UNREACHABLE",
            "error": f"HTTP {page['status_code']}"
        }

    parsed = parse_html_content(page["html"], base_url=referring_url)
    found_links = []
    for href, anchors in parsed["anchor_text_map"].items():
        if target_domain.lower() in href.lower():
            found_links.append({
                "target_url": href,
                "anchors": anchors
            })

    return {
        "referring_url": referring_url,
        "target_domain": target_domain,
        "status": "VERIFIED" if found_links else "LINK_NOT_FOUND",
        "links_found_count": len(found_links),
        "links": found_links,
        "page_robots": parsed["meta_robots"]
    }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python verify_backlinks.py <referring_url> <target_domain>")
        sys.exit(1)
    res = verify_single_backlink(sys.argv[1], sys.argv[2])
    print(json.dumps(res, indent=2))
