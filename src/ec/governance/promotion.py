from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class PromotionDecision:
    allowed:bool; target_status:str; reasons:tuple[str,...]
class KnowledgePromotionPolicy:
    """Explicit gate from candidate intelligence to accepted governed knowledge."""
    def decide(self,*,kind,confidence,independent_sources,contradicted,tenant_scope,human_reviewed=False):
        reasons=[]
        threshold=.9 if kind in ("policy","rule","fact") else .75
        if confidence<threshold:reasons.append("confidence below threshold")
        if contradicted:reasons.append("unresolved contradiction")
        if kind in ("policy","rule") and independent_sources<2:reasons.append("insufficient independent sources")
        if kind=="policy" and not human_reviewed:reasons.append("policy requires human review")
        if not tenant_scope:reasons.append("scope must be explicit")
        return PromotionDecision(not reasons,"accepted" if not reasons else "candidate",tuple(reasons))
