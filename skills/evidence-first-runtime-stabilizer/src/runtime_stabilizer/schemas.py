from __future__ import annotations
from pathlib import Path
import json
from .state import PHASES

def validate_state_file(path: Path) -> dict:
    state_path=path/'incident_state.json' if path.is_dir() else path
    data=json.loads(state_path.read_text())
    errors=[]
    for key in ['schema_version','incident_id','created_at','updated_at','phases','artifacts']:
        if key not in data: errors.append(f'missing {key}')
    phases=data.get('phases',{})
    for p in PHASES:
        if p not in phases: errors.append(f'missing phase {p}')
        elif phases[p].get('status') not in ['PENDING','RUNNING','PASS','FAIL','BLOCKED']:
            errors.append(f'{p} invalid status {phases[p].get("status")}')
    return {'status':'PASS' if not errors else 'FAIL','errors':errors,'path':str(state_path)}
