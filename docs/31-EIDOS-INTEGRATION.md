# Eidos Integration

Eidos exposes a versioned Capability Catalog. EC discovers semantic capabilities and emits an Experience Proposal; it must not depend on Eidos renderer internals. Eidos validates policy, accessibility, attention integrity, shared-reference constraints and supported versions, then realizes the experience.

The current architectural direction remains compatible with the Eidos boundary that EC may propose personalization while Eidos retains deterministic validation and a standard fallback.

## Proposed handshake
1. EC requests Capability Catalog + compatibility version.
2. EC plans regions using capability IDs (e.g. decision-panel, evidence-stack).
3. EC emits proposal + rationale + fallback reference.
4. Eidos validates/fails closed.
5. Eidos runtime renders and routes business actions to the Host/EVO boundary.

EC must never generate arbitrary executable UI code as the only representation of critical semantics.
