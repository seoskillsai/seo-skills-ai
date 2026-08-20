import os
import pytest

from scripts.url_safety import is_request_allowed, validate_redirect, validate_url


def test_valid_public_urls():
    assert validate_url("https://example.com") is True
    assert validate_url("http://example.com/search?q=test") is True


def test_blocked_schemes():
    with pytest.raises(ValueError):
        validate_url("ftp://example.com")
    with pytest.raises(ValueError):
        validate_url("file:///etc/passwd")


def test_blocked_private_ips():
    with pytest.raises(PermissionError):
        validate_url("http://127.0.0.1:8000")
    with pytest.raises(PermissionError):
        validate_url("http://169.254.169.254/latest/meta-data")
    with pytest.raises(PermissionError):
        validate_url("http://10.0.0.5/")
    with pytest.raises(PermissionError):
        validate_url("http://[::1]/")


def test_blocked_localhost_name():
    with pytest.raises(PermissionError):
        validate_url("http://localhost:8080/")


def test_unresolvable_host_fails_closed():
    with pytest.raises(PermissionError):
        validate_url("https://this-host-does-not-exist.invalid/")


def test_allowlist_blocks_other_hosts(monkeypatch):
    monkeypatch.setenv("SEOSKILLS_ALLOWED_HOSTS", "example.com")
    assert validate_url("https://example.com/page") is True
    with pytest.raises(PermissionError):
        validate_url("https://example.org/")


def test_redirect_to_metadata_blocked():
    with pytest.raises(PermissionError):
        validate_redirect("https://example.com/", "http://169.254.169.254/latest/meta-data")


def test_subresource_data_urls_allowed():
    assert is_request_allowed("data:text/plain,hi") is True
    assert is_request_allowed("http://127.0.0.1/") is False
