# Storage Technology Route

Reference production direction, not immutable vendor lock-in:
- PostgreSQL 18-class relational database for canonical governance metadata and transactional integrity.
- S3-compatible object storage for immutable evidence and large artifacts.
- OpenSearch-class engine for full-text/filtering.
- Qdrant-class vector engine for semantic candidates.
- graph projection can begin relationally and move to a dedicated graph engine only when traversal workloads justify it.
- ClickHouse-class analytical engine for high-volume learning/evaluation analytics.
- Kafka-compatible durable event backbone when projection/ingestion volume requires it.
- Temporal-compatible durable workflow layer for long-running research/learning jobs when simple queues cease to be reliable enough.

Every choice sits behind an adapter.
