import os

import pytest

from scripts.full_audit import run_full_audit

pytestmark = pytest.mark.skipif(
    os.environ.get("SEOSKILLS_LIVE_SMOKE") != "1",
    reason="opt-in live network smoke (SEOSKILLS_LIVE_SMOKE=1)",
)


def test_live_example_com_audit_has_real_status_and_title():
    result = run_full_audit("https://example.com")
    assert result["status"] == "SUCCESS"
    assert result["metrics"]["status_code"] == 200
    title = (result["metrics"].get("title") or "").lower()
    assert "example" in title
