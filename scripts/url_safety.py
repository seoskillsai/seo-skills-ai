#!/usr/bin/env python3
"""
SEO Skills AI — Network-target policy
All user-supplied URLs (HTTP fetch, MCP tools, crawler, headless Chromium
navigation) must pass this module before any request is made. Redirect hops
are re-checked. Optional allowlist: SEOSKILLS_ALLOWED_HOSTS (comma-separated).
Set SEOSKILLS_STRICT_BROWSER=1 to apply the same allowlist to Chromium subresources.
"""
import ipaddress
import os
import socket
import sys
from urllib.parse import urljoin, urlparse

BLOCKED_IP_RANGES = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("100.64.0.0/10"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.0.0.0/24"),
    ipaddress.ip_network("192.0.2.0/24"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("198.18.0.0/15"),
    ipaddress.ip_network("198.51.100.0/24"),
    ipaddress.ip_network("203.0.113.0/24"),
    ipaddress.ip_network("224.0.0.0/4"),
    ipaddress.ip_network("240.0.0.0/4"),
    ipaddress.ip_network("::/128"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
    ipaddress.ip_network("ff00::/8"),
]

BLOCKED_HOSTNAMES = {
    "localhost",
    "localhost.localdomain",
    "ip6-localhost",
    "metadata.google.internal",
    "metadata",
}


def allowed_hosts():
    raw = os.environ.get("SEOSKILLS_ALLOWED_HOSTS", "").strip()
    if not raw:
        return None
    return {part.lower().strip().rstrip(".") for part in raw.split(",") if part.strip()}


def _hostname_in_allowlist(hostname: str) -> bool:
    allowed = allowed_hosts()
    if allowed is None:
        return True
    host = hostname.lower().rstrip(".")
    for entry in allowed:
        if host == entry or host.endswith("." + entry):
            return True
    return False


def _ip_is_blocked(ip_obj) -> bool:
    mapped = getattr(ip_obj, "ipv4_mapped", None)
    if mapped is not None:
        ip_obj = mapped
    if ip_obj.is_loopback or ip_obj.is_private or ip_obj.is_link_local or ip_obj.is_multicast or ip_obj.is_reserved:
        return True
    if ip_obj.is_unspecified:
        return True
    for blocked in BLOCKED_IP_RANGES:
        if ip_obj in blocked:
            return True
    return False


def _check_ip_literal_or_resolved(hostname: str) -> None:
    try:
        ip_obj = ipaddress.ip_address(hostname)
    except ValueError:
        ip_obj = None

    if ip_obj is not None:
        if _ip_is_blocked(ip_obj):
            raise PermissionError(
                f"Security Alert: Target host is a prohibited IP {hostname}."
            )
        return

    try:
        addr_info = socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise PermissionError(
            f"Security Alert: Target host {hostname!r} could not be resolved ({exc})."
        ) from exc

    seen = False
    for entry in addr_info:
        ip_str = entry[4][0]
        seen = True
        resolved = ipaddress.ip_address(ip_str)
        if _ip_is_blocked(resolved):
            raise PermissionError(
                f"Security Alert: Target host resolves to private/prohibited IP {ip_str}."
            )
    if not seen:
        raise PermissionError(
            f"Security Alert: Target host {hostname!r} resolved to no addresses."
        )


def _normalize_hostname(hostname: str) -> str:
    host = (hostname or "").strip().lower().rstrip(".")
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1]
    return host


def validate_url(url: str, *, role: str = "navigation") -> bool:
    """Validate a URL against the network-target policy.

    role:
      navigation — user-supplied page URL (allowlist applies)
      redirect — Location hop (same rules as navigation)
      subresource — Chromium asset request (allowlist only if SEOSKILLS_STRICT_BROWSER=1)
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL is required.")

    parsed = urlparse(url.strip())
    if parsed.scheme not in ("http", "https"):
        raise ValueError(
            f"Invalid URL scheme '{parsed.scheme or ''}'. Only http and https are allowed."
        )

    hostname = _normalize_hostname(parsed.hostname or "")
    if not hostname:
        raise ValueError("Invalid URL: missing hostname.")
    if "/" in hostname or "\\" in hostname or "@" in hostname:
        raise ValueError("Invalid URL: malformed hostname.")

    if hostname in BLOCKED_HOSTNAMES or hostname.endswith(".localhost") or hostname.endswith(".internal"):
        raise PermissionError(
            f"Security Alert: Target host {hostname!r} is a blocked name."
        )

    apply_allowlist = role in ("navigation", "redirect") or os.environ.get(
        "SEOSKILLS_STRICT_BROWSER", ""
    ).strip() in ("1", "true", "yes")
    if apply_allowlist and not _hostname_in_allowlist(hostname):
        raise PermissionError(
            f"Security Alert: Host {hostname!r} is not in SEOSKILLS_ALLOWED_HOSTS."
        )

    _check_ip_literal_or_resolved(hostname)
    return True


def validate_redirect(from_url: str, to_url: str) -> bool:
    absolute = urljoin(from_url, to_url)
    return validate_url(absolute, role="redirect")


def is_request_allowed(url: str, *, role: str = "subresource") -> bool:
    """Playwright route check: never raises."""
    if not url:
        return False
    if url.startswith("data:") or url.startswith("blob:"):
        return True
    try:
        validate_url(url, role=role)
        return True
    except (ValueError, PermissionError):
        return False


def normalize_user_url(url: str) -> str:
    text = (url or "").strip()
    if text and "://" not in text:
        return "https://" + text
    return text


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
