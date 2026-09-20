import tempfile,unittest
from pathlib import Path
from runtime_stabilizer.diagnose import diagnose

class TestDiagnose(unittest.TestCase):
    def test_oom(self):
        with tempfile.TemporaryDirectory() as td:
            Path(td,'kernel.log').write_text('Out of memory: Killed process 1')
            self.assertEqual(diagnose(Path(td))['incident_class'],'MEMORY_PRESSURE')
