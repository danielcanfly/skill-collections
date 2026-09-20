"""FastMCP entrypoint for the thin job skill server."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastmcp import FastMCP

from .make_client import MakeClient
from .skill_loader import SkillLoader
from .tool_definitions import (
    run_job_decision_support,
    run_job_ingestion,
    run_job_querying,
    run_job_scoring,
)

BASE_DIR = Path(__file__).resolve().parents[2]
SKILLS_DIR = BASE_DIR / "skills"

load_dotenv(BASE_DIR / ".env")

loader = SkillLoader(SKILLS_DIR)
SKILLS = loader.load_all()
make_client = MakeClient()

mcp = FastMCP(name="job-skills-gateway")


def _skill(name: str):
    try:
        return SKILLS[name]
    except KeyError as exc:
        raise RuntimeError(f"Required skill is missing from skills/: {name}") from exc


@mcp.tool
async def job_ingestion(
    request_id: str,
    session_id: str,
    trace_id: str,
    source_site: str = "jobstreet",
    role_keyword: str | None = None,
    days: int = 3,
    page_from: int = 1,
    page_to: int = 3,
    force_rescore: bool = False,
    source_channel: str = "chatgpt",
    actor_id: str = "",
    parent_run_id: str = "",
) -> dict[str, Any]:
    """Fetch recent jobs from an external source, then score only newly inserted rows.

    Use this tool when the user wants to refresh or ingest recent jobs from JobStreet
    or another configured source.

    Good fits:
    - 抓最近 3 天的 PM 職缺，新的順便打分
    - refresh recent product jobs from JobStreet
    - update the recent job pool

    Do not use this tool for score-only requests against jobs already stored in the sheet.
    For requests like 「把沒打分的都打分」 or "rescore existing jobs", use `job_scoring`.
    """
    payload = {
        "request_id": request_id,
        "session_id": session_id,
        "trace_id": trace_id,
        "source_site": source_site,
        "role_keyword": role_keyword,
        "days": days,
        "page_from": page_from,
        "page_to": page_to,
        "force_rescore": force_rescore,
        "source_channel": source_channel,
        "actor_id": actor_id,
        "parent_run_id": parent_run_id,
    }
    return await run_job_ingestion(make_client, _skill("job_ingestion"), payload)


@mcp.tool
async def job_scoring(
    request_id: str,
    session_id: str,
    trace_id: str,
    target_job_id: str = "",
    force_rescore: bool = False,
    source_channel: str = "chatgpt",
    actor_id: str = "",
    parent_run_id: str = "",
) -> dict[str, Any]:
    """Score jobs that are already stored in the job pool.

    This is the score-only path.

    Use this tool when the user wants to:
    - score all unscored jobs already in storage
    - backfill missing scores
    - rescore one known job
    - rescore existing jobs without fetching new jobs

    Behavior:
    - if `target_job_id` is empty and `force_rescore` is false, score only unscored jobs
    - if `target_job_id` is provided, score or rescore that specific stored job
    - if `force_rescore` is true, allow rescoring instead of only filling blanks

    Do not use this tool to fetch recent jobs from JobStreet. Use `job_ingestion` for that.
    """
    payload = {
        "request_id": request_id,
        "session_id": session_id,
        "trace_id": trace_id,
        "target_job_id": target_job_id,
        "force_rescore": force_rescore,
        "source_channel": source_channel,
        "actor_id": actor_id,
        "parent_run_id": parent_run_id,
    }
    return await run_job_scoring(make_client, _skill("job_scoring"), payload)


@mcp.tool
async def job_querying(
    request_id: str,
    session_id: str,
    trace_id: str,
    days: int | None = None,
    job_status_filter: str | None = None,
    min_score: float | None = None,
    keyword_query: str | None = None,
    top_k: int | None = None,
    sort_by: str | None = None,
    sort_order: str | None = None,
    source_channel: str = "chatgpt",
    actor_id: str = "",
    parent_run_id: str = "",
) -> dict[str, Any]:
    """Query, filter, and rank jobs already stored in the job pool.

    Use this tool for shortlist and retrieval tasks such as:
    - 列出最近 7 天 AI 職缺，80 分以上，按分數排序
    - show me the top 10 product jobs
    - find stored jobs by keyword, URL, or numeric job id

    Do not use this tool to fetch new jobs or to backfill scores.
    """
    payload = {
        "request_id": request_id,
        "session_id": session_id,
        "trace_id": trace_id,
        "days": days,
        "job_status_filter": job_status_filter,
        "min_score": min_score,
        "keyword_query": keyword_query,
        "top_k": top_k,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "source_channel": source_channel,
        "actor_id": actor_id,
        "parent_run_id": parent_run_id,
    }
    return await run_job_querying(make_client, _skill("job_querying"), payload)


@mcp.tool
async def job_decision_support(
    request_id: str,
    session_id: str,
    trace_id: str,
    user_message_raw: str,
    task_type: str = "analyze_job",
    target_job_id: str = "",
    target_company: str = "",
    target_title: str = "",
    source_channel: str = "chatgpt",
    actor_id: str = "",
    parent_run_id: str = "",
) -> dict[str, Any]:
    """Generate a single-job decision artifact.

    Use this tool when the user wants a deep output for one target job:
    - worth-applying analysis
    - application pack
    - interview brief

    This tool is for one resolved job at a time, not for bulk retrieval or score backfill.
    """
    payload = {
        "request_id": request_id,
        "session_id": session_id,
        "trace_id": trace_id,
        "user_message_raw": user_message_raw,
        "task_type": task_type,
        "target_job_id": target_job_id,
        "target_company": target_company,
        "target_title": target_title,
        "source_channel": source_channel,
        "actor_id": actor_id,
        "parent_run_id": parent_run_id,
    }
    return await run_job_decision_support(make_client, _skill("job_decision_support"), payload)


app = mcp.http_app(path="/mcp")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("mcp_server.app.server:app", host="127.0.0.1", port=8001)
