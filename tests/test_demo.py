import unittest
from ec.demos.manufacturing import build_demo
class DemoTests(unittest.TestCase):
    def test_manufacturing_proposal_is_semantic(self):
        ctx,p=build_demo(); caps={r.capability for r in p.regions}
        self.assertTrue({"decision-panel","evidence-stack","impact-preview"}.issubset(caps)); self.assertTrue(p.standard_fallback_ref); self.assertGreater(len(ctx.items),0)
if __name__=='__main__': unittest.main()
