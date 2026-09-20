import sys,tempfile,subprocess,json
from pathlib import Path

def test_validate_state_and_capabilities():
    with tempfile.TemporaryDirectory() as td:
        cfg=Path(td)/'c.toml'
        cfg.write_text('[runtime]\nadapter="custom"\ntarget="x"\n[soak]\nsamples=61\nminimum_seconds=3600\nrequire_heavy_cycle=false\n[policy]\nrequired_signals=[]\nrequire_authority_snapshot=false\n[hooks]\n')
        root=Path(td)/'inc'
        p=subprocess.run([sys.executable,'-m','runtime_stabilizer.cli','init','--config',str(cfg),'--root',str(root),'--id','demo'],text=True,capture_output=True,check=True)
        inc=p.stdout.strip()
        q=subprocess.run([sys.executable,'-m','runtime_stabilizer.cli','validate-state',inc],text=True,capture_output=True,check=True)
        assert '"status": "PASS"' in q.stdout
        c=subprocess.run([sys.executable,'-m','runtime_stabilizer.cli','print-capabilities','--config',str(cfg)],text=True,capture_output=True,check=True)
        assert c.stdout.strip().startswith('{')
