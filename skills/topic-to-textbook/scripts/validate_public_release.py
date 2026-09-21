from pathlib import Path
import re, sys, json

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
errors = []

required = ["LICENSE", "NOTICE", "SECURITY.md", "README.md", "SKILL.md", "CHANGELOG.md"]
for rel in required:
    p = ROOT / rel
    if not p.exists() or p.stat().st_size == 0:
        errors.append(f"missing_or_empty: {rel}")

license_text = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").exists() else ""
if "Apache License" not in license_text or "Version 2.0, January 2004" not in license_text:
    errors.append("LICENSE is not Apache-2.0 text")

# Do not scan this validator's own detection patterns as package content.
text_files = []
for p in ROOT.rglob("*"):
    if not p.is_file() or p.resolve() == SELF or p.name == "MANIFEST.sha256":
        continue
    if p.suffix.lower() not in {".md", ".py", ".json", ".txt", ""}:
        continue
    try:
        text_files.append((p, p.read_text(encoding="utf-8")))
    except UnicodeDecodeError:
        pass

patterns = {
    "private_course_shorthand": re.compile(r"\bW2\b|\bW3\b|W2/W3|W2-W3", re.I),
    "mac_user_path": re.compile(r"/Users/[^/\s]+/"),
    "windows_user_path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
    "openai_like_key": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "tunnel_id": re.compile(r"\btunnel_[A-Za-z0-9]{12,}\b"),
    "private_key_block": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
}
for p, s in text_files:
    rel = p.relative_to(ROOT)
    for name, rx in patterns.items():
        m = rx.search(s)
        if m:
            errors.append(f"{name}: {rel}: {m.group(0)[:80]}")

skill = (ROOT / "SKILL.md").read_text(encoding="utf-8") if (ROOT / "SKILL.md").exists() else ""
readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
if "Version: 2.1.1" not in skill:
    errors.append("SKILL.md version mismatch")
if "v2.1.1" not in readme:
    errors.append("README version mismatch")

try:
    schema = json.loads((ROOT / "schemas/run_state.schema.json").read_text(encoding="utf-8"))
    if schema["properties"]["skill_version"].get("const") != "2.1.1":
        errors.append("run_state schema version mismatch")
except Exception as exc:
    errors.append(f"run_state schema check failed: {exc}")

if (ROOT / "legacy").exists():
    errors.append("legacy/ must not be bundled in public distribution")

if errors:
    print("FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("PASS")
print("license=Apache-2.0")
print("private_shorthand_scan=PASS")
print("local_path_scan=PASS")
print("secret_pattern_scan=PASS")
print("version_consistency=PASS")
print("legacy_not_bundled=PASS")
