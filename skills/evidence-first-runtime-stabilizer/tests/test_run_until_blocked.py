import sys,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class RunUntilBlockedTest(unittest.TestCase):
    def test_stops_on_missing_custom_adapter_action(self):
        # The command must fail closed rather than looping forever.
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            cfg=root/'c.toml'
            cfg.write_text('''[runtime]\nadapter="custom"\ntarget="x"\nhealth_url=""\n[soak]\nsamples=2\ninterval_seconds=0\nminimum_seconds=0\nrequire_heavy_cycle=false\n[policy]\nrequire_authority_snapshot=false\nrequired_signals=[]\n[hooks]\nrollback_snapshot=""\ncleanup_census=""\nregression=""\nresource_qualification=""\ndeploy=""\nproduction_probe=""\nrollback=""\nauthority_snapshot=""\n''')
            q=subprocess.run([sys.executable,'-m','runtime_stabilizer.cli','init','--config',str(cfg),'--root',str(root)],text=True,capture_output=True,check=True)
            inc=q.stdout.strip()
            q=subprocess.run([sys.executable,'-m','runtime_stabilizer.cli','run-until-blocked','--incident',inc,'--max-steps','2'],text=True,capture_output=True)
            self.assertNotEqual(q.returncode,0)
if __name__=='__main__': unittest.main()
