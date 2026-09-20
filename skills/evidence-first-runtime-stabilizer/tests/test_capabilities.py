import unittest
from runtime_stabilizer.adapters import required_signal_gaps

class CapabilityGateTest(unittest.TestCase):
    def test_unknown_required_signal_blocks(self):
        self.assertEqual(required_signal_gaps({'restart_count':'unknown'},['restart_count']),['restart_count'])
    def test_partial_blocks_by_default(self):
        self.assertEqual(required_signal_gaps({'restart_count':'partial'},['restart_count']),['restart_count'])
    def test_partial_can_be_explicitly_allowed(self):
        self.assertEqual(required_signal_gaps({'restart_count':'partial'},['restart_count'],allow_partial=True),[])
    def test_true_signal_passes(self):
        self.assertEqual(required_signal_gaps({'restart_count':True},['restart_count']),[])
    def test_heavy_cycle_requirement_is_capability_gated(self):
        self.assertEqual(required_signal_gaps({'restart_count':True,'heavy_processes':False},['restart_count'],require_heavy_cycle=True),['heavy_processes(required_by_soak)'])

if __name__=='__main__': unittest.main()
