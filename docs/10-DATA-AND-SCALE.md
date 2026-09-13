# Data and Scale Architecture

## Foundational equation

`EC persistent intelligence >> any single model context window`.

## Data classes
Raw evidence, claims, governed knowledge, events, cases, decisions, outcomes, lessons, patterns, policies, preferences, learning methods, evaluations, model-run artifacts, lineage.

## Storage strategy
Canonical governance records live in a transactional store; raw immutable evidence in object storage; search/vector/graph/analytics are independently rebuildable projections. Avoid dual-write correctness by using an outbox/event projection mechanism in production.

## Scale bands
- S0: <1M records: single machine.
- S1: 1M-100M: dedicated PostgreSQL/object store + search/vector nodes.
- S2: 100M-10B: partitioned canonical store, event backbone, distributed indexes, analytics cluster.
- S3: >10B: domain/tenant sharding, federation, tiered hot/warm/cold storage, asynchronous projection fleets.

## Never shard by accident
Choose stable partition keys from tenant/domain/time access patterns. Record IDs remain globally unique. Tenant isolation cannot depend only on application filters.

## Context compilation
Retrieval is multi-stage: authority/time/scope filters -> lexical/vector/graph candidates -> rerank -> diversity/contradiction check -> evidence expansion -> token planning -> model.
