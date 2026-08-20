---
name: seo-schema
description: "Detects, validates, and generates 2026 Google-compliant Schema.org JSON-LD markup. Filters out deprecated types (HowTo, SpecialAnnouncement) and builds unified nested @graph entities."
license: MIT
metadata:
  author: SEO Skills AI
  version: "1.2.0"
---

# 2026 Google-Compliant Schema.org Engine

Generates and validates structured JSON-LD graphs adhering to modern Google Search Central guidelines.

---

## 🚫 Deprecated Schema Types (Never Recommend / Flag as Deprecated)

- **`HowTo`**: Rich results removed by Google globally in September 2023.
- **`FAQPage`**: Restricted to authoritative government and health sites in August 2023; rich snippet visibility deprecated for commercial sites in May 2026. Keep only for internal entity semantics.
- **`SpecialAnnouncement`**: Deprecated in July 2025.
- **`ClaimReview` / `VehicleListing` / `EstimatedSalary` / `LearningVideo` / `CourseInfo Carousel`**: Deprecated in June 2025.

---

## ✅ Active 2026 Schema.org Patterns

Always group into a single nested `<script type="application/ld+json">` with `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "https://example.com/#website",
      "url": "https://example.com/",
      "name": "Site Name",
      "publisher": { "@id": "https://example.com/#organization" }
    },
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Organization Name",
      "url": "https://example.com/",
      "logo": "https://example.com/logo.png"
    },
    {
      "@type": "TechArticle",
      "@id": "https://example.com/page/#article",
      "isPartOf": { "@id": "https://example.com/#website" },
      "headline": "Article Title",
      "description": "Article Summary",
      "inLanguage": "en-US",
      "author": { "@id": "https://example.com/#organization" },
      "datePublished": "2026-08-19T00:00:00Z",
      "dateModified": "2026-08-19T00:00:00Z"
    },
    {
      "@type": "SoftwareApplication",
      "@id": "https://example.com/page/#software",
      "name": "Application Name",
      "applicationCategory": "DeveloperApplication",
      "operatingSystem": "All"
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://example.com/page/#breadcrumbs",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
        { "@type": "ListItem", "position": 2, "name": "Skills", "item": "https://example.com/skills/" }
      ]
    }
  ]
}
```
