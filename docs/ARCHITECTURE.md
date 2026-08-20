# Universal Multi-Agent System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DIRECTIVE LAYER (SKILLS)                          │
│   27 Standardized SKILL.md modules (Technical, EAV Content, Schema, GEO)   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Dispatches
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATION LAYER (SUBAGENTS)                      │
│   18 Specialist Subagent Definitions (Parallel fan-out execution)           │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Executes
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         EXECUTION LAYER (PYTHON ENGINE)                     │
│   42 Core Scripts: GSC API, SQLite Drift, Playwright, Schema Validator      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Supported Agent Interfaces
- **Claude Code CLI:** `.claude-plugin/plugin.json` & `CLAUDE.md`
- **Google Antigravity IDE:** Native `AGENTS.md` & `.agent/skills/`
- **Cursor IDE & Windsurf:** `.cursorrules` & `.windsurfrules`
- **ChatGPT & Codex:** `config/openapi-schema.json`
- **Cline & Roo Code:** `config/cline_mcp_settings.json`
- **Aider CLI:** `config/.aider.conf.yml`
