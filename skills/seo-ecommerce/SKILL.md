---
name: seo-ecommerce
description: "E-commerce SEO, product schema validation, faceted navigation indexing control, out-of-stock URL management, and Google Merchant Center optimization."
---

# E-Commerce SEO & Product Schema Engine

Optimizes product catalogs, category hierarchies, and Google Shopping structured data.

---

## 🛍️ Core E-Commerce Standards

1. **Rich Product JSON-LD Schema:**
   - Must include `name`, `image`, `description`, `sku`, `brand`, `offers` (price, priceCurrency, availability), and `aggregateRating`.
2. **Faceted Navigation Crawl Control:**
   - Apply `rel="canonical"` or `robots.txt` disallow rules on multi-filter search combinations (e.g. `?color=blue&size=m&sort=price`) to prevent infinite crawl loops.
3. **Out-of-Stock URL Management:**
   - Keep URLs live with `availability: "https://schema.org/OutOfStock"`, display related product recommendations, and collect back-in-stock email alerts (never 404 temporary out-of-stock items).
