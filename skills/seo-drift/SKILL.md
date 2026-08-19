---
name: seo-drift
description: "SEO drift monitoring with local SQLite snapshots. Tracks on-page title, schema, heading, and content changes across deployments with 17 comparison rules."
---

# SEO Drift Monitoring with SQLite Baselines

Tracks subtle code regressions, accidental metadata deletions, and content drift across production deployments.

---

## 🗄️ CLI Commands

```bash
# Capture new baseline snapshot in local SQLite database
python scripts/drift_baseline.py --url "https://example.com"

# Compare live site against latest baseline
python scripts/drift_compare.py --url "https://example.com"

# View drift change history
python scripts/drift_history.py --url "https://example.com"
```

## ⚖️ The 17 Drift Comparison Rules (3 Severity Levels)

- **P0 (Critical / Blocker):**
  1. Title tag missing or changed >50%
  2. Meta robots changed to `noindex` or `nofollow`
  3. Canonical tag modified or removed
  4. H1 tag deleted or altered
  5. JSON-LD schema syntax invalid or removed

- **P1 (High):**
  6. Word count decreased by >20%
  7. Key H2/H3 headings removed
  8. Primary internal link conduits broken
  9. `robots.txt` AI crawler permissions changed
  10. `llms.txt` feed missing or modified

- **P2 (Medium / Informational):**
  11. Meta description updated
  12. Image alt text modified
  13. OpenGraph tags changed
  14. Secondary schema properties adjusted
  15. HTML size variance >30%
  16. Minor CSS class changes on centerpiece fold
  17. Outbound external links modified
