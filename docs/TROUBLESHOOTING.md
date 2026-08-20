# Troubleshooting Guide: SEO Skills AI

Common environment scenarios and solutions.

---

## 1. Portability & Permission Issues

### Windows Console Character Encoding
- **Symptom:** `UnicodeEncodeError: 'charmap' codec can't encode character...`
- **Solution:** SEO Skills AI scripts automatically call `sys.stdout.reconfigure(encoding='utf-8')` and use clean ASCII badges `[PASS]`, `[FAIL]`, `[OK]`. Ensure Python 3.10+ is active.

---

## 2. SSRF Security Blocks

### Localhost / Cloud Metadata Warning
- **Symptom:** `Security Alert: Target host resolves to private/prohibited IP...`
- **Cause:** `scripts/url_safety.py` blocks loopback, private networks, link-local, and cloud metadata, and re-checks redirect targets. Playwright navigation uses the same policy.
- **Solution:** Audit public `http`/`https` URLs only. Optional allowlist: `SEOSKILLS_ALLOWED_HOSTS`. Generated files stay under `SEOSKILLS_OUT_DIR` (default: the working directory).

---

## 3. Playwright Rendering Nuances

### Single Page Applications (Next.js / Astro / Vue)
- If pages require client-side hydration, use `scripts/capture_screenshot.py` or run `npx playwright install chromium` to enable headless rendering.
