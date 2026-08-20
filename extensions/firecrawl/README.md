# Firecrawl — first-party Python (optional vendor MCP)

First-party scrape: `scripts/firecrawl_api.py` with `FIRECRAWL_API_KEY`. User URLs still pass `url_safety`.

Optional third-party MCP (`npx firecrawl-mcp`) is **not bundled**. Local crawls without a key: `scripts/site_crawler.py`.

```bash
python scripts/firecrawl_api.py https://example.com
```
