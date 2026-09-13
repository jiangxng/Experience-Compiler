from __future__ import annotations
from dataclasses import dataclass
from ec.context import ContextPack,ContextItem,ContextRequest
from ec.domain import new_id
from ec.retrieval import HybridRetriever
from ec.learning.registry import LearningStrategyRegistry

class AdaptiveContextCompiler:
    def __init__(self,retriever:HybridRetriever,strategies:LearningStrategyRegistry): self.r=retriever; self.s=strategies
    def compile(self,req:ContextRequest)->ContextPack:
        hits=self.r.retrieve(req.query,tenant_id=req.tenant_id,limit=req.max_items)
        budget=req.token_budget or {"normal":50000,"high":500000,"critical":5000000}.get(req.risk_class,50000)
        used=0; items=[]; omissions=[]
        for h in hits:
            r=h.record; estimate=max(20,len(f"{r.subject}{r.predicate}{r.value}")//3)
            if used+estimate>budget: omissions.append("token budget reached before all candidates were included"); break
            items.append(ContextItem(r.record_id,r.kind.value,r.subject,r.predicate,repr(r.value),r.confidence)); used+=estimate
        refs=[]
        for sid in ("external-regulation-research","case-outcome-learning"):
            vs=self.s.versions(sid)
            if vs: refs.append(f"{sid}@{vs[-1].version}")
        if not items: omissions.append("no relevant governed knowledge retrieved")
        return ContextPack(new_id(),req.task,req.role,req.domain,tuple(items),tuple(refs),
          ("EC knowledge is not EVO business truth","preserve tenant boundaries","material claims require provenance",
           "model output is a proposal until validated by the owning boundary"),tuple(omissions))
