from __future__ import annotations
import json, sqlite3
from datetime import datetime
from pathlib import Path
from ec.domain import Scope, ScopeKind, TemporalValidity, Provenance
from ec.knowledge.model import KnowledgeRecord, KnowledgeKind, KnowledgeStatus

class SqliteKnowledgeRepository:
    """Durable reference adapter. Production deployments should use the PostgreSQL adapter contract."""
    def __init__(self, path: str | Path):
        self.path=str(path); self.db=sqlite3.connect(self.path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS knowledge(
          record_id TEXT PRIMARY KEY, kind TEXT NOT NULL, subject TEXT NOT NULL,
          predicate TEXT NOT NULL, value_json TEXT NOT NULL, scope_kind TEXT NOT NULL,
          scope_key TEXT NOT NULL, tenant_id TEXT, confidence REAL NOT NULL,
          status TEXT NOT NULL, valid_from TEXT, valid_to TEXT, observed_at TEXT NOT NULL,
          actor_type TEXT NOT NULL, actor_id TEXT NOT NULL, method TEXT NOT NULL, run_id TEXT NOT NULL)""")
        self.db.execute("CREATE INDEX IF NOT EXISTS ix_knowledge_tenant_subject ON knowledge(tenant_id,subject)")
        self.db.commit()
    def append(self,r:KnowledgeRecord)->None:
        self.db.execute("INSERT INTO knowledge VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(
          r.record_id,r.kind.value,r.subject,r.predicate,json.dumps(r.value,ensure_ascii=False),
          r.scope.kind.value,r.scope.key,r.scope.tenant_id,r.confidence,r.status.value,
          r.temporal.valid_from.isoformat() if r.temporal.valid_from else None,
          r.temporal.valid_to.isoformat() if r.temporal.valid_to else None,r.temporal.observed_at.isoformat(),
          r.provenance.actor_type,r.provenance.actor_id,r.provenance.method,r.provenance.run_id))
        self.db.commit()
    def get(self,record_id):
        row=self.db.execute("SELECT * FROM knowledge WHERE record_id=?",(record_id,)).fetchone()
        return self._decode(row) if row else None
    def query(self,*,text=None,tenant_id=None,kinds=None,at=None,limit=100):
        sql="SELECT * FROM knowledge WHERE 1=1"; args=[]
        if tenant_id is not None: sql+=" AND (tenant_id IS NULL OR tenant_id=?)"; args.append(tenant_id)
        if kinds:
            sql+=" AND kind IN (%s)"%(",".join("?"*len(kinds))); args.extend(kinds)
        if text:
            sql+=" AND lower(subject||' '||predicate||' '||value_json) LIKE ?"; args.append("%"+text.lower()+"%")
        sql+=" ORDER BY rowid DESC LIMIT ?"; args.append(limit*3)
        now=at
        out=[]
        for row in self.db.execute(sql,args):
            r=self._decode(row)
            if now is None or r.temporal.is_valid_at(now):
                out.append(r)
                if len(out)>=limit: break
        return out
    def _decode(self,x):
        vf=datetime.fromisoformat(x[10]) if x[10] else None; vt=datetime.fromisoformat(x[11]) if x[11] else None
        return KnowledgeRecord(record_id=x[0],kind=KnowledgeKind(x[1]),subject=x[2],predicate=x[3],
          value=json.loads(x[4]),scope=Scope(ScopeKind(x[5]),x[6],x[7]),confidence=x[8],
          status=KnowledgeStatus(x[9]),temporal=TemporalValidity(vf,vt,datetime.fromisoformat(x[12])),
          provenance=Provenance(x[13],x[14],x[15],x[16]))
