# Privacy Policy: SEO Skills AI

SEO Skills AI is designed to run on your machine:

1. **No product telemetry:** The skill suite does not send analytics, cookies, or session data to seoskillsai.com.
2. **Local artifacts:** SQLite drift baselines and generated reports stay on the local filesystem (workspace or `~/.config/seoskillsai/`).
3. **Credentials:** Optional API keys stay in `~/.config/seoskillsai/` and are gitignored.
4. **Explicit third-party calls:** When you run PageSpeed, CrUX, RDAP, IndexNow, or a vendor MCP extension, the URL or query you provided is sent to that vendor. Those calls are opt-in by command, not background tracking.
