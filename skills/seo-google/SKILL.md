---
name: seo-google
description: "4-tier Google API automation: PageSpeed Insights, CrUX 25-week history, Google Search Console query mining, URL Inspection, Google Indexing API, and GA4 traffic reports."
---

# Google SEO APIs & Real User Metrics

Automates Google search and performance APIs with a 4-tier progressive credential system.

---

## 🔑 Progressive 4-Tier Credential System

| Tier | Required Key | Unlocked Capabilities |
| :--- | :--- | :--- |
| **Tier 0 (Free/Public)** | None / Public PSI Key | PageSpeed Insights v5, CrUX 25-week performance history, Lighthouse lab tests. |
| **Tier 1 (Search Console)** | Service Account / OAuth | GSC query performance, striking-distance keyword mining (pos 8–20), URL inspection API, Indexing API v3. |
| **Tier 2 (Analytics)** | GA4 Property ID | Organic traffic trends, top landing pages, country/device breakdown. |
| **Tier 3 (Ads Planner)** | Ads Developer Token | Keyword Planner exact search volume and competition data. |

---

## 🛠️ CLI Execution Commands

```bash
# Setup Google Credentials Wizard
python scripts/google_auth.py --setup

# Query Striking Distance Keywords from GSC
python scripts/gsc_query.py --site "https://example.com" --filter "striking-distance"

# Fetch CrUX 25-Week Performance History
python scripts/crux_history.py --url "https://example.com"

# Submit Batch URLs to Google Indexing API
python scripts/indexing_notify.py --urls "public/sitemap-index.xml"
```
