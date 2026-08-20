# Contributing to SEO Skills AI

Thank you for your interest in contributing to the **SEO Skills AI** open standard!

---

## 🛠️ Contribution Principles

1. **Strict Harness Portability:**
   - All skills must implement the open Agent Skills specification and run seamlessly across Antigravity, Claude Code, Cursor, Windsurf, Codex, Cline, and Aider.
2. **Zero-Dependency Python Execution:**
   - Scripts in `scripts/` must run using Python's standard library (or provide deterministic fallbacks when optional packages are not installed).
3. **Primary-Source Grounding:**
   - Every diagnostic check or recommendation must reference primary evidence (W3C standards, Google Search Essentials, Chromium CrUX, or Schema.org).

---

## 🧪 Testing Your Contributions

Before submitting a Pull Request, run:
```bash
python scripts/portability_check.py
python scripts/doctor.py
python tests/run_all_tests.py
python -m pytest tests -q
```
All test suites must pass. Catalog listing also requires the HOL plugin-scanner workflow (`.github/workflows/plugin-scan.yml`) to stay green: score ≥ 80/142 and no high/critical findings.
