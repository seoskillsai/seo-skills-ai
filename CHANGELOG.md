# Changelog: SEO Skills AI

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-08-19

### Added
- **Multi-Page Recursive Crawler (`scripts/site_crawler.py`):** Traverses full domains, builds internal PageRank link graphs, and flags 3x anchor text diversity violations sitewide.
- **Google Information Gain Patent Engine (`scripts/information_gain.py`):** Analyzes US Patent 11,562,019 B2 for empirical data density and entity novelty.
- **Automated Code Remediation Generator (`scripts/remediation_engine.py`):** Produces 1-click drop-in Astro and HTML code patches.
- **Google Discover & Media RSS XML Feeds (`scripts/discover_rss_builder.py`):** `<media:content>` 1200px 16:9 images and AI Byline disclosures.
- **8 Modular MCP Extension Adapters (`extensions/*`):** DataForSEO, Firecrawl, Ahrefs, SE Ranking, Profound, Bing Webmaster, Unlighthouse, and Banana.
- **Auxiliary Diagnostics:** Site Reputation Abuse (`parasite_seo.py`), Speculation Rules & bfcache (`speculation_rules.py`), Consent Mode v2 (`consent_mode.py`), and Domain Heritage (`whois_heritage.py`).
- **Comprehensive Reference Knowledge Library:** Added in-depth reference manuals in `skills/*/references/`.

---

## [1.0.0] - 2026-08-19

### Added
- Initial Universal Open-Source Release across 12 AI agent harnesses.
- 27 Standardized Agent Skills (`skills/*/SKILL.md`).
- 18 Specialist Subagent Definitions (`agents/*.md`).
- Deterministic SQLite Drift Monitoring (`scripts/drift_*.py`).
- Universal Tool Mapping in `AGENTS.md` and CLI Launcher `@seoskillsai/cli`.
