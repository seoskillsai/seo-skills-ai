---
name: seo-audit
description: "Parallel multi-agent full site audit. Spawns up to 15 specialist agents to inspect technical health, Topical Semantic semantic content, 2026 schema, GEO citability, and backlinks."
---

# Parallel Full-Site SEO Audit Standard

Execute an end-to-end site audit by orchestrating specialist subagents in parallel.

## 🚀 Execution Workflow

1. **Safety & SSRF Verification:**
   ```bash
   python scripts/url_safety.py --url "$TARGET_URL"
   ```
2. **Parallel Agent Dispatch:**
   - **Technical Agent:** Crawlability, indexability, security headers, Core Web Vitals.
   - **Content Agent:** Topical E-E-A-T, EAV modeling, centerpiece viewport test.
   - **Schema Agent:** Validate JSON-LD against 2026 Schema.org standards (zero deprecated types).
   - **GEO / AI Search Agent:** Test passage citability, `llms.txt`, and AI crawler access.
   - **Backlink Agent:** Fetch domain link equity via Common Crawl, Moz, and Bing APIs.
   - **SXO Agent:** Inspect centerpiece fold (<350px) and click-input-click loops.
3. **Synthesis & Prioritized Output:**
   - Generate Executive Scorecard (0–100 Health Score).
   - List Critical Blockers (P0: Indexation/Security).
   - List High-Impact Growth Tasks (P1: EAV content depth, schema graphs, llms.txt).
   - List Quick Wins (P2: Meta tags, alt text, internal link conduits).
