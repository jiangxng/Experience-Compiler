# EC v0.8 — Integration & Intelligence Runtime

**Release status:** executable reference system; v0.8/v0.9 integration preview.

This release advances the First-Principles EC platform from architecture seed to an executable
persistence → retrieval → context → model → research → learning reference loop.

Start with `docs/00-START-HERE.md`, then `docs/04-V0.7-REFERENCE-SYSTEM.md` and
`docs/05-RELEASE-MATURITY.md`.

# EC Enterprise Intelligence Platform

EC is a **persistent enterprise intelligence system** designed to survive model changes, infrastructure changes, and decades of operation.

It is not a chatbot, not a vector database, not a UI compiler, and not a single-agent framework.

## Canonical responsibility split

- **EVO** owns enterprise truth, transactions, commands, and execution.
- **EC** owns persistent knowledge, memory, learning methods, context compilation, research, reasoning orchestration, and experience planning.
- **Eidos** owns deterministic experience capabilities, validation, runtime realization, and renderers.
- **LLMs** are replaceable reasoning processors.

## What this v0.1 package is

This repository is the first long-lived architecture seed for the new EC. It contains:

- executable reference core with no mandatory third-party runtime dependency;
- canonical knowledge / case / decision / outcome / lesson / pattern models;
- temporal validity, provenance, scope, confidence, and supersession;
- versioned Learning Strategy Registry;
- LLM Bootstrap and Context Compiler;
- adaptive reasoning budget model;
- model capability registry and model-independent routing;
- external research acquisition boundary;
- EVO and Eidos integration contracts;
- Industry Pack format and manufacturing seed pack;
- in-memory reference persistence plus PostgreSQL schema and scale-out adapters;
- local deployment configuration and production technology route;
- tests, validation scripts, operations, backup, DR, migration, observability and hardware guidance.

## Fastest possible start

Requires Python 3.12+ only.

```bash
python -m unittest discover -s tests -v
PYTHONPATH=src python -m ec demo-manufacturing
PYTHONPATH=src python -m ec doctor
```

For a local editable install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
ec doctor
ec demo-manufacturing
```

## Read first

1. `docs/00-START-HERE.md`
2. `CONSTITUTION.md`
3. `ARCHITECTURE.md`
4. `docs/10-DATA-AND-SCALE.md`
5. `docs/20-HARDWARE-AND-CAPACITY.md`
6. `docs/30-EVO-INTEGRATION.md`
7. `docs/31-EIDOS-INTEGRATION.md`
8. `docs/40-LLM-REPLACEMENT.md`
9. `docs/50-ACTIVE-LEARNING-AND-RESEARCH.md`
10. `docs/90-TWENTY-YEAR-ROADMAP.md`

## Important

The reference implementations in `src/ec/storage/memory.py` are intentionally not production persistence. They make semantics testable before a database choice becomes architectural debt. Production data-plane choices are adapters and projections, not the owner of EC semantics.
