#!/usr/bin/env python3
"""
SEO Skills AI — Enterprise Parallel Multi-Agent Audit Runner
"""
import os
import sys
import json

# Ensure parent directory is on sys.path for direct CLI execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.fetch_page import fetch_page
from scripts.parse_html import parse_html_content
from scripts.schema_validator import validate_schema_json

def run_full_audit(url: str) -> dict:
    page = fetch_page(url)
    if page.get("error") or page["status_code"] != 200:
        return {
            "url": url,
            "status": "FAILED",
            "error": page.get("error", f"HTTP {page['status_code']}"),
            "health_score": 0,
            "critical_issues": [f"Site unreachable or returned error: {page.get('error', page['status_code'])}"],
            "action_plan": ["Verify server configuration, DNS resolution, and SSL certificate."]
        }

    parsed = parse_html_content(page["html"], base_url=url)
    schema_results = [validate_schema_json(s) for s in parsed["schemas"]]

    # Enterprise Scoring Formula (0-100)
    tech_score = 100
    if not parsed["canonical"]:
        tech_score -= 15
    if page["is_redirected"]:
        tech_score -= 5
    if not page["security_headers"].get("csp"):
        tech_score -= 10
    if not page["security_headers"].get("hsts"):
        tech_score -= 5

    content_score = 100
    if parsed["word_count"] < 800:
        content_score -= 30
    if not parsed["h1"]:
        content_score -= 25
    if parsed["heading_hierarchy_errors"]:
        content_score -= 15
    if parsed["over_optimized_anchors"]:
        content_score -= 10

    schema_score = 100
    if not parsed["schemas"]:
        schema_score = 40
    else:
        has_deprecated = any(r["deprecated_warnings"] for r in schema_results)
        if has_deprecated:
            schema_score -= 30
        has_missing = any(r["missing_property_warnings"] for r in schema_results)
        if has_missing:
            schema_score -= 15

    geo_score = 70
    if parsed["citable_passages_count"] >= 2:
        geo_score += 20
    if parsed["has_large_image_preview"]:
        geo_score += 10

    overall_score = max(0, min(100, round(
        (tech_score * 0.30) + (content_score * 0.30) + (schema_score * 0.20) + (geo_score * 0.20)
    )))

    critical_issues = []
    if not parsed["h1"]:
        critical_issues.append("Missing primary H1 heading tag.")
    if parsed["word_count"] < 800:
        critical_issues.append(f"Thin body content ({parsed['word_count']} words). Minimum 800 words required.")
    if not parsed["canonical"]:
        critical_issues.append("Missing self-referencing canonical URL tag.")
    if not parsed["schemas"]:
        critical_issues.append("Zero JSON-LD structured data detected.")

    action_plan = []
    if not parsed["has_large_image_preview"]:
        action_plan.append("Add '<meta name=\"robots\" content=\"max-image-preview:large\">' to unlock Google Discover traffic.")
    if not parsed["schemas"]:
        action_plan.append("Embed unified 2026 Schema.org @graph with TechArticle, SoftwareApplication, and BreadcrumbList.")
    if parsed["heading_hierarchy_errors"]:
        action_plan.append(f"Fix heading sequence skips: {', '.join(parsed['heading_hierarchy_errors'])}.")
    if parsed["citable_passages_count"] < 2:
        action_plan.append("Structure core sections with 130–170 word self-contained answer passages for GEO AI citation.")

    return {
        "url": url,
        "final_url": page["final_url"],
        "status": "SUCCESS",
        "health_score": overall_score,
        "discipline_scores": {
            "technical": max(0, tech_score),
            "content_eeat": max(0, content_score),
            "schema_markup": max(0, schema_score),
            "geo_ai_search": max(0, geo_score)
        },
        "metrics": {
            "status_code": page["status_code"],
            "title": parsed.get("title") or "",
            "latency_ms": page["latency_ms"],
            "word_count": parsed["word_count"],
            "h1_count": len(parsed["h1"]),
            "h2_count": len(parsed["h2"]),
            "images_count": parsed["images_count"],
            "images_missing_alt": len(parsed["images_missing_alt"]),
            "schemas_detected": len(parsed["schemas"]),
            "citable_passages_detected": parsed["citable_passages_count"],
            "internal_links_count": parsed["internal_links_count"],
            "external_links_count": parsed["external_links_count"]
        },
        "critical_issues": critical_issues,
        "action_plan": action_plan
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python full_audit.py <url>")
        sys.exit(1)
    res = run_full_audit(sys.argv[1])
    print(json.dumps(res, indent=2))
