#!/usr/bin/env python3
"""
SEO Skills AI — Common Crawl Open Web Graph Backlink Analyzer
"""
import os
import sys
import json
from urllib.parse import urlparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.url_safety import normalize_user_url, validate_url


def query_common_crawl(domain: str) -> dict:
    url = normalize_user_url(domain)
    try:
        validate_url(url)
    except (ValueError, PermissionError) as exc:
        return {"domain": domain, "status": "BLOCKED", "error": str(exc)}

    clean_domain = urlparse(url).netloc or domain
    return {
        "domain": clean_domain,
        "source": "Common Crawl Open Web Graph",
        "status": "UNAVAILABLE",
        "notice": "Live Common Crawl index queries are not wired in this runtime. No estimated PageRank is invented.",
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python commoncrawl_graph.py <domain>")
        sys.exit(1)
    res = query_common_crawl(sys.argv[1])
    print(json.dumps(res, indent=2))
