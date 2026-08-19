import csv
import os
import sys
from collections import Counter

csv_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "data", "keywords.csv")

keywords = []
if os.path.exists(csv_path):
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for r in reader:
            keywords.append(r)
else:
    print(f"Notice: CSV file not found at {csv_path}. Provide path as argument: python analyze_keywords.py <file.csv>")
    sys.exit(0)

print(f"Total Keywords: {len(keywords)}")

def parse_vol(v):
    v = v.replace(",", "").strip()
    if v.endswith("K"):
        return int(float(v[:-1]) * 1000)
    try:
        return int(v)
    except Exception:
        return 0

by_vol = sorted(keywords, key=lambda x: parse_vol(x.get("Volume", "0")), reverse=True)

print("\n--- TOP 35 KEYWORDS BY SEARCH VOLUME ---")
for k in by_vol[:35]:
    vol = parse_vol(k.get("Volume", "0"))
    print(f"{k.get('Keyword',''):<45} | Vol: {vol:<6} | Pos: {k.get('Position',''):<4} | Traffic: {k.get('Traffic',''):<5} | Intent: {k.get('Intent','')}")

# Group by theme/cluster
clusters = {
    "Claude / Copilot / Agent AI SEO": [],
    "SEO Skills / Core Discipline": [],
    "GitHub SEO / Code SEO": [],
    "SEO Audit & Reporting Tools": [],
    "Backlinks / Moz / Ahrefs / Bing": [],
    "Local SEO / Maps / Citations": [],
    "AEO / GEO / AI Search / Semantics": [],
    "Templates / Excel / Plans": []
}

for k in keywords:
    kw = k.get("Keyword", "").lower()
    if "claude" in kw or "copilot" in kw or "chatgpt" in kw or "agent" in kw:
        clusters["Claude / Copilot / Agent AI SEO"].append(k)
    elif "skill" in kw or "seo skills" in kw:
        clusters["SEO Skills / Core Discipline"].append(k)
    elif "github" in kw or "code" in kw:
        clusters["GitHub SEO / Code SEO"].append(k)
    elif "audit" in kw or "checker" in kw or "analysis" in kw or "software" in kw or "tool" in kw:
        clusters["SEO Audit & Reporting Tools"].append(k)
    elif "backlink" in kw or "moz" in kw or "ahrefs" in kw or "bing" in kw or "semrush" in kw:
        clusters["Backlinks / Moz / Ahrefs / Bing"].append(k)
    elif "local" in kw or "map" in kw or "citation" in kw or "doorway" in kw:
        clusters["Local SEO / Maps / Citations"].append(k)
    elif "aeo" in kw or "geo" in kw or "semantic" in kw or "cannibalization" in kw:
        clusters["AEO / GEO / AI Search / Semantics"].append(k)
    elif "template" in kw or "excel" in kw or "plan" in kw or "guide" in kw:
        clusters["Templates / Excel / Plans"].append(k)

print("\n--- KEYWORD CLUSTER DISTRIBUTION ---")
for cname, items in clusters.items():
    print(f"{cname:<40} : {len(items)} keywords")
