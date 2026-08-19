#!/usr/bin/env python3
"""
SEO Skills AI — Automated llms.txt and llms-full.txt Generator
Extracts page hierarchies and outputs standard llmstxt.org markdown specifications.
"""
import os
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

def generate_llms_txt(site_name: str, site_url: str, sitemap_path: str = None, output_dir: str = "public") -> dict:
    os.makedirs(output_dir, exist_ok=True)
    urls = []

    if sitemap_path and os.path.exists(sitemap_path):
        try:
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            for elem in root.iter():
                if elem.tag.endswith("loc") and elem.text:
                    urls.append(elem.text.strip())
        except Exception as e:
            print(f"Warning: Failed to parse sitemap XML: {e}", file=sys.stderr)

    if not urls:
        urls = [
            f"{site_url}/",
            f"{site_url}/skills",
            f"{site_url}/skills/seo-audit",
            f"{site_url}/skills/seo-schema",
            f"{site_url}/skills/seo-content",
            f"{site_url}/skills/seo-llms-txt"
        ]

    # Generate llms.txt
    llms_txt = f"""# {site_name}

> Universal open-source directory and package manager for AI SEO skills across Claude, Antigravity, ChatGPT, Cursor, Windsurf, and DeepSeek.

## Core Documentation & Tools

"""
    for u in urls:
        path = urlparse(u).path.strip("/") or "home"
        name = path.replace("-", " ").replace("/", " > ").title()
        llms_txt += f"- [{name}]({u})\n"

    llms_path = os.path.join(output_dir, "llms.txt")
    with open(llms_path, "w", encoding="utf-8") as f:
        f.write(llms_txt)

    # Generate llms-full.txt
    llms_full_path = os.path.join(output_dir, "llms-full.txt")
    with open(llms_full_path, "w", encoding="utf-8") as f:
        f.write(llms_txt + "\n## Complete Technical Specification\n\nAll skills implement the open Agent Skills spec.\n")

    return {
        "llms_txt": llms_path,
        "llms_full_txt": llms_full_path,
        "total_urls_indexed": len(urls)
    }

if __name__ == "__main__":
    res = generate_llms_txt("SEO Skills AI", "https://seoskillsai.com", "public/sitemap-index.xml")
    print(f"[SUCCESS] Generated {res['llms_txt']} and {res['llms_full_txt']} ({res['total_urls_indexed']} URLs)")
