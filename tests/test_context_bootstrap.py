import unittest
from ec.domain import Provenance, Scope, ScopeKind
from ec.knowledge.model import KnowledgeKind, KnowledgeRecord, KnowledgeStatus
from ec.storage.memory import InMemoryKnowledgeRepository
from ec.learning.registry import LearningStrategyRegistry
from ec.learning.defaults import external_regulation_strategy, case_outcome_learning_strategy
from ec.context import ContextCompiler, ContextRequest
from ec.models import ModelCapabilityProfile
from ec.bootstrap import build_bootstrap

class BootstrapTests(unittest.TestCase):
    def test_model_replacement_inherits_learning_methods(self):
        repo=InMemoryKnowledgeRepository(); reg=LearningStrategyRegistry(); reg.register(external_regulation_strategy()); reg.register(case_outcome_learning_strategy())
        scope=Scope(ScopeKind.INDUSTRY,"manufacturing"); prov=Provenance("test","seed","unit","r")
        repo.append(KnowledgeRecord(KnowledgeKind.PATTERN,"shortage","response","evaluate alternatives",scope,prov,0.8,status=KnowledgeStatus.ACCEPTED))
        ctx=ContextCompiler(repo,reg).compile(ContextRequest("shortage","planner",None,"manufacturing","shortage"))
        model=ModelCapabilityProfile("future-model-x","replaceable",1_000_000,("reasoning",),("text",),("private",),True,True,"medium","medium",("normal",))
        boot=build_bootstrap(model,ctx,reg)
        self.assertGreaterEqual(len(boot.learning_methods),2); self.assertEqual(boot.current_model.model_id,"future-model-x")

if __name__=='__main__': unittest.main()
