---
name: seo-cluster
description: "SERP-based semantic keyword and topic clustering. Groups search terms by SERP URL overlap percentage to eliminate keyword cannibalization."
license: MIT
metadata:
  author: SEO Skills AI
  version: "1.2.0"
---

# SERP-Based Semantic Keyword Clustering

Clusters keyword lists into distinct topic silos based on real-world SERP URL overlap to prevent keyword cannibalization.

---

## 🎯 Overlap Heuristic Rules

- **$\ge$ 4 Shared URLs in Top 10 SERPs:** Combine into a **single comprehensive article** (identical search intent).
- **1–3 Shared URLs in Top 10 SERPs:** Create **separate child articles** with directional cross-links.
- **0 Shared URLs:** Distinct search intent; assign to separate topical silos.

## 🛠️ CLI Execution
```bash
python scripts/serp_cluster.py --keywords "keywords.csv" --output "clusters.json"
```
