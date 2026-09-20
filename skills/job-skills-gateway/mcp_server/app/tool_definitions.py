"""Shared helper functions for skill-level tool execution."""

from __future__ import annotations

from typing import Any

from .make_client import MakeClient
from .skill_loader import SkillDefinition


REQUIRED_CONTEXT_FIELDS = ("request_id", "session_id", "trace_id")


def ensure_required_context(payload: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_CONTEXT_FIELDS if not payload.get(field)]
    if missing:
        raise ValueError(f"Missing required context: {', '.join(missing)}")


async def run_job_ingestion(
    make_client: MakeClient,
    skill: SkillDefinition,
    payload: dict[str, Any],
) -> dict[str, Any]:
    ensure_required_context(payload)
    fetch_result = await make_client.fetch_recent_jobs(payload)

    result_payload = {
        "skill": skill.name,
        "skill_version": skill.manifest.get("version"),
        "mode": "fetch_then_score_new_rows",
        "fetch": fetch_result,
        "scoring": None,
    }

    inserted_count = _nested_number(fetch_result, ["result", "data", "inserted_count"], default=0)
    explicit_rescore = bool(payload.get("force_rescore"))
    if inserted_count > 0 or explicit_rescore:
        result_payload["scoring"] = await make_client.bulk_score_new_jobs(payload)

    return result_payload


async def run_job_scoring(
    make_client: MakeClient,
    skill: SkillDefinition,
    payload: dict[str, Any],
) -> dict[str, Any]:
    ensure_required_context(payload)
    scoring_result = await make_client.bulk_score_new_jobs(payload)
    return {
        "skill": skill.name,
        "skill_version": skill.manifest.get("version"),
        "mode": "score_only",
        "scoring": scoring_result,
    }


async def run_job_querying(
    make_client: MakeClient,
    skill: SkillDefinition,
    payload: dict[str, Any],
) -> dict[str, Any]:
    ensure_required_context(payload)
    query_result = await make_client.query_jobs(payload)
    return {
        "skill": skill.name,
        "skill_version": skill.manifest.get("version"),
        "query": query_result,
    }


async def run_job_decision_support(
    make_client: MakeClient,
    skill: SkillDefinition,
    payload: dict[str, Any],
) -> dict[str, Any]:
    ensure_required_context(payload)

    generation_result = await make_client.generate_job_output(payload)
    return {
        "skill": skill.name,
        "skill_version": skill.manifest.get("version"),
        "generation": generation_result,
    }


def _nested_number(container: dict[str, Any], path: list[str], default: int = 0) -> int:
    current: Any = container
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return int(current) if isinstance(current, (int, float)) else default
