import json,tempfile,unittest,os
from pathlib import Path
from runtime_stabilizer.config import load
from runtime_stabilizer.adapters import adapter_dir,capabilities,run_adapter

class TestCustomAdapter(unittest.TestCase):
    def test_external_adapter_path(self):
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); ad=td/'adapter'; ad.mkdir()
            (ad/'capabilities.json').write_text(json.dumps({'runtime':'fixture','restart_count':True,'oom_killed':True,'heavy_processes':True,'public_health':True}))
            sh=ad/'preflight.sh'; sh.write_text('#!/bin/sh\necho ok\n'); sh.chmod(0o755)
            cfgp=td/'c.toml'; cfgp.write_text('[runtime]\nadapter="custom"\nadapter_path="adapter"\ntarget="x"\nhealth_url="http://localhost/health"\n')
            cfg=load(cfgp)
            self.assertEqual(adapter_dir(cfg),ad.resolve())
            self.assertIs(capabilities(cfg)['restart_count'],True)
            q=run_adapter(cfg,'preflight')
            self.assertEqual(q.returncode,0)
            self.assertIn('ok',q.stdout)
