from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

@dataclass(frozen=True, slots=True)
class EidosCapability:
    capability_id: str
    version: str
    maturity: str
    semantic_purpose: tuple[str, ...]
    constraints: Mapping[str, Any]

@dataclass(frozen=True, slots=True)
class ExperienceRegionProposal:
    region_id: str
    capability: str
    stability: str
    attention: str
    props: Mapping[str, Any]

@dataclass(frozen=True, slots=True)
class ExperienceProposal:
    contract_version: str
    proposal_id: str
    produced_at: str
    experience_id: str
    title: str
    mode: str
    regions: tuple[ExperienceRegionProposal, ...]
    rationale: tuple[str, ...]
    standard_fallback_ref: str

class EidosGateway(Protocol):
    def capability_catalog(self) -> Sequence[EidosCapability]: ...
    def validate_proposal(self, proposal: ExperienceProposal) -> Sequence[str]: ...

# EC never emits renderer-private executable code as the semantic contract.
