import unittest
from datetime import datetime, timezone
from ec.domain import Provenance, Scope, ScopeKind, TemporalValidity
from ec.knowledge.model import KnowledgeKind, KnowledgeRecord, KnowledgeStatus
from ec.storage.memory import InMemoryKnowledgeRepository

class KnowledgeTests(unittest.TestCase):
    def test_temporal_query_and_tenant_scope(self):
        repo=InMemoryKnowledgeRepository(); prov=Provenance("test","t","unit","r")
        a=Scope(ScopeKind.TENANT,"a",tenant_id="a"); b=Scope(ScopeKind.TENANT,"b",tenant_id="b")
        repo.append(KnowledgeRecord(KnowledgeKind.FACT,"supplier-x","status","preferred",a,prov,0.9,TemporalValidity(valid_from=datetime(2025,1,1,tzinfo=timezone.utc),valid_to=datetime(2026,1,1,tzinfo=timezone.utc)),KnowledgeStatus.ACCEPTED))
        repo.append(KnowledgeRecord(KnowledgeKind.FACT,"supplier-x","status","blocked",a,prov,0.95,TemporalValidity(valid_from=datetime(2026,1,1,tzinfo=timezone.utc)),KnowledgeStatus.ACCEPTED))
        repo.append(KnowledgeRecord(KnowledgeKind.FACT,"supplier-x","status","tenant-b-private",b,prov,0.99,status=KnowledgeStatus.ACCEPTED))
        old=repo.query(text="supplier-x",tenant_id="a",at=datetime(2025,6,1,tzinfo=timezone.utc)); self.assertEqual(old[0].value,"preferred")
        new=repo.query(text="supplier-x",tenant_id="a",at=datetime(2026,6,1,tzinfo=timezone.utc)); self.assertEqual(new[0].value,"blocked"); self.assertTrue(all(r.scope.tenant_id!="b" for r in new))

if __name__=='__main__': unittest.main()
