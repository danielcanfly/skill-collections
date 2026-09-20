"""Deterministic routing helpers for future freeform routing support.

Version 2 keeps routing deliberately narrow and explainable.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RouteDecision:
    skill_name: str | None
    reason: str
    needs_clarification: bool = False


_DECISION_SIGNALS = {
    "job_decision_support": [
        "worth applying",
        "should i apply",
        "analyze this job",
        "application pack",
        "interview brief",
        "interview prep",
        "值不值得投",
        "分析這份職缺",
        "投遞包",
        "準備面試",
    ],
    "job_scoring": [
        "score unscored",
        "score all unscored",
        "backfill scores",
        "score missing scores",
        "rescore existing jobs",
        "rescore stored jobs",
        "score only",
        "補打分",
        "把沒打分的都打分",
        "未打分",
        "空白分數",
        "重打分",
    ],
    "job_ingestion": [
        "fetch recent jobs",
        "refresh jobs",
        "update jobs",
        "scrape jobs",
        "ingest jobs",
        "抓最近職缺",
        "抓最近",
        "更新職缺",
        "刷新職缺",
        "jobstreet",
    ],
    "job_querying": [
        "list jobs",
        "show jobs",
        "filter jobs",
        "rank jobs",
        "shortlist",
        "80 分以上",
        "列出職缺",
        "篩選職缺",
        "高分職缺",
        "top 10",
        "top 5",
    ],
}


class SkillRouter:
    def route_text(self, text: str) -> RouteDecision:
        normalized = " ".join(text.lower().split())

        for skill_name in (
            "job_decision_support",
            "job_scoring",
            "job_ingestion",
            "job_querying",
        ):
            if any(signal in normalized for signal in _DECISION_SIGNALS[skill_name]):
                return RouteDecision(skill_name=skill_name, reason=f"matched_{skill_name}")

        return RouteDecision(
            skill_name=None,
            reason="no_deterministic_match",
            needs_clarification=True,
        )
