import json,tempfile,unittest,datetime
from pathlib import Path
from runtime_stabilizer.soak import evaluate

class TestSoak(unittest.TestCase):
    def make(self,baseline_restart=0,restart_bump=False,heavy=True,runtime_health='healthy'):
        td=tempfile.TemporaryDirectory()
        p=Path(td.name)/'x.jsonl'
        t=datetime.datetime(2026,1,1,tzinfo=datetime.timezone.utc)
        rows=[]
        for i in range(61):
            restart=baseline_restart + (1 if restart_bump and i>=10 else 0)
            rows.append({
                'ts':(t+datetime.timedelta(seconds=61*i)).isoformat(),
                'sample':i+1,
                'running':True,
                'oom_killed':False,
                'restart_count':restart,
                'runtime_health':runtime_health,
                'kernel_oom_events':0,
                'public_health_http':200,
                'public_health_seconds':0.01,
                'heavy_processes':2 if heavy and 5<=i<=7 else 1,
            })
        p.write_text('\n'.join(json.dumps(x) for x in rows)+'\n')
        return td,p

    def test_pass(self):
        td,p=self.make()
        self.assertEqual(evaluate(p,require_heavy_cycle=True)['status'],'PASS')
        td.cleanup()

    def test_historical_restart_baseline_can_be_stable(self):
        td,p=self.make(baseline_restart=3)
        r=evaluate(p,require_heavy_cycle=True)
        self.assertEqual(r['status'],'PASS')
        self.assertEqual(r['restart_count_baseline'],3)
        td.cleanup()

    def test_restart_change_fails(self):
        td,p=self.make(baseline_restart=3,restart_bump=True)
        self.assertEqual(evaluate(p,require_heavy_cycle=True)['status'],'FAIL')
        td.cleanup()

    def test_runtime_health_failure_fails(self):
        td,p=self.make(runtime_health='unhealthy')
        self.assertEqual(evaluate(p,require_heavy_cycle=True)['status'],'FAIL')
        td.cleanup()

    def test_missing_heavy_cycle_fails_when_required(self):
        td,p=self.make(heavy=False)
        self.assertEqual(evaluate(p,require_heavy_cycle=True)['status'],'FAIL')
        td.cleanup()
