# Technology Baseline — 2026-09

This document is **time-stamped implementation guidance**, not Constitution. Future maintainers may replace every product below while preserving EC contracts and canonical assets.

## Current reference choices

- PostgreSQL 18-class database: canonical governance metadata and transactional integrity. PostgreSQL 18 added native `uuidv7()` and asynchronous I/O; the Reference Runtime deliberately does not require these features.
- S3-compatible object storage: immutable raw evidence, large artifacts and cold data.
- OpenSearch-class full-text engine: lexical/filter candidates and operational search.
- Qdrant-class vector engine: semantic candidate retrieval; distributed mode supports sharding/replication when vertical scaling is exhausted.
- ClickHouse-class analytical engine: high-volume evaluations, learning analytics and operational intelligence aggregates.
- Kafka-compatible event log: projection/ingestion backbone once single-process/outbox throughput is insufficient. Production deployments should separate controller/broker roles rather than use development combined mode.
- Temporal-compatible durable execution: long-running research, learning and recovery-sensitive workflows.
- OpenTelemetry: vendor-neutral traces, metrics and logs across ingestion/retrieval/model/EVO/Eidos flows.
- Kubernetes (or equivalent scheduler): production orchestration once multiple stateful/stateless services require independent scaling.

## Why products are not public contracts

The public EC contract is KnowledgeRecord / LearningStrategy / ContextPack / integration protocols. A database or index may be replaced by migration/rebuild without changing the meaning or stable IDs of canonical intelligence.

## Upgrade rule

Review this baseline at least annually. Upgrade only after contract tests, replay tests, backup-restore tests and representative load benchmarks pass. Never upgrade all stateful layers simultaneously.
