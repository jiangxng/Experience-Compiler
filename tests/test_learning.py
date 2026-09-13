import unittest
from ec.learning.registry import LearningStrategyRegistry
from ec.learning.defaults import external_regulation_strategy
from ec.learning.model import LearningStrategy, StrategyEvaluation

class LearningTests(unittest.TestCase):
    def test_strategy_is_versioned_and_evaluated(self):
        reg=LearningStrategyRegistry(); s=external_regulation_strategy(); reg.register(s)
        s2=LearningStrategy(**{**s.__dict__,"version":"1.1.0","minimum_independent_sources":3}) if hasattr(s,"__dict__") else LearningStrategy(s.strategy_id,"1.1.0",s.name,s.applicable_domains,s.applicable_knowledge_kinds,s.source_priority,3,s.freshness_days,s.contradiction_policy,s.confidence_threshold,s.stop_conditions,s.review_policy,s.steps,s.model_selection_policy)
        reg.register(s2); reg.record_evaluation(StrategyEvaluation(s.strategy_id,"1.1.0",100,{"precision":0.94},"improved corroboration"))
        self.assertEqual([x.version for x in reg.versions(s.strategy_id)],["1.0.0","1.1.0"])
        self.assertEqual(reg.evaluations(s.strategy_id)[0].metrics["precision"],0.94)

if __name__=='__main__': unittest.main()
