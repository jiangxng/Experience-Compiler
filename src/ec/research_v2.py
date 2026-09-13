from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol,Sequence
from ec.domain import Scope,Provenance,new_id
from ec.knowledge.model import KnowledgeRecord,KnowledgeKind,KnowledgeStatus
@dataclass(frozen=True,slots=True)
class SourceDocument:
    uri:str; publisher:str; text:str; source_class:str; authority:float
class AcquisitionProvider(Protocol):
    def acquire(self,query:str)->Sequence[SourceDocument]: ...
@dataclass(frozen=True,slots=True)
class ResearchFinding:
    claim:str; sources:tuple[str,...]; confidence:float; contradicted:bool
class ResearchPipeline:
    """Acquisition -> claim extraction -> corroboration -> candidate knowledge. Network access belongs in adapters."""
    def __init__(self,providers): self.providers=providers
    def research(self,query):
        docs=[d for p in self.providers for d in p.acquire(query)]
        # Reference extractor intentionally simple; production extractor is model/provider replaceable.
        claims={}
        for d in docs:
            for line in (x.strip() for x in d.text.splitlines() if x.strip()):
                claims.setdefault(line,[]).append(d)
        out=[]
        for claim,ds in claims.items():
            independent=len({d.publisher for d in ds}); authority=sum(d.authority for d in ds)/len(ds)
            conf=min(.99,.45+.15*independent+.25*authority)
            out.append(ResearchFinding(claim,tuple(d.uri for d in ds),conf,False))
        return tuple(sorted(out,key=lambda x:-x.confidence))
    def ingest_candidates(self,findings,repo,scope):
        out=[]
        for f in findings:
            r=KnowledgeRecord(kind=KnowledgeKind.CLAIM,subject="external-research",predicate="claims",value=f.claim,
              scope=scope,confidence=f.confidence,status=KnowledgeStatus.CANDIDATE,
              provenance=Provenance("system","research-pipeline","corroborated-external-research",new_id()))
            repo.append(r); out.append(r)
        return tuple(out)
