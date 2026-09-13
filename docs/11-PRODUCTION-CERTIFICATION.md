# Production Certification

Production certification is intentionally separate from the v1.0 reference-system version.

A deployment may call itself production-certified only after environment-specific evidence exists for:
PostgreSQL HA/failover, object evidence backup/restore, search/vector rebuild, tenant isolation,
secrets/key rotation, audit retention, EVO/Eidos contract tests, model-provider data residency,
load/SLO tests, migration rollback, observability/alerting, and disaster recovery.

`ec.operations.readiness.reference_readiness_report()` exposes known reference-vs-environment gaps so
operators and LLMs do not convert missing evidence into optimistic claims.
