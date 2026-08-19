---
name: seo-sitemap
description: "Twin XML and dynamic HTML sitemap architecture. Generates machine-readable XML sitemaps and accessible, categorized HTML sitemaps ensuring zero orphan pages and <=2 click crawl depth."
---

# Twin XML & Dynamic HTML Sitemap Architecture

Generates and audits a dual-layer sitemap architecture:
1. **Machine-Readable XML Sitemap (`/sitemap-index.xml`):** Consumed by Googlebot, Bingbot, and IndexNow.
2. **User-Facing Dynamic HTML Sitemap (`/sitemap`):** Guarantees zero orphan pages, passes internal PageRank equity, and ensures all content is reachable within $\le 2$ clicks of the homepage.

---

## 🏗️ Dynamic HTML Sitemap Structure

```
/sitemap/ (User & Crawler Hub)
├── 1. Core Platform Pages (Home, Directory, Tools, Guides)
├── 2. Category Silo Hubs (Audit, Schema, Content, GEO, Backlinks)
├── 3. Dynamic Collection Nodes (Categorized with count badges)
└── 4. Link to /sitemap-index.xml (Direct bot handoff)
```

## 📋 SEO & Crawl Quality Gates

| Metric | Target Standard |
| :--- | :--- |
| **Max Crawl Depth** | All pages reachable within **$\le 2$ clicks** from root. |
| **Orphan Pages** | **0** orphan pages (100% of collection items listed in HTML sitemap). |
| **JavaScript Dependency** | **Zero client-side JS** (Static server-rendered HTML output). |
| **Heading Hierarchy** | Single `<h1>`, `<h2>` for silos, `<h3>` for category groups. |
