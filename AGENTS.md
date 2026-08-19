# SEO Skills AI: Universal Multi-Platform Agent Instructions

> **Applies to:** Anthropic Claude Code, Google Antigravity IDE, Gemini CLI, Cursor IDE, Windsurf Cascade, OpenAI ChatGPT / Codex CLI, Cline, Roo Code, Aider CLI, Grok Build, DeepSeek R1, and Nous Hermes Agent.
>
> Claude Code CLI users: see `CLAUDE.md`.

---

## 1. Universal Cross-Platform Portability

Every skill in `skills/*/SKILL.md` is authored to the **open Agent Skills specification**. This repository is 100% harness-agnostic.

To verify compatibility with your active agent runtime:
```bash
python scripts/portability_check.py
```

### Agent Harness Loading Directives

| AI Agent Harness | How to Load & Execute SEO Skills AI |
| :--- | :--- |
| **Google Antigravity & Gemini CLI** | Point workspace at repository root. Antigravity reads `AGENTS.md` automatically and auto-discovers all skills in `skills/`. |
| **Cursor IDE** | Reads `.cursorrules` from root. Skills are auto-discovered from `skills/` or symlinked to `.cursor/rules/`. |
| **Windsurf Cascade** | Reads `.windsurfrules` from root. Cascade flows execute multi-file refactoring and sitemap generation. |
| **Anthropic Claude Code** | Auto-discovered via `.claude-plugin/plugin.json` or invoked via `/seo [command]`. |
| **OpenAI ChatGPT / Codex CLI** | Reads `AGENTS.md` at root. Custom Actions utilize `config/openapi-schema.json`. |
| **Cline & Roo Code (VS Code)** | Loads `AGENTS.md` from root. MCP tools are configured in `config/cline_mcp_settings.json`. |
| **Aider CLI** | Reads `AGENTS.md` from root. Executes SEO refactoring directly with automatic Git diff commits. |
| **DeepSeek R1 / Local Ollama** | Contextually ingest `skills/{skill}/SKILL.md` for zero-token-cost local execution. |

---

## 2. Universal Tool-Name Mapping

Where skills reference tool execution commands, each harness maps them transparently:

| Action | Claude Code | Codex / ChatGPT | Cline / Roo Code | Cursor / Antigravity | Aider |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Read File** | `Read` | `read_file` | `read_file` | `read` / `view_file` | inline |
| **Write File** | `Write` | `write_file` | `write_file` | `write` / `write_to_file` | `/add` then edit |
| **Edit Block** | `Edit` | `apply_diff` | `replace_in_file` | `edit` / `replace_file_content` | `/edit` |
| **Run Command**| `Bash` | `bash` | `execute_command` | `shell` / `run_command` | `/run` |
| **Grep / Search**| `Grep` | `grep` | `search_files` | `grep` / `grep_search` | `/grep` |
| **Find Files** | `Glob` | `glob` | `search_files` | `find` / `find_by_name` | inline |
| **Fetch Web** | `WebFetch` | `fetch` | `browser_tool` | `fetch` / `read_url_content` | inline |

---

## 3. Core Architectural Rules

When executing any SEO analysis or generating content:

1. **Holistic Semantic SEO Standard:**
   - Always perform **Entity-Attribute-Value (EAV)** modeling before drafting.
   - Enforce **800+ words of structured educational prose** beneath any interactive widget or calculator.
   - Enforce **Directional Internal Link Conduits** (Outer Nodes $\rightarrow$ Category Silo Hub $\rightarrow$ Core Pillar).
   - Enforce **3x Anchor Diversity Rule**: Exact-match anchor text must never appear more than 3 times sitewide.

2. **2026 Structured Data Standard:**
   - Only output valid, non-deprecated Schema.org JSON-LD.
   - Never generate deprecated types (`HowTo`, `SpecialAnnouncement`, `ClaimReview`).
   - Group schemas into a unified `@graph` including `TechArticle`, `SoftwareApplication`, `SoftwareSourceCode`, `BreadcrumbList`, and `FAQPage`.

3. **Zero-Hallucination & Falsifiability:**
   - Every diagnostic finding must reference exact primary evidence (DOM node, HTTP status, header value, CrUX field metric).
   - Recommendations must include a falsifiability check (*"How would we know this failed?"*).

---

## 4. Master Command Routing Table

```
/seo audit <url>              -> skills/seo-audit/SKILL.md
/seo technical <url>          -> skills/seo-technical/SKILL.md
/seo content <url>            -> skills/seo-content/SKILL.md
/seo content-brief <topic>    -> skills/seo-content-brief/SKILL.md
/seo schema <url>             -> skills/seo-schema/SKILL.md
/seo llms-txt <url>           -> skills/seo-llms-txt/SKILL.md
/seo robots-ai <url>          -> skills/seo-robots-ai/SKILL.md
/seo discover <url>           -> skills/seo-discover/SKILL.md
/seo sitemap <url>            -> skills/seo-sitemap/SKILL.md
/seo sxo <url>                -> skills/seo-sxo/SKILL.md
/seo geo <url>                -> skills/seo-geo/SKILL.md
/seo drift <url>              -> skills/seo-drift/SKILL.md
/seo google [command]         -> skills/seo-google/SKILL.md
/seo backlinks <url>          -> skills/seo-backlinks/SKILL.md
/seo cluster <seed>           -> skills/seo-cluster/SKILL.md
/seo local <url>              -> skills/seo-local/SKILL.md
/seo maps <url>               -> skills/seo-maps/SKILL.md
/seo plan <type>              -> skills/seo-plan/SKILL.md
/seo flow [stage]             -> skills/seo-flow/SKILL.md
/seo programmatic <url>       -> skills/seo-programmatic/SKILL.md
/seo competitor-pages <url>   -> skills/seo-competitor-pages/SKILL.md
/seo hreflang <url>           -> skills/seo-hreflang/SKILL.md
/seo ecommerce <url>          -> skills/seo-ecommerce/SKILL.md
/seo images <url>             -> skills/seo-images/SKILL.md
/seo dataforseo [command]     -> skills/seo-dataforseo/SKILL.md
```
