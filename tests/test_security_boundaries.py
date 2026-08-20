from scripts.capture_screenshot import capture_page_screenshot
from scripts.mcp_server import handle_request


def test_screenshot_blocks_localhost():
    res = capture_page_screenshot("http://127.0.0.1:9222/")
    assert res["status"] == "BLOCKED"


def test_mcp_initialize_and_tool_list():
    init = handle_request({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    assert init["result"]["serverInfo"]["name"] == "seoskillsai"
    listed = handle_request({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    names = {t["name"] for t in listed["result"]["tools"]}
    assert names == {"seo_audit", "seo_schema", "seo_drift"}


def test_mcp_audit_blocks_private_url():
    resp = handle_request({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "seo_audit", "arguments": {"url": "http://127.0.0.1/"}},
    })
    assert resp["result"]["isError"] is True
    assert "Security Alert" in resp["result"]["content"][0]["text"]
