#!/usr/bin/env python3
"""
Post-write hook: validate the tool's target path stays in the workspace.
Does not apply patches. Reads Claude-style JSON from stdin or a path argv.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.path_safety import resolve_workspace_path


def _extract_path(payload: dict) -> str | None:
    tool_input = payload.get("tool_input") or payload.get("input") or {}
    if isinstance(tool_input, dict):
        for key in ("file_path", "path", "filePath", "file"):
            value = tool_input.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    for key in ("file_path", "path", "filePath", "file"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def main() -> int:
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    path = None
    if raw.strip():
        try:
            path = _extract_path(json.loads(raw))
        except json.JSONDecodeError:
            path = None
    if not path and len(sys.argv) > 1:
        path = sys.argv[1]
    if not path:
        return 0
    try:
        resolve_workspace_path(path)
    except (PermissionError, FileNotFoundError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
