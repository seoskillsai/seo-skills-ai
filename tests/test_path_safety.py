import pytest

from scripts.path_safety import resolve_workspace_path, workspace_root


def test_relative_path_stays_in_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("SEOSKILLS_OUT_DIR", raising=False)
    monkeypatch.delenv("SEOSKILLS_WORKSPACE", raising=False)
    target = resolve_workspace_path("public/llms.txt")
    assert target == (tmp_path / "public" / "llms.txt").resolve()


def test_parent_escape_blocked(tmp_path, monkeypatch):
    monkeypatch.setenv("SEOSKILLS_OUT_DIR", str(tmp_path))
    with pytest.raises(PermissionError):
        resolve_workspace_path("../outside.txt")


def test_explicit_root_env(tmp_path, monkeypatch):
    monkeypatch.setenv("SEOSKILLS_OUT_DIR", str(tmp_path))
    nested = resolve_workspace_path("reports/audit.html")
    assert nested == (tmp_path / "reports" / "audit.html").resolve()
    assert workspace_root() == tmp_path.resolve()
