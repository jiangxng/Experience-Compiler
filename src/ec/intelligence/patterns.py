from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class PatternCandidate:
    decision:str; outcomes:tuple[str,...]; observations:int; mean_metric_delta:float; confidence:float
class PatternMiner:
    """Conservative cohort miner: produces candidates, never global practices."""
    def mine(self,observations,min_observations=3):
        g=defaultdict(list)
        for o in observations:g[o.decision].append(o)
        out=[]
        for decision,rows in g.items():
            if len(rows)<min_observations:continue
            mean=sum(x.metric_delta for x in rows)/len(rows)
            conf=min(.9,.45+.08*len(rows))
            out.append(PatternCandidate(decision,tuple(x.outcome for x in rows),len(rows),mean,conf))
        return tuple(sorted(out,key=lambda x:(-x.confidence,x.decision)))
