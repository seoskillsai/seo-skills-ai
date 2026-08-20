# Installation & Setup Guide: SEO Skills AI

Clone the public repository and open that folder as the agent workspace.

```bash
git clone https://github.com/seoskillsai/seo-skills-ai.git
cd seo-skills-ai
```

Unix / macOS: `bash install.sh`  
Windows: `powershell -ExecutionPolicy Bypass -File .\install.ps1`

`install.sh` / `install.ps1` create `~/.config/seoskillsai/venv` and install optional Playwright Chromium. `/seo setup` only initializes the local SQLite drift database. `/seo doctor` checks Python, SQLite, skills, and reports Playwright as optional.

The npm package `@seoskillsai/cli` is not published.

---

## Claude Code CLI

```text
/plugin marketplace add seoskillsai/seo-skills-ai
/plugin install seo-skills@seoskillsai-seo-skills
/seo setup
/seo doctor
```

## Other harnesses

Point Antigravity, Cursor, Windsurf, Codex, or Cline at the cloned repository root. `AGENTS.md`, `.cursorrules`, `.windsurfrules`, and `skills/` load from that root.
