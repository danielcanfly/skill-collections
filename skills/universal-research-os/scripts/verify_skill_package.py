#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORCH_NAME = "UNIVERSAL_RESEARCH_ORCHESTRATION_OS_v10_PROOF_CARRYING_RESEARCH_CONSTRUCTION"
AUDIT_NAME = "UNIVERSAL_RESEARCH_AUDIT_OS_v6_PROOF_CARRYING_RESEARCH_CONSTRUCTION"
ORCH_ZIP = ROOT / "canonical_sources" / "0.UNIVERSAL_RESEARCH_ORCHESTRATION_OS_v10_PROOF_CARRYING_RESEARCH_CONSTRUCTION.zip"
AUDIT_ZIP = ROOT / "canonical_sources" / "0.UNIVERSAL_RESEARCH_AUDIT_OS_v6_PROOF_CARRYING_RESEARCH_CONSTRUCTION.zip"
ORCH_ROOT = ROOT / "engines" / ORCH_NAME
AUDIT_ROOT = ROOT / "engines" / AUDIT_NAME
EXPECTED = {
    ORCH_ZIP.name: "579500a92581b2fb7f9c7aac5d03ebfc8cdfe2560813ec6c688d52aeef60b2c6",
    AUDIT_ZIP.name: "73abeddf57edb566b8bff861cc8cabacdbb8ab2dd4e6d039732c78ebfa28b230",
}
APACHE_2_LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
OPENAI_AGENT_REQUIRED = [
    'display_name: "Universal Research OS"',
    'short_description: "Proof-carrying research orchestration, audit, repair, and release"',
    'default_prompt:',
    'allow_implicit_invocation: true',
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise SystemExit(1)


def verify_zip_hash(path: Path) -> None:
    if not path.is_file():
        fail(f"missing canonical ZIP: {path}")
    got = sha256_file(path)
    if got != EXPECTED[path.name]:
        fail(f"canonical ZIP SHA mismatch for {path.name}: {got}")


def verify_extracted_tree(zip_path: Path, extracted_root: Path, archive_root: str) -> None:
    if not extracted_root.is_dir():
        fail(f"missing extracted root: {extracted_root}")
    with zipfile.ZipFile(zip_path) as zf:
        archive_files = {}
        prefix = archive_root.rstrip("/") + "/"
        for info in zf.infolist():
            if info.is_dir():
                continue
            if not info.filename.startswith(prefix):
                fail(f"unexpected archive root entry: {info.filename}")
            rel = info.filename[len(prefix):]
            archive_files[rel] = sha256_bytes(zf.read(info.filename))

    disk_files = {
        str(p.relative_to(extracted_root)).replace("\\", "/"): sha256_file(p)
        for p in extracted_root.rglob("*") if p.is_file()
    }
    if set(archive_files) != set(disk_files):
        missing = sorted(set(archive_files) - set(disk_files))[:10]
        extra = sorted(set(disk_files) - set(archive_files))[:10]
        fail(f"tree membership mismatch for {archive_root}; missing={missing}, extra={extra}")
    diffs = [rel for rel in sorted(archive_files) if archive_files[rel] != disk_files[rel]]
    if diffs:
        fail(f"byte mismatch in {archive_root}: {diffs[:10]}")


def verify_audit_parity() -> None:
    embedded = ORCH_ROOT / "modules" / "audit_os_v6_proof_carrying_construction"
    stand = {
        str(p.relative_to(AUDIT_ROOT)).replace("\\", "/"): sha256_file(p)
        for p in AUDIT_ROOT.rglob("*") if p.is_file()
    }
    emb = {
        str(p.relative_to(embedded)).replace("\\", "/"): sha256_file(p)
        for p in embedded.rglob("*") if p.is_file()
    }
    if stand != emb:
        fail("standalone Audit OS v6 differs from embedded Audit OS v6")
    if len(stand) != 57:
        fail(f"unexpected Audit OS v6 file count: {len(stand)}")


def verify_package_checksums() -> None:
    sums = ROOT / "SHA256SUMS.txt"
    if not sums.is_file():
        return
    expected = {}
    for line in sums.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        expected[rel] = digest
    actual_files = {
        str(p.relative_to(ROOT)).replace("\\", "/")
        for p in ROOT.rglob("*") if p.is_file() and p != sums
    }
    if set(expected) != actual_files:
        missing = sorted(actual_files - set(expected))[:10]
        stale = sorted(set(expected) - actual_files)[:10]
        fail(f"package checksum membership mismatch; unlisted={missing}, stale={stale}")
    for rel, digest in expected.items():
        got = sha256_file(ROOT / rel)
        if got != digest:
            fail(f"package checksum mismatch: {rel}")


def verify_versions() -> None:
    orch = json.loads((ORCH_ROOT / "VERSION.json").read_text(encoding="utf-8"))
    audit = json.loads((AUDIT_ROOT / "VERSION.json").read_text(encoding="utf-8"))
    if orch.get("version") != "10.0.0" or orch.get("audit_os_version") != "6.0.0":
        fail("unexpected Orchestration version identity")
    if audit.get("version") != "6.0.0" or audit.get("orchestration_contract") != "v10":
        fail("unexpected Audit version identity")


def verify_public_wrapper() -> None:
    version = json.loads((ROOT / "VERSION.json").read_text(encoding="utf-8"))
    if version.get("version") != "1.0.1" or version.get("status") != "PUBLIC_RELEASE":
        fail("unexpected public Skill wrapper version/status")

    agent = ROOT / "agents" / "openai.yaml"
    if not agent.is_file():
        fail("missing agents/openai.yaml")
    agent_text = agent.read_text(encoding="utf-8")
    for required in OPENAI_AGENT_REQUIRED:
        if required not in agent_text:
            fail(f"agents/openai.yaml missing required metadata: {required}")

    license_path = ROOT / "LICENSE"
    if not license_path.is_file():
        fail("missing LICENSE")
    if sha256_file(license_path) != APACHE_2_LICENSE_SHA256:
        fail("LICENSE is not the qualified Apache License 2.0 text")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for heading in ["## Quick Start", "## Example Prompts", "## License"]:
        if heading not in readme:
            fail(f"README missing public usage section: {heading}")


def main() -> None:
    for required in [
        ROOT / "SKILL.md",
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / "agents" / "openai.yaml",
        ROOT / "router" / "ROUTING.md",
        ROOT / "router" / "INDEPENDENCE_BOUNDARY.md",
    ]:
        if not required.is_file():
            fail(f"missing wrapper file: {required.relative_to(ROOT)}")
    verify_zip_hash(ORCH_ZIP)
    verify_zip_hash(AUDIT_ZIP)
    verify_extracted_tree(ORCH_ZIP, ORCH_ROOT, ORCH_NAME)
    verify_extracted_tree(AUDIT_ZIP, AUDIT_ROOT, AUDIT_NAME)
    verify_audit_parity()
    verify_versions()
    verify_public_wrapper()
    verify_package_checksums()
    print("PASS: UNIVERSAL_RESEARCH_OS_SKILL package verified")
    print("Orchestration ZIP SHA256:", EXPECTED[ORCH_ZIP.name])
    print("Audit ZIP SHA256:", EXPECTED[AUDIT_ZIP.name])
    print("Standalone/embedded Audit parity: 57/57 files identical")


if __name__ == "__main__":
    main()
