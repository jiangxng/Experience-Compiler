from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable
from ec.domain import new_id
from ec.knowledge.model import KnowledgeRecord
from ec.ports import KnowledgeRepository
from ec.learning.registry import LearningStrategyRegistry

@dataclass(frozen=True, slots=True)
class ContextRequest:
    task: str
    role: str
    tenant_id: str | None
    domain: str
    query: str
    risk_class: str = "normal"
    max_items: int = 50
    token_budget: int | None = None

@dataclass(frozen=True, slots=True)
class ContextItem:
    record_id: str
    kind: str
    subject: str
    predicate: str
    value: str
    confidence: float

@dataclass(frozen=True, slots=True)
class ContextPack:
    request_id: str
    task: str
    role: str
    domain: str
    items: tuple[ContextItem, ...]
    learning_strategy_refs: tuple[str, ...]
    invariants: tuple[str, ...]
    omissions: tuple[str, ...] = ()

class ContextCompiler:
    def __init__(self, repo: KnowledgeRepository, strategies: LearningStrategyRegistry) -> None:
        self.repo = repo
        self.strategies = strategies

    def compile(self, req: ContextRequest) -> ContextPack:
        records = self.repo.query(text=req.query, tenant_id=req.tenant_id, limit=req.max_items)
        items = tuple(ContextItem(r.record_id, r.kind.value, r.subject, r.predicate, repr(r.value), r.confidence) for r in records)
        refs = []
        for sid in ("external-regulation-research", "case-outcome-learning"):
            versions = self.strategies.versions(sid)
            if versions:
                refs.append(f"{sid}@{versions[-1].version}")
        return ContextPack(
            request_id=new_id(), task=req.task, role=req.role, domain=req.domain,
            items=items, learning_strategy_refs=tuple(refs),
            invariants=(
                "EC knowledge is not EVO business truth",
                "do not execute business actions without EVO command contract",
                "cite provenance for material claims",
                "preserve tenant boundaries",
            ),
            omissions=(() if records else ("no relevant governed knowledge retrieved",)),
        )
