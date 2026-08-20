import io
import json

from scripts.capture_screenshot import should_abort_request
from scripts.hook_validate_fetch import main as fetch_hook
from scripts.hook_validate_write import main as write_hook
from scripts.url_safety import is_request_allowed, revalidate_hostname


class _Stdin(io.StringIO):
    def isatty(self):
        return False


def test_private_ip_subresource_is_aborted():
    assert should_abort_request("http://127.0.0.1/pixel", is_navigation=False) is True
    assert should_abort_request("https://example.com/", is_navigation=True) is False


def test_strict_browser_allowlist_blocks_other_hosts(monkeypatch):
    monkeypatch.setenv("SEOSKILLS_STRICT_BROWSER", "1")
    monkeypatch.setenv("SEOSKILLS_ALLOWED_HOSTS", "example.com")
    assert is_request_allowed("https://example.com/app.js", role="subresource") is True
    assert is_request_allowed("https://evil.example.org/app.js", role="subresource") is False
    assert should_abort_request("https://evil.example.org/app.js", is_navigation=False) is True


def test_revalidate_hostname_blocks_loopback():
    try:
        revalidate_hostname("127.0.0.1")
        raise AssertionError("expected PermissionError")
    except PermissionError:
        pass


def test_fetch_hook_blocks_private(monkeypatch):
    payload = json.dumps({"tool_name": "WebFetch", "tool_input": {"url": "http://127.0.0.1/"}})
    monkeypatch.setattr("sys.stdin", _Stdin(payload))
    assert fetch_hook() == 2


def test_fetch_hook_allows_public(monkeypatch):
    payload = json.dumps({"tool_name": "WebFetch", "tool_input": {"url": "https://example.com/"}})
    monkeypatch.setattr("sys.stdin", _Stdin(payload))
    assert fetch_hook() == 0


def test_write_hook_blocks_escape(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("SEOSKILLS_OUT_DIR", str(tmp_path))
    payload = json.dumps({"tool_input": {"file_path": "../outside-seoskills-test.txt"}})
    monkeypatch.setattr("sys.stdin", _Stdin(payload))
    assert write_hook() == 1
