# Model Context Protocol (MCP) Integration Guide

Connect SEO Skills AI to Claude Desktop, VS Code Cline, Cursor IDE, and Roo Code via standard JSON-RPC.

---

## 1. VS Code Cline / Roo Code Setup

Add to `cline_mcp_settings.json`:
```json
{
  "mcpServers": {
    "seoskillsai": {
      "command": "python",
      "args": ["scripts/mcp_server.py"]
    }
  }
}
```

---

## 2. Available MCP Tools

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `seo_audit` | `url: string` | Runs parallel multi-agent full site audit. |
| `seo_schema` | `schema_json: string` | Deep validation of 2026 Schema.org structured data graphs. |
| `seo_drift` | `url: string` | Compares live on-page signals against latest SQLite baseline. |
