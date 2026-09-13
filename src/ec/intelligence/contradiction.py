from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Contradiction:
    subject:str; predicate:str; record_ids:tuple[str,...]; values:tuple[str,...]
def detect_contradictions(records):
    groups={}
    for r in records: groups.setdefault((r.subject,r.predicate),[]).append(r)
    out=[]
    for (s,p),rs in groups.items():
        vals={repr(r.value) for r in rs}
        if len(vals)>1: out.append(Contradiction(s,p,tuple(r.record_id for r in rs),tuple(sorted(vals))))
    return tuple(out)
