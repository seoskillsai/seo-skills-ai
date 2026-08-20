import json

from scripts.ga4_report import fetch_ga4_organic_report
from scripts.gsc_query import query_gsc
from scripts.google_oauth import get_tier_status, unavailable
from scripts.mcp_server import handle_request


def test_gsc_unavailable_without_creds(monkeypatch):
    monkeypatch.setattr("scripts.gsc_query.load_google_credentials", lambda: None)
    res = query_gsc("https://example.com")
    assert res["status"] == "UNAVAILABLE"
    assert "clicks" not in res
    assert "total_clicks" not in res


def test_gsc_blocks_private_property():
    res = query_gsc("http://127.0.0.1/")
    assert res["status"] == "BLOCKED"


def test_gsc_mocked_searchanalytics(monkeypatch):
    monkeypatch.setattr(
        "scripts.gsc_query.load_google_credentials",
        lambda: {"client_id": "id", "client_secret": "secret", "refresh_token": "rt"},
    )
    monkeypatch.setattr(
        "scripts.gsc_query.refresh_access_token",
        lambda creds=None: {"status": "OK", "access_token": "ya29.test"},
    )
    monkeypatch.setattr(
        "scripts.gsc_query.json_request",
        lambda *a, **k: {
            "rows": [
                {"keys": ["ai seo"], "clicks": 12, "impressions": 400, "ctr": 0.03, "position": 9.2},
                {"keys": ["brand"], "clicks": 80, "impressions": 200, "ctr": 0.4, "position": 2.1},
            ]
        },
    )
    res = query_gsc("https://example.com", filter_type="striking-distance")
    assert res["status"] == "OK"
    assert res["row_count"] == 1
    assert res["keywords"][0]["query"] == "ai seo"


def test_ga4_unavailable_without_creds(monkeypatch):
    monkeypatch.setattr("scripts.ga4_report.load_google_credentials", lambda: None)
    res = fetch_ga4_organic_report()
    assert res["status"] == "UNAVAILABLE"
    assert "organic_sessions" not in res


def test_ga4_mocked_report(monkeypatch):
    monkeypatch.setattr(
        "scripts.ga4_report.load_google_credentials",
        lambda: {
            "client_id": "id",
            "client_secret": "secret",
            "refresh_token": "rt",
            "ga4_property_id": "123456",
        },
    )
    monkeypatch.setattr(
        "scripts.ga4_report.refresh_access_token",
        lambda creds=None: {"status": "OK", "access_token": "ya29.test"},
    )
    monkeypatch.setattr(
        "scripts.ga4_report.json_request",
        lambda *a, **k: {"rows": [{"metricValues": [{"value": "42"}, {"value": "30"}]}]},
    )
    res = fetch_ga4_organic_report()
    assert res["status"] == "OK"
    assert res["organic_sessions"] == 42
    assert res["organic_users"] == 30


def test_mcp_gsc_unavailable():
    resp = handle_request(
        {
            "jsonrpc": "2.0",
            "id": 9,
            "method": "tools/call",
            "params": {"name": "seo_gsc", "arguments": {"site_url": "https://example.com"}},
        }
    )
    payload = json.loads(resp["result"]["content"][0]["text"])
    assert payload["status"] == "UNAVAILABLE"


def test_tier_status_without_file(monkeypatch, tmp_path):
    monkeypatch.setattr("scripts.google_oauth.credentials_path", lambda: tmp_path / "missing.json")
    status = get_tier_status()
    assert status["status"] == "UNAVAILABLE"
    assert unavailable()["status"] == "UNAVAILABLE"
