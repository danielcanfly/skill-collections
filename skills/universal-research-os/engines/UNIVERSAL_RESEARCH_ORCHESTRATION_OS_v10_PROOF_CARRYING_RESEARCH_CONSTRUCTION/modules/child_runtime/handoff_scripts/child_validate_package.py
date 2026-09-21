#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, csv, hashlib, json, re, sys

try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML required: python -m pip install pyyaml")

REQUIRED_HEADERS = {
    "research/accepted_sources.csv": ["source_id","trust_tier","authority","method","directness","recency","independence","applicability","decision","notes"],
    "research/source_family_map.csv": ["module_id","research_question","source_family","priority","target_examples","status"],
    "research/source_coverage_matrix.csv": ["module_id","question_id","source_id","coverage","directness","status","gap"],
    "research/claim_ledger.csv": ["claim_id","module_id","claim","claim_type","subtype","source_id","evidence_family_id","support_challenge","scope","confidence","candidate_node","notes"],
    "research/canonical_concept_registry.csv": ["id","title","kind","module_id","aliases","broader","contrasts","source_ids","maturity","confidence","status"],
    "research/alias_map.csv": ["alias","canonical_id","language","reason","source"],
    "research/confidence_assessment.csv": ["canonical_id","confidence","maturity","evidence_basis","conflicts","notes"],
    "research/evidence_family_registry.csv": ["evidence_family_id","canonical_name","description","source_ids","independence_basis","modules","claims","status","notes"],
    "research/source_metadata_reconciliation.csv": ["source_id","current_title","verified_title","verified_authors","verified_year","effective_date_or_period_end","accessed_at","verified_source_type","verified_publisher","verified_doi_or_url","access_status","verification_status","action","evidence_family_id","entity_identity_notes","notes"],
    "research/case_registry.csv": ["case_id","case_type","title","domain","jurisdiction_or_context","decision_or_problem","source_ids","mechanism","what_was_known_at_the_time","outcome","decision_quality_interpretation","transfer_limit","status"],
    "research/claim_migration_log.csv": ["old_claim_id","new_claim_id","action","reason","sources_changed","nodes_changed","confidence_change"],
}
ALLOWED_SUPPORT = {"support","partial-support","contextual-support","challenge"}
SHARED_CLAIM_TYPES={"definition","formula","boundary","mechanism","driver","decision-rule","diagnostic-rule","audit-rule","case-fact","failure-mode","comparison","relationship","limitation","assumption","calculation","framework"}
ALLOWED_VERIFICATION = {"verified","corrected","replaced","removed","unresolved"}
SEARCH_URL_PATTERNS = [
    r"[?&](?:q|query|term|search)=",
    r"google\.[^/]+/search",
    r"scholar\.google",
    r"bing\.com/search",
    r"pubmed\.ncbi\.nlm\.nih\.gov/\?term=",
]

def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2]

def section_ids(body: str, headings):
    values=set()
    for h in headings:
        m=re.search(rf"## {re.escape(h)}\s*(.*?)(?:\n## |\Z)", body, re.S)
        if not m: continue
        values.update(re.findall(r"`(C\d+[A-Z]?)`", m.group(1)))
    return values

def concepts_updated(body: str):
    m=re.search(r"## Concepts Updated\s*(.*?)(?:\n## |\Z)", body, re.S)
    if not m: return set()
    return set(re.findall(r"`([^`]+)`",m.group(1)))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--case-min",type=int,default=6)
    ap.add_argument("--json-output")
    args=ap.parse_args()
    root=Path(args.root).resolve()
    errors=[]; warnings=[]

    for rel, expected in REQUIRED_HEADERS.items():
        p=root/rel
        if not p.exists():
            errors.append(f"Missing required CSV: {rel}")
            continue
        with p.open(encoding="utf-8-sig",newline="") as f:
            actual=next(csv.reader(f),[])
        if actual != expected:
            errors.append(f"Header mismatch {rel}: {actual} != {expected}")

    nodes={}; sources={}; node_records=[]; source_records=[]
    for p in sorted((root/"knowledge").rglob("*.md")):
        fm,body=frontmatter(p)
        rel=p.relative_to(root).as_posix()
        if fm.get("source_id"):
            sid=str(fm["source_id"])
            if sid in sources: errors.append(f"Duplicate source_id {sid}")
            sources[sid]=rel; source_records.append((sid,rel,fm,body))
        elif fm.get("id"):
            nid=str(fm["id"])
            if nid in nodes: errors.append(f"Duplicate node id {nid}")
            nodes[nid]=rel; node_records.append((nid,rel,fm,body))

    titles={}
    for nid,rel,fm,body in node_records:
        title=str(fm.get("title","")).strip().lower()
        if title:
            if title in titles: errors.append(f"Duplicate title {title}: {rel} / {titles[title]}")
            titles[title]=rel
        if str(fm.get("x-kos-version"))!="0.1":
            errors.append(f"{rel}: x-kos-version must be 0.1")
        aliases=fm.get("aliases") or []
        if isinstance(aliases,str): aliases=[aliases]
        for a in aliases:
            s=str(a).strip()
            if len(s)>80 or "?" in s or "？" in s:
                warnings.append(f"{rel}: possible query-like alias: {s}")
        for related in fm.get("related") or []:
            if related in nodes: continue
            # External cross-topic relationship must be documented.
            overlap=(root/"handoff/cross_topic_overlap.md")
            if not overlap.exists() or str(related) not in overlap.read_text(encoding="utf-8"):
                errors.append(f"{rel}: unresolved related ID not documented as external: {related}")
        for sid in fm.get("source_ids") or []:
            if sid not in sources: errors.append(f"{rel}: unresolved source_id {sid}")

    # Markdown local links.
    link_re=re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
    for p in root.rglob("*.md"):
        text=p.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            clean=target.split("#",1)[0]
            if not clean: continue
            q=(p.parent/clean).resolve()
            if not q.exists(): errors.append(f"Broken Markdown link: {p.relative_to(root)} -> {target}")

    # Evidence families.
    families=set()
    fp=root/"research/evidence_family_registry.csv"
    if fp.exists():
        with fp.open(encoding="utf-8-sig",newline="") as f:
            families={r["evidence_family_id"].strip() for r in csv.DictReader(f) if r.get("evidence_family_id")}

    claims_by_id={}; claim_edges=set()
    cp=root/"research/claim_ledger.csv"
    if cp.exists():
        with cp.open(encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f):
                cid=r.get("claim_id","").strip()
                if not re.fullmatch(r"C\d+[A-Z]?",cid):
                    errors.append(f"Invalid claim ID: {cid}")
                signature=(r.get("claim",""),r.get("claim_type",""),r.get("confidence",""))
                if cid in claims_by_id and claims_by_id[cid]!=signature:
                    errors.append(f"Inconsistent claim text/type/confidence for {cid}")
                claims_by_id[cid]=signature
                ctype=r.get("claim_type","").strip()
                if ctype not in SHARED_CLAIM_TYPES: errors.append(f"{cid}: non-standard claim_type {ctype}")
                if not r.get("subtype","").strip(): errors.append(f"{cid}: missing preserved local subtype")
                support=r.get("support_challenge","").strip()
                if support not in ALLOWED_SUPPORT:
                    errors.append(f"{cid}: invalid support_challenge {support}")
                if not r.get("scope","").strip(): errors.append(f"{cid}: empty scope")
                if not r.get("notes","").strip(): warnings.append(f"{cid}: empty notes")
                fam=r.get("evidence_family_id","").strip()
                if fam and fam not in families: errors.append(f"{cid}: unregistered evidence family {fam}")
                sid=r.get("source_id","").strip(); nid=r.get("candidate_node","").strip()
                if sid not in sources: errors.append(f"{cid}: missing source note {sid}")
                if nid not in nodes: errors.append(f"{cid}: missing candidate node {nid}")
                claim_edges.add((cid,sid,nid,support))

    # Metadata reconciliation and accepted sources.
    recon={}
    rp=root/"research/source_metadata_reconciliation.csv"
    if rp.exists():
        with rp.open(encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f):
                sid=r.get("source_id","").strip()
                status=r.get("verification_status","").strip()
                if status not in ALLOWED_VERIFICATION: errors.append(f"{sid}: invalid verification status {status}")
                url=r.get("verified_doi_or_url","").strip().lower()
                if any(re.search(pat,url) for pat in SEARCH_URL_PATTERNS):
                    errors.append(f"{sid}: search/query URL cannot be canonical: {url}")
                recon[sid]=status

    apath=root/"research/accepted_sources.csv"
    if apath.exists():
        with apath.open(encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f):
                sid=r.get("source_id","").strip()
                if recon.get(sid) not in {"verified","corrected"}:
                    errors.append(f"Accepted source {sid} is not verified/corrected")

    # Bidirectional lineage.
    source_claims={}; source_concepts={}
    for sid,rel,fm,body in source_records:
        required_sections=[
            "Source-specific Findings","Claims Supported","Contextual or Partial Contributions",
            "What This Source Does Not Establish","Caveats and Transfer Limits","Concepts Updated"
        ]
        for h in required_sections:
            if f"## {h}" not in body: errors.append(f"{rel}: missing section {h}")
        source_claims[sid]=section_ids(body,["Claims Supported","Contextual or Partial Contributions"])
        source_concepts[sid]=concepts_updated(body)

    for nid,rel,fm,body in node_records:
        for sid in fm.get("source_ids") or []:
            if nid not in source_concepts.get(sid,set()):
                errors.append(f"Missing reverse Concepts Updated: {nid} -> {sid}")
            matching=[x for x in claim_edges if x[1]==sid and x[2]==nid]
            if not matching:
                errors.append(f"Missing claim-ledger edge: {nid} -> {sid}")
            elif not any(cid in source_claims.get(sid,set()) for cid,_,_,_ in matching):
                errors.append(f"Source note missing claim ID for edge: {nid} -> {sid}")

    # Cases.
    case_path=root/"research/case_registry.csv"
    evidence_cases=0
    if case_path.exists():
        with case_path.open(encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f):
                if r.get("case_type")=="evidence-backed":
                    evidence_cases+=1
                    if not r.get("source_ids","").strip():
                        errors.append(f"Evidence-backed case missing source_ids: {r.get('case_id')}")
    if evidence_cases < args.case_min:
        errors.append(f"Evidence-backed case count {evidence_cases} below required {args.case_min}")

    # Retrieval.
    retr=root/"qa/retrieval_results.json"
    if not retr.exists():
        errors.append("Missing qa/retrieval_results.json")
    else:
        try:
            data=json.loads(retr.read_text(encoding="utf-8"))
            summary=data.get("summary",{})
            if int(summary.get("total",0))<40: errors.append("Retrieval tests below 40")
            if int(summary.get("failed",1))!=0: errors.append("Retrieval benchmark has failures")
        except Exception as e:
            errors.append(f"Cannot parse retrieval results: {e}")

    # Required artifacts.
    for rel in [
        "qa/run_retrieval_benchmark.py","qa/REPRODUCE_RETRIEVAL.md","qa/corpus_manifest.json",
        "qa/validate_package.py","qa/validate_semantic_provenance.py",
        "handoff/file_manifest.json","handoff/merge_manifest.json",
        "handoff/source_metadata_reconciliation.csv","handoff/claim_migration_log.csv",
        "handoff/production_build_summary.md"
    ]:
        if not (root/rel).exists(): errors.append(f"Missing required artifact: {rel}")

    # File manifest hash check.
    mf=root/"handoff/file_manifest.json"
    if mf.exists():
        try:
            data=json.loads(mf.read_text(encoding="utf-8"))
            entries=data.get("files",data if isinstance(data,list) else [])
            for e in entries:
                rel=e.get("path"); expected=e.get("sha256")
                if not rel or not expected: continue
                p=root/rel
                if not p.exists(): errors.append(f"Manifest missing file: {rel}")
                elif hashlib.sha256(p.read_bytes()).hexdigest()!=expected:
                    errors.append(f"Manifest hash mismatch: {rel}")
        except Exception as e:
            errors.append(f"Cannot validate file manifest: {e}")

    result={
        "root":str(root),
        "status":"PASS" if not errors and not warnings else ("PASS_WITH_WARNINGS" if not errors else "FAIL"),
        "stats":{"nodes":len(nodes),"source_notes":len(sources),"claims":len(claims_by_id),"claim_edges":len(claim_edges),"evidence_families":len(families),"evidence_backed_cases":evidence_cases},
        "errors":errors,"warnings":warnings
    }
    out=json.dumps(result,ensure_ascii=False,indent=2)
    print(out)
    op=Path(args.json_output) if args.json_output else root/"qa/package_validation.json"
    op.write_text(out,encoding="utf-8")
    raise SystemExit(0 if not errors and not warnings else 1)

if __name__=="__main__":
    main()
