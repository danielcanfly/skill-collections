#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, csv, json, re, sys
try:
    import yaml
except ImportError:
    raise SystemExit("PyYAML required: python -m pip install pyyaml")

def fm(path):
    t=path.read_text(encoding="utf-8")
    if not t.startswith("---"): return {},t
    p=t.split("---",2)
    return (yaml.safe_load(p[1]) or {},p[2]) if len(p)==3 else ({},t)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--json-output")
    args=ap.parse_args()
    root=Path(args.root).resolve()
    errors=[]; warnings=[]

    ledger=root/"research/claim_ledger.csv"
    rows=list(csv.DictReader(ledger.open(encoding="utf-8-sig",newline=""))) if ledger.exists() else []
    by_claim={}
    for r in rows:
        cid=r.get("claim_id","").strip()
        by_claim.setdefault(cid,[]).append(r)
        ctype=r.get("claim_type","").lower()
        support=r.get("support_challenge","")
        scope=r.get("scope","").strip()
        notes=r.get("notes","").strip()
        if support in {"partial-support","contextual-support"} and len(scope)<20:
            errors.append(f"{cid}: {support} scope is too vague")
        if "canonical synthesis" in ctype and support=="support" and scope in {"canonical node support","direct support",""}:
            warnings.append(f"{cid}: canonical synthesis has unqualified direct support")
        if len(r.get("claim",""))>420:
            warnings.append(f"{cid}: claim may be too broad/long")
        if r.get("claim","").count(";")>=3 or r.get("claim","").lower().count(" and ")>=5:
            warnings.append(f"{cid}: possible multi-clause overbreadth")
        if not notes:
            warnings.append(f"{cid}: no semantic provenance note")

    for cid,rs in by_claim.items():
        fams={r.get("evidence_family_id","") for r in rs if r.get("evidence_family_id")}
        types={r.get("claim_type","") for r in rs}
        if any("canonical synthesis" in t.lower() for t in types) and len(fams)<2:
            warnings.append(f"{cid}: canonical synthesis has fewer than two evidence families")
        if len({r.get("claim","") for r in rs})>1:
            errors.append(f"{cid}: inconsistent claim text across rows")

    # Source-note boilerplate and direct/partial section alignment.
    findings_fingerprints={}
    for p in sorted((root/"knowledge/sources").glob("*.md")):
        meta,body=fm(p)
        sid=meta.get("source_id",p.stem)
        m=re.search(r"## Source-specific Findings\s*(.*?)(?:\n## |\Z)",body,re.S)
        text=re.sub(r"\s+"," ",m.group(1).strip()) if m else ""
        if text:
            findings_fingerprints.setdefault(text,[]).append(str(sid))
        if "## What This Source Does Not Establish" not in body:
            errors.append(f"{sid}: missing anti-overattribution section")
        direct=set(re.findall(r"`(C\d+[A-Z]?)`", re.search(r"## Claims Supported\s*(.*?)(?:\n## |\Z)",body,re.S).group(1) if re.search(r"## Claims Supported\s*(.*?)(?:\n## |\Z)",body,re.S) else ""))
        partial=set(re.findall(r"`(C\d+[A-Z]?)`", re.search(r"## Contextual or Partial Contributions\s*(.*?)(?:\n## |\Z)",body,re.S).group(1) if re.search(r"## Contextual or Partial Contributions\s*(.*?)(?:\n## |\Z)",body,re.S) else ""))
        for r in rows:
            if r.get("source_id")!=sid: continue
            cid=r.get("claim_id"); typ=r.get("support_challenge")
            if typ=="support" and cid not in direct:
                errors.append(f"{sid}: direct claim {cid} not in Claims Supported")
            if typ in {"partial-support","contextual-support"} and cid not in partial:
                errors.append(f"{sid}: {typ} claim {cid} not in Contextual/Partial section")

    for fp,sids in findings_fingerprints.items():
        if len(sids)>=4:
            warnings.append(f"Boilerplate source findings repeated across {len(sids)} notes: {sids[:6]}")

    # Alias purity heuristic.
    amap=root/"research/alias_map.csv"
    if amap.exists():
        for r in csv.DictReader(amap.open(encoding="utf-8-sig",newline="")):
            a=r.get("alias","").strip()
            if len(a)>80 or "?" in a or "？" in a or a.endswith("案例"):
                warnings.append(f"Possible non-alias: {r.get('canonical_id')} -> {a}")

    result={"root":str(root),"status":"PASS" if not errors and not warnings else ("PASS_WITH_WARNINGS" if not errors else "FAIL"),"errors":errors,"warnings":warnings}
    out=json.dumps(result,ensure_ascii=False,indent=2)
    print(out)
    op=Path(args.json_output) if args.json_output else root/"qa/semantic_provenance_validation.json"
    op.write_text(out,encoding="utf-8")
    raise SystemExit(0 if not errors and not warnings else 1)

if __name__=="__main__":
    main()
