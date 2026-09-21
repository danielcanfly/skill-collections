#!/usr/bin/env python3
from pathlib import Path
import argparse,re,collections,difflib
from common import result,emit,load_json,norm

ap=argparse.ArgumentParser(); ap.add_argument('root'); ap.add_argument('--config'); ap.add_argument('--profile'); ap.add_argument('--output'); a=ap.parse_args()
root=Path(a.root); profile=load_json(a.profile,{}) if a.profile else {}; errors=[]; warnings=[]
mins=profile.get('minimum_node_body_chars',{'concepts':1800,'patterns':1800,'checklists':1200})
files=[]
for kind in ['concepts','patterns','checklists']:
    d=root/'knowledge'/kind
    if d.exists(): files.extend((kind,p) for p in d.rglob('*.md'))
if not files: errors.append('no production nodes found under knowledge/concepts|patterns|checklists')

def strip_front(t): return re.sub(r'^---\s*.*?\s*---\s*','',t,flags=re.S)
def headings(t): return [x.strip().lower() for x in re.findall(r'^##+\s+(.+?)\s*$',t,re.M)]
def has_any(hs,terms): return any(any(term in h for term in terms) for h in hs)
section_groups={
 'definition_boundary':['definition','scope','boundary','what it is','定義','範圍','邊界','是什麼'],
 'decision_use':['decision','when to use','application','how to use','workflow','action','決策','適用','如何使用','流程','行動'],
 'failure_limits':['failure','limitation','risk','caveat','counterexample','misuse','失敗','限制','風險','反例','誤用'],
 'evidence_provenance':['evidence','source','provenance','support','citation','證據','來源','溯源','支持']}
paragraph_owners=collections.defaultdict(set); bodies=[]
for kind,p in files:
    raw=p.read_text(encoding='utf-8',errors='replace'); body=strip_front(raw); text=re.sub(r'\s+',' ',body).strip(); hs=headings(body); rel=p.relative_to(root).as_posix(); minimum=int(mins.get(kind,1200))
    if len(text)<minimum: errors.append(f'{rel}: operational body too short {len(text)} < {minimum}')
    if len(hs)<4: errors.append(f'{rel}: fewer than four substantive sections')
    for gid,terms in section_groups.items():
        if not has_any(hs,terms): errors.append(f'{rel}: missing {gid} section')
    paragraphs=[re.sub(r'\s+',' ',x).strip() for x in re.split(r'\n\s*\n',body) if len(re.sub(r'\s+',' ',x).strip())>=120 and not x.lstrip().startswith('#')]
    for para in paragraphs: paragraph_owners[norm(para)].add(rel)
    bodies.append((rel,norm(text)))
threshold=max(3,int(len(files)*float(profile.get('max_shared_paragraph_fraction',0.10)))+1)
shared={p:owners for p,owners in paragraph_owners.items() if len(owners)>=threshold}
for para,owners in shared.items(): errors.append(f'repeated boilerplate paragraph appears in {len(owners)} nodes: {sorted(owners)[:4]}')
# A stricter operational-core pairwise check than the legacy full-page diversity gate.
thr=float(profile.get('operational_node_similarity_threshold',0.82))
for i,(a1,t1) in enumerate(bodies):
    for a2,t2 in bodies[i+1:]:
        if len(t1)>500 and len(t2)>500:
            q=difflib.SequenceMatcher(None,t1,t2).ratio()
            if q>=thr: errors.append(f'operational node similarity {q:.3f}: {a1} / {a2}')
emit(result('PASS' if not errors else 'FAIL',errors,warnings,{'nodes':len(files),'shared_boilerplate_clusters':len(shared),'minimums':mins,'pairwise_threshold':thr}),a.output)
