#!/usr/bin/env python3
"""
SEO Skills AI — Enterprise HTML & Semantic DOM Parser
"""
import re
import sys
import json
from html.parser import HTMLParser
from urllib.parse import urlparse

class EnterpriseSEOParser(HTMLParser):
    def __init__(self, base_url: str = ""):
        super().__init__()
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc if base_url else ""
        
        self.title = ""
        self.meta_description = ""
        self.meta_robots = ""
        self.canonical = ""
        self.viewport = ""
        self.charset = ""
        
        self.opengraph = {}
        self.twitter_card = {}
        
        self.h1_tags = []
        self.h2_tags = []
        self.h3_tags = []
        self.heading_sequence = []
        
        self.schemas = []
        self.images = []
        self.internal_links = []
        self.external_links = []
        self.anchor_text_map = {}  # url -> list of anchors
        self.text_paragraphs = []
        
        self._in_title = False
        self._in_script_ldjson = False
        self._current_tag = None
        self._current_anchor_href = None
        self._current_anchor_text = ""
        self._current_p_text = ""

    def handle_starttag(self, tag, attrs):
        self._current_tag = tag
        attr_dict = {k.lower(): v for k, v in attrs}

        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = attr_dict.get("name", "").lower()
            prop = attr_dict.get("property", "").lower()
            content = attr_dict.get("content", "")
            
            if name == "description":
                self.meta_description = content
            elif name == "robots":
                self.meta_robots = content
            elif name == "viewport":
                self.viewport = content
            elif "charset" in attr_dict:
                self.charset = attr_dict["charset"]
                
            if prop.startswith("og:"):
                self.opengraph[prop[3:]] = content
            elif name.startswith("twitter:"):
                self.twitter_card[name[8:]] = content
                
        elif tag == "link":
            rel = attr_dict.get("rel", "").lower()
            href = attr_dict.get("href", "")
            if rel == "canonical":
                self.canonical = href
        elif tag == "script":
            stype = attr_dict.get("type", "").lower()
            if stype == "application/ld+json":
                self._in_script_ldjson = True
        elif tag == "img":
            self.images.append({
                "src": attr_dict.get("src", ""),
                "alt": attr_dict.get("alt", ""),
                "width": attr_dict.get("width", ""),
                "height": attr_dict.get("height", ""),
                "loading": attr_dict.get("loading", "")
            })
        elif tag == "a":
            href = attr_dict.get("href", "")
            self._current_anchor_href = href
            self._current_anchor_text = ""
            if href.startswith("http"):
                parsed = urlparse(href)
                if self.base_domain and parsed.netloc == self.base_domain:
                    self.internal_links.append(href)
                else:
                    self.external_links.append(href)
            elif href and not href.startswith("#") and not href.startswith("javascript:") and not href.startswith("mailto:"):
                self.internal_links.append(href)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heading_sequence.append(tag.upper())
        elif tag == "p":
            self._current_p_text = ""

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            self._in_script_ldjson = False
        elif tag == "a":
            if self._current_anchor_href:
                clean_anchor = self._current_anchor_text.strip()
                if self._current_anchor_href not in self.anchor_text_map:
                    self.anchor_text_map[self._current_anchor_href] = []
                if clean_anchor:
                    self.anchor_text_map[self._current_anchor_href].append(clean_anchor)
            self._current_anchor_href = None
            self._current_anchor_text = ""
        elif tag == "p":
            if self._current_p_text.strip():
                self.text_paragraphs.append(self._current_p_text.strip())
            self._current_p_text = ""
        self._current_tag = None

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self._in_title:
            self.title += text
        elif self._in_script_ldjson:
            self.schemas.append(data)
        elif self._current_tag == "h1":
            self.h1_tags.append(text)
        elif self._current_tag == "h2":
            self.h2_tags.append(text)
        elif self._current_tag == "h3":
            self.h3_tags.append(text)
        elif self._current_tag == "p" or self._current_p_text != "":
            self._current_p_text += " " + text
        
        if self._current_anchor_href:
            self._current_anchor_text += " " + text

def parse_html_content(html: str, base_url: str = "") -> dict:
    parser = EnterpriseSEOParser(base_url=base_url)
    parser.feed(html)
    
    full_body_text = " ".join(parser.text_paragraphs)
    words = re.findall(r"\b\w+\b", full_body_text)
    word_count = len(words)

    # GEO Passage Citability: Extract chunks with 100-200 words
    citable_passages = []
    for p in parser.text_paragraphs:
        p_words = len(re.findall(r"\b\w+\b", p))
        if 100 <= p_words <= 200:
            citable_passages.append({
                "word_count": p_words,
                "text": p[:300] + ("..." if len(p) > 300 else "")
            })

    # Anchor text diversity analysis (3x Anchor Diversity Rule)
    anchor_frequencies = {}
    for href, anchors in parser.anchor_text_map.items():
        for a in anchors:
            norm_a = a.lower().strip()
            if len(norm_a) > 2:
                anchor_frequencies[norm_a] = anchor_frequencies.get(norm_a, 0) + 1

    over_optimized_anchors = [
        {"anchor": a, "count": c} for a, c in anchor_frequencies.items() if c > 3
    ]

    heading_hierarchy_errors = []
    levels = {"H1": 1, "H2": 2, "H3": 3, "H4": 4, "H5": 5, "H6": 6}
    last_level = 0
    for h in parser.heading_sequence:
        curr_level = levels.get(h, 0)
        if last_level > 0 and curr_level > last_level + 1:
            heading_hierarchy_errors.append(f"Heading skipped level: from H{last_level} directly to H{curr_level}")
        last_level = curr_level

    has_large_image_preview = "max-image-preview:large" in parser.meta_robots.lower()
    high_res_images = [img for img in parser.images if img.get("width") and img["width"].isdigit() and int(img["width"]) >= 1200]

    return {
        "title": parser.title,
        "title_length": len(parser.title),
        "meta_description": parser.meta_description,
        "meta_description_length": len(parser.meta_description),
        "meta_robots": parser.meta_robots,
        "canonical": parser.canonical,
        "viewport": parser.viewport,
        "h1": parser.h1_tags,
        "h2": parser.h2_tags,
        "h3": parser.h3_tags,
        "heading_sequence": parser.heading_sequence,
        "heading_hierarchy_errors": heading_hierarchy_errors,
        "word_count": word_count,
        "opengraph": parser.opengraph,
        "twitter_card": parser.twitter_card,
        "images_count": len(parser.images),
        "images_missing_alt": [img["src"] for img in parser.images if not img.get("alt")],
        "high_res_discover_images": len(high_res_images),
        "has_large_image_preview": has_large_image_preview,
        "schemas": parser.schemas,
        "schemas_count": len(parser.schemas),
        "internal_links_count": len(parser.internal_links),
        "external_links_count": len(parser.external_links),
        "anchor_text_map": parser.anchor_text_map,
        "citable_passages": citable_passages,
        "citable_passages_count": len(citable_passages),
        "over_optimized_anchors": over_optimized_anchors
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_html.py <html_file_or_string>")
        sys.exit(1)
    arg = sys.argv[1]
    html_text = open(arg, "r", encoding="utf-8").read() if arg.endswith(".html") else arg
    res = parse_html_content(html_text)
    print(json.dumps(res, indent=2))
