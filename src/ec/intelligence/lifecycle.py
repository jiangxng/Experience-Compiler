from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Mapping
from ec.context import ContextRequest
from ec.model_gateway import ModelRequest
from ec.learning.loop import DecisionObservation
@dataclass(frozen=True,slots=True)
class IntelligenceTask:
    tenant_id:str; domain:str; role:str; task:str; query:str; risk_class:str="normal"
@dataclass(frozen=True,slots=True)
class DecisionDraft:
    recommendation:str; assumptions:tuple[str,...]; evidence_record_ids:tuple[str,...]; model_id:str
@dataclass(frozen=True,slots=True)
class LifecycleResult:
    context_pack:Any; decision:DecisionDraft; experience_proposal:Any
class IntelligenceLifecycle:
    """Reference orchestration. Every side effect remains behind an owning boundary."""
    def __init__(self,context_compiler,model_gateway,model_id,experience_planner,learning_loop):
        self.context_compiler=context_compiler;self.models=model_gateway;self.model_id=model_id
        self.experience_planner=experience_planner;self.learning_loop=learning_loop
    def analyze(self,t:IntelligenceTask):
        cp=self.context_compiler.compile(ContextRequest(t.task,t.role,t.tenant_id,t.domain,t.query,t.risk_class))
        evidence=tuple(x.record_id for x in cp.items)
        mr=self.models.complete(self.model_id,ModelRequest(t.task,"\n".join(cp.invariants),repr([(x.subject,x.predicate,x.value) for x in cp.items])))
        decision=DecisionDraft(mr.text,("model output requires owning-boundary validation",),evidence,mr.model_id)
        xp=self.experience_planner(t,decision,cp)
        return LifecycleResult(cp,decision,xp)
    def observe_outcome(self,*,task:IntelligenceTask,decision:DecisionDraft,outcome:str,metric_delta:float):
        return self.learning_loop.observe(DecisionObservation(task.query,decision.recommendation,outcome,metric_delta,task.tenant_id,task.domain))
