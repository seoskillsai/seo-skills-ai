# Migration Guide: v1.0.0 to v1.1.0

Summary of new architectural features, upgraded scripts, and backward-compatible changes.

---

## 🚀 Key Upgrades in v1.1.0

1. **Multi-Page Recursive Crawler:** Introduced `scripts/site_crawler.py` to map internal link graphs, orphan pages, and 3x Anchor Diversity Rule anchor text violations sitewide.
2. **Google Information Gain Patent Engine:** Introduced `scripts/information_gain.py` implementing US Patent 11,562,019 B2.
3. **Automated Remediation Generator:** Introduced `scripts/remediation_engine.py` producing instant drop-in HTML/Astro code patches and Git diffs.
4. **8 MCP Extension Wrappers:** Introduced modular `extensions/` directory with dedicated adapters for Ahrefs, SE Ranking, Firecrawl, Profound, Bing Webmaster, Unlighthouse, and Banana.
5. **Auxiliary Security & Web Standards Linters:** Added Site Reputation Abuse scanner (`parasite_seo.py`), Speculation Rules & bfcache (`speculation_rules.py`), and Consent Mode v2 (`consent_mode.py`).
