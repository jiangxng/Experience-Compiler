from __future__ import annotations
from dataclasses import dataclass
import math,re,hashlib
from ec.ports import KnowledgeRepository
from ec.knowledge.model import KnowledgeRecord

def _tokens(s): return set(re.findall(r"[\w\u4e00-\u9fff]+",s.casefold()))
def _embed(s,d=64):
    v=[0.0]*d
    for t in _tokens(s):
        h=int(hashlib.sha256(t.encode()).hexdigest()[:16],16); v[h%d]+=1.0
    n=math.sqrt(sum(x*x for x in v)) or 1
    return [x/n for x in v]
def _cos(a,b): return sum(x*y for x,y in zip(a,b))

@dataclass(frozen=True,slots=True)
class RetrievalHit:
    record: KnowledgeRecord
    lexical: float
    semantic: float
    authority: float
    freshness: float
    score: float

class HybridRetriever:
    """Deterministic reference hybrid retriever; production projections can replace each scorer."""
    def __init__(self,repo:KnowledgeRepository): self.repo=repo
    def retrieve(self,query,*,tenant_id=None,limit=20,candidate_limit=500):
        candidates=self.repo.query(tenant_id=tenant_id,limit=candidate_limit)
        qtok=_tokens(query); qv=_embed(query); hits=[]
        for r in candidates:
            text=f"{r.subject} {r.predicate} {r.value}"; rt=_tokens(text)
            lex=len(qtok & rt)/max(1,len(qtok|rt)); sem=_cos(qv,_embed(text))
            authority=max(0,min(1,r.confidence))
            freshness=1.0
            score=.35*lex+.35*sem+.2*authority+.1*freshness
            hits.append(RetrievalHit(r,lex,sem,authority,freshness,score))
        return sorted(hits,key=lambda h:(-h.score,h.record.record_id))[:limit]
