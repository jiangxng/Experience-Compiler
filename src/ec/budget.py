from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ReasoningBudget:
    mode: str
    max_tokens: int
    max_parallel_tasks: int
    require_critic: bool
    require_cross_model_review: bool
    stop_when_confidence_at_least: float

BUDGETS = {
    "fast": ReasoningBudget("fast", 20_000, 2, False, False, 0.80),
    "deep": ReasoningBudget("deep", 500_000, 16, True, False, 0.90),
    "research": ReasoningBudget("research", 10_000_000, 100, True, True, 0.95),
    "audit": ReasoningBudget("audit", 50_000_000, 200, True, True, 0.99),
}

def choose_budget(risk_class: str, estimated_value: float = 0.0) -> ReasoningBudget:
    if risk_class in {"audit", "regulated", "critical"}:
        return BUDGETS["audit"]
    if risk_class in {"high", "strategic"} or estimated_value >= 1_000_000:
        return BUDGETS["research"]
    if risk_class in {"medium", "decision"} or estimated_value >= 10_000:
        return BUDGETS["deep"]
    return BUDGETS["fast"]
