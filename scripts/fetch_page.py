#!/usr/bin/env python3
"""
SEO Skills AI — Enterprise Page Fetcher with Redirect Chain Tracking & Header Diagnostics
"""
import os
import sys
import time
import urllib.request
import urllib.error

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.url_safety import validate_url, validate_redirect

USER_AGENTS = {
    "desktop": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "mobile": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "googlebot_mobile": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
}

class RedirectTracker(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.redirect_chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        try:
            validate_redirect(req.full_url, newurl)
        except (ValueError, PermissionError) as exc:
            raise urllib.error.URLError(str(exc)) from exc
        self.redirect_chain.append({
            "status_code": code,
            "from_url": req.full_url,
            "to_url": newurl
        })
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def _blocked_result(url: str, error: str) -> dict:
    return {
        "url": url,
        "final_url": url,
        "is_redirected": False,
        "redirect_chain": [],
        "redirect_count": 0,
        "status_code": 0,
        "latency_ms": 0,
        "headers": {},
        "html": "",
        "size_bytes": 0,
        "error": error,
        "security_headers": {}
    }


def fetch_page(url: str, ua_type: str = "desktop", timeout: int = 15) -> dict:
    try:
        validate_url(url)
    except (ValueError, PermissionError) as exc:
        return _blocked_result(url, str(exc))
    ua = USER_AGENTS.get(ua_type, USER_AGENTS["desktop"])
    headers = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",
        "Connection": "close"
    }

    redirect_tracker = RedirectTracker()
    opener = urllib.request.build_opener(redirect_tracker)

    req = urllib.request.Request(url, headers=headers)
    start_time = time.time()
    try:
        with opener.open(req, timeout=timeout) as response:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            raw_bytes = response.read()
            charset = response.headers.get_content_charset() or "utf-8"
            html_content = raw_bytes.decode(charset, errors="replace")
            response_headers = {k.lower(): v for k, v in response.headers.items()}
            status_code = response.status
            final_url = response.geturl()

            return {
                "url": url,
                "final_url": final_url,
                "is_redirected": len(redirect_tracker.redirect_chain) > 0,
                "redirect_chain": redirect_tracker.redirect_chain,
                "redirect_count": len(redirect_tracker.redirect_chain),
                "status_code": status_code,
                "latency_ms": latency_ms,
                "headers": response_headers,
                "html": html_content,
                "size_bytes": len(raw_bytes),
                "security_headers": {
                    "hsts": "strict-transport-security" in response_headers,
                    "csp": "content-security-policy" in response_headers,
                    "x_frame_options": response_headers.get("x-frame-options", ""),
                    "x_content_type_options": response_headers.get("x-content-type-options", ""),
                    "referrer_policy": response_headers.get("referrer-policy", "")
                }
            }
    except urllib.error.HTTPError as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        raw = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        return {
            "url": url,
            "final_url": url,
            "is_redirected": False,
            "redirect_chain": redirect_tracker.redirect_chain,
            "redirect_count": len(redirect_tracker.redirect_chain),
            "status_code": e.code,
            "latency_ms": latency_ms,
            "headers": {k.lower(): v for k, v in e.headers.items()} if hasattr(e, "headers") else {},
            "html": raw,
            "size_bytes": len(raw),
            "error": f"HTTP Error {e.code}: {e.reason}",
            "security_headers": {}
        }
    except Exception as e:
        return {
            "url": url,
            "final_url": url,
            "is_redirected": False,
            "redirect_chain": [],
            "redirect_count": 0,
            "status_code": 0,
            "latency_ms": 0,
            "headers": {},
            "html": "",
            "size_bytes": 0,
            "error": str(e),
            "security_headers": {}
        }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_page.py <url>")
        sys.exit(1)
    res = fetch_page(sys.argv[1])
    print(f"Status: {res['status_code']} | Final URL: {res['final_url']} | Latency: {res['latency_ms']}ms | Redirects: {res['redirect_count']}")
