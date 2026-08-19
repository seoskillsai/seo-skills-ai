#!/usr/bin/env python3
"""
SEO Skills AI — Model Context Protocol (MCP) Server
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
from scripts.llms_txt_builder import generate_llms_txt

TOOLS = [
    {
        "name": "seo_audit",
        "description": "Run parallel full-site multi-agent AI SEO audit",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target website URL"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "seo_schema",
        "description": "Validate 2026 Schema.org JSON-LD structured data",
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
        "description": "Compare live site against latest SQLite baseline to detect SEO regressions",
        "inputSchema": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "Target website URL"}
            },
            "required": ["url"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "seo_audit":
            url = args.get("url")
            res = run_full_audit(url)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tool_name == "seo_schema":
            schema_json = args.get("schema_json")
            res = validate_schema_json(schema_json)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tool_name == "seo_drift":
            url = args.get("url")
            res = compare_drift(url)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def run_mcp_server():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line.strip())
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run_mcp_server()
