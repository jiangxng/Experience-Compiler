from __future__ import annotations
from ec.domain import Provenance, Scope, ScopeKind, TemporalValidity, new_id, now_utc
from ec.knowledge.model import KnowledgeKind, KnowledgeRecord, KnowledgeStatus
from ec.learning.defaults import external_regulation_strategy, case_outcome_learning_strategy
from ec.learning.registry import LearningStrategyRegistry
from ec.storage.memory import InMemoryKnowledgeRepository
from ec.context import ContextCompiler, ContextRequest
from ec.integration.eidos import ExperienceProposal, ExperienceRegionProposal


def build_demo() -> tuple[object, ExperienceProposal]:
    repo=InMemoryKnowledgeRepository()
    strategies=LearningStrategyRegistry()
    strategies.register(external_regulation_strategy()); strategies.register(case_outcome_learning_strategy())
    scope=Scope(ScopeKind.TENANT, "demo-manufacturing", tenant_id="demo-manufacturing")
    prov=Provenance("seed", "manufacturing-pack", "curated-seed", new_id())
    records=[
        KnowledgeRecord(KnowledgeKind.FACT, "SO-20260913-0182", "promised_delivery", "2026-09-18", scope, prov, 0.99, status=KnowledgeStatus.ACCEPTED, tags=("sales-order",)),
        KnowledgeRecord(KnowledgeKind.FACT, "MAT-CRIT-44", "supplier_eta", "2026-09-20", scope, prov, 0.95, status=KnowledgeStatus.ACCEPTED, tags=("shortage",)),
        KnowledgeRecord(KnowledgeKind.FACT, "SO-20260913-0182", "revenue_at_risk_usd", 280000, scope, prov, 0.95, status=KnowledgeStatus.ACCEPTED),
        KnowledgeRecord(KnowledgeKind.PATTERN, "material-shortage", "recommended_experience", "decision+evidence+impact", scope, prov, 0.86, status=KnowledgeStatus.ACCEPTED),
        KnowledgeRecord(KnowledgeKind.PRACTICE, "strategic-customer-shortage", "decision_options", ["wait", "expedite alternate supplier", "split shipment", "replan production"], scope, prov, 0.83, status=KnowledgeStatus.ACCEPTED),
    ]
    for r in records: repo.append(r)
    ctx=ContextCompiler(repo,strategies).compile(ContextRequest("resolve delivery risk","production-planner",scope.tenant_id,"manufacturing","SO-20260913-0182",risk_class="decision"))
    proposal=ExperienceProposal(
        contract_version="0.1.0", proposal_id=new_id(), produced_at=now_utc().isoformat(), experience_id="manufacturing.delivery-risk.SO-20260913-0182",
        title="Production Delivery Risk Decision Workspace", mode="role",
        regions=(
            ExperienceRegionProposal("exceptions","exception-queue","shared-stable","important",{"order":"SO-20260913-0182","risk":"material shortage"}),
            ExperienceRegionProposal("decision","decision-panel","invariant","requires-review",{"options":["wait","alternate supplier","split shipment","replan production"]}),
            ExperienceRegionProposal("evidence","evidence-stack","shared-stable","informative",{"contextRecordIds":[i.record_id for i in ctx.items]}),
            ExperienceRegionProposal("impact","impact-preview","adaptive","important",{"revenueAtRisk":280000,"currency":"USD"}),
            ExperienceRegionProposal("timeline","timeline","personal-stable","informative",{"focus":"promise vs material ETA"}),
        ),
        rationale=("critical material ETA exceeds customer promise", "material revenue is at risk", "decision should expose options, evidence and impact together"),
        standard_fallback_ref="fallback://manufacturing/delivery-risk/v1",
    )
    return ctx, proposal
