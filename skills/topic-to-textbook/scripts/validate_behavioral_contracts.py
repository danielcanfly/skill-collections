from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
fixtures = sorted((ROOT / "qualification/fixtures").glob("*.json"))
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
domain = (ROOT / "references/05_DOMAIN_ADAPTERS.md").read_text(encoding="utf-8")
research = (ROOT / "references/02_RESEARCH_PROTOCOL.md").read_text(encoding="utf-8")
refresh = (ROOT / "references/14_REFRESH_AND_REVISION_IMPACT.md").read_text(encoding="utf-8")
errors = []

for path in fixtures:
    obj = json.loads(path.read_text(encoding="utf-8"))
    mode = obj["expected_mode"]
    if mode not in skill:
        errors.append(f"{path.name}: expected mode absent from core: {mode}")
    adapter = obj.get("primary_adapter")
    if adapter and adapter not in domain:
        errors.append(f"{path.name}: adapter absent: {adapter}")
    if obj.get("requires_curriculum_triangulation") and "Curriculum Triangulation" not in research:
        errors.append(f"{path.name}: triangulation contract missing")
    if obj.get("requires_revision_impact") and "Revision impact graph" not in refresh:
        errors.append(f"{path.name}: revision impact contract missing")
    if obj.get("requires_executable_validation") and "Executable" not in skill:
        errors.append(f"{path.name}: executable validation contract missing")

if errors:
    print("FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("PASS")
print(f"fixtures={len(fixtures)}")
print("routing_contract_coverage=PASS")
print("domain_contract_coverage=PASS")
print("research_contract_coverage=PASS")
print("revision_contract_coverage=PASS")
