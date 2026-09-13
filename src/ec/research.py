from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Sequence
from ec.domain import EvidenceRef, Provenance, Scope, ScopeKind, TemporalValidity, new_id
from ec.knowledge.model import KnowledgeKind, KnowledgeRecord, KnowledgeStatus

@dataclass(frozen=True, slots=True)
class ResearchQuery:
    question: str
    domain: str
    preferred_source_classes: tuple[str, ...]
    jurisdiction: str | None = None
    max_sources: int = 20

@dataclass(frozen=True, slots=True)
class AcquiredDocument:
    uri: str
    title: str
    text: str
    publisher: str | None
    source_class: str
    sha256: str

class ResearchAdapter(Protocol):
    def acquire(self, query: ResearchQuery) -> Sequence[AcquiredDocument]: ...

class ResearchPolicy:
    def allow_uri(self, uri: str) -> bool:
        return uri.startswith("https://")
    def may_promote_without_review(self, source_class: str) -> bool:
        return source_class in {"regulator-primary", "official-gazette"}

class ResearchIngestor:
    """External content becomes claims/candidates. It never becomes business truth by ingestion alone."""
    def __init__(self, policy: ResearchPolicy) -> None:
        self.policy = policy
    def to_claim(self, doc: AcquiredDocument, *, subject: str, predicate: str, value: str, scope: Scope) -> KnowledgeRecord:
        if not self.policy.allow_uri(doc.uri):
            raise PermissionError("source URI rejected by research policy")
        ev = EvidenceRef(new_id(), doc.uri, sha256=doc.sha256, title=doc.title, source_class=doc.source_class, publisher=doc.publisher)
        return KnowledgeRecord(
            kind=KnowledgeKind.CLAIM, subject=subject, predicate=predicate, value=value,
            scope=scope, provenance=Provenance("research-adapter", "external", "source-acquisition", new_id(), evidence=(ev,)),
            confidence=0.5, temporal=TemporalValidity(), status=KnowledgeStatus.CANDIDATE,
        )
