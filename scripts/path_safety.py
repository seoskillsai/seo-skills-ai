#!/usr/bin/env python3
"""
SEO Skills AI — Filesystem / repo scope for generated files.
Writes stay inside SEOSKILLS_OUT_DIR (default: process cwd). Generated
patches are never auto-applied; see remediation_engine.py.
"""
import os
import sys
from pathlib import Path


def workspace_root() -> Path:
    env = os.environ.get("SEOSKILLS_OUT_DIR") or os.environ.get("SEOSKILLS_WORKSPACE")
    if env:
        return Path(env).expanduser().resolve()
    return Path.cwd().resolve()


def resolve_workspace_path(path: str | os.PathLike, *, must_exist: bool = False) -> Path:
    root = workspace_root()
    raw = Path(path).expanduser()
    target = raw.resolve() if raw.is_absolute() else (root / raw).resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise PermissionError(
            f"Security Alert: path {target} is outside workspace root {root}. "
            "Set SEOSKILLS_OUT_DIR to expand the allowed write/read scope."
        ) from exc
    if must_exist and not target.exists():
        raise FileNotFoundError(str(target))
    return target


def prepare_output_file(path: str | os.PathLike) -> Path:
    target = resolve_workspace_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python path_safety.py <path>")
        sys.exit(1)
    try:
        resolved = resolve_workspace_path(sys.argv[1])
        print(f"[SAFE] {resolved}")
        sys.exit(0)
    except Exception as e:
        print(f"[BLOCKED] {e}", file=sys.stderr)
        sys.exit(1)
