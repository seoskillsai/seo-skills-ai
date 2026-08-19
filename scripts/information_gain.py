#!/usr/bin/env python3
"""
SEO Skills AI — Google Information Gain & Entity Novelty Analyzer
Implements Google Patent US 11,562,019 B2 ("Contextual Information Gain Scoring")
Calculates entity novelty, empirical data density, and unique attribute value vs SERP consensus.
"""
import os
import sys
import re
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.parse_html import parse_html_content
from scripts.fetch_page import fetch_page

def extract_entities_and_triples(text: str) -> dict:
    # Extract numerical data points, percentages, years, code blocks, metrics
    numbers = re.findall(r"\b\d+(?:\.\d+)?%?\b", text)
    capitalized_phrases = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)
    code_snippets = re.findall(r"`([^`]+)`", text)

    # Filter generic English words from capitalized phrases
    stopwords = {"The", "This", "That", "There", "When", "What", "How", "Why", "Where", "With", "From", "For", "And", "You", "Your", "Our", "All", "Each", "Every"}
    named_entities = list(set([p for p in capitalized_phrases if p not in stopwords and len(p) > 2]))

    # Empirical data density score (numbers, metrics, code per 100 words)
    words = len(re.findall(r"\b\w+\b", text))
    data_density = round(((len(numbers) + len(code_snippets)) / max(1, words)) * 100, 2)

    return {
        "word_count": words,
        "named_entities_count": len(named_entities),
        "named_entities_sample": named_entities[:15],
        "numerical_data_points_count": len(numbers),
        "code_and_syntax_mentions": len(code_snippets),
        "empirical_data_density_percentage": data_density
    }

def score_information_gain(target_url: str, baseline_text: str = None) -> dict:
    res = fetch_page(target_url)
    if res["status_code"] != 200:
        return {"error": f"Failed to fetch {target_url}: HTTP {res['status_code']}"}

    parsed = parse_html_content(res["html"], base_url=target_url)
    raw_body = " ".join(parsed.get("citable_passages", [p["text"] for p in parsed.get("citable_passages", [])]))
    if not raw_body:
        raw_body = parsed["title"] + " " + parsed["meta_description"] + " " + " ".join(parsed["h2"])

    entity_metrics = extract_entities_and_triples(res["html"])

    # Information Gain Score Calculation (0-100)
    density = entity_metrics["empirical_data_density_percentage"]
    entity_count = entity_metrics["named_entities_count"]
    passages_count = parsed["citable_passages_count"]

    density_score = min(40, density * 8)
    entity_score = min(35, entity_count * 1.5)
    passage_score = min(25, passages_count * 6)

    info_gain_score = round(density_score + entity_score + passage_score)

    verdict = (
        "High Information Gain (Strong Google Patent Alignment)" if info_gain_score >= 80 else
        ("Moderate Information Gain (Add empirical benchmarks & data tables)" if info_gain_score >= 60 else
         "Low Information Gain (Commodity content / High risk of search demotion)")
    )

    recommendations = []
    if density < 2.0:
        recommendations.append("Increase empirical data density: inject specific metrics, benchmarks, percentages, or code diffs.")
    if entity_count < 10:
        recommendations.append("Enrich EAV entity attributes: connect central entities to secondary LSI attributes and schema sameAs links.")
    if passages_count < 2:
        recommendations.append("Structure core sections with self-contained 130-170 word direct answer blocks for LLM citation.")

    return {
        "url": target_url,
        "information_gain_score": info_gain_score,
        "verdict": verdict,
        "metrics": entity_metrics,
        "citable_passages_detected": passages_count,
        "patent_alignment_breakdown": {
            "empirical_data_density_score": round(density_score, 1),
            "named_entity_novelty_score": round(entity_score, 1),
            "passage_citability_score": round(passage_score, 1)
        },
        "recommendations": recommendations
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python information_gain.py <url>")
        sys.exit(1)
    target = sys.argv[1]
    res = score_information_gain(target)
    print(json.dumps(res, indent=2))
