#!/usr/bin/env python3
"""
PreToolUse hook: block fetch tools unless the URL passes url_safety.
Reads Claude/Codex JSON from stdin. Does not interpolate {file} into a shell.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.url_safety import normalize_user_url, validate_url

FETCH_TOOLS = {
    "WebFetch",
    "web_fetch",
    "fetch",
    "mcp__web_fetch",
    "seo_audit",
    "seo_drift",
}


def _extract_url(payload: dict) -> str | None:
    tool_input = payload.get("tool_input") or payload.get("input") or payload.get("arguments") or {}
    if isinstance(tool_input, dict):
        for key in ("url", "uri", "href", "target"):
            value = tool_input.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    for key in ("url", "uri", "href"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def main() -> int:
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw.strip():
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return 0
    tool = str(payload.get("tool_name") or payload.get("tool") or "")
    url = _extract_url(payload)
    if not url:
        return 0
    if tool and tool not in FETCH_TOOLS and "fetch" not in tool.lower() and "WebFetch" not in tool:
        # Still validate when a URL is present on a fetch-like payload.
        if "url" not in json.dumps(payload).lower():
            return 0
    try:
        validate_url(normalize_user_url(url), role="navigation")
    except (ValueError, PermissionError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
