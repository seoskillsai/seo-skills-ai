# Security Policy: SEO Skills AI

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 1.1.x   | Yes       |
| < 1.1   | No        |

## Security Boundaries

Skills inherit the host agent's tools. This repository adds two extra fences so an SEO skill cannot silently use the agent's full network or filesystem reach.

### 1. Network-target policy (`scripts/url_safety.py`)

Every user-supplied URL is checked **before** HTTP fetch, MCP `seo_audit` / `seo_drift`, the crawler, and Playwright navigation:

- `http` and `https` only
- DNS must resolve (fail closed)
- Loopback, RFC1918, link-local, metadata (`169.254.169.254`), and other non-routable ranges are blocked
- **Redirect hops are re-validated**
- Optional allowlist: `SEOSKILLS_ALLOWED_HOSTS=example.com,www.example.com`
- Headless Chromium subresources use the same private-IP block; set `SEOSKILLS_STRICT_BROWSER=1` to apply the allowlist to subresources too

Shipped MCP config does **not** auto-approve tools. Host agents must prompt before `seo_audit` / `seo_drift`.

### 2. Filesystem / repo scope (`scripts/path_safety.py`)

Generated files (`llms.txt`, RSS, screenshots, HTML reports) may only be written under `SEOSKILLS_OUT_DIR` (default: the process working directory).

`scripts/remediation_engine.py` **prints patches for review**. It never writes them into the repo. There is no `--apply` mode.

Optional credentials stay in `~/.config/seoskillsai/` with `0o600` permissions and are gitignored.

## Privacy

- This project does not phone home or collect telemetry for SEO Skills AI.
- Optional third-party APIs (PageSpeed Insights, CrUX, RDAP, IndexNow, Moz, Bing, DataForSEO) send the **target URL you asked to audit** to those vendors when you invoke those scripts. They are not silent trackers.

## Reporting a Vulnerability

Email **security@seoskillsai.com** with reproducible steps. Please do not open a public GitHub issue for undisclosed vulnerabilities.
