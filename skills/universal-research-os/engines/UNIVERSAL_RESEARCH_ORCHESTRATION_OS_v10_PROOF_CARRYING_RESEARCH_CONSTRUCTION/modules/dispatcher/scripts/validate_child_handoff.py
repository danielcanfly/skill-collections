#!/usr/bin/env python3
from pathlib import Path
import argparse,zipfile,tempfile,json,hashlib,py_compile
ap=argparse.ArgumentParser();ap.add_argument('package');a=ap.parse_args();zpath=Path(a.package).resolve();errors=[]
with zipfile.ZipFile(zpath) as z:
    if any('__pycache__/' in n or n.endswith('.pyc') for n in z.namelist()): errors.append('package contains forbidden Python cache artifacts')
    bad=z.testzip()
    if bad: errors.append('ZIP CRC failure '+bad)
    roots={Path(n).parts[0] for n in z.namelist() if n and not n.startswith('__MACOSX/')}
    if len(roots)!=1: errors.append('package must contain exactly one root')
    with tempfile.TemporaryDirectory() as td:
        z.extractall(td); root=Path(td)/next(iter(roots))
        req=['OUTPUT_SKELETON/research/source_identity_verification.csv','OUTPUT_SKELETON/research/edge_entailment.csv','OUTPUT_SKELETON/research/lineage_cascade_register.csv','OUTPUT_SKELETON/qa/candidate_self_check_receipt.json','OUTPUT_SKELETON/qa/TOPIC_SEMANTIC_RED_TEAM_TESTS.json','OUTPUT_SKELETON/qa/TOPIC_SEMANTIC_RED_TEAM_RESULTS.csv','OUTPUT_SKELETON/research/claim_clause_matrix.csv','OUTPUT_SKELETON/research/source_passage_registry.csv','OUTPUT_SKELETON/research/source_claim_domain_compatibility.csv','OUTPUT_SKELETON/qa/seal_state.json','OUTPUT_SKELETON/qa/reproduction_contract.json','OUTPUT_SKELETON/qa/production_surface_manifest.json','OUTPUT_SKELETON/research/source_refresh_queue.csv','AUDIT_OS/UNIVERSAL_RESEARCH_AUDIT_OS_v6_PROOF_CARRYING_RESEARCH_CONSTRUCTION/VERSION.json','AUDIT_OS/UNIVERSAL_RESEARCH_AUDIT_OS_v6_PROOF_CARRYING_RESEARCH_CONSTRUCTION/templates/independent_review/INDEPENDENT_TOPIC_RISK_REVIEW.csv','scripts/child_finalize_candidate.py','HANDOFF_IDENTITY.json','HANDOFF_REGISTRATION_TEMPLATE.json','OUTPUT_SKELETON/handoff/contract_lineage.json','manifest.json','SOURCE_INPUT_REGISTRY.json','TARGET_IDENTITY.json','PROTECTED_SURFACE_BASELINE.json','ALLOWED_CHANGE_MATRIX.csv','REQUIRED_OUTPUTS_AND_ACCEPTANCE.json','INDEPENDENCE_STATE_MACHINE.json','PACKAGE_VALIDATION.json','OUTPUT_SKELETON/external_stage_review/STAGE_REVIEW_IDENTITY.json','OUTPUT_SKELETON/external_stage_review/PASSAGE_REVIEW.csv','OUTPUT_SKELETON/external_stage_review/CLAUSE_REVIEW.csv']
        for rel in req:
            if not (root/rel).exists(): errors.append('missing '+rel)
        for rel in ['OUTPUT_SKELETON/research/provenance_edge_entailment.csv','OUTPUT_SKELETON/qa/SEAL_STATE.json']:
            if (root/rel).exists(): errors.append('forbidden legacy path '+rel)
        # v10 identity and generic finalizer checks
        if (root/'HANDOFF_IDENTITY.json').exists():
            hi=json.loads((root/'HANDOFF_IDENTITY.json').read_text(encoding='utf-8'))
            if hi.get('orchestration_os_version')!='10.0.0': errors.append('handoff identity is not v10')
            if hi.get('contract_generation')!='v10': errors.append('handoff contract generation is not v10')
        if (root/'OUTPUT_SKELETON/handoff/contract_lineage.json').exists():
            cl=json.loads((root/'OUTPUT_SKELETON/handoff/contract_lineage.json').read_text(encoding='utf-8'))
            if cl.get('status')!='PENDING_BINDING': errors.append('lineage skeleton must start PENDING_BINDING')
        fp=root/'OUTPUT_SKELETON/qa/finalize_candidate.py'
        if fp.exists():
            ft=fp.read_text(encoding='utf-8')
            if 'BFA_' in ft or 'SPSDA' in ft: errors.append('topic contamination in generic finalizer')
            if "cfg['final_output_name']" not in ft: errors.append('finalizer is not audit_config driven')
        # canonical headers
        checks={'OUTPUT_SKELETON/research/edge_entailment.csv':{'evidence_boundary','shared_concept_or_method','transfer_boundary','candidate_reviewer_status','evidence_origin'},'OUTPUT_SKELETON/research/source_identity_verification.csv':{'exact_metadata_locator','identity_status','temporal_status','reviewer_status','responsible_entity','author_basis','production_eligibility'},'OUTPUT_SKELETON/research/source_passage_registry.csv':{'capture_method','source_access_level','production_eligibility'},'OUTPUT_SKELETON/research/lineage_cascade_register.csv':{'source_note_reverse_source_ids','source_count','status'}}
        import csv
        for rel,cols in checks.items():
            p=root/rel
            if p.exists():
                with p.open(encoding='utf-8-sig',newline='') as f: hdr=set(next(csv.reader(f),[]))
                if not cols.issubset(hdr): errors.append(rel+' missing '+','.join(sorted(cols-hdr)))
        # manifest exact hashes
        mp=root/'manifest.json'
        if mp.exists():
            m=json.loads(mp.read_text(encoding='utf-8')); exp={x['path']:x['sha256'] for x in m.get('files',[])}
            actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix() not in {'manifest.json','SHA256SUMS.txt'}}
            if set(exp)!=actual: errors.append('manifest exact coverage mismatch')
            for rel,h in exp.items():
                p=root/rel
                if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=h: errors.append('manifest mismatch '+rel)
        for p in root.rglob('*.py'):
            try: py_compile.compile(str(p),doraise=True)
            except Exception as e: errors.append('compile failure '+str(p.relative_to(root))+': '+str(e))
print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors},ensure_ascii=False,indent=2));raise SystemExit(0 if not errors else 1)
