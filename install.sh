#!/usr/bin/env bash
# ==============================================================================
# SEO Skills AI — Isolated Runtime Installer (Unix / macOS / Linux)
# ==============================================================================
set -euo pipefail

INSTALL_DIR="${HOME}/.config/seoskillsai"
VENV_DIR="${INSTALL_DIR}/venv"

echo "==> [SEO Skills AI] Initializing isolated runtime..."
mkdir -p "${INSTALL_DIR}"

# Check for Python 3.10+
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "ERROR: Python 3.10+ is required but not found in PATH." >&2
    exit 1
fi

echo "==> [SEO Skills AI] Using Python at $(${PYTHON_BIN} --version)..."

# Create isolated venv if not exists
if [ ! -d "${VENV_DIR}" ]; then
    echo "==> [SEO Skills AI] Creating isolated virtualenv in ${VENV_DIR}..."
    "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

# Upgrade pip and install baseline dependencies
"${VENV_DIR}/bin/python" -m pip install --quiet --upgrade pip setuptools wheel
"${VENV_DIR}/bin/python" -m pip install --quiet requests beautifulsoup4 urllib3 pytest playwright

echo "==> [SEO Skills AI] Installing Playwright Chromium browser..."
"${VENV_DIR}/bin/python" -m playwright install --with-deps chromium || echo "Playwright dependencies skipped or already present."

echo "==> [SEO Skills AI] Setup complete! You can now run:"
echo "    /seo setup"
echo "    /seo doctor"
echo "    /seo audit https://example.com"
