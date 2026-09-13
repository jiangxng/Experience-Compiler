import json, unittest
from dataclasses import dataclass
from ec.storage.postgres import PostgresKnowledgeRepository
from ec.domain import Scope,ScopeKind,Provenance
from ec.knowledge.model import KnowledgeRecord,KnowledgeKind,KnowledgeStatus
from ec.projections import ProjectionFanout
from ec.model_gateway import ModelGateway,ModelRequest
from ec.model_providers.openai_compatible import OpenAICompatibleProvider
from ec.integration.http import HttpEvoGateway,HttpEidosGateway

class Cursor:
    def __init__(self,row=None,rows=None): self.row=row;self.rows=rows or []
    def fetchone(self): return self.row
    def fetchall(self): return self.rows
class FakeDb:
    def __init__(self): self.calls=[];self.commits=0
    def execute(self,q,args=()): self.calls.append((q,args)); return Cursor()
    def commit(self): self.commits+=1
class FakeHttp:
    def __init__(self): self.calls=[]
    def request(self,m,p,payload=None):
        self.calls.append((m,p,payload))
        if "semantic" in p:return {"entity_type":"SalesOrder","entity_id":"SO1","version":"1","attributes":{"status":"approved"}}
        if "commands" in p and m=="GET":return [{"command":"release","version":"1","input_schema_ref":"x","risk_class":"high","requires_human_authorization":True}]
        if "proposals" in p:return {"proposal_id":"P1"}
        if "capabilities" in p:return [{"capability_id":"decision-panel","version":"0.1","maturity":"stable","semantic_purpose":["decision"],"constraints":{}}]
        return {"diagnostics":[]}

class V08Test(unittest.TestCase):
    def test_postgres_adapter_emits_canonical_insert(self):
        db=FakeDb(); repo=PostgresKnowledgeRepository(db)
        r=KnowledgeRecord(kind=KnowledgeKind.FACT,subject="material",predicate="status",value="short",
          scope=Scope(ScopeKind.TENANT,"t","t"),provenance=Provenance("test","x","fixture","r"),
          status=KnowledgeStatus.ACCEPTED)
        repo.append(r); self.assertIn("ec_knowledge_record",db.calls[0][0]);self.assertEqual(db.commits,1)
    def test_projection_failure_does_not_change_canonical_semantics(self):
        class Bad:
            def upsert(self,r): raise RuntimeError("index unavailable")
        r=KnowledgeRecord(kind=KnowledgeKind.FACT,subject="x",predicate="y",value="z",
          scope=Scope(ScopeKind.PUBLIC,"public"),provenance=Provenance("test","x","fixture","r"))
        fs=ProjectionFanout(search=Bad()).project(r); self.assertEqual(fs[0].projection,"search")
    def test_http_gateways_are_boundary_configurable(self):
        c=FakeHttp(); evo=HttpEvoGateway(c); self.assertEqual(evo.semantic_snapshot("t","SalesOrder","SO1").entity_id,"SO1")
        self.assertTrue(evo.command_catalog("t")[0].requires_human_authorization)
        eidos=HttpEidosGateway(c); self.assertEqual(eidos.capability_catalog()[0].capability_id,"decision-panel")
    def test_manufacturing_pack_has_decision_density(self):
        from pathlib import Path
        p=Path(__file__).parents[1]/"industry-packs/manufacturing/decisions/catalog-v0.8.json"
        d=json.loads(p.read_text()); self.assertGreaterEqual(len(d["families"]),5)
        self.assertIn("quality-containment",{x["id"] for x in d["families"]})
if __name__=="__main__":unittest.main()
