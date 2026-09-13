from __future__ import annotations
import json
from dataclasses import asdict
from urllib.request import Request,urlopen
from dataclasses import asdict
from ec.integration.evo import EvoSemanticEntity,EvoCommandDescriptor
from ec.integration.eidos import EidosCapability
class JsonHttpClient:
    def __init__(self,base_url,token=None,timeout=20): self.base=base_url.rstrip("/"); self.token=token; self.timeout=timeout
    def request(self,method,path,payload=None):
        h={"Accept":"application/json"}
        if self.token:h["Authorization"]="Bearer "+self.token
        data=None
        if payload is not None:h["Content-Type"]="application/json"; data=json.dumps(payload).encode()
        with urlopen(Request(self.base+path,data=data,method=method,headers=h),timeout=self.timeout) as r:return json.loads(r.read())
class HttpEvoGateway:
    """Preview adapter. Endpoint paths are configurable because EVO's authoritative production API must own them."""
    def __init__(self,client,paths=None): self.c=client; self.p=paths or {"snapshot":"/ec/v1/semantic/{tenant}/{type}/{id}","commands":"/ec/v1/commands/{tenant}","propose":"/ec/v1/commands/{tenant}/proposals"}
    def semantic_snapshot(self,tenant_id,entity_type,entity_id):
        d=self.c.request("GET",self.p["snapshot"].format(tenant=tenant_id,type=entity_type,id=entity_id)); return EvoSemanticEntity(d["entity_type"],d["entity_id"],d["version"],d["attributes"])
    def command_catalog(self,tenant_id):
        return tuple(EvoCommandDescriptor(**x) for x in self.c.request("GET",self.p["commands"].format(tenant=tenant_id)))
    def propose_command(self,tenant_id,proposal):
        d=self.c.request("POST",self.p["propose"].format(tenant=tenant_id),asdict(proposal)); return d["proposal_id"]
class HttpEidosGateway:
    def __init__(self,client,paths=None): self.c=client; self.p=paths or {"catalog":"/ec/v1/capabilities","validate":"/ec/v1/proposals/validate"}
    def capability_catalog(self):
        return tuple(EidosCapability(x["capability_id"],x["version"],x["maturity"],tuple(x.get("semantic_purpose",())),x.get("constraints",{})) for x in self.c.request("GET",self.p["catalog"]))
    def validate_proposal(self,proposal):
        d=self.c.request("POST",self.p["validate"],asdict(proposal)); return tuple(d.get("diagnostics",()))
