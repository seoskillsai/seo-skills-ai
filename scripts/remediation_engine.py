#!/usr/bin/env python3
"""
SEO Skills AI — Review-only code remediation snippets
Prints copy-paste HTML/Astro patches. Never writes the repository and has no --apply mode.
"""
import os
import sys
import json
from urllib.parse import urlparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.full_audit import run_full_audit

APPLY_REFUSED = (
    "Patches are generated for human review only. This tool never writes them "
    "into your repository and there is no --apply mode. Copy snippets after you inspect them."
)

def generate_remediation_patches(url: str) -> dict:
    audit = run_full_audit(url)
    if audit.get("status") == "FAILED":
        return {"error": audit.get("error", "Audit failed")}

    parsed_url = urlparse(url)
    domain = parsed_url.netloc or url
    page_name = parsed_url.path.strip("/").replace("-", " ").title() or "Home"

    patches = []

    # Patch 1: Missing Canonical
    if "Missing self-referencing canonical URL tag." in audit.get("critical_issues", []):
        patches.append({
            "target": "HTML <head>",
            "issue": "Missing Canonical Tag",
            "code_snippet": f'<link rel="canonical" href="{url}" />',
            "astro_snippet": f'<link rel="canonical" href={{Astro.url.href}} />'
        })

    # Patch 2: Missing Google Discover Tag
    patches.append({
        "target": "HTML <head>",
        "issue": "Google Discover & AI Search Preview",
        "code_snippet": '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />'
    })

    # Patch 3: 2026 Unified Schema.org @graph
    if "Zero JSON-LD structured data detected." in audit.get("critical_issues", []) or audit["metrics"]["schemas_detected"] == 0:
        schema_graph = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "@id": f"https://{domain}/#website",
                    "url": f"https://{domain}/",
                    "name": domain.title()
                },
                {
                    "@type": "TechArticle",
                    "@id": f"{url}#article",
                    "isPartOf": {"@id": f"https://{domain}/#website"},
                    "headline": page_name,
                    "description": f"Comprehensive guide and operational standard for {page_name}.",
                    "inLanguage": "en-US"
                },
                {
                    "@type": "BreadcrumbList",
                    "@id": f"{url}#breadcrumbs",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"https://{domain}/"},
                        {"@type": "ListItem", "position": 2, "name": page_name, "item": url}
                    ]
                }
            ]
        }
        patches.append({
            "target": "HTML <head> / Astro Layout",
            "issue": "Missing 2026 Structured Data Graph",
            "code_snippet": f'<script type="application/ld+json">\n{json.dumps(schema_graph, indent=2)}\n</script>'
        })

    return {
        "url": url,
        "health_score_before": audit["health_score"],
        "projected_health_score_after": min(100, audit["health_score"] + 28),
        "total_patches_generated": len(patches),
        "apply_mode": "review_only",
        "notice": APPLY_REFUSED,
        "patches": patches
    }

if __name__ == "__main__":
    if "--apply" in sys.argv:
        print(APPLY_REFUSED, file=sys.stderr)
        sys.exit(2)
    args = [a for a in sys.argv[1:] if a != "--apply"]
    if not args:
        print("Usage: python remediation_engine.py <url>")
        print(APPLY_REFUSED)
        sys.exit(1)
    target = args[0]
    res = generate_remediation_patches(target)
    print(json.dumps(res, indent=2))
