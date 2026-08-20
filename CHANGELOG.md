# Changelog: SEO Skills AI

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0] - 2026-08-20

### Security
- Codex/Claude marketplace and plugin metadata for HOL plugin-scanner (skills path, author object, `.mcp.json`, `.codexignore`, lockfiles, SKILL.md `license` + metadata).
- PreToolUse hooks for fetch URL policy and write path policy (stdin JSON, no `{file}` interpolation).
- `fetch_page.py` re-resolves the final hostname after connect (DNS rebinding TOCTOU).
- Playwright: `should_abort_request` for private-IP subresources; document `SEOSKILLS_STRICT_BROWSER=1`.

### Added
- Real Google Search Console Search Analytics and GA4 Data API organic sessions via `~/.config/seoskillsai/gsc_ga4.json` (`scripts/google_installed_app.py`).
- First-party HTTP for DataForSEO, Firecrawl scrape, and Bing Webmaster metrics.
- Packaged `@seoskillsai/cli` that copies skills/scripts from the npm tarball.
- Live `https://example.com` audit smoke in CI.
- `CODE_OF_CONDUCT.md` and GitHub issue templates.

### Fixed
- GSC and GA4 no longer invent clicks, impressions, or sessions when OAuth is missing (`UNAVAILABLE` only).
- One FAQPage rule: do not emit commercial `FAQPage` JSON-LD in every `@graph`.
- Extensions: first-party Python vs third-party MCP labeled honestly.
- `config/openapi-schema.json` no longer implies a live `api.seoskillsai.com`.

---

## [1.1.1] - 2026-08-20

### Security
- Network-target policy: fail-closed DNS, redirect re-validation, optional `SEOSKILLS_ALLOWED_HOSTS`, Playwright navigation/subresource checks.
- Filesystem scope: generated files must stay under `SEOSKILLS_OUT_DIR` / cwd.
- Remediation engine is review-only (no `--apply`, no repo writes).
- MCP: `initialize` handshake, URL policy on fetch tools, no shipped `autoApprove`.
- HOL `plugin-scanner` GitHub Action (score ≥ 80, fail on high) plus Dependabot and SHA-pinned CI actions.

### Fixed
- Repository URLs now point at `seoskillsai/seo-skills-ai`.
- Honest install docs (clone the repo; npm CLI is not published).
- PageSpeed, IndexNow, Moz, Bing, Common Crawl, and DataForSEO stubs no longer invent success metrics.

---

## [1.1.0] - 2026-08-19

### Added
- **Multi-Page Recursive Crawler (`scripts/site_crawler.py`):** Traverses full domains, builds internal PageRank link graphs, and flags 3x anchor text diversity violations sitewide.
- **Google Information Gain Patent Engine (`scripts/information_gain.py`):** Analyzes US Patent 11,562,019 B2 for empirical data density and entity novelty.
- **Automated Code Remediation Generator (`scripts/remediation_engine.py`):** Prints HTML/Astro snippets for review (does not write the repo).
- **Google Discover & Media RSS XML Feeds (`scripts/discover_rss_builder.py`):** `<media:content>` 1200px 16:9 images and AI Byline disclosures.
- Vendor extension folders (`extensions/*`): first-party DataForSEO/Bing scripts plus third-party MCP pointers (Ahrefs, SE Ranking, Profound, Unlighthouse, Banana).
- **Auxiliary Diagnostics:** Site Reputation Abuse (`parasite_seo.py`), Speculation Rules & bfcache (`speculation_rules.py`), Consent Mode v2 (`consent_mode.py`), and Domain Heritage (`whois_heritage.py`).
- **Comprehensive Reference Knowledge Library:** Added in-depth reference manuals in `skills/*/references/`.

---

## [1.0.0] - 2026-08-19

### Added
- Initial Universal Open-Source Release across 12 AI agent harnesses.
- 27 Standardized Agent Skills (`skills/*/SKILL.md`).
- 18 Specialist Subagent Definitions (`agents/*.md`).
- Deterministic SQLite Drift Monitoring (`scripts/drift_*.py`).
- Universal Tool Mapping in `AGENTS.md` and CLI launcher.
