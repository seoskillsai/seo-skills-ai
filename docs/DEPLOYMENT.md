# Deployment map — SEO Skills AI

Public, no-secret inventory of where this project lives and what v1.2.0 shipped.

## Canonical locations

| What | Where |
| --- | --- |
| GitHub repository | https://github.com/seoskillsai/seo-skills-ai |
| Website | https://seoskillsai.com |
| npm CLI | `@seoskillsai/cli` |
| Default branch | `main` |
| Current release line | **1.2.0** |
| Local Cursor / git workspace | `C:\Users\sutar\Documents\Cursor\Websites\seoskillsai.comREPO` |
| Claude plugin manifest | `.claude-plugin/plugin.json` |
| Codex plugin manifest | `.codex-plugin/plugin.json` |
| Claude marketplace | `.claude-plugin/marketplace.json` |
| Codex marketplace | `.agents/plugins/marketplace.json` |
| MCP stdio + Cisco scan root | `.mcp.json` + `scripts/mcp_server.py` |
| Network-target policy | `scripts/url_safety.py` |
| Filesystem / repo scope | `scripts/path_safety.py` |
| Host-agent hooks | `hooks/hooks.json` |
| Review-only patches | `scripts/remediation_engine.py` (no `--apply`) |
| Test suites | `python tests/run_all_tests.py` and `python -m pytest tests -q` |

## GitHub Actions (run on every push / PR to `main`)

| Workflow | File | Purpose |
| --- | --- | --- |
| Multi-agent CI | `.github/workflows/ci.yml` | Portability, doctor, unittest, pytest, live example.com smoke |
| HOL plugin-scanner | `.github/workflows/plugin-scan.yml` | Catalog gate: score ≥ 80, `fail_on_severity: high` |
| Dependabot | `.github/dependabot.yml` | Weekly GitHub Actions, pip, npm |

Scanner listing target: [awesome-ai-plugins](https://github.com/hashgraph-online/awesome-ai-plugins) (Cross-AI tools). Submit a PR **only after** `plugin-scan.yml` is green.

## Credentials (never commit)

Real tokens live only in gitignored files:

| File | Role |
| --- | --- |
| `config/credentials.json` | Workspace GitHub PAT (gitignored). Rotate if it ever appeared in chat. |
| `config/credentials.example.json` | Shape only; placeholder token |
| `~/.config/seoskillsai/credentials.json` | Same map on the user machine |
| `~/.config/seoskillsai/google_credentials.json` | GSC/GA4 OAuth (mode 0o600) |
| `config/deployment-local.json` | Local ops log (gitignored) |

Copy the example, then paste a PAT locally:

```powershell
Copy-Item config\credentials.example.json config\credentials.json
```

Optional vendor keys (Moz, Bing, DataForSEO, Firecrawl, Google OAuth) belong under `~/.config/seoskillsai/` with `0o600` permissions — not in git. Do **not** import the private Websites analytics identity DB into this public plugin.

## What v1.2.0 changed (2026-08-20)

1. HOL scanner metadata (Codex plugin/marketplace, skills frontmatter, lockfiles, `.mcp.json`, `.codexignore`).
2. Honest GSC/GA4 (`UNAVAILABLE` without OAuth) plus real Search Analytics / GA4 Data API when creds exist.
3. First-party DataForSEO / Firecrawl / Bing HTTP; third-party MCP labeled as not ours.
4. `@seoskillsai/cli` copies package contents; OpenAPI marked not-shipped.
5. PreToolUse url/path hooks, Playwright abort helper, DNS revalidation after connect.

## Push from this machine

From the workspace root, with `config/credentials.json` present, use `Authorization: Basic` of `x-access-token:PAT` (not a PAT in `.git/config`). Do not commit `config/credentials.json`.

## After a push

1. Confirm Actions: https://github.com/seoskillsai/seo-skills-ai/actions
2. If `plugin-scan.yml` is green (score ≥ 80, 0 high/critical), open the awesome-ai-plugins listing PR.
3. If a new MCP/browser **High** appears, use the Reddit maintainer offer — not for leftover mediums.
