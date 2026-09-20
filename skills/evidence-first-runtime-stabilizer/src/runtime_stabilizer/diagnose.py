from pathlib import Path
import re,datetime

def read(p):
    try:
        return p.read_text(errors='replace')
    except Exception:
        return ''

def diagnose(evidence:Path):
    texts='\n'.join(
        read(p) for p in evidence.rglob('*')
        if p.is_file() and p.stat().st_size<5_000_000
    )
    oom=bool(re.search(r'oom-kill|Out of memory|OOMKilled|Killed process',texts,re.I))
    swap=bool(re.search(r'swap',texts,re.I))
    restart=bool(re.search(r'restart[^\n]{0,30}[1-9]',texts,re.I))
    cls='MEMORY_PRESSURE' if oom else 'RESTART_LOOP' if restart else 'UNCLASSIFIED'
    return {
        'schema_version':'runtime-stabilizer-diagnosis/v2',
        'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'incident_class':cls,
        'signals':{
            'oom_evidence':oom,
            'swap_evidence_present':swap,
            'restart_evidence':restart,
        },
        'final_trigger':{
            'confidence':'UNKNOWN',
            'finding':'Requires AI adjudication.',
        },
        'structural_defect_draft':'Inspect workload shape, overlap, retention, and pressure timeline.' if cls=='MEMORY_PRESSURE' else 'Requires AI adjudication.',
        'warning':'Heuristic draft only.',
    }
