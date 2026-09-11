# New Chat / New LLM Handoff

You are working on **Experience Compiler**, an independent project.

Current milestone: **EC-M0 — Contract & Form Compilation Foundation**.

Ecosystem context:
- **EVO** is the first upstream enterprise semantic source. It owns enterprise truth and Commands.
- **Experience Compiler** compiles a versioned semantic snapshot into UIDL.
- **Eidos** is the first downstream runtime. It renders UIDL but must not require EVO knowledge.

Do not use any previous chat as architecture authority. Follow `LLM.md` and `context.manifest.json`.

M0 acceptance: the included EVO sales-order fixture compiles deterministically to UIDL 0.1 and passes tests.
