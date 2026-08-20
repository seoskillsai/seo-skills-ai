import os
import pytest

from scripts.llms_txt_builder import generate_llms_txt


def test_llms_txt_generation(tmp_path, monkeypatch):
    monkeypatch.setenv("SEOSKILLS_OUT_DIR", str(tmp_path))
    out_dir = str(tmp_path)
    res = generate_llms_txt("Test Site", "https://example.com", output_dir=out_dir)
    assert os.path.exists(res["llms_txt"])
    assert os.path.exists(res["llms_full_txt"])

    with open(res["llms_txt"], "r", encoding="utf-8") as f:
        content = f.read()
    assert "# Test Site" in content
    assert "https://example.com" in content
