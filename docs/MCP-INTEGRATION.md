# Model Context Protocol (MCP) Integration Guide

Connect SEO Skills AI to Cline, Roo Code, Cursor, or Claude Desktop via stdio JSON-RPC (`scripts/mcp_server.py`).

---

## 1. VS Code Cline / Roo Code Setup

Use `config/cline_mcp_settings.json` (or copy it into Cline settings):

```json
{
  "mcpServers": {
    "seoskillsai": {
      "command": "python",
      "args": ["scripts/mcp_server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

Do **not** add `autoApprove` for `seo_audit` or `seo_drift`. Those tools fetch the URL you pass and must stay behind the host agent's confirmation prompt.

---

## 2. Available MCP Tools

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `seo_audit` | `url: string` | Full-site audit. URL must pass `scripts/url_safety.py`. |
| `seo_schema` | `schema_json: string` | Validate JSON-LD. No network. |
| `seo_drift` | `url: string` | Compare live URL to the local SQLite baseline. URL must pass the network-target policy. |

The server implements `initialize`, `ping`, `tools/list`, and `tools/call`. It does not apply code patches.
