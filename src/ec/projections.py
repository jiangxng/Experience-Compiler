from __future__ import annotations
from dataclasses import dataclass
from ec.knowledge.model import KnowledgeRecord
@dataclass(frozen=True,slots=True)
class ProjectionFailure:
    projection:str; record_id:str; error:str
class ProjectionFanout:
    """Canonical writes succeed independently; projections are rebuildable and failures are reportable."""
    def __init__(self,search=None,vector=None,graph=None): self.search=search; self.vector=vector; self.graph=graph
    def project(self,r:KnowledgeRecord,embedding=None):
        failures=[]
        for name,fn in [
          ("search",lambda:self.search and self.search.upsert(r)),
          ("vector",lambda:self.vector and embedding is not None and self.vector.upsert_vector(r.record_id,embedding,{"kind":r.kind.value})),
          ("graph",lambda:self.graph and self.graph.upsert_record(r))]:
            try: fn()
            except Exception as e: failures.append(ProjectionFailure(name,r.record_id,str(e)))
        return tuple(failures)
