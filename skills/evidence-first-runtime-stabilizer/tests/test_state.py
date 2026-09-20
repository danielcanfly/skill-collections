import tempfile,unittest
from pathlib import Path
from runtime_stabilizer.state import init,load,next_phase

class TestState(unittest.TestCase):
    def test_init(self):
        with tempfile.TemporaryDirectory() as td:
            d=init(Path(td),'x')
            s=load(d)
            self.assertEqual(next_phase(s),'P0_PREFLIGHT')
