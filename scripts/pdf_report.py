#!/usr/bin/env python3
"""
SEO Skills AI — Enterprise Executive HTML/PDF Audit Report Generator
"""
import sys
import json
import os
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.path_safety import prepare_output_file

def generate_html_report(audit_data: dict, output_path: str = "audit_report.html") -> str:
    url = audit_data.get("url", "https://example.com")
    health_score = audit_data.get("health_score", 85)
    now_str = datetime.datetime.now().strftime("%B %d, %Y")
    
    score_color = "#10B981" if health_score >= 85 else ("#F59E0B" if health_score >= 70 else "#EF4444")
    
    metrics = audit_data.get("metrics", {})
    critical_issues = [i for i in audit_data.get("critical_issues", []) if i]
    action_plan = audit_data.get("action_plan", [])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Enterprise AI SEO Audit Report — {url}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0A0D12; color: #F3F4F6; margin: 0; padding: 40px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: #111827; border: 1px solid #374151; border-radius: 12px; padding: 32px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #374151; padding-bottom: 24px; margin-bottom: 32px; }}
        .brand {{ font-size: 20px; font-weight: 800; color: #00E5FF; letter-spacing: -0.5px; }}
        .score-box {{ text-align: center; background: #1F2937; border-radius: 12px; padding: 24px; border: 2px solid {score_color}; }}
        .score-num {{ font-size: 56px; font-weight: 900; color: {score_color}; line-height: 1; }}
        .score-label {{ font-size: 13px; text-transform: uppercase; color: #9CA3AF; letter-spacing: 1px; margin-top: 8px; }}
        .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 24px 0; }}
        .metric-card {{ background: #1F2937; padding: 16px; border-radius: 8px; border: 1px solid #374151; }}
        .metric-val {{ font-size: 22px; font-weight: 700; color: #F9FAFB; }}
        .metric-lbl {{ font-size: 12px; color: #9CA3AF; margin-top: 4px; }}
        .section-title {{ font-size: 18px; font-weight: 700; margin-top: 32px; margin-bottom: 16px; color: #00E5FF; border-left: 4px solid #00E5FF; padding-left: 12px; }}
        .issue-item {{ background: rgba(239, 68, 68, 0.1); border-left: 4px solid #EF4444; padding: 12px 16px; margin-bottom: 8px; border-radius: 4px; font-size: 14px; }}
        .action-item {{ background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; padding: 12px 16px; margin-bottom: 8px; border-radius: 4px; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <div class="brand">SEO SKILLS AI — AUDIT REPORT</div>
                <div style="color: #9CA3AF; font-size: 14px; margin-top: 4px;">Target: <strong>{url}</strong> | Date: {now_str}</div>
            </div>
            <div class="score-box">
                <div class="score-num">{health_score}</div>
                <div class="score-label">Health Score</div>
            </div>
        </div>

        <div class="grid">
            <div class="metric-card">
                <div class="metric-val">{metrics.get('word_count', 0)}</div>
                <div class="metric-lbl">Total Word Count</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{metrics.get('latency_ms', 0)} ms</div>
                <div class="metric-lbl">Server Latency / TTFB</div>
            </div>
            <div class="metric-card">
                <div class="metric-val">{metrics.get('schemas_detected', 0)}</div>
                <div class="metric-lbl">JSON-LD Schemas Detected</div>
            </div>
        </div>

        <div class="section-title">Critical Technical & Indexation Blockers</div>
        {"".join([f'<div class="issue-item">🚨 {i}</div>' for i in critical_issues]) if critical_issues else '<div style="color: #10B981;">✔ Zero critical blockers detected!</div>'}

        <div class="section-title">Prioritized Strategic Action Plan</div>
        {"".join([f'<div class="action-item">✔ {a}</div>' for a in action_plan])}
    </div>
</body>
</html>"""
    
    dest = prepare_output_file(output_path)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    return str(dest)

if __name__ == "__main__":
    sample_audit = {
        "url": "https://seoskillsai.com",
        "health_score": 96,
        "metrics": {"word_count": 1950, "latency_ms": 110, "schemas_detected": 4},
        "critical_issues": [],
        "action_plan": [
            "Maintain current 2026 Schema.org @graph configuration.",
            "Verify weekly IndexNow pings upon publishing new skill pages.",
            "Monitor AI citation visibility across Perplexity and ChatGPT Search."
        ]
    }
    out = generate_html_report(sample_audit, "audit_report.html")
    print(f"[SUCCESS] Generated executive HTML audit report at {out}")
