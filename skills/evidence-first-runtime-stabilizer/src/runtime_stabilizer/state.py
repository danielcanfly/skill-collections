from __future__ import annotations
import datetime,json,uuid
from pathlib import Path

PHASES=[
 'P0_PREFLIGHT','P1_EVIDENCE_CAPTURED','P2_TIMELINE_BUILT','P3_ROOT_CAUSE_QUALIFIED',
 'P4_ROLLBACK_READY','P5_CLEANUP_QUALIFIED','P6_REPAIR_CANDIDATE_READY',
 'P7_REGRESSION_PASS','P8_RESOURCE_QUALIFICATION_PASS','P9_DEPLOY_READY',
 'P10_PRODUCTION_VALIDATED','P11_FINAL_SOAK_PASS','P12_AUTHORITY_CHECK_PASS','P13_CLOSURE_PASS'
]

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def init(root:Path,iid:str|None=None)->Path:
    iid=iid or 'runtime-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]
    d=root/iid
    (d/'receipts').mkdir(parents=True)
    (d/'evidence'/'raw').mkdir(parents=True)
    (d/'artifacts').mkdir()
    s={
        'schema_version':'runtime-stabilizer-incident-state/v2',
        'incident_id':iid,
        'created_at':now(),
        'updated_at':now(),
        'phases':{p:{'status':'PENDING','updated_at':None} for p in PHASES},
        'artifacts':{},
    }
    save(d,s)
    return d

def load(d:Path):
    return json.loads((d/'incident_state.json').read_text())

def save(d:Path,s):
    s['updated_at']=now()
    (d/'incident_state.json').write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')

def next_phase(s):
    for p in PHASES:
        if s['phases'][p]['status']!='PASS':
            return p
    return None

def set_phase(s,p,status,**kw):
    s['phases'][p].update({'status':status,'updated_at':now(),**kw})

def require_predecessor(s,p):
    i=PHASES.index(p)
    if i and s['phases'][PHASES[i-1]]['status']!='PASS':
        raise RuntimeError(f'{PHASES[i-1]} not PASS')
