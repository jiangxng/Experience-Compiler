# Global Invariants

- EC-01: Experience Compiler never owns or mutates enterprise business truth.
- EC-02: Compiler output must be deterministic for the same pinned input and compiler version.
- EC-03: UIDL is runtime-neutral; compiler-core must not import Eidos implementation code.
- EC-04: Business actions are represented by declared command contracts, never hidden HTTP calls.
- EC-05: Source semantic fields are mapped explicitly; unknown semantic/control mappings fail closed.
- EC-06: Generated interaction definitions are serializable and versioned.
- EC-07: No implicit use of the latest upstream schema version; contract versions are explicit.
- EC-08: AI-generated future plans are Draft until accepted by policy; M0 is deterministic only.
- EC-09: No architectural decision may depend on prior LLM chat history.
- EC-10: EVO is an integration peer, not an internal module of this project.
