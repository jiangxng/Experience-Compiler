from __future__ import annotations
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Mapping
from ec.domain import Provenance, Scope, TemporalValidity, new_id, now_utc

class KnowledgeKind(StrEnum):
    RAW = "raw"
    CLAIM = "claim"
    FACT = "fact"
    RULE = "rule"
    POLICY = "policy"
    ONTOLOGY = "ontology"
    CASE = "case"
    DECISION = "decision"
    OUTCOME = "outcome"
    LESSON = "lesson"
    PATTERN = "pattern"
    PRACTICE = "practice"
    HYPOTHESIS = "hypothesis"
    PREFERENCE = "preference"
    RECOMMENDATION = "recommendation"

class KnowledgeStatus(StrEnum):
    CANDIDATE = "candidate"
    ACCEPTED = "accepted"
    DISPUTED = "disputed"
    SUPERSEDED = "superseded"
    QUARANTINED = "quarantined"
    ARCHIVED = "archived"

@dataclass(frozen=True, slots=True)
class KnowledgeRecord:
    kind: KnowledgeKind
    subject: str
    predicate: str
    value: Any
    scope: Scope
    provenance: Provenance
    confidence: float = 0.5
    temporal: TemporalValidity = field(default_factory=TemporalValidity)
    status: KnowledgeStatus = KnowledgeStatus.CANDIDATE
    tags: tuple[str, ...] = ()
    supersedes: tuple[str, ...] = ()
    record_id: str = field(default_factory=new_id)
    schema_version: str = "0.1.0"

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0,1]")
        if not self.subject or not self.predicate:
            raise ValueError("subject and predicate are required")

@dataclass(frozen=True, slots=True)
class CaseRecord:
    title: str
    situation: Mapping[str, Any]
    scope: Scope
    provenance: Provenance
    case_id: str = field(default_factory=new_id)
    occurred_at: str | None = None
    tags: tuple[str, ...] = ()

@dataclass(frozen=True, slots=True)
class DecisionRecord:
    case_id: str
    decision_type: str
    options_considered: tuple[str, ...]
    chosen_option: str
    rationale: str
    scope: Scope
    provenance: Provenance
    decision_id: str = field(default_factory=new_id)

@dataclass(frozen=True, slots=True)
class OutcomeRecord:
    decision_id: str
    measures: Mapping[str, float | int | str | bool]
    evaluation: str
    scope: Scope
    provenance: Provenance
    outcome_id: str = field(default_factory=new_id)

@dataclass(frozen=True, slots=True)
class LessonRecord:
    source_case_ids: tuple[str, ...]
    statement: str
    confidence: float
    scope: Scope
    provenance: Provenance
    lesson_id: str = field(default_factory=new_id)
