#!/usr/bin/env python3
"""Deterministic lexical retrieval smoke test for a universal Knowledge OS candidate.

This validates lexical retrievability only. It does not claim production vector,
reranker, graph or agent-planner performance.
"""
from pathlib import Path
import argparse, hashlib, json, math, re, unicodedata
try:
    import yaml
except ImportError as e:
    raise SystemExit("PyYAML required: python -m pip install pyyaml") from e

CONFIG={"k1":1.2,"b":0.75,"weights":{"title":6.0,"aliases":4.5,"summary":2.5,"body":1.0,"identifier":3.0},"phrase_bonus":5.0,"top_k":10}

def frontmatter(path):
    t=path.read_text(encoding="utf-8")
    if not t.startswith("---"): return {},t
    parts=t.split("---",2)
    return (yaml.safe_load(parts[1]) or {},parts[2]) if len(parts)==3 else ({},t)

def tokens(text):
    s=unicodedata.normalize("NFKC",str(text)).lower()
    out=re.findall(r"[a-z0-9]+(?:[-'][a-z0-9]+)*",s)
    for run in re.findall(r"[\u3400-\u9fff]+",s):
        out.extend(list(run))
        out.extend(run[i:i+2] for i in range(len(run)-1))
    return out

def first_summary(body):
    m=re.search(r"## (?:定義|Context|Problem|Source-specific Findings)\s*(.*?)(?:\n## |\Z)",body,re.S)
    return m.group(1).strip() if m else body[:800]

def load(root):
    docs=[]
    for p in sorted((root/"knowledge").rglob("*.md")):
        fm,b=frontmatter(p); did=fm.get("id") or fm.get("source_id")
        if not did: continue
        aliases=fm.get("aliases") or []
        if isinstance(aliases,str): aliases=[aliases]
        fields={"title":str(fm.get("title","")),"aliases":" ".join(map(str,aliases)),"summary":first_summary(b),"body":b,"identifier":str(did).replace("/"," ").replace("-"," ")}
        docs.append({"id":did,"path":p.relative_to(root).as_posix(),"title":fm.get("title",""),"aliases":aliases,"doc_type":("source" if fm.get("source_id") else fm.get("x-kos-kind","node")),"fields":fields})
    return docs

def rank(query,docs,query_class):
    q=tokens(query); N=len(docs); dfs={}; fts=[]
    for d in docs:
        ft={k:tokens(v) for k,v in d["fields"].items()}; fts.append(ft)
        for t in set(x for xs in ft.values() for x in xs): dfs[t]=dfs.get(t,0)+1
    avg={k:sum(len(ft[k]) for ft in fts)/max(N,1) for k in CONFIG["weights"]}
    scored=[]; qnorm=unicodedata.normalize("NFKC",query).lower()
    for d,ft in zip(docs,fts):
        score=0.0
        for field,w in CONFIG["weights"].items():
            counts={}
            for t in ft[field]: counts[t]=counts.get(t,0)+1
            dl=len(ft[field]) or 1
            for t in q:
                tf=counts.get(t,0)
                if not tf: continue
                idf=math.log(1+(N-dfs.get(t,0)+.5)/(dfs.get(t,0)+.5))
                denom=tf+CONFIG["k1"]*(1-CONFIG["b"]+CONFIG["b"]*dl/max(avg[field],1))
                score+=w*idf*(tf*(CONFIG["k1"]+1)/denom)
        title=unicodedata.normalize("NFKC",str(d["title"])).lower()
        aliases=[unicodedata.normalize("NFKC",str(a)).lower() for a in d["aliases"]]
        if title and title in qnorm: score+=CONFIG["phrase_bonus"]
        if any(a and a in qnorm for a in aliases): score+=CONFIG["phrase_bonus"]
        if query_class=="source-provenance":
            score+=28 if d["doc_type"]=="source" else -6
        else:
            score+=20 if d["doc_type"]!="source" else 0
            if query_class=="audit" and d["doc_type"]=="checklist": score+=12
            if query_class=="how-to" and d["doc_type"] in {"checklist","pattern"}: score+=5
        scored.append((score,d))
    return sorted(scored,key=lambda x:(-x[0],x[1]["id"]))

def stable_generated_at(root):
    cfg_path=root/"audit_config.json"
    try:
        cfg=json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    except Exception:
        cfg={}
    return str(cfg.get("reproducible_generated_at","2000-01-01T00:00:00Z"))

def manifest(root,docs):
    files=[]; digest=hashlib.sha256()
    for d in docs:
        p=root/d["path"]; h=hashlib.sha256(p.read_bytes()).hexdigest()
        files.append({"id":d["id"],"path":d["path"],"sha256":h})
        digest.update(d["path"].encode()); digest.update(bytes.fromhex(h))
    return {"generated_at":stable_generated_at(root),"configuration":CONFIG,"document_count":len(files),"corpus_hash":digest.hexdigest(),"files":files}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("root_positional",nargs="?"); ap.add_argument("--root",dest="root_option"); args=ap.parse_args()
    root_arg=args.root_option or args.root_positional or str(Path(__file__).resolve().parents[1])
    root=Path(root_arg).resolve(); docs=load(root)
    tests=json.loads((root/"qa/retrieval_test_cases.json").read_text(encoding="utf-8"))
    if not isinstance(tests,list) or len(tests)<40:
        raise SystemExit("At least 40 retrieval tests are required.")
    required_classes={"definition","comparison","how-to","decision/application","audit","source-provenance","multi-hop","adversarial"}
    classes={str(t.get("class","")).strip().lower() for t in tests}
    holdout=sum(1 for t in tests if t.get("split")=="holdout" or t.get("is_holdout") is True)
    negative=sum(1 for t in tests if t.get("negative_ids"))
    if not required_classes.issubset(classes):
        raise SystemExit(f"Missing required retrieval classes: {sorted(required_classes-classes)}")
    if holdout/len(tests)<0.25 or negative/len(tests)<0.25:
        raise SystemExit(f"Weak retrieval design: holdout={holdout}/{len(tests)}, negatives={negative}/{len(tests)}")
    if sum(1 for t in tests if t.get("class")=="adversarial")<4 or sum(1 for t in tests if t.get("class")=="multi-hop")<4:
        raise SystemExit("At least four adversarial and four multi-hop tests are required.")
    cm=manifest(root,docs); (root/"qa/corpus_manifest.json").write_text(json.dumps(cm,ensure_ascii=False,indent=2),encoding="utf-8")
    results=[]; passed=0
    for t in tests:
        ranked=rank(t["query"],docs,t["class"])[:CONFIG["top_k"]]
        ids=[d["id"] for _,d in ranked]; exp=t["expected_ids"]; neg=t.get("negative_ids",[])
        ranks={e:(ids.index(e)+1 if e in ids else None) for e in exp}
        first=ranks.get(exp[0]); neg_ok=all((n not in ids) or (first is not None and ids.index(n)+1>first) for n in neg)
        ok=all(ranks[e] is not None for e in exp) and first is not None and first<=5 and neg_ok
        passed+=int(ok)
        results.append({**t,"status":"PASS" if ok else "FAIL","query_sha256":hashlib.sha256(t["query"].encode()).hexdigest(),"corpus_sha256":cm["corpus_hash"],"ranked_ids":[d["id"] for s,d in ranked],"expected_ranks":ranks,"negative_check_passed":neg_ok,"top_k":[{"rank":i+1,"id":d["id"],"title":d["title"],"score":round(s,6),"path":d["path"]} for i,(s,d) in enumerate(ranked)]})
    out={"generated_at":stable_generated_at(root),"corpus_hash":cm["corpus_hash"],"configuration":CONFIG,"scope_note":"Lexical smoke test only; not a production vector/reranker/graph benchmark.","summary":{"total":len(tests),"passed":passed,"failed":len(tests)-passed},"results":results}
    (root/"qa/retrieval_results.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# Retrieval Benchmark Results","",f"- Corpus hash: `{cm['corpus_hash']}`",f"- Documents: **{len(docs)}**",f"- Passed: **{passed}/{len(tests)}**","- Scope: lexical smoke test only.","","| ID | Class | Query | Primary expected | Rank | Status |","|---|---|---|---|---:|---|"]
    for r in results:
        er=r["expected_ranks"].get(r["expected_ids"][0]); lines.append(f"| {r['test_id']} | {r['class']} | {r['query'].replace('|','/')} | `{r['expected_ids'][0]}` | {er or '—'} | {r['status']} |")
    (root/"qa/retrieval_results.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(out["summary"]))
    raise SystemExit(0 if passed==len(tests) else 1)

if __name__=="__main__":
    main()
