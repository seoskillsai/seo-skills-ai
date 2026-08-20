#!/usr/bin/env python3
"""
SEO Skills AI — Multi-Agent Portability & SKILL.md Spec Checker
Validates that all SKILL.md files conform to the open Agent Skills standard.
"""
import os
import re
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SKILLS_DIR = Path("skills")

def check_skill_file(skill_path: Path) -> list:
    errors = []
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Frontmatter regex
    fm_match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", content)
    if not fm_match:
        errors.append("Missing YAML frontmatter delimiters (---)")
        return errors

    fm_text = fm_match.group(1)
    if not re.search(r"^name:\s*[\w-]+", fm_text, re.MULTILINE):
        errors.append("Frontmatter missing valid 'name:' field")
    if not re.search(r"^description:\s*", fm_text, re.MULTILINE):
        errors.append("Frontmatter missing 'description:' field")
    if not re.search(r"^license:\s*MIT\s*$", fm_text, re.MULTILINE):
        errors.append("Frontmatter missing 'license: MIT'")

    return errors

def run_portability_checks():
    if not SKILLS_DIR.exists():
        print(f"ERROR: {SKILLS_DIR} not found.")
        sys.exit(1)

    skill_files = list(SKILLS_DIR.glob("*/SKILL.md"))
    total_skills = len(skill_files)
    failed = 0

    print(f"==> Checking portability across {total_skills} agent skills...")
    for sf in skill_files:
        errs = check_skill_file(sf)
        if errs:
            print(f"  [FAIL] {sf}: {', '.join(errs)}")
            failed += 1
        else:
            print(f"  [PASS] {sf.parent.name} (Valid)")

    if failed == 0:
        print(f"\n[SUCCESS] 100% Portability Passed! All {total_skills} skills conform to the Agent Skills Open Spec.")
        return 0
    else:
        print(f"\n[FAILED] {failed} skills failed portability validation.")
        return 1

if __name__ == "__main__":
    sys.exit(run_portability_checks())
