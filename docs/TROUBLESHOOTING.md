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
- **Solution:** `scripts/url_safety.py` protects against SSRF by blocking loopback (`127.0.0.0/8`), private networks (`10.0.0.0/8`, `192.168.0.0/16`), and AWS metadata (`169.254.169.254`). Audits must target public HTTP/HTTPS URLs.

---

## 3. Playwright Rendering Nuances

### Single Page Applications (Next.js / Astro / Vue)
- If pages require client-side hydration, use `scripts/capture_screenshot.py` or run `npx playwright install chromium` to enable headless rendering.
