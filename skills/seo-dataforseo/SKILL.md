---
name: seo-dataforseo
description: "DataForSEO live SERP, search volume, backlink, and keyword ranking API connector. Provides enterprise-grade live SERP data without manual browser scraping."
license: MIT
metadata:
  author: SEO Skills AI
  version: "1.2.0"
---

# DataForSEO Live SERP & Keyword Data Connector

Set `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` in the environment. `python scripts/dataforseo_api.py "<keyword>"` calls the live SERP endpoint. Missing credentials return `UNAVAILABLE` (no sample rows).

This is first-party HTTP in this repo. Ahrefs / SE Ranking / Profound remain third-party MCP servers you install separately.


---

## 🛠️ CLI Commands

```bash
# Fetch live Google SERP for target keyword
python scripts/dataforseo_api.py --query "ai seo tools" --location "United States"

# Pull live backlink summary
python scripts/dataforseo_api.py --domain "example.com" --action "backlinks"
```
