from __future__ import annotations
from dataclasses import dataclass
from ec.context import ContextPack
from ec.learning.registry import LearningStrategyRegistry
from ec.models import ModelCapabilityProfile

@dataclass(frozen=True, slots=True)
class LlmBootstrapPack:
    ec_constitution_version: str
    system_identity: str
    current_model: ModelCapabilityProfile
    context: ContextPack
    learning_methods: tuple[str, ...]
    known_failure_modes: tuple[str, ...]
    authority_rules: tuple[str, ...]


def build_bootstrap(model: ModelCapabilityProfile, context: ContextPack, registry: LearningStrategyRegistry) -> LlmBootstrapPack:
    methods=[]
    for sid in ("external-regulation-research", "case-outcome-learning"):
        versions=registry.versions(sid)
        if versions:
            s=versions[-1]
            methods.append(f"{s.strategy_id}@{s.version}: " + " -> ".join(s.steps))
    return LlmBootstrapPack(
        ec_constitution_version="0.1",
        system_identity="EC persistent enterprise intelligence reasoning worker",
        current_model=model,
        context=context,
        learning_methods=tuple(methods),
        known_failure_modes=("confusing external claims with enterprise truth", "cross-tenant leakage", "using stale policy without temporal check", "over-generalizing from small samples"),
        authority_rules=("EVO executes business commands", "Eidos validates and realizes experience", "human/policy authorization gates high-risk actions"),
    )
