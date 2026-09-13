# Architecture

## System boundary

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
   |                        Experience Planning
   |                                |
   +<--- Command Proposal ----------+----------> Eidos Proposal
```

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
Uses replaceable models according to capability, cost, latency, privacy and risk requirements.

### Experience Plane
Plans semantic human experiences and emits Eidos-facing proposals using discoverable Eidos capabilities.

### Governance Plane
Scope, provenance, lineage, policy, authorization, versioning, retention, audit and tenant isolation.

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
