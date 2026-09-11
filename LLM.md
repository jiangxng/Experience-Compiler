# LLM Engineering Contract

A fresh LLM must be able to work on this repository without any prior conversation.

Mandatory read order:
1. `/PHILOSOPHY.md`
2. `/CONCEPTS.md`
3. `/INVARIANTS.md`
4. `/ARCHITECTURE.md`
5. `/PUBLIC-API.md`
6. `/context.manifest.json`
7. relevant integration doc
8. relevant source and tests

Before changing code, establish: owner module, public contract impact, invariant impact, compatibility impact, deterministic-output impact, and tests required.

Never assume:
- EVO internal database shapes are compiler contracts;
- Eidos internals are UIDL semantics;
- source fields may be silently dropped;
- unsupported semantic types may be guessed;
- chat history is authoritative.

If authoritative repository sources conflict at the same priority, stop and report the conflict.
