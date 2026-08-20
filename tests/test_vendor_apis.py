from scripts.dataforseo_api import fetch_live_serp
from scripts.firecrawl_api import scrape_url
from scripts.bing_webmaster import fetch_bing_metrics


def test_dataforseo_unavailable_without_env(monkeypatch):
    monkeypatch.delenv("DATAFORSEO_LOGIN", raising=False)
    monkeypatch.delenv("DATAFORSEO_PASSWORD", raising=False)
    res = fetch_live_serp("ai seo")
    assert res["status"] == "UNAVAILABLE"
    assert "items" not in res


def test_dataforseo_mocked_serp(monkeypatch):
    monkeypatch.setenv("DATAFORSEO_LOGIN", "user")
    monkeypatch.setenv("DATAFORSEO_PASSWORD", "pass")
    monkeypatch.setattr(
        "scripts.dataforseo_api.json_request",
        lambda *a, **k: {
            "tasks": [
                {
                    "result": [
                        {
                            "items": [
                                {
                                    "type": "organic",
                                    "rank_group": 1,
                                    "url": "https://example.com",
                                    "title": "Example",
                                    "description": "Desc",
                                }
                            ]
                        }
                    ]
                }
            ]
        },
    )
    res = fetch_live_serp("ai seo")
    assert res["status"] == "OK"
    assert res["items"][0]["url"] == "https://example.com"


def test_firecrawl_blocks_private():
    res = scrape_url("http://127.0.0.1/")
    assert res["status"] == "BLOCKED"


def test_firecrawl_unavailable_without_key(monkeypatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    res = scrape_url("https://example.com")
    assert res["status"] == "UNAVAILABLE"


def test_firecrawl_mocked(monkeypatch):
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test")
    monkeypatch.setattr(
        "scripts.firecrawl_api.json_request",
        lambda *a, **k: {"data": {"markdown": "# Hi", "metadata": {"title": "Example Domain"}}},
    )
    res = scrape_url("https://example.com")
    assert res["status"] == "OK"
    assert res["title"] == "Example Domain"


def test_bing_unavailable_without_key(monkeypatch):
    monkeypatch.delenv("BING_API_KEY", raising=False)
    monkeypatch.delenv("BING_WEBMASTER_API_KEY", raising=False)
    res = fetch_bing_metrics("https://example.com")
    assert res["status"] == "UNAVAILABLE"
    assert "impressions" not in res


def test_bing_mocked(monkeypatch):
    monkeypatch.setenv("BING_WEBMASTER_API_KEY", "bing-test")
    monkeypatch.setattr(
        "scripts.bing_webmaster.json_request",
        lambda url, **k: {"d": [{"Query": "example", "Impressions": 10}]} if "GetQueryStats" in url else {"d": []},
    )
    res = fetch_bing_metrics("https://example.com")
    assert res["status"] == "OK"
    assert res["query_stats"][0]["Query"] == "example"
