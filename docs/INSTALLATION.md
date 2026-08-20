# Installation & Setup Guide: SEO Skills AI

## Option A — git clone (works today)

```bash
git clone https://github.com/seoskillsai/seo-skills-ai.git
cd seo-skills-ai
node packages/cli/index.mjs add cursor
```

Unix / macOS: `bash install.sh`  
Windows: `powershell -ExecutionPolicy Bypass -File .\install.ps1`

## Option B — npm (`@seoskillsai/cli`)

The package metadata and `files` list are ready so `npx @seoskillsai/cli add cursor` copies skills from the tarball. **It is not published** until an npm automation token is stored in gitignored `~/.config/seoskillsai/` (or `npm login`). Do not advertise `npx` until `npm view @seoskillsai/cli version` succeeds.

`install.sh` / `install.ps1` create `~/.config/seoskillsai/venv` and install optional Playwright Chromium. `/seo setup` only initializes the local SQLite drift database. `/seo doctor` checks Python, SQLite, skills, and reports Playwright as optional.

---

## Google Search Console and GA4 (optional)

This plugin does **not** include Google Cloud client IDs or anyone else's analytics properties.

1. In Google Cloud Console, create an OAuth **Desktop** client.
2. Enable Search Console API and Google Analytics Data API.
3. Create `~/.config/seoskillsai/google_credentials.json` (mode `0o600`) with `client_id`, `client_secret`, `refresh_token`, and optional `ga4_property_id`. Do not commit this file.
4. Run `python scripts/google_oauth.py --setup` (copy-paste authorization code). The file is written mode `0o600`.

**Scopes**

- `https://www.googleapis.com/auth/webmasters.readonly`
- `https://www.googleapis.com/auth/analytics.readonly`

Optional extras: `pip install -e ".[google]"` (stdlib urllib is enough for the shipped clients).

Set `ga4_property_id` in the same JSON for GA4 organic sessions. Without credentials, GSC/GA4 scripts return `UNAVAILABLE` and invent **no** numbers.

---

## Vendor env vars (optional)

| Variable | Used by |
| --- | --- |
| `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` | `scripts/dataforseo_api.py` |
| `FIRECRAWL_API_KEY` | `scripts/firecrawl_api.py` |
| `BING_WEBMASTER_API_KEY` | `scripts/bing_webmaster.py` |
| `SEOSKILLS_STRICT_BROWSER=1` | Playwright subresource allowlist |
| `SEOSKILLS_ALLOWED_HOSTS` | optional host allowlist |

---

## Claude Code CLI

```text
/plugin marketplace add seoskillsai/seo-skills-ai
/plugin install seo-skills@seoskillsai-seo-skills
/seo setup
/seo doctor
```

## Other harnesses

Point Antigravity, Cursor, Windsurf, Codex, or Cline at the cloned (or CLI-copied) repository root. `AGENTS.md`, `.cursorrules`, `.windsurfrules`, and `skills/` load from that root.

There is **no** hosted `https://api.seoskillsai.com` API in this repository. Use `scripts/mcp_server.py` or the Python CLIs. `config/openapi-schema.json` is marked not-shipped.
