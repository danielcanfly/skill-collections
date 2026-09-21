from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "SKILL.md", "README.md", "CHANGELOG.md", "MIGRATION_AND_CAPABILITY_MAP.md",
    "references/01_ORCHESTRATION_AND_MODES.md",
    "references/02_RESEARCH_PROTOCOL.md",
    "references/03_EVIDENCE_PROVENANCE_AND_FRESHNESS.md",
    "references/04_PEDAGOGY_PROTOCOL.md",
    "references/05_DOMAIN_ADAPTERS.md",
    "references/06_ASSESSMENT_AND_MASTERY.md",
    "references/07_QA_AND_PUBLICATION.md",
    "references/08_VISUALS_AND_ACCESSIBILITY.md",
    "references/09_RESEARCH_BASIS.md",
    "references/10_RUN_STATE_AND_CHECKPOINTS.md",
    "references/11_RESEARCH_FREEZE_AND_CLAIM_CRITICALITY.md",
    "references/12_UNTRUSTED_SOURCES_AND_EXECUTION_SAFETY.md",
    "references/13_EXECUTABLE_VALIDATION_AND_LABS.md",
    "references/14_REFRESH_AND_REVISION_IMPACT.md",
    "templates/00_TOPIC_SCOPE_CONTRACT.md",
    "templates/01_RESEARCH_MAP.md",
    "templates/02_EVIDENCE_LEDGER.md",
    "templates/03_KNOWLEDGE_MAP.md",
    "templates/04_CONCEPT_DEPENDENCY_GRAPH.md",
    "templates/05_MISCONCEPTION_MAP.md",
    "templates/06_CURRICULUM_MAP.md",
    "templates/07_LESSON_MANUSCRIPT.md",
    "templates/08_LEARNER_FRICTION_LOG.md",
    "templates/09_COVERAGE_MATRIX.md",
    "templates/10_ASSESSMENT_ALIGNMENT_MATRIX.md",
    "templates/11_FINAL_QUALIFICATION.md",
    "templates/12_RUN_STATE.md",
    "templates/13_RESEARCH_FREEZE_MANIFEST.md",
    "templates/14_EXECUTABLE_VALIDATION_LOG.md",
    "templates/15_REVISION_IMPACT_MAP.md",
    "templates/16_COLD_REVIEW.md",
    "schemas/run_state.schema.json",
    "schemas/research_freeze.schema.json",
        "qualification/TEST_MATRIX.md",
]

FIXTURES = [
    "qualification/fixtures/topic_only_working_capital.json",
    "qualification/fixtures/topic_only_kubernetes_autoscaling.json",
    "qualification/fixtures/topic_only_agent_evaluation.json",
    "qualification/fixtures/source_grounded.json",
    "qualification/fixtures/refresh_revision.json",
]

errors = []
notes = []

for rel in REQUIRED + FIXTURES:
    p = ROOT / rel
    if not p.exists() or p.stat().st_size == 0:
        errors.append(f"missing_or_empty: {rel}")

skill_path = ROOT / "SKILL.md"
skill = skill_path.read_text(encoding="utf-8") if skill_path.exists() else ""

if not skill.startswith("---\n"):
    errors.append("SKILL.md missing YAML front matter")
if "name: universal-topic-to-textbook" not in skill:
    errors.append("unexpected skill name")
if "Version: 2.1.1" not in skill:
    errors.append("SKILL.md version is not 2.1.0")

must_have = [
    "TOPIC_ONLY_AUTONOMOUS",
    "SOURCE_GROUNDED_EXPANSION",
    "TRANSCRIPT_TO_TEXTBOOK",
    "INTERACTIVE_LEARNING_FIRST",
    "REFRESH_OR_REVISION",
    "RUN_STATE",
    "Curriculum Triangulation",
    "Research Freeze Manifest",
    "CRITICAL",
    "Lesson Manuscripts",
    "Post-Reconstruction Claim Drift Audit",
    "Executable",
    "Independent Cold Review",
    "TEXTBOOK_COMPLETE",
    "PUBLIC_READY",
]
for token in must_have:
    if token not in skill:
        errors.append(f"core capability missing from SKILL.md: {token}")

# Core should remain orchestration-first rather than becoming a giant manual.
line_count = len(skill.splitlines())
if line_count > 450:
    errors.append(f"SKILL.md orchestration core too large: {line_count} lines > 450")
else:
    notes.append(f"core_line_budget=PASS({line_count})")

# Verify referenced support files.
for rel in re.findall(r"`((?:references|templates)/[^`]+\.(?:md|json))`", skill):
    if not (ROOT / rel).exists():
        errors.append(f"broken reference: {rel}")

# Universal-core guard.
forbidden_phrases = [
    "每章必須包含 Architecture",
    "每章必須包含 Enterprise PM Case",
    "所有教材必須包含 Hands-on Lab",
]
for phrase in forbidden_phrases:
    if phrase in skill:
        errors.append(f"domain lock detected: {phrase}")

# Explicit safety / evidence hardening must exist.
required_protocol_tokens = {
    "references/02_RESEARCH_PROTOCOL.md": ["Curriculum Triangulation", "Challenge / Falsification", "Research Sufficiency"],
    "references/03_EVIDENCE_PROVENANCE_AND_FRESHNESS.md": ["CRITICAL", "Final Textbook Locator", "Post-reconstruction"],
    "references/12_UNTRUSTED_SOURCES_AND_EXECUTION_SAFETY.md": ["Prompt-injection", "Copyright / licensing"],
    "references/13_EXECUTABLE_VALIDATION_AND_LABS.md": ["EXECUTED", "UNEXECUTED", "NOT_RUNTIME_VALIDATED"],
    "references/14_REFRESH_AND_REVISION_IMPACT.md": ["Revision impact graph", "No-blind-rebuild"],
}
for rel, tokens in required_protocol_tokens.items():
    text = (ROOT / rel).read_text(encoding="utf-8") if (ROOT / rel).exists() else ""
    for token in tokens:
        if token.lower() not in text.lower():
            errors.append(f"protocol invariant missing: {rel}: {token}")

# JSON schemas must be valid JSON and contain required fields.
for rel in ["schemas/run_state.schema.json", "schemas/research_freeze.schema.json"]:
    try:
        obj = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        if obj.get("type") != "object" or not obj.get("required"):
            errors.append(f"schema missing object/required contract: {rel}")
    except Exception as exc:
        errors.append(f"invalid JSON schema {rel}: {exc}")

# Behavioral contract fixtures: package must cover materially different routing cases.
expected_modes = {
    "TOPIC_ONLY_AUTONOMOUS",
    "SOURCE_GROUNDED_EXPANSION",
    "REFRESH_OR_REVISION",
}
fixture_modes = set()
for rel in FIXTURES:
    try:
        obj = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        if not obj.get("prompt") or not obj.get("expected_mode"):
            errors.append(f"fixture incomplete: {rel}")
        fixture_modes.add(obj.get("expected_mode"))
    except Exception as exc:
        errors.append(f"invalid fixture {rel}: {exc}")
if not expected_modes.issubset(fixture_modes):
    errors.append(f"fixture mode coverage incomplete: {sorted(expected_modes - fixture_modes)}")

# Static package must not self-claim host runtime smoke qualification in the core.
if "RUNTIME_SMOKE_QUALIFIED: PASS" in skill:
    errors.append("static core improperly claims runtime smoke PASS")

if errors:
    print("FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("PASS")
print(f"root={ROOT}")
print(f"files={sum(1 for p in ROOT.rglob('*') if p.is_file())}")
for note in notes:
    print(note)
print("supporting_refs=PASS")
print("schema_contracts=PASS")
print("behavioral_fixture_coverage=PASS")
print("universal_core_guard=PASS")
print("hardening_protocols=PASS")
