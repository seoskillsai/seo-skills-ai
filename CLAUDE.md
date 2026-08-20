# Claude SEO: SEO Skills AI Orchestration Configuration

This repository contains **SEO Skills AI**, a Tier 4 autonomous agent skill suite for Claude Code and all agent harnesses. It implements the open **Agent Skills specification** with a 3-layer architecture:
1. **Directive Layer:** `skills/*/SKILL.md` (Operational definitions and workflows).
2. **Orchestration Layer:** `skills/seo/SKILL.md` and `agents/*.md` (Parallel subagent coordination).
3. **Execution Layer:** `scripts/*.py` (Deterministic Python runtime tools).

---

## 1. Fast Setup & Diagnostics

Run once upon installation:
```bash
/seo setup
/seo doctor
```

`/seo setup` initializes the local SQLite drift database under `~/.config/seoskillsai/`. Playwright Chromium is installed by `install.sh` / `install.ps1`, not by `/seo setup`. Check readiness with `/seo doctor`.

---

## 2. Parallel Delegation Pattern

When the user invokes `/seo audit <url>`, dispatch up to 15 specialist subagents in parallel:

- `agents/seo-technical.md` -> Crawlability, indexability, security, Core Web Vitals (INP/LCP/CLS).
- `agents/seo-content.md` -> Topical E-E-A-T, EAV modeling, anti-thin prose.
- `agents/seo-schema.md` -> 2026 JSON-LD graph validation.
- `agents/seo-geo.md` -> AI search citability (Perplexity, ChatGPT, AI Overviews).
- `agents/seo-llms-txt.md` -> llms.txt and llms-full.txt structure.
- `agents/seo-discover.md` -> Google Discover, Media RSS, and AI disclosure bylines.
- `agents/seo-sitemap.md` -> Twin XML and dynamic HTML sitemap architecture.
- `agents/seo-sxo.md` -> Dwell-time retention moats and centerpiece fold annotation.
- `agents/seo-drift.md` -> SQLite on-page baseline tracking.
- `agents/seo-backlinks.md` -> Common Crawl, Moz, and Bing link equity.

Collect all agent findings, score using the weighted heuristic triage formula, and output a prioritized, testable action plan.
