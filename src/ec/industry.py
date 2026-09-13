from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True, slots=True)
class IndustryPackManifest:
    pack_id: str
    version: str
    industry: str
    subindustry: str | None
    ontology_refs: tuple[str, ...]
    knowledge_refs: tuple[str, ...]
    process_refs: tuple[str, ...]
    decision_pattern_refs: tuple[str, ...]
    experience_pattern_refs: tuple[str, ...]
    demo_scenario_refs: tuple[str, ...]
    license_class: str
    provenance_policy: str
