from pathlib import Path

from mcp_server.app.skill_loader import SkillLoader


def test_load_all_skills() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    loader = SkillLoader(repo_root / "skills")
    skills = loader.load_all()

    assert {"job_ingestion", "job_querying", "job_decision_support"}.issubset(skills)
    assert skills["job_ingestion"].manifest["entrypoint_type"] == "skill"
