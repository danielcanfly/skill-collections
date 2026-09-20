import sys,json,subprocess,tempfile,unittest
from pathlib import Path

class RedactCliTest(unittest.TestCase):
    def test_binary_omitted_and_reported(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); src=root/'src'; dst=root/'dst'; src.mkdir()
            (src/'a.txt').write_text('Authorization:'+' Bearer '+'SECRET')
            (src/'b.bin').write_bytes(b'abc\x00SECRET')
            q=subprocess.run([sys.executable,'-m','runtime_stabilizer.cli','redact',str(src),str(dst)],text=True,capture_output=True)
            self.assertEqual(q.returncode,0,q.stderr)
            self.assertTrue((dst/'a.txt').exists())
            self.assertFalse((dst/'b.bin').exists())
            report=json.loads((dst/'REDACTION_REPORT.json').read_text())
            self.assertIn('b.bin',report['omitted_binary_or_non_utf8'])
            self.assertNotIn('SECRET',(dst/'a.txt').read_text())

if __name__=='__main__': unittest.main()
