import pytest
from pathlib import Path
from scripts.portability_check import check_skill_file

def test_all_skills_have_valid_frontmatter():
    skills_dir = Path("skills")
    skill_files = list(skills_dir.glob("*/SKILL.md"))
    assert len(skill_files) >= 20, f"Expected at least 20 skills, found {len(skill_files)}"

    for sf in skill_files:
        errors = check_skill_file(sf)
        assert len(errors) == 0, f"Skill {sf} failed portability: {errors}"
