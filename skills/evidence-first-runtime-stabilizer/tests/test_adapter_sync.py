import unittest
from pathlib import Path

class TestAdapterSync(unittest.TestCase):
    def test_public_and_packaged_adapters_match(self):
        root=Path(__file__).resolve().parents[1]
        a=root/'adapters'; b=root/'src/runtime_stabilizer/adapters_data'
        af={str(p.relative_to(a)):p.read_bytes() for p in a.rglob('*') if p.is_file()}
        bf={str(p.relative_to(b)):p.read_bytes() for p in b.rglob('*') if p.is_file()}
        self.assertEqual(af,bf)
