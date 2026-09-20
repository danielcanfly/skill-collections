import json,tempfile,unittest
from pathlib import Path
from runtime_stabilizer.state import init,load,save
from runtime_stabilizer import cli
import subprocess,sys

class TestRetry(unittest.TestCase):
    def test_retry_only_current_blocked_phase(self):
        with tempfile.TemporaryDirectory() as td:
            inc=init(Path(td),'demo')
            s=load(inc)
            s['phases']['P0_PREFLIGHT']['status']='BLOCKED'
            s['phases']['P0_PREFLIGHT']['reason']='fixture blocker'
            save(inc,s)
            q=subprocess.run([sys.executable,'-m','runtime_stabilizer.cli','retry-blocked','--incident',str(inc)],text=True,capture_output=True)
            self.assertEqual(q.returncode,0,q.stderr)
            s=load(inc)
            self.assertEqual(s['phases']['P0_PREFLIGHT']['status'],'PENDING')
            self.assertEqual(s['phases']['P0_PREFLIGHT']['previous_blocker'],'fixture blocker')
