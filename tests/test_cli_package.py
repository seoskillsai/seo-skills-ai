from pathlib import Path


def test_cli_package_ships_index_mjs_and_skills():
    root = Path(__file__).resolve().parents[1]
    assert (root / "packages" / "cli" / "index.mjs").is_file()
    assert (root / "skills" / "seo" / "SKILL.md").is_file()
    assert (root / "AGENTS.md").is_file()
    pkg = (root / "package.json").read_text(encoding="utf-8")
    assert '"@seoskillsai/cli"' in pkg
    assert "packages/cli/index.mjs" in pkg
    assert '"skills"' in pkg
