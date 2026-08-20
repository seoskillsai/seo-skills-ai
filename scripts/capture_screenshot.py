#!/usr/bin/env python3
"""
SEO Skills AI — Playwright Headless Screenshot Renderer
Navigation and subresource requests go through the network-target policy.
Set SEOSKILLS_STRICT_BROWSER=1 so Chromium subresources also honor SEOSKILLS_ALLOWED_HOSTS.
Screenshots are written only inside the workspace (SEOSKILLS_OUT_DIR / cwd).
"""
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.path_safety import prepare_output_file
from scripts.url_safety import is_request_allowed, validate_url


def should_abort_request(url: str, is_navigation: bool) -> bool:
    """True when Playwright must abort (private IP, blocked host, strict allowlist)."""
    role = "navigation" if is_navigation else "subresource"
    return not is_request_allowed(url, role=role)


def capture_page_screenshot(url: str, output_path: str = "screenshot.png", viewport_mode: str = "desktop") -> dict:
    dim = {"width": 1920, "height": 1080} if viewport_mode == "desktop" else {"width": 390, "height": 844}

    try:
        validate_url(url, role="navigation")
        dest = prepare_output_file(output_path)
    except (ValueError, PermissionError, OSError) as exc:
        return {
            "url": url,
            "output_path": str(output_path),
            "viewport": dim,
            "status": "BLOCKED",
            "message": str(exc),
        }

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as e:
        return {
            "url": url,
            "output_path": str(dest),
            "viewport": dim,
            "status": "PLAYWRIGHT_UNAVAILABLE",
            "message": f"Playwright is not installed ({e}). Run install.sh / install.ps1 for Chromium.",
        }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport=dim)

            def enforce_network_policy(route):
                request_url = route.request.url
                is_nav = route.request.is_navigation_request()
                if should_abort_request(request_url, is_nav):
                    route.abort("blockedbyclient")
                else:
                    route.continue_()

            page.route("**/*", enforce_network_policy)
            page.goto(url, timeout=30000, wait_until="networkidle")
            page.screenshot(path=str(dest), full_page=False)
            browser.close()
            return {
                "url": url,
                "output_path": str(dest),
                "viewport": dim,
                "status": "CAPTURED",
            }
    except Exception as e:
        return {
            "url": url,
            "output_path": str(dest),
            "viewport": dim,
            "status": "PLAYWRIGHT_FAILED",
            "message": str(e),
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python capture_screenshot.py <url> [output_path]")
        sys.exit(1)
    target = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"
    res = capture_page_screenshot(target, output_path=out)
    print(json.dumps(res, indent=2))
    if res.get("status") in ("BLOCKED", "PLAYWRIGHT_FAILED"):
        sys.exit(1)
