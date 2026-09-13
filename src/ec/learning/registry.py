from __future__ import annotations
from collections import defaultdict
from ec.learning.model import LearningStrategy, StrategyEvaluation

class LearningStrategyRegistry:
    def __init__(self) -> None:
        self._strategies: dict[tuple[str, str], LearningStrategy] = {}
        self._evaluations: list[StrategyEvaluation] = []

    def register(self, strategy: LearningStrategy) -> None:
        key = (strategy.strategy_id, strategy.version)
        if key in self._strategies:
            raise ValueError(f"strategy version already registered: {key}")
        self._strategies[key] = strategy

    def get(self, strategy_id: str, version: str) -> LearningStrategy:
        return self._strategies[(strategy_id, version)]

    def versions(self, strategy_id: str) -> list[LearningStrategy]:
        return sorted([s for (sid, _), s in self._strategies.items() if sid == strategy_id], key=lambda s: s.version)

    def record_evaluation(self, evaluation: StrategyEvaluation) -> None:
        if (evaluation.strategy_id, evaluation.strategy_version) not in self._strategies:
            raise KeyError("cannot evaluate unknown strategy version")
        self._evaluations.append(evaluation)

    def evaluations(self, strategy_id: str) -> list[StrategyEvaluation]:
        return [e for e in self._evaluations if e.strategy_id == strategy_id]
