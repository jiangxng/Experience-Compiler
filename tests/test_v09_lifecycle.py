import json,tempfile,unittest
from pathlib import Path
from ec.domain import Scope,ScopeKind,Provenance
from ec.knowledge.model import KnowledgeRecord,KnowledgeKind,KnowledgeStatus
from ec.storage.sqlite import SqliteKnowledgeRepository
from ec.retrieval import HybridRetriever
from ec.context_v2 import AdaptiveContextCompiler
from ec.learning.registry import LearningStrategyRegistry
from ec.learning.defaults import external_regulation_strategy,case_outcome_learning_strategy
from ec.learning.loop import OutcomeLearningLoop,DecisionObservation
from ec.model_gateway import ModelGateway,DeterministicReferenceModel
from ec.intelligence.lifecycle import IntelligenceLifecycle,IntelligenceTask
from ec.intelligence.manufacturing import manufacturing_experience_planner
from ec.intelligence.contradiction import detect_contradictions
from ec.intelligence.patterns import PatternMiner
from ec.intelligence.quality import assess_context

def registry():
 r=LearningStrategyRegistry();r.register(external_regulation_strategy());r.register(case_outcome_learning_strategy());return r
def fact(repo,value,confidence=.9):
 x=KnowledgeRecord(kind=KnowledgeKind.FACT,subject="critical material",predicate="availability",value=value,
  scope=Scope(ScopeKind.TENANT,"acme","acme"),provenance=Provenance("test","fixture","seed","r"),
  confidence=confidence,status=KnowledgeStatus.ACCEPTED);repo.append(x);return x

class V09Test(unittest.TestCase):
 def test_end_to_end_intelligence_learning_lifecycle(self):
  with tempfile.TemporaryDirectory() as d:
   repo=SqliteKnowledgeRepository(Path(d)/"ec.db");fact(repo,"shortage")
   compiler=AdaptiveContextCompiler(HybridRetriever(repo),registry())
   loop=OutcomeLearningLoop(repo)
   life=IntelligenceLifecycle(compiler,ModelGateway([DeterministicReferenceModel()]),"reference/deterministic-v1",manufacturing_experience_planner,loop)
   task=IntelligenceTask("acme","manufacturing","production-planner","resolve material shortage","critical material shortage","high")
   result=life.analyze(task)
   self.assertTrue(result.context_pack.items);self.assertEqual(result.experience_proposal.regions[0].capability,"decision-panel")
   learned=life.observe_outcome(task=task,decision=result.decision,outcome="order delivered on time",metric_delta=.15)
   self.assertEqual(learned[-1].kind,KnowledgeKind.LESSON)
 def test_contradictions_block_decision_readiness(self):
  with tempfile.TemporaryDirectory() as d:
   repo=SqliteKnowledgeRepository(Path(d)/"ec.db");a=fact(repo,"available");b=fact(repo,"shortage")
   cs=detect_contradictions([a,b]);self.assertEqual(len(cs),1)
   class I:
    def __init__(self,c):self.confidence=c
   q=assess_context([I(.9),I(.9)],cs);self.assertFalse(q.decision_ready)
 def test_pattern_mining_requires_repetition(self):
  obs=[DecisionObservation("late","alternate supplier","on time",.1,"t","manufacturing") for _ in range(4)]
  ps=PatternMiner().mine(obs);self.assertEqual(ps[0].observations,4);self.assertGreater(ps[0].confidence,.7)
 def test_manufacturing_has_five_reference_scenarios(self):
  p=Path(__file__).parents[1]/"industry-packs/manufacturing/demos/scenario-catalog-v0.9.json"
  self.assertEqual(len(json.loads(p.read_text())["scenarios"]),5)
if __name__=="__main__":unittest.main()
