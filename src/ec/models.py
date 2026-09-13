from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Sequence

@dataclass(frozen=True, slots=True)
class ModelCapabilityProfile:
    model_id: str
    provider: str
    context_window: int | None
    strengths: tuple[str, ...]
    modalities: tuple[str, ...]
    data_residency: tuple[str, ...]
    supports_tools: bool
    supports_structured_output: bool
    cost_class: str
    latency_class: str
    approved_risk_classes: tuple[str, ...]

@dataclass(frozen=True, slots=True)
class ModelTask:
    task_type: str
    required_strengths: tuple[str, ...] = ()
    required_residency: str | None = None
    risk_class: str = "normal"
    prefer_cost_class: str | None = None

class ModelRegistry:
    def __init__(self) -> None:
        self._profiles: dict[str, ModelCapabilityProfile] = {}
    def register(self, profile: ModelCapabilityProfile) -> None:
        self._profiles[profile.model_id] = profile
    def select(self, task: ModelTask) -> ModelCapabilityProfile:
        candidates = []
        for p in self._profiles.values():
            if task.required_residency and task.required_residency not in p.data_residency:
                continue
            if task.risk_class not in p.approved_risk_classes:
                continue
            if any(s not in p.strengths for s in task.required_strengths):
                continue
            candidates.append(p)
        if not candidates:
            raise LookupError("no approved model satisfies task")
        candidates.sort(key=lambda p: (p.cost_class != (task.prefer_cost_class or p.cost_class), p.model_id))
        return candidates[0]
