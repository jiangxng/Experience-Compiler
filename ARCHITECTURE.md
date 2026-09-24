# Architecture

## System boundary

EC is an **enterprise advisory intelligence layer** around, but not inside, the deterministic EVO + Eidos enterprise runtime. EC may disappear without making already-published enterprise operation unavailable.

```text
                 External World / Industry / Experts
                              |
                        Research Plane
                              |
                              v
EVO Truth ---> Ingestion ---> Knowledge Plane <--- Industry Packs
   |                          /    |    \
   |                         /     |     \
   |                   Memory  Learning  Governance
   |                         \     |      /
   |                          \    |     /
   |                           Context Plane
   |                                |
   |                         Model / Reasoning Plane
   |                                |
   |                    Advisory Intelligence Plane
   |                     /                     \
   |        Recommendation / Proposal      Experience Intent
   |                   |                       |
   +<------------------+                       +----> Eidos Proposal

Human / governed policy decides and approves
                    |
                    v
     App Platform governed admission
                    |
                    v
      deterministic runtime execution
      (EVO Ledger Runtime where applicable)
```

The EC path is advisory. It does not sit on the mandatory transaction path between humans, Eidos and EVO.

## Lifecycle operating model

### Implementation consulting
During enterprise-system establishment, EC + replaceable LLM reasoning engines help understand the enterprise, compile/propose governed enterprise definitions/packages and experience intent, assist validation/configuration/migration/testing/training/go-live, and identify implementation gaps.

### Ongoing consulting and operations support
After go-live, EC observes governed enterprise information and provides diagnosis, recommendation, research, knowledge maintenance, continuous-improvement proposals and business/IT operations assistance.

Neither lifecycle role grants EC management, approval or execution authority.

## Logical planes

### Knowledge Plane
Canonical governed representations of claims, facts, rules, policies, ontologies and domain knowledge.

### Memory Plane
Cases, decisions, outcomes, lessons, patterns, preferences and longitudinal enterprise experience.

### Learning Plane
Knowledge acquisition, consolidation, pattern formation, drift detection, strategy evaluation and meta-learning.

### Research Plane
Knowledge-gap detection and controlled external acquisition. Crawlers/search/APIs are adapters, not the architecture.

### Context Plane
Transforms massive persistent intelligence into bounded, task-specific, evidence-rich context packs.

### Model / Reasoning Plane
Uses replaceable models according to capability, cost, latency, privacy and risk requirements. Models are reasoning processors, not the persistent owner of enterprise intelligence.

### Advisory Intelligence Plane
Turns governed evidence and context into consultant-style analysis, diagnosis, forecasts, scenarios, recommendations and proposals. Outputs preserve evidence, uncertainty, scope and expected impact. Advisory output is not operational truth and does not imply authorization.

### Experience Plane
Plans semantic human experiences and emits Eidos-facing proposals using discoverable Eidos capabilities. Eidos validates and deterministically realizes accepted experience definitions.

### Governance Plane
Scope, provenance, lineage, policy, authorization evidence, versioning, retention, audit and tenant isolation. EC governance constrains EC artifacts; it does not replace App Platform/Host authorization orchestration or any deterministic runtime's own validation boundary.

## Runtime independence invariant

The normal deterministic enterprise runtime is:

`Human -> Eidos deterministic interaction -> App Platform/Host governance + authorization orchestration -> owned deterministic runtime -> governed enterprise state`

EC may observe and advise around this runtime but is not required for it. If EC/LLMs are unavailable:

- published EVO enterprise definitions remain valid;
- authorized platform actions and deterministic runtime operations continue to execute through their owning public contracts;
- governed facts, ledger state and deterministic derived state remain available according to their owning runtime boundaries;
- published Eidos experiences continue to render and interact;
- EC-only diagnosis, recommendation, research, learning and improvement assistance may be unavailable.

## Canonical advisory loop

`Observation/Evidence -> Analysis/Diagnosis -> Recommendation/Proposal -> Human/Policy Decision -> App Platform Governance/Admission -> Deterministic Runtime Execution -> Outcome -> EC Learning`

This loop is intentionally asymmetric: EC may learn from outcomes, but learned output returns through governance before it can affect deterministic enterprise operation.

## Canonical vs projections

Canonical assets must survive technology replacement:
- raw evidence references + hashes;
- knowledge records;
- events/cases/decisions/outcomes;
- learning strategy versions and evaluations;
- provenance/lineage;
- industry pack versions;
- model-independent context records and important reasoning artifacts.

Rebuildable projections may use specialized technologies:
- lexical index;
- vector index;
- graph projection;
- analytical warehouse;
- caches;
- materialized summaries.

## Deployment evolution

```text
Developer laptop
  -> single-node enterprise
  -> HA data services
  -> Kubernetes cluster
  -> independent data-plane scaling
  -> multi-region / sovereign / air-gapped federations
```

No upper layer imports a vendor-specific database SDK directly. Vendor adapters live below ports.


## App Platform package boundary

EC repository topology and Enterprise Agent package topology are intentionally separate.

```text
jiangxng/Experience-Compiler
  durable intelligence assets + services
              │
              │ versioned public contracts
              ▼
EVO App Platform
  enterprise-agent AGENT Package
  lifecycle / Eidos Experience / tool boundary / Provider resolution
```

The host-side TypeScript `agents/enterprise-agent` runtime is retained as an integration asset. It does not replace EC knowledge, memory, learning, research or Context Compiler semantics.

Model vendor adapters are not package identity. Target model access is resolved through the App Platform `llm.inference` Provider capability.
