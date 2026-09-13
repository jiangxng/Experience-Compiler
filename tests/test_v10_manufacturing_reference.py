import json,unittest
from pathlib import Path
from ec.manufacturing.assessment import ManufacturingSituation,ManufacturingDecisionEngine
from ec.manufacturing.benchmarks import ManufacturingBenchmark
from ec.governance.promotion import KnowledgePromotionPolicy
from ec.governance.authorization import ScopeAuthorizer
from ec.operations.readiness import reference_readiness_report
from ec.domain import Scope,ScopeKind
from ec.integration.eidos import ExperienceProposal,ExperienceRegionProposal

class V10Test(unittest.TestCase):
 def test_manufacturing_preassessment_preserves_hard_constraints(self):
  s=ManufacturingSituation("capacity-overload",{},{"promise_date":"2026-09-18","customer_priority":"strategic"},{"overtime_allowed":False})
  a=ManufacturingDecisionEngine().assess(s,["overtime","subcontract"])
  self.assertFalse(a[0].feasible);self.assertTrue(a[1].feasible)
 def test_knowledge_promotion_is_governed(self):
  p=KnowledgePromotionPolicy()
  self.assertFalse(p.decide(kind="policy",confidence=.99,independent_sources=2,contradicted=False,tenant_scope=True).allowed)
  self.assertTrue(p.decide(kind="policy",confidence=.99,independent_sources=2,contradicted=False,tenant_scope=True,human_reviewed=True).allowed)
 def test_cross_tenant_scope_is_denied(self):
  s=Scope(ScopeKind.TENANT,"a","a")
  self.assertFalse(ScopeAuthorizer().can_read(s,tenant_id="b").allowed)
  self.assertTrue(ScopeAuthorizer().can_read(s,tenant_id="a").allowed)
 def test_reference_readiness_never_claims_environment_certification(self):
  r=reference_readiness_report();self.assertFalse(r.passed)
  failed={x.name for x in r.checks if not x.passed};self.assertIn("production load/HA/DR certification",failed)
 def test_all_five_scenarios_have_playbooks(self):
  p=Path(__file__).parents[1]/"industry-packs/manufacturing/decisions/playbooks-v1.json"
  self.assertEqual(len(json.loads(p.read_text())["playbooks"]),5)
 def test_benchmark_requires_decision_evidence_impact(self):
  regs=tuple(ExperienceRegionProposal(x,x,"shared-stable","important",{}) for x in ("decision-panel","evidence-stack","impact-preview"))
  xp=ExperienceProposal("0.1.0","p","now","x","x","role",regs,(),"fallback")
  self.assertTrue(ManufacturingBenchmark().evaluate_experience("quality-hold",xp).passed)
if __name__=="__main__":unittest.main()
