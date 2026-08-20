#!/usr/bin/env python3
"""JSON HTTP helper. User URLs and vendor endpoints must pass url_safety."""
from __future__ import annotations

import base64
import json
import ssl
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlparse

from scripts.url_safety import validate_url


def json_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: Any = None,
    timeout: int = 30,
    basic_auth: tuple[str, str] | None = None,
) -> dict:
    validate_url(url, role="navigation")
    hdrs = {
        "Accept": "application/json",
        "User-Agent": "seoskillsai/1.2.0 (+https://github.com/seoskillsai/seo-skills-ai)",
    }
    if headers:
        hdrs.update(headers)
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/json")
    if basic_auth:
        token = base64.b64encode(f"{basic_auth[0]}:{basic_auth[1]}".encode("utf-8")).decode("ascii")
        hdrs["Authorization"] = f"Basic {token}"

    req = urllib.request.Request(url, data=data, headers=hdrs, method=method.upper())
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
            final_url = response.geturl()
            validate_url(final_url, role="redirect")
            raw = response.read().decode("utf-8", errors="replace")
            if not raw.strip():
                return {"status_code": response.status, "body": None}
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                return {
                    "status": "ERROR",
                    "error": "Vendor response was not JSON",
                    "status_code": response.status,
                    "host": urlparse(final_url).hostname,
                }
            if isinstance(parsed, dict):
                parsed.setdefault("http_status", response.status)
                return parsed
            return {"http_status": response.status, "body": parsed}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
        detail: Any
        try:
            detail = json.loads(raw) if raw else exc.reason
        except json.JSONDecodeError:
            detail = raw or str(exc.reason)
        return {"status": "ERROR", "error": f"HTTP {exc.code}", "detail": detail, "status_code": exc.code}
    except Exception as exc:
        return {"status": "ERROR", "error": str(exc)}


def form_request(url: str, fields: dict[str, str], *, timeout: int = 30) -> dict:
    validate_url(url, role="navigation")
    from urllib.parse import urlencode

    data = urlencode(fields).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "User-Agent": "seoskillsai/1.2.0 (+https://github.com/seoskillsai/seo-skills-ai)",
        },
        method="POST",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
            validate_url(response.geturl(), role="redirect")
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
        return {"status": "ERROR", "error": f"HTTP {exc.code}", "detail": raw or str(exc.reason)}
    except Exception as exc:
        return {"status": "ERROR", "error": str(exc)}
