import sys,tempfile,unittest,subprocess
from pathlib import Path

class TestCli(unittest.TestCase):
    def test_init_and_status(self):
        with tempfile.TemporaryDirectory() as td:
            cfg=Path(td)/'c.toml'
            cfg.write_text('[runtime]\nadapter="custom"\ntarget="x"\n[soak]\nsamples=61\nminimum_seconds=3600\nrequire_heavy_cycle=false\n[policy]\nrequired_signals=[]\nrequire_authority_snapshot=false\n[hooks]\n')
            root=Path(td)/'inc'
            p=subprocess.run([sys.executable,'-m','runtime_stabilizer.cli','init','--config',str(cfg),'--root',str(root),'--id','demo'],text=True,capture_output=True,check=True)
            inc=p.stdout.strip()
            q=subprocess.run([sys.executable,'-m','runtime_stabilizer.cli','status','--incident',inc],text=True,capture_output=True,check=True)
            self.assertIn('P0_PREFLIGHT',q.stdout)
