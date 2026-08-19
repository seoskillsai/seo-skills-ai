# Crawl Budget & Crawl Demand Architecture Standard

Optimizing search bot crawling resource allocation across enterprise and programmatic web architectures.

---

## 🚦 The 4 Crawl Efficiency Rules

1. **Shallow Crawl Depth ($\le 2$ Clicks):**
   - 100% of indexable pages must be reachable within 2 internal hops from the root domain via dynamic HTML sitemaps and category silo hubs.
2. **Elimination of Faceted Parameter Waste:**
   - Parameter combinations (`?color=blue&size=m`) must be canonicalized or blocked in `robots.txt` to prevent exponential URL trap generation.
3. **HTTP 301 Redirect Chain Compression:**
   - Compress multi-hop redirect chains (`A -> B -> C`) into direct 1-hop 301 redirects (`A -> C`).
4. **Instant Push Discovery via IndexNow:**
   - Instantly dispatch updated and newly published URLs to IndexNow (Bing/Yandex/Seznam) to trigger immediate crawling without waiting for standard bot polling.
