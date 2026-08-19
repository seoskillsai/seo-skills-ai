#!/usr/bin/env python3
"""
SEO Skills AI — Google Consent Mode v2 & EU Digital Markets Act (DMA) Validator
Verifies implementation of Google Consent Mode v2 (ad_user_data, ad_personalization, ad_storage, analytics_storage).
"""
import os
import sys
import json
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.fetch_page import fetch_page

V2_SIGNALS = ["ad_storage", "analytics_storage", "ad_user_data", "ad_personalization"]
KNOWN_CMPS = ["onetrust", "cookiebot", "didomi", "usercentrics", "complianz", "quantcast", "axeptio", "klaro"]

def audit_consent_mode(url: str) -> dict:
    res = fetch_page(url)
    if res["status_code"] != 200:
        return {"error": f"HTTP error {res['status_code']} fetching {url}"}

    html = res["html"].lower()

    # 1. Detect CMP Provider
    detected_cmps = [cmp for cmp in KNOWN_CMPS if cmp in html]

    # 2. Check for GTAG consent defaults
    has_gtag_consent = "gtag('consent'" in html or 'gtag("consent"' in html
    
    signals_found = {}
    for sig in V2_SIGNALS:
        signals_found[sig] = sig in html

    v2_complete = all(signals_found.values())
    has_google_tag = "googletagmanager.com/gtm.js" in html or "googletagmanager.com/gtag/js" in html

    issues = []
    if has_google_tag and not has_gtag_consent:
        issues.append("Google Tags detected but no default 'gtag(consent, default, ...)' initialization found.")
    if has_gtag_consent and not v2_complete:
        missing = [k for k, v in signals_found.items() if not v]
        issues.append(f"Incomplete Consent Mode v2. Missing required DMA signals: {', '.join(missing)}.")

    status = (
        "COMPLIANT (Consent Mode v2 Fully Active)" if v2_complete and has_gtag_consent else
        ("PARTIAL / LEGACY (v1 or Incomplete Signals)" if has_gtag_consent else
         ("NON-COMPLIANT (Google Tags Firing Without Consent Gate)" if has_google_tag else "NO_GOOGLE_TAGS_DETECTED"))
    )

    return {
        "url": url,
        "consent_mode_status": status,
        "cmp_detected": detected_cmps or ["None / Custom"],
        "has_google_tag": has_google_tag,
        "has_gtag_consent_call": has_gtag_consent,
        "signals_presence": signals_found,
        "compliance_issues": issues,
        "reference": "Google Consent Mode v2 & EU DMA Compliance Standard (March 2024 / 2026)"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python consent_mode.py <url>")
        sys.exit(1)
    target = sys.argv[1]
    res = audit_consent_mode(target)
    print(json.dumps(res, indent=2))
