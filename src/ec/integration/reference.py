from __future__ import annotations
class ReferenceEvoGateway:
    def __init__(self,events=(),commands=()): self.events=list(events); self.commands=list(commands); self.proposals=[]
    def semantic_events(self): return tuple(self.events)
    def command_catalog(self): return tuple(self.commands)
    def propose(self,proposal): self.proposals.append(proposal); return {"status":"accepted-for-validation","proposal":proposal}
class ReferenceEidosGateway:
    def __init__(self,capabilities): self.capabilities=tuple(capabilities)
    def capability_catalog(self): return self.capabilities
    def validate_proposal(self,proposal):
        known={c.capability_id for c in self.capabilities}
        return tuple(f"unknown capability: {r.capability}" for r in proposal.regions if r.capability not in known)
