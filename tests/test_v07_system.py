import tempfile, unittest
from pathlib import Path
from ec.domain import Scope,ScopeKind,Provenance
from ec.knowledge.model import KnowledgeRecord,KnowledgeKind,KnowledgeStatus
from ec.storage.sqlite import SqliteKnowledgeRepository
from ec.storage.evidence import FileEvidenceArchive
from ec.retrieval import HybridRetriever
from ec.context_v2 import AdaptiveContextCompiler
from ec.context import ContextRequest
from ec.learning.defaults import external_regulation_strategy,case_outcome_learning_strategy
from ec.learning.registry import LearningStrategyRegistry
from ec.learning.loop import OutcomeLearningLoop,DecisionObservation
from ec.research_v2 import ResearchPipeline,SourceDocument
from ec.model_gateway import ModelGateway,DeterministicReferenceModel,ModelRequest

def rec(subject,value,tenant="acme"):
    return KnowledgeRecord(kind=KnowledgeKind.FACT,subject=subject,predicate="status",value=value,
      scope=Scope(ScopeKind.TENANT,tenant,tenant),provenance=Provenance("test","suite","fixture","run"),
      confidence=.9,status=KnowledgeStatus.ACCEPTED)

class V07Test(unittest.TestCase):
    def test_durable_persistence_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            repo=SqliteKnowledgeRepository(Path(d)/"ec.db"); r=rec("critical material","delayed")
            repo.append(r); got=repo.get(r.record_id)
            self.assertEqual(got.value,"delayed"); self.assertEqual(got.scope.tenant_id,"acme")
    def test_content_addressed_evidence_is_deduplicated(self):
        with tempfile.TemporaryDirectory() as d:
            a=FileEvidenceArchive(d); x=a.put(b"evidence",media_type="text/plain",source_uri="fixture://one")
            y=a.put(b"evidence",media_type="text/plain",source_uri="fixture://two")
            self.assertEqual(x,y); self.assertEqual(a.get(x),b"evidence")
    def test_hybrid_retrieval_and_context_budget(self):
        with tempfile.TemporaryDirectory() as d:
            repo=SqliteKnowledgeRepository(Path(d)/"ec.db")
            repo.append(rec("manufacturing critical material shortage","production delivery risk"))
            repo.append(rec("hotel occupancy","normal"))
            hits=HybridRetriever(repo).retrieve("critical material production risk",tenant_id="acme")
            self.assertIn("critical material",hits[0].record.subject)
            c=AdaptiveContextCompiler(HybridRetriever(repo),(lambda r:(r.register(external_regulation_strategy()),r.register(case_outcome_learning_strategy()),r)[-1])(LearningStrategyRegistry())).compile(
              ContextRequest("assess delivery","planner","acme","manufacturing","critical material production risk",token_budget=1000))
            self.assertTrue(c.items)
    def test_research_enters_as_candidate_claim(self):
        class P:
            def acquire(self,q): return [SourceDocument("a://1","A","Lead time increased","official",.9),
                                         SourceDocument("b://1","B","Lead time increased","industry",.8)]
        with tempfile.TemporaryDirectory() as d:
            repo=SqliteKnowledgeRepository(Path(d)/"ec.db"); pipe=ResearchPipeline([P()])
            fs=pipe.research("lead time"); self.assertGreater(fs[0].confidence,.7)
            rs=pipe.ingest_candidates(fs,repo,Scope(ScopeKind.INDUSTRY,"manufacturing"))
            self.assertEqual(rs[0].kind,KnowledgeKind.CLAIM); self.assertEqual(rs[0].status,KnowledgeStatus.CANDIDATE)
    def test_outcome_learning_never_auto_promotes_truth(self):
        with tempfile.TemporaryDirectory() as d:
            repo=SqliteKnowledgeRepository(Path(d)/"ec.db"); loop=OutcomeLearningLoop(repo)
            rs=loop.observe(DecisionObservation("material late","use supplier B","on time",.12,"acme","manufacturing"))
            self.assertEqual([x.kind for x in rs], [KnowledgeKind.CASE,KnowledgeKind.DECISION,KnowledgeKind.OUTCOME,KnowledgeKind.LESSON])
            self.assertTrue(all(x.status==KnowledgeStatus.CANDIDATE for x in rs))
    def test_replaceable_model_gateway(self):
        g=ModelGateway([DeterministicReferenceModel()])
        r=g.complete("reference/deterministic-v1",ModelRequest("diagnose","constitution","case"))
        self.assertEqual(r.model_id,"reference/deterministic-v1")
if __name__=="__main__": unittest.main()
