from __future__ import annotations
from dataclasses import dataclass, field
from typing import Mapping
from ec.domain import new_id, now_utc

@dataclass(frozen=True, slots=True)
class LearningStrategy:
    strategy_id: str
    version: str
    name: str
    applicable_domains: tuple[str, ...]
    applicable_knowledge_kinds: tuple[str, ...]
    source_priority: tuple[str, ...]
    minimum_independent_sources: int
    freshness_days: int | None
    contradiction_policy: str
    confidence_threshold: float
    stop_conditions: tuple[str, ...]
    review_policy: str
    steps: tuple[str, ...]
    model_selection_policy: str = "capability-first"

@dataclass(frozen=True, slots=True)
class StrategyEvaluation:
    strategy_id: str
    strategy_version: str
    sample_count: int
    metrics: Mapping[str, float]
    notes: str
    evaluation_id: str = field(default_factory=new_id)
    created_at: str = field(default_factory=lambda: now_utc().isoformat())
