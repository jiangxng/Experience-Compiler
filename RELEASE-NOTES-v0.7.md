# EC v0.7 Release Notes

## Added
- Durable SQLite canonical reference repository.
- Content-addressed immutable evidence archive.
- Deterministic hybrid lexical/semantic retrieval.
- Adaptive Context Compiler with explicit token budgets.
- Provider-neutral Model Gateway and deterministic reference provider.
- Active Research Pipeline that creates candidate claims rather than truth.
- Conservative Decision → Outcome → Lesson learning loop.
- EVO/Eidos reference gateways.
- Six new end-to-end subsystem tests; eleven total tests.

## Integration preview
v0.8/v0.9 boundaries are present as contracts/reference gateways. Real production EVO/Eidos endpoints
must converge against their authoritative public APIs; EC does not invent or bypass them.

## Scale note
SQLite, filesystem evidence, and hashed-vector semantic retrieval are executable reference adapters.
They prove contracts and behavior, not hyperscale performance. PostgreSQL/object storage/search/vector/
graph/analytics projections remain independently replaceable along the documented scaling route.
