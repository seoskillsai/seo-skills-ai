# Deployment map — SEO Skills AI

Public, no-secret inventory of where this project lives and what v1.1.1 shipped.

## Canonical locations

| What | Where |
| --- | --- |
| GitHub repository | https://github.com/seoskillsai/seo-skills-ai |
| Website | https://seoskillsai.com |
| Default branch | `main` |
| Current release line | **1.1.1** (security boundaries + scanner CI) |
| Local Cursor / git workspace | `C:\Users\sutar\Documents\Cursor\Websites\seoskillsai.comREPO` |
| Claude plugin manifest | `.claude-plugin/plugin.json` |
| Codex plugin manifest | `.codex-plugin/plugin.json` |
| Marketplace metadata | `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json` |
| MCP stdio server | `scripts/mcp_server.py` (example: `config/cline_mcp_settings.json`) |
| Network-target policy | `scripts/url_safety.py` |
| Filesystem / repo scope | `scripts/path_safety.py` |
| Review-only patches | `scripts/remediation_engine.py` (no `--apply`) |
| Test suites | `python tests/run_all_tests.py` and `python -m pytest tests -q` |

## GitHub Actions (run on every push / PR to `main`)

| Workflow | File | Purpose |
| --- | --- | --- |
| Multi-agent CI | `.github/workflows/ci.yml` | Portability, doctor, unittest, pytest. SHA-pinned checkout + setup-python. `permissions: contents: read` |
| HOL plugin-scanner | `.github/workflows/plugin-scan.yml` | Catalog gate: score ≥ 80, `fail_on_severity: high` |
| Dependabot | `.github/dependabot.yml` | Weekly GitHub Actions, pip, npm |

Scanner listing target: [awesome-ai-plugins](https://github.com/hashgraph-online/awesome-ai-plugins) (Cross-AI tools). Submit a PR **only after** `plugin-scan.yml` is green.

## Credentials (never commit)

Real tokens live only in gitignored files:

| File | Role |
| --- | --- |
| `config/credentials.json` | Workspace GitHub PAT (gitignored) |
| `config/credentials.example.json` | Shape only; placeholder token |
| `~/.config/seoskillsai/credentials.json` | Same map on the user machine |
| `config/deployment-local.json` | Local ops log (gitignored): last commit, push time, paths |

Copy the example, then paste a PAT locally:

```powershell
Copy-Item config\credentials.example.json config\credentials.json
```

Optional vendor keys (Moz, Bing, DataForSEO, etc.) also belong under `~/.config/seoskillsai/` with `0o600` permissions — not in git.

## What v1.1.1 changed (2026-08-20)

1. Explicit **network-target policy** (scheme, fail-closed DNS, private/metadata IPs, redirect re-check, optional `SEOSKILLS_ALLOWED_HOSTS`; Playwright uses the same policy).
2. Explicit **workspace write scope** (`SEOSKILLS_OUT_DIR` / cwd). Generated `llms.txt`, RSS, screenshots, reports cannot escape the root.
3. **MCP:** `initialize` + URL checks; shipped Cline config has **no** `autoApprove`.
4. **Patches are review-only**; `--apply` is refused.
5. Install docs use `seoskillsai/seo-skills-ai` (the old `seo-skills` clone URL 404’d). `@seoskillsai/cli` is documented as unpublished.
6. PageSpeed / IndexNow / Moz / Bing stubs no longer invent success metrics.

## Push from this machine

From the workspace root, with `config/credentials.json` present:

```powershell
python -c "import json,subprocess,os; from pathlib import Path; t=json.loads(Path('config/credentials.json').read_text(encoding='utf-8'))['github']['token']; r=subprocess.run(['git','-c',f'http.extraHeader=AUTHORIZATION: bearer {t}','push','origin','HEAD'], check=False); raise SystemExit(r.returncode)"
```

Do not put the PAT in the remote URL in `.git/config`. Do not commit `config/credentials.json`.

## After a push

1. Confirm Actions: https://github.com/seoskillsai/seo-skills-ai/actions
2. If `plugin-scan.yml` fails on MCP / headless Chrome, keep the finding and ask the awesome-ai-plugins maintainer who offered to interpret it.
3. Only then open a listing PR against `hashgraph-online/awesome-ai-plugins`.
