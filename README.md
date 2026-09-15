> **Windows v1.0.1 quick start:** install Python 3.12 or 3.13, then double-click `START-EC-V1.0.1-WINDOWS.bat`.
> This patch fixes deterministic SQLite handle release required by Windows temporary-file cleanup.
> See `WINDOWS-ONE-CLICK-DEPLOYMENT.md`.

# EC v1.0.1 — Manufacturing Intelligence Reference System

**Release status:** executable reference system; v0.8/v0.9 integration preview.

This release advances the First-Principles EC platform from architecture seed to an executable
persistence → retrieval → context → model → research → learning reference loop.

Start with `docs/00-START-HERE.md`, then `docs/04-V0.7-REFERENCE-SYSTEM.md` and
`docs/05-RELEASE-MATURITY.md`.

# EC Enterprise Advisory Intelligence Platform

EC is the **persistent knowledge, memory, learning and advisory substrate for an enterprise consulting capability** designed to survive model changes, infrastructure changes, and decades of operation.

LLMs operating with EC are replaceable reasoning engines. Together, EC + LLM may provide management, strategy, business/process, finance, supply-chain, manufacturing/operations, quality, IT, data, security, implementation, operations/maintenance and other specialist consulting capabilities.

EC is **not** a virtual CEO/CIO/CTO, not enterprise management authority, not a source of operational truth, and not an automatic decision or execution authority. It is also not a chatbot, vector database, UI compiler, or single-agent framework.

## Lifecycle role

During initial enterprise-system establishment, EC primarily serves as an **implementation consulting capability**: understand the enterprise, compile/propose governed definitions and packages, help validate/configure/migrate/test/train/go-live, and identify gaps.

After go-live, EC primarily serves as an **ongoing advisory and operations/maintenance consulting capability**: observe governed enterprise information, diagnose, recommend, research, preserve experience, propose governed improvements, and assist business and IT operations.

## Runtime independence

**EVO + Eidos are the deterministic enterprise information system and must continue to operate normally without EC or any LLM.**

EC augments that system with advisory intelligence. If EC or its LLMs are unavailable, already-published enterprise definitions, authorized commands, business execution, governed facts and deterministic human interaction continue to work. What is lost or degraded is consulting intelligence: diagnosis, recommendation, research, learning and continuous-improvement assistance.

## Canonical responsibility split

- **EVO** owns enterprise truth, transactions, commands, authorization and deterministic execution.
- **EC** owns persistent knowledge, memory, learning methods, context compilation, research, reasoning orchestration, diagnosis, recommendation and governed proposals.
- **Eidos** owns deterministic experience capabilities, validation, runtime realization and renderers.
- **LLMs** are replaceable reasoning processors; project/development LLMs are not customer runtime participants.
- **Humans / governed policies** retain enterprise decision, approval and delegation authority.

Canonical loop:

`Observation/Evidence → Analysis/Diagnosis → Recommendation/Proposal → Human/Policy Decision → Validation/Authorization → EVO Execution → Outcome → EC Learning`

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
