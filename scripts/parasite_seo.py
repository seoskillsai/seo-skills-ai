#!/usr/bin/env python3
"""
SEO Skills AI — Google Site Reputation Abuse & Parasite SEO Detector
Alarms on subdomains, directories, or third-party hosted content that deviate from root brand authority
per Google's November 2024 / 2026 Site Reputation Abuse policy.
"""
import os
import sys
import json
import re
from urllib.parse import urlparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.fetch_page import fetch_page
from scripts.parse_html import parse_html_content

AFFILIATE_PATTERNS = [
    r"amzn\.to", r"amazon\.com/.*tag=", r"awin1\.com", r"shareasale\.com",
    r"impactradius\.com", r"cj\.com", r"rakuten\.com", r"clickbank\.net",
    r"partnerize\.com", r"prf\.hn", r"go\.skimresources\.com"
]

COMMERCIAL_INTENT_TERMS = [
    "best coupon", "promo code", "discount code", "voucher code",
    "best online casino", "best slots", "loan fast", "crypto trading bot"
]

def scan_parasite_seo_risk(url: str) -> dict:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path.lower()
    subdomain = domain.split(".")[0] if len(domain.split(".")) > 2 else ""

    res = fetch_page(url)
    if res["status_code"] != 200:
        return {"error": f"HTTP error {res['status_code']} fetching {url}"}

    parsed = parse_html_content(res["html"], base_url=url)
    
    # 1. Check commercial intent mismatch
    title_lower = parsed["title"].lower()
    h1_lower = " ".join(parsed["h1"]).lower()
    matched_commercial_terms = [
        term for term in COMMERCIAL_INTENT_TERMS if term in title_lower or term in h1_lower or term in path
    ]

    # 2. Check third-party affiliate footprint density
    affiliate_links_found = []
    for href in parsed.get("external_links", []):
        for pattern in AFFILIATE_PATTERNS:
            if re.search(pattern, href, re.IGNORECASE):
                affiliate_links_found.append(href)

    # 3. Assess Subdomain / Path Isolation
    is_niche_subdomain = subdomain in ("coupons", "deals", "reviews", "casino", "loans", "vouchers")
    is_niche_path = any(p in path for p in ("/coupons", "/deals", "/vouchers", "/casino", "/best-deals"))

    risk_score = 0
    risk_factors = []

    if is_niche_subdomain:
        risk_score += 35
        risk_factors.append(f"Subdomain '{subdomain}' matches high-risk parasite commercial silo.")
    if is_niche_path:
        risk_score += 25
        risk_factors.append(f"Path '{path}' matches high-risk affiliate directory pattern.")
    if matched_commercial_terms:
        risk_score += 30
        risk_factors.append(f"High-risk commercial search query detected: {', '.join(matched_commercial_terms)}")
    if len(affiliate_links_found) > 3:
        risk_score += 20
        risk_factors.append(f"Heavy third-party affiliate redirection density ({len(affiliate_links_found)} links).")

    verdict = (
        "HIGH PARASITE RISK (Site Reputation Abuse Alert)" if risk_score >= 60 else
        ("MODERATE RISK (Verify editorial oversight & first-party involvement)" if risk_score >= 30 else
         "CLEAN / LOW RISK (Aligned with first-party brand intent)")
    )

    return {
        "url": url,
        "domain": domain,
        "risk_score": min(100, risk_score),
        "verdict": verdict,
        "risk_factors": risk_factors,
        "affiliate_links_detected": len(affiliate_links_found),
        "policy_reference": "Google Site Reputation Abuse Policy (November 2024 / 2026 Manual Action Protection)"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parasite_seo.py <url>")
        sys.exit(1)
    target = sys.argv[1]
    res = scan_parasite_seo_risk(target)
    print(json.dumps(res, indent=2))
