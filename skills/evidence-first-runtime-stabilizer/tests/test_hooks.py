import tempfile,unittest
from pathlib import Path
from runtime_stabilizer.hooks import run

class TestHooks(unittest.TestCase):
    def test_relative_hook_resolves_from_config_dir(self):
        with tempfile.TemporaryDirectory() as td:
            d=Path(td)
            script=d/'ok.sh'
            script.write_text('#!/usr/bin/env bash\necho hook-ok\n')
            script.chmod(0o755)
            cfg={'_meta':{'config_dir':td},'hooks':{'x':'./ok.sh'}}
            p=run(cfg,'x')
            self.assertEqual(p.returncode,0)
            self.assertIn('hook-ok',p.stdout)
