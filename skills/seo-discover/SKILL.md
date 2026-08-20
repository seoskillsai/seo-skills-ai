---
name: seo-discover
description: "Google Discover optimization, Media RSS XML feed generation, and First-Exposure AI Editorial Byline disclosure protocol for high-traffic editorial reach."
license: MIT
metadata:
  author: SEO Skills AI
  version: "1.2.0"
---

# Google Discover, Media RSS & AI Disclosure Standard

This skill establishes the protocol for maximizing Google Discover traffic via high-resolution image signaling, Media RSS XML syndication, and transparent AI editorial disclosure bylines.

---

## 📸 1. Google Discover Technical Prerequisites

1. **Meta Robots Directive:**
   Every page `<head>` must include:
   ```html
   <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />
   ```
   `max-image-preview:large` enables Google Discover to display high-resolution 16:9 thumbnails, increasing click-through rates by up to **300%**.

2. **Image Dimensions:**
   Featured images must be at least **1200px wide** with a **16:9 aspect ratio** (e.g. `1200x675` or `1600x900`).

---

## 📰 2. Media RSS Syndication Engine

Standard RSS feeds only deliver text. Google Discover and feed aggregators prioritize feeds with explicit Media RSS `<media:content>` enclosures.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:media="http://search.yahoo.com/mrss/"
     xmlns:dc="http://purl.org/dc/elements/1.1/">
  <channel>
    <title>Site Name — Verified Articles</title>
    <link>https://example.com/</link>
    <item>
      <title>Article Title</title>
      <link>https://example.com/article-slug/</link>
      <pubDate>Wed, 19 Aug 2026 00:00:00 GMT</pubDate>
      <media:content 
        url="https://example.com/images/feature.jpg" 
        medium="image" 
        type="image/jpeg" 
        width="1200" 
        height="675">
        <media:title>Feature Image</media:title>
        <media:credit>Editorial Staff</media:credit>
      </media:content>
    </item>
  </channel>
</rss>
```

---

## 🛡️ 3. First-Exposure AI Editorial Disclosure

Every article features a transparent editorial disclosure directly beneath the `H1`:
- **Human Verification:** Verified by named subject-matter experts.
- **AI Assistance:** Discloses algorithmic synthesis under human oversight.
- **Zero Hallucination Guarantee:** Facts and citations cross-checked against primary sources.
