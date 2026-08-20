---
name: seo-backlinks
description: "Free backlink profile audit using Common Crawl web graphs, Moz Link Explorer API, and Bing Webmaster Tools without expensive SaaS subscriptions."
license: MIT
metadata:
  author: SEO Skills AI
  version: "1.2.0"
---

# Free Backlink Profile & Authority Auditor

Analyzes external link equity, referring domains, toxic link patterns, and competitor link gaps using open and free API datasets.

---

## 🔗 Supported Free & Open Data Sources

1. **Common Crawl Web Graph:**
   - Free global web graph dataset providing PageRank estimates, in-degree link counts, and referring domains.
2. **Moz Link Explorer API (Free Tier):**
   - Domain Authority (DA), Page Authority (PA), spam score, and top anchor text distributions.
3. **Bing Webmaster Tools API:**
   - Inbound link metrics and competitive domain comparison.
4. **Live Link Verification Crawler:**
   - Directly crawls referring URLs to verify `rel="nofollow"`, `rel="ugc"`, anchor text, and indexation status.

---

## 🛠️ CLI Execution
```bash
python scripts/commoncrawl_graph.py --domain "example.com"
python scripts/verify_backlinks.py --domain "example.com"
```
