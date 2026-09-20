import subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SecretScanTest(unittest.TestCase):
    def test_clean_and_binary(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); (p/'a.txt').write_text('safe'); (p/'b.bin').write_bytes(b'x\x00ghp_' + b'A'*30)
            q=subprocess.run(['python3',str(ROOT/'scripts/secret_scan.py'),td])
            self.assertEqual(q.returncode,0)
    def test_secret_fails(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); (p/'a.txt').write_text('ghp_'+'A'*30)
            q=subprocess.run(['python3',str(ROOT/'scripts/secret_scan.py'),td],stdout=subprocess.DEVNULL)
            self.assertNotEqual(q.returncode,0)
if __name__=='__main__': unittest.main()
