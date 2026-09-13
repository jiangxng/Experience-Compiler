from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

@dataclass(frozen=True, slots=True)
class EvoSemanticEntity:
    entity_type: str
    entity_id: str
    version: str
    attributes: Mapping[str, Any]

@dataclass(frozen=True, slots=True)
class EvoEventEnvelope:
    event_id: str
    event_type: str
    event_version: str
    occurred_at: str
    tenant_id: str
    actor: str
    subject: EvoSemanticEntity
    payload: Mapping[str, Any]
    trace_id: str | None = None

@dataclass(frozen=True, slots=True)
class EvoCommandDescriptor:
    command: str
    version: str
    input_schema_ref: str
    risk_class: str
    requires_human_authorization: bool

@dataclass(frozen=True, slots=True)
class EvoCommandProposal:
    command: str
    version: str
    input: Mapping[str, Any]
    rationale: str
    evidence_record_ids: tuple[str, ...]

class EvoGateway(Protocol):
    def semantic_snapshot(self, tenant_id: str, entity_type: str, entity_id: str) -> EvoSemanticEntity: ...
    def command_catalog(self, tenant_id: str) -> Sequence[EvoCommandDescriptor]: ...
    def propose_command(self, tenant_id: str, proposal: EvoCommandProposal) -> str: ...

# Boundary invariant: EC may prepare/propose commands but EVO remains the execution authority.
