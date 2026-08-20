#!/usr/bin/env python3
"""
Google OAuth helper for Search Console and GA4.

Credentials live only in ~/.config/seoskillsai/google_credentials.json (mode 0o600).
This repo never ships client secrets or the private Websites analytics identity DB.

Scopes:
  https://www.googleapis.com/auth/webmasters.readonly
  https://www.googleapis.com/auth/analytics.readonly
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
TOKEN_URL = "https://oauth2.googleapis.com/token"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
CRED_DIR = Path.home() / ".config" / "seoskillsai"
CRED_PATH = CRED_DIR / "google_credentials.json"
UNAVAILABLE_NOTICE = (
    "Google OAuth credentials were not found. Copy config/google_credentials.example.json "
    "to ~/.config/seoskillsai/google_credentials.json and run: python scripts/google_oauth.py --setup"
)


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
    if not data.get("client_id") or not data.get("refresh_token"):
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
        "has_refresh_token": True,
        "ga4_property_id_present": bool(creds.get("ga4_property_id")),
    }


def refresh_access_token(creds: dict | None = None) -> dict:
    creds = creds or load_google_credentials()
    if not creds:
        return unavailable()
    secret = creds.get("client_secret")
    if not secret:
        return {
            "status": "UNAVAILABLE",
            "notice": "client_secret is missing from google_credentials.json",
        }
    result = form_request(
        TOKEN_URL,
        {
            "client_id": creds["client_id"],
            "client_secret": secret,
            "refresh_token": creds["refresh_token"],
            "grant_type": "refresh_token",
        },
    )
    if result.get("status") == "ERROR" or not result.get("access_token"):
        return {
            "status": "ERROR",
            "error": result.get("error") or "token refresh failed",
            "detail": result.get("detail") or result.get("error_description"),
        }
    return {"status": "OK", "access_token": result["access_token"], "token_type": result.get("token_type", "Bearer")}


def authorization_url(client_id: str, redirect_uri: str = "urn:ietf:wg:oauth:2.0:oob") -> str:
    return AUTH_URL + "?" + urlencode(
        {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": SCOPES.strip(),
            "access_type": "offline",
            "prompt": "consent",
        }
    )


def exchange_code(client_id: str, client_secret: str, code: str, redirect_uri: str = "urn:ietf:wg:oauth:2.0:oob") -> dict:
    result = form_request(
        TOKEN_URL,
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        },
    )
    if not result.get("refresh_token"):
        return {
            "status": "ERROR",
            "error": result.get("error") or "no refresh_token in response",
            "detail": result.get("detail") or result.get("error_description"),
        }
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": result["refresh_token"],
        "ga4_property_id": "",
    }
    path = save_google_credentials(payload)
    return {"status": "OK", "path": str(path)}


def setup_interactive() -> int:
    print("Google OAuth setup (installed-app / copy-paste).")
    print("Create a Desktop OAuth client in Google Cloud Console.")
    print("Scopes: webmasters.readonly, analytics.readonly")
    client_id = input("client_id: ").strip()
    client_secret = input("client_secret: ").strip()
    if not client_id or not client_secret:
        print("client_id and client_secret are required.", file=sys.stderr)
        return 2
    print("\nOpen this URL, then paste the code:\n")
    print(authorization_url(client_id))
    print()
    code = input("authorization code: ").strip()
    result = exchange_code(client_id, client_secret, code)
    print(json.dumps(result, indent=2))
    return 0 if result.get("status") == "OK" else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SEO Skills AI Google OAuth")
    parser.add_argument("--setup", action="store_true", help="Interactive copy-paste OAuth flow")
    parser.add_argument("--status", action="store_true", help="Print local credential status")
    args = parser.parse_args()
    if args.setup:
        raise SystemExit(setup_interactive())
    print(json.dumps(get_tier_status(), indent=2))
