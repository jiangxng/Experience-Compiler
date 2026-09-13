from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping,Any
@dataclass(frozen=True,slots=True)
class ManufacturingSituation:
    scenario_type:str; signals:Mapping[str,Any]; evidence:Mapping[str,Any]; constraints:Mapping[str,Any]
@dataclass(frozen=True,slots=True)
class OptionAssessment:
    option:str; feasible:bool; impact:Mapping[str,float]; risks:tuple[str,...]; missing_evidence:tuple[str,...]
class ManufacturingDecisionEngine:
    """Deterministic option pre-assessment; LLM reasoning may enrich but never silently replace constraints."""
    def assess(self,s:ManufacturingSituation,options):
        out=[]
        for o in options:
            missing=tuple(k for k in ("promise_date","customer_priority") if k not in s.evidence)
            risks=[]
            if o=="alternate-supplier" and not s.evidence.get("alternate_supplier_qualified",False):risks.append("supplier qualification unknown")
            if o=="substitute-material" and not s.evidence.get("substitute_approved",False):risks.append("engineering/quality approval required")
            if o=="overtime" and s.constraints.get("overtime_allowed") is False:risks.append("overtime prohibited")
            feasible=not any("prohibited" in r for r in risks)
            impact={"delivery":.7 if o in ("expedite","alternate-supplier","overtime") else .3,
                    "cost":-.4 if o in ("expedite","alternate-supplier","overtime","subcontract") else -.1,
                    "quality":-.3 if o in ("alternate-supplier","substitute-material") else 0.0}
            out.append(OptionAssessment(o,feasible,impact,tuple(risks),missing))
        return tuple(out)
