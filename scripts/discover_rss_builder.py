#!/usr/bin/env python3
"""
SEO Skills AI — Google Discover Media RSS Generator
Generates Media RSS feeds with explicit <media:content> 1200px 16:9 images for Google Discover ingestion.
"""
import os
import sys
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.path_safety import prepare_output_file

def build_media_rss(channel_title: str, channel_link: str, items: list, output_path: str = "public/feed.xml"):
    now_rfc822 = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:media="http://search.yahoo.com/mrss/"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{channel_title}</title>
    <link>{channel_link}</link>
    <description>Verified AI SEO Articles and Guides for Google Discover</description>
    <language>en-us</language>
    <lastBuildDate>{now_rfc822}</lastBuildDate>
"""
    for item in items:
        xml += f"""    <item>
      <title>{item.get('title', '')}</title>
      <link>{item.get('link', '')}</link>
      <guid isPermaLink="true">{item.get('link', '')}</guid>
      <pubDate>{item.get('pubDate', now_rfc822)}</pubDate>
      <description>{item.get('description', '')}</description>
      <media:content 
        url="{item.get('image_url', '')}" 
        medium="image" 
        type="image/jpeg" 
        width="1200" 
        height="675">
        <media:title>{item.get('title', '')}</media:title>
        <media:credit>SEO Skills AI Editorial</media:credit>
      </media:content>
    </item>
"""
    xml += """  </channel>
</rss>
"""
    dest = prepare_output_file(output_path)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(xml)
    return str(dest)

if __name__ == "__main__":
    sample_items = [
        {
            "title": "Universal AI SEO Standard: 22 Free Skills for Claude & Cursor",
            "link": "https://seoskillsai.com/skills/seo-audit",
            "description": "Automate technical audits, schema, and GEO across 12 AI coding agents.",
            "image_url": "https://seoskillsai.com/images/discover-hero.jpg"
        }
    ]
    out = build_media_rss("SEO Skills AI", "https://seoskillsai.com", sample_items)
    print(f"[SUCCESS] Built Google Discover Media RSS feed at {out}")
