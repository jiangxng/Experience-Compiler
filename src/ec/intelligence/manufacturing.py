from __future__ import annotations
from ec.domain import new_id,now_utc
from ec.integration.eidos import ExperienceProposal,ExperienceRegionProposal
def manufacturing_experience_planner(task,decision,context):
    attention="requires-review" if task.risk_class in ("high","critical") else "important"
    return ExperienceProposal("0.1.0",new_id(),now_utc().isoformat(),
      "manufacturing-decision-workspace",f"Manufacturing Decision — {task.task}","role",
      (ExperienceRegionProposal("decision","decision-panel","shared-stable",attention,{"recommendation":decision.recommendation}),
       ExperienceRegionProposal("evidence","evidence-stack","invariant","informative",{"recordIds":list(decision.evidence_record_ids)}),
       ExperienceRegionProposal("impact","impact-preview","shared-stable","important",{"domain":task.domain})),
      ("EC compiled governed context","decision remains a proposal until validated"),"manufacturing-standard-fallback")
