from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Mapping
from uuid import uuid4

Json = None | bool | int | float | str | list["Json"] | dict[str, "Json"]


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def new_id() -> str:
    return str(uuid4())

class ScopeKind(StrEnum):
    PUBLIC = "public"
    LICENSED = "licensed"
    GLOBAL_LEARNED = "global-learned"
    INDUSTRY = "industry"
    TENANT = "tenant"
    ORGANIZATION = "organization"
    ROLE = "role"
    USER = "user"
    TASK = "task"
    SESSION = "session"

@dataclass(frozen=True, slots=True)
class Scope:
    kind: ScopeKind
    key: str
    tenant_id: str | None = None

@dataclass(frozen=True, slots=True)
class TemporalValidity:
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    observed_at: datetime = field(default_factory=now_utc)

    def is_valid_at(self, at: datetime) -> bool:
        if self.valid_from and at < self.valid_from:
            return False
        if self.valid_to and at >= self.valid_to:
            return False
        return True

@dataclass(frozen=True, slots=True)
class EvidenceRef:
    evidence_id: str
    uri: str
    sha256: str | None = None
    title: str | None = None
    source_class: str | None = None
    publisher: str | None = None
    retrieved_at: datetime = field(default_factory=now_utc)

@dataclass(frozen=True, slots=True)
class Provenance:
    actor_type: str
    actor_id: str
    method: str
    run_id: str
    evidence: tuple[EvidenceRef, ...] = ()
    parent_record_ids: tuple[str, ...] = ()
    model_id: str | None = None
    strategy_id: str | None = None
    strategy_version: str | None = None
