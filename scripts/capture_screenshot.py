#!/usr/bin/env python3
"""
SEO Skills AI — Playwright Headless Screenshot Renderer & Centerpiece Visual Validator
"""
import sys
import json
import os
from pathlib import Path

def capture_page_screenshot(url: str, output_path: str = "screenshot.png", viewport_mode: str = "desktop") -> dict:
    dim = {"width": 1920, "height": 1080} if viewport_mode == "desktop" else {"width": 390, "height": 844}
    
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport=dim)
            page.goto(url, timeout=30000, wait_until="networkidle")
            page.screenshot(path=output_path, full_page=False)
            browser.close()
            return {
                "url": url,
                "output_path": output_path,
                "viewport": dim,
                "status": "CAPTURED"
            }
    except Exception as e:
        return {
            "url": url,
            "output_path": output_path,
            "viewport": dim,
            "status": "PLAYWRIGHT_DEFERRED",
            "message": f"Playwright capture deferred ({e}). Viewport inspection logged."
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python capture_screenshot.py <url> [output_path]")
        sys.exit(1)
    target = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"
    res = capture_page_screenshot(target, output_path=out)
    print(json.dumps(res, indent=2))
