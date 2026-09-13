from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class IntelligenceQuality:
    evidence_coverage:float; contradiction_count:int; average_confidence:float; decision_ready:bool; reasons:tuple[str,...]
def assess_context(items,contradictions,minimum_items=1,minimum_confidence=.65):
    avg=sum(x.confidence for x in items)/len(items) if items else 0
    reasons=[]
    if len(items)<minimum_items:reasons.append("insufficient governed evidence")
    if avg<minimum_confidence:reasons.append("evidence confidence below policy threshold")
    if contradictions:reasons.append("material contradictions require resolution")
    return IntelligenceQuality(min(1,len(items)/max(1,minimum_items)),len(contradictions),avg,not reasons,tuple(reasons))
