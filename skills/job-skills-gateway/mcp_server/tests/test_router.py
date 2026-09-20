from mcp_server.app.router import SkillRouter


def test_router_prefers_decision_support_for_analysis_requests() -> None:
    router = SkillRouter()
    decision = router.route_text("幫我分析這份職缺值不值得投")
    assert decision.skill_name == "job_decision_support"


def test_router_maps_fetch_to_ingestion() -> None:
    router = SkillRouter()
    decision = router.route_text("抓最近三天 product manager 職缺")
    assert decision.skill_name == "job_ingestion"


def test_router_maps_list_to_querying() -> None:
    router = SkillRouter()
    decision = router.route_text("列出 80 分以上職缺")
    assert decision.skill_name == "job_querying"
