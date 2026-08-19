import pytest
from scripts.url_safety import validate_url

def test_valid_public_urls():
    assert validate_url("https://example.com") is True
    assert validate_url("http://google.com/search?q=test") is True

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
