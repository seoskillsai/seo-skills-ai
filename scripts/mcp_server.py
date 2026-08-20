#!/usr/bin/env python3
"""
SEO Skills AI — Model Context Protocol (MCP) Server

Network tools validate URLs with scripts/url_safety.py before fetching.
This server never auto-approves tools; host configs must not set autoApprove
for seo_audit / seo_drift. Patches are not applied from MCP.
"""
import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from scripts.full_audit import run_full_audit
from scripts.schema_validator import validate_schema_json
from scripts.drift_compare import compare_drift
from scripts.gsc_query import query_gsc
from scripts.ga4_report import fetch_ga4_organic_report
from scripts.url_safety import validate_url

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "seoskillsai", "version": "1.2.0"}

TOOLS = [
    {
        "name": "seo_audit",
        "description": "Run a full-site SEO audit. The URL must pass the network-target policy (public http/https only).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Public http(s) website URL"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "seo_schema",
        "description": "Validate Schema.org JSON-LD structured data. Does not fetch URLs or write files.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "schema_json": {"type": "string", "description": "Raw JSON-LD string"}
            },
            "required": ["schema_json"]
        }
    },
    {
        "name": "seo_drift",
        "description": "Compare a live public URL against the local SQLite baseline. URL must pass the network-target policy.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Public http(s) website URL"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "seo_gsc",
        "description": "Google Search Console Search Analytics for a user-supplied site URL. Returns UNAVAILABLE until local OAuth credentials exist.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "site_url": {"type": "string", "description": "Search Console property URL (sc-domain: or https://)"},
                "filter": {"type": "string", "description": "all or striking-distance"}
            },
            "required": ["site_url"]
        }
    },
    {
        "name": "seo_ga4",
        "description": "GA4 Data API organic-search sessions. Returns UNAVAILABLE unless ga4_property_id is in local Google credentials.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "property_id": {"type": "string", "description": "Optional GA4 numeric property id override"}
            }
        }
    }
]


def _tool_error(req_id, message: str):
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "content": [{"type": "text", "text": json.dumps({"error": message}, indent=2)}],
            "isError": True,
        },
    }


def _tool_text(req_id, payload) -> dict:
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {"content": [{"type": "text", "text": json.dumps(payload, indent=2)}]},
    }


def _require_public_url(args: dict) -> str:
    url = args.get("url")
    if not isinstance(url, str) or not url.strip():
        raise ValueError("url is required")
    validate_url(url.strip(), role="navigation")
    return url.strip()


def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": SERVER_INFO,
            },
        }
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {}) or {}

        try:
            if tool_name == "seo_audit":
                url = _require_public_url(args)
                return _tool_text(req_id, run_full_audit(url))
            if tool_name == "seo_schema":
                schema_json = args.get("schema_json")
                return _tool_text(req_id, validate_schema_json(schema_json))
            if tool_name == "seo_drift":
                url = _require_public_url(args)
                return _tool_text(req_id, compare_drift(url))
            if tool_name == "seo_gsc":
                site_url = args.get("site_url") or args.get("url")
                if not isinstance(site_url, str) or not site_url.strip():
                    raise ValueError("site_url is required")
                return _tool_text(req_id, query_gsc(site_url.strip(), filter_type=args.get("filter") or "striking-distance"))
            if tool_name == "seo_ga4":
                pid = args.get("property_id")
                return _tool_text(req_id, fetch_ga4_organic_report(pid if isinstance(pid, str) else None))
        except (ValueError, PermissionError) as exc:
            return _tool_error(req_id, str(exc))

        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


def run_mcp_server():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line.strip())
            resp = handle_request(req)
            if resp is None:
                continue
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    run_mcp_server()
