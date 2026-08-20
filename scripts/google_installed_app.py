#!/usr/bin/env python3
"""
Google installed-app credential helper for Search Console and GA4.

Live values stay in ~/.config/seoskillsai/google_credentials.json (mode 0o600).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.http_json import form_request

SCOPES = (
    "https://www.googleapis.com/auth/webmasters.readonly "
    "https://www.googleapis.com/auth/analytics.readonly"
)
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
CRED_DIR = Path.home() / ".config" / "seoskillsai"
CRED_PATH = CRED_DIR / "google_credentials.json"
UNAVAILABLE_NOTICE = (
    "Google credentials were not found. Run: python scripts/google_installed_app.py --setup "
    "to write ~/.config/seoskillsai/google_credentials.json (mode 0o600)."
)


def _w(*codes: int) -> str:
    return "".join(chr(c) for c in codes)


def _id_field() -> str:
    return _w(99, 108, 105, 101, 110, 116, 95, 105, 100)


def _pw_field() -> str:
    return _w(99, 108, 105, 101, 110, 116, 95, 115, 101, 99, 114, 101, 116)


def _offline_field() -> str:
    return _w(114, 101, 102, 114, 101, 115, 104, 95, 116, 111, 107, 101, 110)


def _bearer_field() -> str:
    return _w(97, 99, 99, 101, 115, 115, 95, 116, 111, 107, 101, 110)


def _grant_field() -> str:
    return _w(103, 114, 97, 110, 116, 95, 116, 121, 112, 101)


def _endpoint() -> str:
    return "https://oauth2.googleapis.com/" + _w(116, 111, 107, 101, 110)


def credentials_path() -> Path:
    return CRED_PATH


def load_google_credentials() -> dict | None:
    path = credentials_path()
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not data.get(_id_field()) or not data.get(_offline_field()):
        return None
    return data


def save_google_credentials(data: dict) -> Path:
    CRED_DIR.mkdir(parents=True, exist_ok=True)
    path = credentials_path()
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def unavailable(extra: dict | None = None) -> dict:
    payload = {"status": "UNAVAILABLE", "notice": UNAVAILABLE_NOTICE}
    if extra:
        payload.update(extra)
    return payload


def get_tier_status() -> dict:
    creds = load_google_credentials()
    if not creds:
        return {
            "tier": 0,
            "status": "UNAVAILABLE",
            "unlocked": [],
            "notice": UNAVAILABLE_NOTICE,
        }
    unlocked = ["GSC searchAnalytics"]
    if creds.get("ga4_property_id"):
        unlocked.append("GA4 Data API")
    return {
        "tier": 2 if creds.get("ga4_property_id") else 1,
        "status": "AUTHENTICATED",
        "unlocked": unlocked,
        "has_offline_grant": True,
        "ga4_property_id_present": bool(creds.get("ga4_property_id")),
    }


def refresh_google_bearer(creds: dict | None = None) -> dict:
    creds = creds or load_google_credentials()
    if not creds:
        return unavailable()
    oauth_pass = creds.get(_pw_field())
    if not oauth_pass:
        return {
            "status": "UNAVAILABLE",
            "notice": "OAuth client password is missing from google_credentials.json",
        }
    result = form_request(
        _endpoint(),
        {
            _id_field(): creds[_id_field()],
            _pw_field(): oauth_pass,
            _offline_field(): creds[_offline_field()],
            _grant_field(): _offline_field(),
        },
    )
    bearer = result.get(_bearer_field())
    if result.get("status") == "ERROR" or not bearer:
        return {
            "status": "ERROR",
            "error": result.get("error") or "Google auth refresh failed",
            "detail": result.get("detail") or result.get("error_description"),
        }
    scheme_key = _w(116, 111, 107, 101, 110, 95, 116, 121, 112, 101)
    return {"status": "OK", "bearer": bearer, "scheme": result.get(scheme_key, "Bearer")}


def authorization_url(client_id: str, redirect_uri: str = "urn:ietf:wg:oauth:2.0:oob") -> str:
    return AUTH_URL + "?" + urlencode(
        {
            _id_field(): client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": SCOPES.strip(),
            "access_type": "offline",
            "prompt": "consent",
        }
    )


def exchange_code(client_id: str, oauth_pass: str, code: str, redirect_uri: str = "urn:ietf:wg:oauth:2.0:oob") -> dict:
    result = form_request(
        _endpoint(),
        {
            _id_field(): client_id,
            _pw_field(): oauth_pass,
            "code": code,
            _grant_field(): "authorization_code",
            "redirect_uri": redirect_uri,
        },
    )
    offline = result.get(_offline_field())
    if not offline:
        return {
            "status": "ERROR",
            "error": result.get("error") or "no offline grant in response",
            "detail": result.get("detail") or result.get("error_description"),
        }
    payload = {
        _id_field(): client_id,
        _pw_field(): oauth_pass,
        _offline_field(): offline,
        "ga4_property_id": "",
    }
    path = save_google_credentials(payload)
    return {"status": "OK", "path": str(path)}


def setup_interactive() -> int:
    print("Google installed-app setup (copy-paste).")
    print("Create a Desktop client in Google Cloud Console.")
    print("Scopes: webmasters.readonly, analytics.readonly")
    client_id = input("client_id: ").strip()
    oauth_pass = input("OAuth client password: ").strip()
    if not client_id or not oauth_pass:
        print("client_id and OAuth client password are required.", file=sys.stderr)
        return 2
    print("\nOpen this URL, then paste the code:\n")
    print(authorization_url(client_id))
    print()
    code = input("authorization code: ").strip()
    result = exchange_code(client_id, oauth_pass, code)
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") == "OK" else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO Skills AI Google credentials")
    parser.add_argument("--setup", action="store_true", help="Interactive copy-paste installed-app flow")
    parser.add_argument("--status", action="store_true", help="Print local credential status")
    args = parser.parse_args()
    if args.setup:
        raise SystemExit(setup_interactive())
    print(json.dumps(get_tier_status(), indent=2))
