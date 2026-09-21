#!/usr/bin/env python3
from pathlib import Path
import argparse,re,difflib
from common import result,emit,norm,load_json
ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--config');ap.add_argument('--profile');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root);errors=[];notes=[]
paths=list((root/'knowledge/sources').glob('*.md')) if (root/'knowledge/sources').exists() else []
def section(t,h):
    m=re.search(rf'##\s+{re.escape(h)}\s*(.*?)(?:\n##\s+|\Z)',t,re.S|re.I);return re.sub(r'\s+',' ',m.group(1).strip()) if m else ''
for p in paths:
    t=p.read_text(encoding='utf-8',errors='replace'); findings=section(t,'Source-specific Findings'); limits=section(t,'What This Source Does Not Establish'); loc=section(t,'Locators') or section(t,'Evidence Locators')
    if len(findings)<100: errors.append(f'{p.name}: source-specific findings too short')
    if len(limits)<80: errors.append(f'{p.name}: source-specific limitations too short')
    if len(loc)<15 or re.fullmatch(r'https?://\S+',loc): errors.append(f'{p.name}: precise locator section missing')
    notes.append((p.name,findings+' | '+limits))
for i,(a1,t1) in enumerate(notes):
    for a2,t2 in notes[i+1:]:
        q=difflib.SequenceMatcher(None,norm(t1),norm(t2)).ratio()
        if q>.88: errors.append(f'source-note semantic template cluster {q:.3f}: {a1}/{a2}')
r=load_json(root/'qa/source_note_depth_receipt.json',{})
if r.get('status')!='PASS': errors.append('source-note depth receipt not PASS')
emit(result('PASS' if not errors else 'FAIL',errors,stats={'source_notes':len(paths)}),a.output)
