# Experience Compiler Current Authority Boundary v0.1

**Status:** CURRENT_AUTHORITY  
**Purpose:** fast ownership classification before implementation

## Fresh-task rule

Before changing EC, answer:

> Does this belong to persistent advisory intelligence: knowledge, memory, learning, context compilation, research, reasoning, evaluation or governed proposals?

If **no**, EC is probably not the owner.

## EC owns

- persistent enterprise/industry knowledge and memory;
- provenance, temporal validity, confidence and supersession;
- learning methods / Learning Strategy Registry;
- context compilation for replaceable reasoning models;
- research acquisition/orchestration and evidence synthesis;
- diagnosis, recommendation, proposal and outcome learning;
- evaluation of intelligence quality and learning behavior;
- long-term model-portability of knowledge/methods.

## EC does not own by default

- enterprise operational source-of-truth execution;
- BusinessData posting / LedgerEntry / Balance calculation;
- Package/Feature lifecycle or Provider selection;
- login/session/user-directory implementation;
- authorization policy / delegated authority;
- Eidos rendering/runtime/Workbench;
- Human product UI;
- vendor-specific LLM ownership when a platform Provider boundary can supply the model;
- Enterprise Context business-definition authority.

## Placement rule

~~~text
persistent advisory knowledge / learning / reasoning
  -> Experience Compiler

deterministic business execution / ledger truth
  -> EVO / owning business runtime

package/provider/identity/authorization governance
  -> EVO App Platform

Human interaction/design
  -> Eidos Experience

LLM/vendor implementation
  -> replaceable Provider Plugin

external source/product compatibility
  -> bounded Integration Adapter / acquisition connector
~~~

EC may consume evidence from enterprise systems and propose governed changes, but it does not become the authority merely because it learned or inferred something.

## Model rule

LLMs are replaceable reasoning processors.

Do not put durable enterprise knowledge, learning method identity or business authority into one vendor/model integration. Model/vendor-specific code belongs behind a replaceable Provider/Adapter boundary.

## Research connector rule

External research acquisition connectors may live behind EC's acquisition boundary when EC owns the learning/research workflow, but the connector itself is translation/transport—not knowledge truth. Provenance remains explicit.

## Documentation loading rule

For ordinary work, read:

1. `LLM.md`
2. `CONSTITUTION.md`
3. this document
4. directly relevant current architecture/contracts

Load historical releases/ADRs/migration evidence only for compatibility, archaeology or rationale.

Current architecture may evolve; historical release evidence and accepted ADRs preserve project memory.

## Drift signal

Stop and reassess when EC starts to own:

- login/session flows;
- authorization or enterprise membership;
- package installation/lifecycle;
- deterministic ledger/accounting mutation;
- UI rendering primitives;
- one LLM vendor as architectural truth;
- direct automatic enterprise execution without governed admission.


## Project identity vs package integration

Experience-Compiler is a current owner project, not merely an App Platform package implementation detail.

The two identities are intentionally different:

```text
Experience-Compiler project
= durable advisory intelligence authority
  knowledge / memory / learning / research / context / reasoning semantics

EVO App Platform enterprise-agent package
= installable lifecycle/integration boundary
  tools / Experience contribution / Provider binding / governed access
```

The App Platform package may integrate EC capabilities through public contracts. It does not own or replace EC's durable intelligence semantics.

Historical ADR-0004/0005 describe the convergence path. Their older wording about EC product identity is historical context where it conflicts with this current authority boundary.
