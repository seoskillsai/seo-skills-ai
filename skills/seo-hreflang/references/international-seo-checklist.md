# International SEO & Hreflang Validation Checklist

Requirements for multi-regional and multi-lingual website architectures.

---

## 🌍 1. Hreflang Reciprocity Standard

- **Reciprocal Links:** If page A targets `en-US` and links to page B for `de-DE`, page B MUST link back to page A with `hreflang="en-US"`. Broken reciprocity breaks international indexation.
- **x-default Fallback:** Always provide `<link rel="alternate" hreflang="x-default" href="https://example.com/" />` for non-targeted language users or global landing selectors.
- **Valid ISO Codes:** Language must use ISO 639-1 (e.g. `en`, `es`, `de`) and country must use ISO 3166-1 alpha-2 (e.g. `US`, `GB`, `DE`).
