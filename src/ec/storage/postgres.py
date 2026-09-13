from __future__ import annotations
import json
from datetime import datetime
from typing import Any
from ec.domain import Scope,ScopeKind,TemporalValidity,Provenance
from ec.knowledge.model import KnowledgeRecord,KnowledgeKind,KnowledgeStatus

class PostgresKnowledgeRepository:
    """Production-shaped PostgreSQL adapter. Connection must implement DB-API execute/commit semantics (psycopg 3)."""
    def __init__(self,connection): self.db=connection
    def append(self,r:KnowledgeRecord)->None:
        q="""INSERT INTO ec_knowledge_record
        (record_id,schema_version,kind,subject,predicate,value_json,scope_json,provenance_json,confidence,
         valid_from,valid_to,observed_at,status,tags,supersedes)
        VALUES (%s,%s,%s,%s,%s,%s::jsonb,%s::jsonb,%s::jsonb,%s,%s,%s,%s,%s,%s,%s)"""
        scope={"kind":r.scope.kind.value,"key":r.scope.key,"tenant_id":r.scope.tenant_id}
        prov={"actor_type":r.provenance.actor_type,"actor_id":r.provenance.actor_id,"method":r.provenance.method,
              "run_id":r.provenance.run_id,"model_id":r.provenance.model_id,"strategy_id":r.provenance.strategy_id,
              "strategy_version":r.provenance.strategy_version,"parent_record_ids":list(r.provenance.parent_record_ids)}
        self.db.execute(q,(r.record_id,r.schema_version,r.kind.value,r.subject,r.predicate,json.dumps(r.value),
          json.dumps(scope),json.dumps(prov),r.confidence,r.temporal.valid_from,r.temporal.valid_to,
          r.temporal.observed_at,r.status.value,list(r.tags),list(r.supersedes))); self.db.commit()
    def get(self,record_id):
        cur=self.db.execute("SELECT record_id,schema_version,kind,subject,predicate,value_json,scope_json,provenance_json,confidence,valid_from,valid_to,observed_at,status,tags,supersedes FROM ec_knowledge_record WHERE record_id=%s",(record_id,))
        row=cur.fetchone(); return self._decode(row) if row else None
    def query(self,*,text=None,tenant_id=None,kinds=None,at=None,limit=100):
        clauses=["1=1"]; args=[]
        if tenant_id is not None:
            clauses.append("(scope_json->>'tenant_id' IS NULL OR scope_json->>'tenant_id'=%s)"); args.append(tenant_id)
        if kinds:
            clauses.append("kind = ANY(%s)"); args.append(list(kinds))
        if text:
            clauses.append("lower(subject||' '||predicate||' '||value_json::text) LIKE %s"); args.append("%"+text.lower()+"%")
        if at:
            clauses+=["(valid_from IS NULL OR valid_from<=%s)","(valid_to IS NULL OR valid_to>%s)"]; args += [at,at]
        args.append(limit)
        cur=self.db.execute("SELECT record_id,schema_version,kind,subject,predicate,value_json,scope_json,provenance_json,confidence,valid_from,valid_to,observed_at,status,tags,supersedes FROM ec_knowledge_record WHERE "+" AND ".join(clauses)+" ORDER BY created_at DESC LIMIT %s",args)
        return [self._decode(x) for x in cur.fetchall()]
    def _decode(self,x):
        value=x[5] if not isinstance(x[5],str) else json.loads(x[5]); sc=x[6] if not isinstance(x[6],str) else json.loads(x[6]); pr=x[7] if not isinstance(x[7],str) else json.loads(x[7])
        return KnowledgeRecord(record_id=str(x[0]),schema_version=x[1],kind=KnowledgeKind(x[2]),subject=x[3],predicate=x[4],value=value,
          scope=Scope(ScopeKind(sc["kind"]),sc["key"],sc.get("tenant_id")),provenance=Provenance(pr["actor_type"],pr["actor_id"],pr["method"],pr["run_id"],
          parent_record_ids=tuple(pr.get("parent_record_ids",())),model_id=pr.get("model_id"),strategy_id=pr.get("strategy_id"),strategy_version=pr.get("strategy_version")),
          confidence=x[8],temporal=TemporalValidity(x[9],x[10],x[11]),status=KnowledgeStatus(x[12]),tags=tuple(x[13] or ()),supersedes=tuple(str(i) for i in (x[14] or ())))
