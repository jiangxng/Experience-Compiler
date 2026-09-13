# EVO Integration

EVO is the authoritative business system. Integration is contract-based, never database-table coupling.

## EVO -> EC
- versioned semantic entity snapshots;
- append-only business event envelopes;
- command catalog / schemas;
- outcome measurements linked to decisions/actions;
- authorization context where policy permits.

## EC -> EVO
EC emits recommendations or `EvoCommandProposal`; EVO validates identity, permissions, invariants, idempotency and business rules before execution. EC never writes EVO ledgers/tables directly.

## Idempotency and lineage
Every event/action carries event ID, command ID, trace ID and tenant ID. Preserve the relationship `EC recommendation -> human/policy decision -> EVO command -> EVO events -> outcome`.

## Failure mode
If EC is unavailable, EVO remains able to execute deterministic enterprise operations. EC is an intelligence layer, not a required hidden transaction coordinator.
