#!/usr/bin/env python3
"""
SEO Skills AI — SERP Overlap Keyword Clustering Algorithm
"""
import sys
import json

def cluster_keywords(keyword_serp_map: dict) -> list:
    """
    Groups keywords by URL overlap:
    - >= 4 overlapping URLs in top 10 -> same cluster (single page)
    - 1-3 overlapping URLs -> sibling cluster (separate pages with cross-links)
    """
    clusters = []
    processed = set()
    keywords = list(keyword_serp_map.keys())

    for i, kw1 in enumerate(keywords):
        if kw1 in processed:
            continue
        urls1 = set(keyword_serp_map[kw1])
        current_cluster = [kw1]
        processed.add(kw1)

        for kw2 in keywords[i+1:]:
            if kw2 in processed:
                continue
            urls2 = set(keyword_serp_map[kw2])
            overlap = len(urls1.intersection(urls2))
            if overlap >= 4:
                current_cluster.append(kw2)
                processed.add(kw2)

        clusters.append({
            "primary_keyword": current_cluster[0],
            "synonyms": current_cluster[1:],
            "cluster_size": len(current_cluster),
            "recommendation": "Single comprehensive pillar page" if len(current_cluster) > 1 else "Standalone cluster node"
        })

    return clusters

if __name__ == "__main__":
    sample_data = {
        "seo audit": ["https://sitea.com", "https://siteb.com", "https://sitec.com", "https://sited.com"],
        "free seo audit": ["https://sitea.com", "https://siteb.com", "https://sitec.com", "https://sited.com"],
        "local seo audit": ["https://sitee.com", "https://sitef.com"]
    }
    res = cluster_keywords(sample_data)
    print(json.dumps(res, indent=2))
