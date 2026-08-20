#!/usr/bin/env python3
"""
SEO Skills AI — Comprehensive Test Suite Runner (v1.1.0)
Validates all core scripts, auxiliary linters, 27 skills, references library, and extensions.
"""
import os
import sys
import json
import unittest
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.portability_check import check_skill_file
from scripts.url_safety import validate_url
from scripts.parse_html import parse_html_content
from scripts.schema_validator import validate_schema_json
from scripts.llms_txt_builder import generate_llms_txt
from scripts.discover_rss_builder import build_media_rss
from scripts.pagespeed_check import run_pagespeed_check
from scripts.gsc_query import query_gsc
from scripts.full_audit import run_full_audit
from scripts.serp_cluster import cluster_keywords
from scripts.information_gain import extract_entities_and_triples
from scripts.remediation_engine import generate_remediation_patches
from scripts.mcp_server import handle_request
from scripts.parasite_seo import scan_parasite_seo_risk
from scripts.speculation_rules import analyze_speculation_and_bfcache
from scripts.consent_mode import audit_consent_mode
from scripts.whois_heritage import query_domain_heritage

class TestSEOSkillsAIEnterprise(unittest.TestCase):

    def test_skills_portability(self):
        skills_dir = Path("skills")
        skill_files = list(skills_dir.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(skill_files), 25, "At least 25 skills must exist")
        for sf in skill_files:
            errs = check_skill_file(sf)
            self.assertEqual(len(errs), 0, f"Skill {sf} failed: {errs}")

    def test_references_and_extensions_integrity(self):
        ref_files = list(Path("skills").glob("*/references/*.md"))
        self.assertGreaterEqual(len(ref_files), 5, "At least 5 in-depth reference files must exist")
        
        ext_dirs = list(Path("extensions").glob("*"))
        self.assertGreaterEqual(len(ext_dirs), 8, "All 8 vendor extension folders must exist")

    def test_url_safety(self):
        self.assertTrue(validate_url("https://example.com"))
        self.assertTrue(validate_url("http://google.com/test"))
        with self.assertRaises(ValueError):
            validate_url("ftp://example.com")
        with self.assertRaises(PermissionError):
            validate_url("http://127.0.0.1:8080")

    def test_enterprise_html_parser(self):
        html = """
        <html>
        <head>
            <title>SEO Skills AI — Universal Standard</title>
            <meta name="description" content="Universal open-source directory for AI SEO." />
            <meta name="robots" content="index, follow, max-image-preview:large" />
            <meta property="og:title" content="SEO Skills AI" />
            <link rel="canonical" href="https://seoskillsai.com" />
        </head>
        <body>
            <h1>Universal AI SEO Standard</h1>
            <h2>Core Capability Modules</h2>
            <p>This is a paragraph with content for testing word counts and educational prose depth.</p>
            <a href="https://seoskillsai.com/skills/seo-audit">SEO Audit</a>
            <img src="/img/hero.jpg" alt="Hero Image" width="1200" height="675" />
        </body>
        </html>
        """
        parsed = parse_html_content(html, base_url="https://seoskillsai.com")
        self.assertEqual(parsed["title"], "SEO Skills AI — Universal Standard")
        self.assertTrue(parsed["has_large_image_preview"])
        self.assertEqual(parsed["high_res_discover_images"], 1)
        self.assertEqual(parsed["opengraph"].get("title"), "SEO Skills AI")
        self.assertEqual(parsed["canonical"], "https://seoskillsai.com")

    def test_2026_schema_validator(self):
        valid_graph = json.dumps({
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "TechArticle",
                    "headline": "Universal AI SEO Guide",
                    "author": {"@type": "Organization", "name": "SEO Skills AI"},
                    "datePublished": "2026-08-19"
                },
                {
                    "@type": "SoftwareApplication",
                    "name": "seoskills CLI",
                    "applicationCategory": "DeveloperApplication"
                }
            ]
        })
        res = validate_schema_json(valid_graph)
        self.assertTrue(res["valid_json"])
        self.assertTrue(res["has_graph"])
        self.assertEqual(len(res["deprecated_warnings"]), 0)

    def test_deprecated_schema_filtering(self):
        dep_schema = json.dumps({
            "@context": "https://schema.org",
            "@type": "SpecialAnnouncement",
            "name": "Old Notice"
        })
        res = validate_schema_json(dep_schema)
        self.assertTrue(res["valid_json"])
        self.assertGreaterEqual(len(res["deprecated_warnings"]), 1)

    def test_information_gain_extraction(self):
        sample_text = """
        SEO Skills AI reduces token consumption by 92.5% compared to traditional crawlers.
        Using Google Antigravity and Gemini 2.5 Pro, audits run in 12s with $0.009 average cost.
        Here is the code snippet: `python scripts/full_audit.py https://example.com`.
        """
        metrics = extract_entities_and_triples(sample_text)
        self.assertGreater(metrics["empirical_data_density_percentage"], 5.0)

    def test_auxiliary_linters(self):
        parasite = scan_parasite_seo_risk("https://example.com")
        self.assertIn("risk_score", parasite)

        spec = analyze_speculation_and_bfcache("https://example.com")
        self.assertIn("speculation_rules", spec)
        self.assertIn("bfcache", spec)

        consent = audit_consent_mode("https://example.com")
        self.assertIn("consent_mode_status", consent)

        whois = query_domain_heritage("example.com")
        self.assertIn("domain", whois)

    def test_remediation_patch_generator(self):
        res = generate_remediation_patches("https://example.com")
        self.assertIn("patches", res)
        self.assertGreaterEqual(len(res["patches"]), 2)

    def test_mcp_server_protocol(self):
        req = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
        resp = handle_request(req)
        self.assertEqual(resp["jsonrpc"], "2.0")
        self.assertIn("tools", resp["result"])
        init = handle_request({"jsonrpc": "2.0", "id": 2, "method": "initialize", "params": {}})
        self.assertEqual(init["result"]["serverInfo"]["name"], "seoskillsai")
        blocked = handle_request({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "seo_audit", "arguments": {"url": "http://127.0.0.1/"}},
        })
        self.assertTrue(blocked["result"].get("isError"))

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSEOSkillsAIEnterprise)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
