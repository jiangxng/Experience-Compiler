from __future__ import annotations
from datetime import datetime, timezone
from threading import RLock
from ec.knowledge.model import KnowledgeRecord

class InMemoryKnowledgeRepository:
    """Deterministic semantic reference store. Not a production data store."""
    def __init__(self) -> None:
        self._records: dict[str, KnowledgeRecord] = {}
        self._order: list[str] = []
        self._lock = RLock()

    def append(self, record: KnowledgeRecord) -> None:
        with self._lock:
            if record.record_id in self._records:
                raise ValueError(f"record already exists: {record.record_id}")
            self._records[record.record_id] = record
            self._order.append(record.record_id)

    def get(self, record_id: str) -> KnowledgeRecord | None:
        with self._lock:
            return self._records.get(record_id)

    def query(self, *, text: str | None = None, tenant_id: str | None = None,
              kinds=None, at: datetime | None = None, limit: int = 100) -> list[KnowledgeRecord]:
        at = at or datetime.now(timezone.utc)
        kindset = set(kinds or [])
        needle = text.casefold() if text else None
        result: list[KnowledgeRecord] = []
        with self._lock:
            for rid in reversed(self._order):
                rec = self._records[rid]
                if tenant_id is not None and rec.scope.tenant_id not in (None, tenant_id):
                    continue
                if kindset and rec.kind.value not in kindset:
                    continue
                if not rec.temporal.is_valid_at(at):
                    continue
                if needle and needle not in f"{rec.subject} {rec.predicate} {rec.value}".casefold():
                    continue
                result.append(rec)
                if len(result) >= limit:
                    break
        return result
