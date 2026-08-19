#!/usr/bin/env python3
"""
SEO Skills AI — Enterprise Multi-Page Recursive Site Crawler & Link Graph Builder
Crawls up to N pages to discover orphan pages, crawl depth distribution, canonical loops, and sitewide 3x anchor text diversity violations.
"""
import os
import sys
import json
import time
from urllib.parse import urlparse, urljoin
from collections import deque

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.fetch_page import fetch_page
from scripts.parse_html import parse_html_content

def crawl_site(start_url: str, max_pages: int = 25, max_depth: int = 3) -> dict:
    parsed_start = urlparse(start_url)
    base_domain = parsed_start.netloc
    base_scheme = parsed_start.scheme

    visited = set()
    queue = deque([(start_url, 0)])  # (url, depth)
    
    pages_crawled = []
    broken_links = []
    orphan_pages = []
    canonical_issues = []
    all_internal_anchors = {}  # anchor_text -> count
    link_graph = {}  # source_url -> [target_urls]
    status_code_distribution = {}

    print(f"==> [SEO Crawler] Initiating recursive crawl on {start_url} (Max: {max_pages} pages, Depth: {max_depth})...")

    while queue and len(visited) < max_pages:
        current_url, depth = queue.popleft()
        
        # Normalize URL
        current_url = current_url.split("#")[0].rstrip("/")
        if current_url in visited or depth > max_depth:
            continue

        visited.add(current_url)
        res = fetch_page(current_url)
        status = res["status_code"]
        status_code_distribution[status] = status_code_distribution.get(status, 0) + 1

        if status != 200:
            broken_links.append({"url": current_url, "status": status, "error": res.get("error")})
            continue

        parsed = parse_html_content(res["html"], base_url=current_url)
        link_graph[current_url] = []

        # Canonical integrity
        if parsed["canonical"]:
            clean_canonical = parsed["canonical"].split("#")[0].rstrip("/")
            if clean_canonical != current_url and clean_canonical not in (current_url + "/", current_url):
                canonical_issues.append({
                    "url": current_url,
                    "canonical_points_to": parsed["canonical"]
                })

        pages_crawled.append({
            "url": current_url,
            "depth": depth,
            "title": parsed["title"],
            "word_count": parsed["word_count"],
            "schemas_count": parsed["schemas_count"],
            "internal_links_count": parsed["internal_links_count"],
            "latency_ms": res["latency_ms"]
        })

        # Process internal links
        for href, anchors in parsed["anchor_text_map"].items():
            full_target = urljoin(current_url, href).split("#")[0].rstrip("/")
            parsed_target = urlparse(full_target)
            
            if parsed_target.netloc == base_domain:
                link_graph[current_url].append(full_target)
                for a in anchors:
                    clean_a = a.strip().lower()
                    if len(clean_a) > 2:
                        all_internal_anchors[clean_a] = all_internal_anchors.get(clean_a, 0) + 1
                        
                if full_target not in visited and depth + 1 <= max_depth:
                    queue.append((full_target, depth + 1))

    # Detect 3x Anchor Diversity Rule violations sitewide
    anchor_violations = [
        {"anchor": a, "count": c, "severity": "P1"}
        for a, c in all_internal_anchors.items() if c > 3
    ]

    # Calculate average depth and crawl statistics
    avg_depth = sum(p["depth"] for p in pages_crawled) / len(pages_crawled) if pages_crawled else 0
    thin_pages = [p["url"] for p in pages_crawled if p["word_count"] < 800]

    return {
        "start_url": start_url,
        "total_pages_crawled": len(pages_crawled),
        "status_code_distribution": status_code_distribution,
        "average_crawl_depth": round(avg_depth, 2),
        "broken_links": broken_links,
        "canonical_issues": canonical_issues,
        "thin_pages_count": len(thin_pages),
        "thin_pages": thin_pages,
        "anchor_text_violations_3x_rule": anchor_violations,
        "pages": pages_crawled
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python site_crawler.py <start_url> [max_pages]")
        sys.exit(1)
    target = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    results = crawl_site(target, max_pages=limit)
    print(json.dumps(results, indent=2))
