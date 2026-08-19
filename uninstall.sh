#!/usr/bin/env bash
set -e

echo "==> [SEO Skills AI] Uninstalling runtime and local configurations..."

CONFIG_DIR="$HOME/.config/seoskillsai"
if [ -d "$CONFIG_DIR" ]; then
    rm -rf "$CONFIG_DIR"
    echo "  ✔ Removed configuration directory: $CONFIG_DIR"
fi

echo "✔ [SEO Skills AI] Uninstallation completed cleanly."
