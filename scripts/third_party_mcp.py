#!/usr/bin/env python3
"""Placeholder for third-party MCP vendors we do not bundle."""
import json
import sys

name = sys.argv[1] if len(sys.argv) > 1 else "vendor"
print(
    json.dumps(
        {
            "status": "UNAVAILABLE",
            "vendor": name,
            "notice": "Third-party MCP only. This repository does not bundle or implement that vendor's server. Install their official MCP with your own API key.",
        },
        indent=2,
    )
)
