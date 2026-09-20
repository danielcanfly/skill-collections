from __future__ import annotations
import argparse,json,os,shutil,sys
from pathlib import Path

from . import __version__
from .config import load
from .state import (
    init as init_state, load as load_state, save, set_phase,
    next_phase, require_predecessor, PHASES, now
)
from .adapters import run_adapter,capabilities,adapter_dir,required_signal_gaps
from .diagnose import diagnose
from .hooks import run as run_hook,get as get_hook
from .soak import evaluate

def outjson(path,data):
    Path(path).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps(data,indent=2,sort_keys=True))

def cfg_for(incident,explicit=None):
    if explicit:
        return Path(explicit)
    p=Path(incident)/'config.toml'
    if not p.exists():
        raise SystemExit('incident config missing; pass --config or restore config.toml')
    return p

def main():
    ap=argparse.ArgumentParser(prog='runtime-stabilizer')
    ap.add_argument('--version',action='version',version=__version__)
    sp=ap.add_subparsers(dest='cmd',required=True)

    p=sp.add_parser('init')
    p.add_argument('--config',required=True)
    p.add_argument('--root',required=True)
    p.add_argument('--id')

    p=sp.add_parser('status')
    p.add_argument('--incident',required=True)

    p=sp.add_parser('run-next')
    p.add_argument('--incident',required=True)
    p.add_argument('--config')

    p=sp.add_parser('run-until-blocked')
    p.add_argument('--incident',required=True)
    p.add_argument('--config')
    p.add_argument('--max-steps',type=int,default=20)

    p=sp.add_parser('retry-blocked')
    p.add_argument('--incident',required=True)

    p=sp.add_parser('diagnose-evidence')
    p.add_argument('evidence_dir')

    p=sp.add_parser('record-root-cause')
    p.add_argument('--incident',required=True)
    p.add_argument('--trigger',required=True)
    p.add_argument('--confidence',choices=['PROVEN','HIGH','MEDIUM','LOW','UNKNOWN'],required=True)
    p.add_argument('--structural-defect',required=True)

    p=sp.add_parser('record-candidate')
    p.add_argument('--incident',required=True)
    p.add_argument('--revision',required=True)
    p.add_argument('--artifact',required=True)
    p.add_argument('--digest',required=True)

    p=sp.add_parser('evaluate-soak')
    p.add_argument('log')
    p.add_argument('--require-heavy-cycle',action='store_true')

    p=sp.add_parser('redact')
    p.add_argument('src')
    p.add_argument('dst')

    p=sp.add_parser('print-capabilities')
    p.add_argument('--config',required=True)

    p=sp.add_parser('validate-state')
    p.add_argument('incident')

    a=ap.parse_args()

    if a.cmd=='init':
        d=init_state(Path(a.root),a.id)
        shutil.copy2(a.config,d/'config.toml')
        print(d)
        return

    if a.cmd=='evaluate-soak':
        print(json.dumps(evaluate(Path(a.log),require_heavy_cycle=a.require_heavy_cycle),indent=2))
        return

    if a.cmd=='print-capabilities':
        cfg=load(Path(a.config))
        print(json.dumps(capabilities(cfg),indent=2,sort_keys=True))
        return

    if a.cmd=='validate-state':
        from .schemas import validate_state_file
        res=validate_state_file(Path(a.incident))
        print(json.dumps(res,indent=2,sort_keys=True))
        raise SystemExit(0 if res['status']=='PASS' else 2)

    if a.cmd=='diagnose-evidence':
        print(json.dumps(diagnose(Path(a.evidence_dir)),indent=2,sort_keys=True))
        return

    if a.cmd=='run-until-blocked':
        d=Path(a.incident)
        for _ in range(a.max_steps):
            current=load_state(d)
            p=next_phase(current)
            if p is None:
                print('COMPLETE')
                return
            status=current['phases'][p]['status']
            if status in ('BLOCKED','FAIL'):
                print(json.dumps({'status':status,'phase':p,'reason':current['phases'][p].get('reason')},indent=2))
                if status=='FAIL': raise SystemExit(2)
                return
            cmd=[sys.executable,'-m','runtime_stabilizer.cli','run-next','--incident',str(d)]
            if a.config:
                cmd += ['--config',a.config]
            q=__import__('subprocess').run(cmd)
            if q.returncode:
                raise SystemExit(q.returncode)
        raise SystemExit(f'BLOCKED: exceeded max steps {a.max_steps}')

    if a.cmd=='redact':
        from .privacy import redact,read_text_strict
        src,dst=Path(a.src),Path(a.dst)
        dst.mkdir(parents=True,exist_ok=True)
        copied=[]; omitted=[]
        for p in src.rglob('*'):
            if not p.is_file():
                continue
            text=read_text_strict(p)
            rel=str(p.relative_to(src))
            if text is None:
                omitted.append(rel)
                continue
            q=dst/p.relative_to(src)
            q.parent.mkdir(parents=True,exist_ok=True)
            q.write_text(redact(text),encoding='utf-8')
            copied.append(rel)
        report={'copied_text_files':copied,'omitted_binary_or_non_utf8':omitted}
        (dst/'REDACTION_REPORT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        print(json.dumps(report,indent=2,sort_keys=True))
        return

    d=Path(a.incident)
    s=load_state(d)

    if a.cmd=='status':
        print(json.dumps({
            'incident_id':s['incident_id'],
            'next_phase':next_phase(s),
            'phases':{p:s['phases'][p]['status'] for p in PHASES},
            'artifacts':s.get('artifacts',{}),
        },indent=2))
        return

    if a.cmd=='retry-blocked':
        p=next_phase(s)
        if p is None:
            print('COMPLETE')
            return
        if s['phases'][p]['status']!='BLOCKED':
            raise SystemExit(f'BLOCKED: current phase {p} is not BLOCKED')
        require_predecessor(s,p)
        previous=s['phases'][p].get('reason')
        set_phase(s,p,'PENDING',previous_blocker=previous,reason=None)
        save(d,s)
        print(json.dumps({'status':'PENDING','phase':p,'previous_blocker':previous},indent=2))
        return

    if a.cmd=='record-root-cause':
        require_predecessor(s,'P3_ROOT_CAUSE_QUALIFIED')
        r={
            'phase':'P3_ROOT_CAUSE_QUALIFIED',
            'status':'PASS',
            'captured_at':now(),
            'final_trigger':{'finding':a.trigger,'confidence':a.confidence},
            'structural_defect':a.structural_defect,
        }
        rp=d/'receipts'/'P3_ROOT_CAUSE_QUALIFIED.json'
        outjson(rp,r)
        set_phase(s,'P3_ROOT_CAUSE_QUALIFIED','PASS',receipt=str(rp))
        save(d,s)
        return

    if a.cmd=='record-candidate':
        require_predecessor(s,'P6_REPAIR_CANDIDATE_READY')
        r={
            'revision':a.revision,
            'artifact':a.artifact,
            'digest':a.digest,
            'captured_at':now(),
        }
        s['artifacts']['candidate']=r
        rp=d/'receipts'/'P6_REPAIR_CANDIDATE_READY.json'
        outjson(rp,{'phase':'P6_REPAIR_CANDIDATE_READY','status':'PASS',**r})
        set_phase(s,'P6_REPAIR_CANDIDATE_READY','PASS',receipt=str(rp))
        save(d,s)
        return

    cfg=load(cfg_for(d,a.config))
    p=next_phase(s)
    require_predecessor(s,p)
    set_phase(s,p,'RUNNING')
    save(d,s)
    rp=d/'receipts'/(p+'.json')
    ok=False

    try:
        if p=='P0_PREFLIGHT':
            q=run_adapter(cfg,'preflight')
            caps=capabilities(cfg)
            required=list(cfg.get('policy',{}).get('required_signals',[]))
            allow_partial=bool(cfg.get('policy',{}).get('allow_partial_required_signals',False))
            heavy_required=bool(cfg.get('soak',{}).get('require_heavy_cycle',False))
            missing=required_signal_gaps(
                caps, required,
                allow_partial=allow_partial,
                require_heavy_cycle=heavy_required,
            )
            ok=q.returncode==0 and not missing
            s['artifacts']['capabilities']=caps
            outjson(rp,{
                'phase':p,'status':'PASS' if ok else 'BLOCKED','captured_at':now(),
                'adapter':cfg['runtime']['adapter'],
                'adapter_path':str(adapter_dir(cfg)),
                'capabilities':caps,
                'required_signals':required,
                'allow_partial_required_signals':allow_partial,
                'heavy_cycle_required':heavy_required,
                'unavailable_required_signals':missing,
                'stdout':q.stdout,'stderr':q.stderr,
            })

        elif p=='P1_EVIDENCE_CAPTURED':
            q=run_adapter(cfg,'collect',str(d/'evidence'/'raw'))
            ok=q.returncode==0
            outjson(rp,{
                'phase':p,'status':'PASS' if ok else 'FAIL','captured_at':now(),
                'evidence_dir':str(d/'evidence'/'raw'),
                'stdout':q.stdout[-12000:],'stderr':q.stderr[-12000:],
            })

        elif p=='P2_TIMELINE_BUILT':
            r=diagnose(d/'evidence'/'raw')
            r.update({'phase':p,'status':'PASS'})
            outjson(rp,r)
            ok=True

        elif p=='P3_ROOT_CAUSE_QUALIFIED':
            set_phase(s,p,'BLOCKED',reason='ROOT_CAUSE_ADJUDICATION_REQUIRED: review P2 and run record-root-cause')
            save(d,s)
            print(s['phases'][p]['reason'])
            return

        elif p=='P4_ROLLBACK_READY':
            q=run_hook(cfg,'rollback_snapshot',s['incident_id'])
            ok=q.returncode==0
            if ok:
                s['artifacts']['rollback_snapshot']=q.stdout.strip()
            outjson(rp,{
                'phase':p,'status':'PASS' if ok else 'BLOCKED','captured_at':now(),
                'stdout':q.stdout,'stderr':q.stderr,
            })

        elif p=='P5_CLEANUP_QUALIFIED':
            q=run_hook(cfg,'cleanup_census',s['incident_id'],required=False)
            ok=True
            outjson(rp,{
                'phase':p,'status':'PASS','captured_at':now(),
                'note':'Cleanup is optional; census output is attached only when configured.',
                'stdout':q.stdout if q else '',
            })

        elif p=='P6_REPAIR_CANDIDATE_READY':
            set_phase(s,p,'BLOCKED',reason='REPAIR_REQUIRED: AI/application owner must create an exact candidate, then run record-candidate')
            save(d,s)
            print(s['phases'][p]['reason'])
            return

        elif p=='P7_REGRESSION_PASS':
            q=run_hook(cfg,'regression',s['incident_id'])
            ok=q.returncode==0
            outjson(rp,{
                'phase':p,'status':'PASS' if ok else 'FAIL','captured_at':now(),
                'stdout':q.stdout[-12000:],'stderr':q.stderr[-12000:],
            })

        elif p=='P8_RESOURCE_QUALIFICATION_PASS':
            q=run_hook(cfg,'resource_qualification',s['incident_id'])
            ok=q.returncode==0
            outjson(rp,{
                'phase':p,'status':'PASS' if ok else 'FAIL','captured_at':now(),
                'stdout':q.stdout[-12000:],'stderr':q.stderr[-12000:],
            })

        elif p=='P9_DEPLOY_READY':
            if os.environ.get('RUNTIME_STABILIZER_ALLOW_DEPLOY')!='YES_I_UNDERSTAND' or os.environ.get('RUNTIME_STABILIZER_DEPLOY_INCIDENT')!=s['incident_id']:
                set_phase(
                    s,p,'BLOCKED',
                    reason=f'DEPLOY_AUTHORIZATION_REQUIRED: set RUNTIME_STABILIZER_ALLOW_DEPLOY=YES_I_UNDERSTAND and RUNTIME_STABILIZER_DEPLOY_INCIDENT={s["incident_id"]}'
                )
                save(d,s)
                print(s['phases'][p]['reason'])
                return

            require_authority=bool(cfg.get('policy',{}).get('require_authority_snapshot',False))
            if get_hook(cfg,'authority_snapshot'):
                q=run_hook(cfg,'authority_snapshot','pre')
                if q.returncode!=0:
                    raise RuntimeError('authority_snapshot pre failed')
                pre=d/'artifacts'/'authority-pre.json'
                pre.write_text(q.stdout)
                s['artifacts']['authority_pre']=str(pre)
            elif require_authority:
                raise RuntimeError('MISSING_HOOK:authority_snapshot')

            ok=True
            outjson(rp,{
                'phase':p,'status':'PASS','captured_at':now(),
                'authorization':'incident-bound deploy gate',
                'authority_pre':s.get('artifacts',{}).get('authority_pre'),
            })

        elif p=='P10_PRODUCTION_VALIDATED':
            q=run_hook(cfg,'deploy',s['incident_id'])
            ok=q.returncode==0
            probe=None
            if ok:
                probe=run_hook(cfg,'production_probe',s['incident_id'])
                ok=probe.returncode==0

            rollback_attempted=False
            rollback_ok=None
            if not ok:
                rollback_cmd=get_hook(cfg,'rollback')
                if rollback_cmd:
                    rollback_attempted=True
                    rb=run_hook(cfg,'rollback',s['incident_id'],required=False)
                    rollback_ok=rb is not None and rb.returncode==0

            outjson(rp,{
                'phase':p,'status':'PASS' if ok else 'FAIL','captured_at':now(),
                'deploy_stdout':q.stdout[-12000:],
                'deploy_stderr':q.stderr[-12000:],
                'probe_stdout':probe.stdout[-12000:] if probe else '',
                'probe_stderr':probe.stderr[-12000:] if probe else '',
                'automatic_rollback_attempted':rollback_attempted,
                'automatic_rollback_succeeded':rollback_ok,
            })

        elif p=='P11_FINAL_SOAK_PASS':
            log=d/'artifacts'/'final-soak.jsonl'
            q=run_adapter(cfg,'soak',str(log))
            res=evaluate(
                log,
                min_samples=int(cfg.get('soak',{}).get('samples',61)),
                min_seconds=int(cfg.get('soak',{}).get('minimum_seconds',3600)),
                require_heavy_cycle=bool(cfg.get('soak',{}).get('require_heavy_cycle',False)),
            )
            ok=q.returncode==0 and res['status']=='PASS'
            outjson(rp,{
                'phase':p,'status':'PASS' if ok else 'FAIL','captured_at':now(),
                'evaluation':res,
                'adapter_stderr':q.stderr[-12000:],
            })

        elif p=='P12_AUTHORITY_CHECK_PASS':
            require_authority=bool(cfg.get('policy',{}).get('require_authority_snapshot',False))
            hook=get_hook(cfg,'authority_snapshot')
            if hook:
                pre_path=s.get('artifacts',{}).get('authority_pre')
                if not pre_path:
                    raise RuntimeError('pre-deploy authority snapshot missing')
                q=run_hook(cfg,'authority_snapshot','post')
                if q.returncode!=0:
                    raise RuntimeError('authority_snapshot post failed')
                post=d/'artifacts'/'authority-post.json'
                post.write_text(q.stdout)
                try:
                    a1=json.loads(Path(pre_path).read_text())
                    a2=json.loads(post.read_text())
                    ok=a1==a2
                except Exception:
                    ok=False
                outjson(rp,{
                    'phase':p,'status':'PASS' if ok else 'FAIL','captured_at':now(),
                    'authority_equal':ok,
                })
            elif require_authority:
                raise RuntimeError('MISSING_HOOK:authority_snapshot')
            else:
                ok=True
                outjson(rp,{
                    'phase':p,'status':'PASS','captured_at':now(),
                    'authority_check':'NOT_CONFIGURED_NOT_REQUIRED',
                })

        elif p=='P13_CLOSURE_PASS':
            ok=all(v['status']=='PASS' for k,v in s['phases'].items() if k!=p)
            outjson(rp,{
                'phase':p,
                'status':'PASS' if ok else 'BLOCKED',
                'captured_at':now(),
                'terminal':'RUNTIME_STABILIZATION_PASS' if ok else 'BLOCKED',
                'incident_id':s['incident_id'],
                'candidate':s.get('artifacts',{}).get('candidate'),
                'rollback_snapshot':s.get('artifacts',{}).get('rollback_snapshot'),
            })

        else:
            raise RuntimeError(p)

        set_phase(s,p,'PASS' if ok else 'FAIL',receipt=str(rp))
        save(d,s)
        if not ok:
            raise SystemExit(2)

    except RuntimeError as e:
        set_phase(s,p,'BLOCKED',reason=str(e))
        save(d,s)
        print(f'BLOCKED: {e}')
        raise SystemExit(3)


if __name__=='__main__':
    main()
