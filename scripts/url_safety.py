#!/usr/bin/env python3
"""
SEO Skills AI — URL Safety & SSRF Validator
Protects against SSRF, internal network scanning, and invalid protocol attacks.
"""
import ipaddress
import socket
import sys
from urllib.parse import urlparse

BLOCKED_IP_RANGES = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),  # AWS/Cloud metadata
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
]

def validate_url(url: str) -> bool:
    """Validates that a URL is well-formed, uses HTTP/HTTPS, and does not target private IPs."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid URL scheme '{parsed.scheme}'. Only http and https are allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Invalid URL: missing hostname.")

    try:
        addr_info = socket.getaddrinfo(hostname, None)
        for entry in addr_info:
            ip_str = entry[4][0]
            ip_obj = ipaddress.ip_address(ip_str)
            for blocked in BLOCKED_IP_RANGES:
                if ip_obj in blocked:
                    raise PermissionError(f"Security Alert: Target host resolves to private/prohibited IP {ip_str}.")
    except socket.gaierror:
        pass  # Host resolution error handled downstream in fetcher

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python url_safety.py <url>")
        sys.exit(1)
    target = sys.argv[1]
    try:
        validate_url(target)
        print(f"[SAFE] URL '{target}' passed SSRF security checks.")
        sys.exit(0)
    except Exception as e:
        print(f"[BLOCKED] URL '{target}' failed safety check: {e}", file=sys.stderr)
        sys.exit(1)
