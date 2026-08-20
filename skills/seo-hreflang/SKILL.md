---
name: seo-hreflang
description: "International SEO, multi-regional architecture, and hreflang tag validation. Enforces bidirectional return tags and cultural localization profiles."
license: MIT
metadata:
  author: SEO Skills AI
  version: "1.2.0"
---

# International SEO & Hreflang Validation

Audits and generates international URL architectures to eliminate cross-language cannibalization.

---

## 🌐 Hreflang Validation Rules

1. **Bidirectional Return Tag Verification:** If Page A links to Page B with `hreflang="de"`, Page B MUST link back to Page A with `hreflang="en"`.
2. **`x-default` Fallback:** Always include `hreflang="x-default"` pointing to the global language selector or default locale.
3. **Canonical Self-Alignment:** Each localized variant must specify its own URL as the canonical tag (never point canonicals across different language versions).
