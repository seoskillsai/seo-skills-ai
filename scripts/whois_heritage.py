#!/usr/bin/env python3
"""
SEO Skills AI — Domain Age, RDAP Registration & Expired Domain Heritage Analyzer
"""
import os
import sys
import json
import urllib.request
from urllib.parse import urlparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.url_safety import normalize_user_url, validate_url


def query_domain_heritage(domain_or_url: str) -> dict:
    parsed = urlparse(normalize_user_url(domain_or_url))
    domain = (parsed.hostname or domain_or_url).split(":")[0].strip().lower()
    try:
        validate_url(f"https://{domain}/")
    except (ValueError, PermissionError) as exc:
        return {"domain": domain, "status": "BLOCKED", "error": str(exc)}

    rdap_url = f"https://rdap.org/domain/{domain}"
    req = urllib.request.Request(
        rdap_url,
        headers={"User-Agent": "SEOSkillsAI-RDAP/1.0", "Accept": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            events = {e.get("eventAction"): e.get("eventDate") for e in data.get("events", [])}
            return {
                "domain": domain,
                "status": "VERIFIED_RDAP",
                "registration_date": events.get("registration", "Unknown"),
                "expiration_date": events.get("expiration", "Unknown"),
                "last_changed": events.get("last changed", "Unknown"),
                "source": "ICANN RDAP Protocol"
            }
    except Exception as e:
        return {
            "domain": domain,
            "status": "UNAVAILABLE",
            "error": str(e),
            "notice": "RDAP query failed. No heuristic registration date is invented.",
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python whois_heritage.py <domain_or_url>")
        sys.exit(1)
    target = sys.argv[1]
    res = query_domain_heritage(target)
    print(json.dumps(res, indent=2))
