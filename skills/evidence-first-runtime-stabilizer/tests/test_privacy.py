import tempfile,unittest,json
from pathlib import Path
from runtime_stabilizer.privacy import redact,read_text_strict

class PrivacyTest(unittest.TestCase):
    def test_redact(self):
        s='Authorization:'+' Bearer '+'abc123\npassword=supersecret\nghp_'+'A'*30
        r=redact(s)
        self.assertNotIn('abc123',r)
        self.assertNotIn('supersecret',r)
        self.assertNotIn('ghp_',r)
    def test_binary_is_not_text(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'binary.bin'; p.write_bytes(b'abc\x00def')
            self.assertIsNone(read_text_strict(p))
    def test_non_utf8_is_not_text(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'binary.bin'; p.write_bytes(b'\xff\xfe\x80')
            self.assertIsNone(read_text_strict(p))

if __name__=='__main__': unittest.main()
