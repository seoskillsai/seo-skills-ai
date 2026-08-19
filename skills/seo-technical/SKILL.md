---
name: seo-technical
description: "9-category technical SEO audit: crawlability, indexability, security, Core Web Vitals (INP/LCP/CLS), canonicals, redirects, HTTP headers, and IndexNow."
---

# 9-Category Technical SEO Audit

Performs rigorous diagnostics on technical infrastructure and crawl optimization.

## 📋 The 9 Audit Categories

1. **Crawlability & Bot Access:**
   - `robots.txt` syntax, crawl delays, AI bot policies (`GPTBot`, `ClaudeBot`, `Google-Extended`).
2. **Indexability & Status Codes:**
   - Meta robots (`noindex`, `nofollow`, `max-image-preview:large`), HTTP 200 vs 301/404 chains.
3. **Core Web Vitals & Real User Metrics:**
   - **INP (Interaction to Next Paint):** Target <200ms (CrUX field data).
   - **LCP (Largest Contentful Paint):** Target <2.5s (subparts: TTFB, load delay, render delay).
   - **CLS (Cumulative Layout Shift):** Target <0.1.
4. **Security & Protocol Hardening:**
   - HTTPS enforcement, HSTS, Content-Security-Policy (CSP), `X-Frame-Options`, `Referrer-Policy`.
5. **Canonical & URL Structure:**
   - Self-referencing canonicals, trailing-slash consistency, parameter handling.
6. **Mobile-Friendliness & Viewport:**
   - Responsive viewport configuration, touch target spacing, font legibility.
7. **Structured Data Syntax:**
   - Absence of parse errors, valid nesting in `@graph`.
8. **Server Latency & TTFB:**
   - Time-to-First-Byte <800ms globally via edge CDN (Cloudflare/Fastly).
9. **IndexNow & Instant Discovery:**
   - IndexNow key verification for instant Bing & Yandex notification.
