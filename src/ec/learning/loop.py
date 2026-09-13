from __future__ import annotations
from dataclasses import dataclass
from ec.domain import Scope,Provenance,new_id
from ec.knowledge.model import KnowledgeRecord,KnowledgeKind,KnowledgeStatus
@dataclass(frozen=True,slots=True)
class DecisionObservation:
    situation:str; decision:str; outcome:str; metric_delta:float; tenant_id:str; domain:str
class OutcomeLearningLoop:
    """Conservative learning loop: observations create candidates; they do not auto-promote to universal truth."""
    def __init__(self,repo): self.repo=repo
    def observe(self,o:DecisionObservation):
        run=new_id(); scope=Scope(kind=__import__("ec.domain",fromlist=["ScopeKind"]).ScopeKind.TENANT,key=o.tenant_id,tenant_id=o.tenant_id)
        prov=Provenance("system","outcome-learning-loop","decision-outcome-observation",run)
        made=[]
        for kind,pred,val,conf in [
          (KnowledgeKind.CASE,"situation",o.situation,.95),(KnowledgeKind.DECISION,"decision",o.decision,.95),
          (KnowledgeKind.OUTCOME,"outcome",{"text":o.outcome,"metric_delta":o.metric_delta},.95),
          (KnowledgeKind.LESSON,"candidate_lesson",f"{o.decision} -> {o.outcome}",.60)]:
            r=KnowledgeRecord(kind=kind,subject=o.domain,predicate=pred,value=val,scope=scope,confidence=conf,
              status=KnowledgeStatus.CANDIDATE,provenance=prov)
            self.repo.append(r); made.append(r)
        return tuple(made)
