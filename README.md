# Experience Compiler

**Milestone:** EC-M0 — Contract & Form Compilation Foundation  
**Status:** runnable foundation  
**UIDL contract:** 0.1.0 (`sha256:c7e8f92e66bb4e3399aaa67271c7d0fb4ad5db8b958ada071eb65fc3fdabc092`)

Experience Compiler is the semantic-to-interaction compiler between enterprise systems and experience runtimes.
Its first upstream integration target is **EVO — Enterprise Operating System**. Its first downstream runtime target is **Eidos**.

It does **not** own enterprise truth, execute EVO Commands, or render UI. It compiles a versioned semantic snapshot into a deterministic, versioned interaction document (UIDL).

## Start here for humans and LLMs
Read in order:
1. `PHILOSOPHY.md`
2. `CONCEPTS.md`
3. `INVARIANTS.md`
4. `ARCHITECTURE.md`
5. `PUBLIC-API.md`
6. `LLM.md`
7. `context.manifest.json`
8. `docs/integration/EVO.md`
9. `docs/integration/EIDOS.md`
10. relevant source + tests

## Quick validation
```bash
npm run build
npm test
npm run example
```
No runtime npm dependencies are required for M0.
