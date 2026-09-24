# ADR-0005: EC implementation converges behind the Enterprise Agent Package

**Status:** Accepted  
**Date:** 2026-09-24

## Context

ADR-0004 redefined Experience Compiler as the durable intelligence behind an Enterprise Agent and deferred the repository/package integration decision.

Since that decision, EVO App Platform has established:

- an `AGENT` Package type;
- Package/Feature lifecycle;
- Eidos App Host contributions;
- ActionHost/tool boundaries;
- Provider Plugin contracts;
- an existing model-independent Enterprise Agent runtime and installation proofs.

The EC repository already contains substantial durable intelligence assets and must not be replaced by a new parallel implementation.

## Decision

The **Experience-Compiler repository remains an independent implementation/asset repository**, while the product is installed and lifecycle-managed as the **`enterprise-agent` AGENT Package** by EVO App Platform.

This repository remains authoritative for durable intelligence semantics:

- knowledge;
- memory;
- learning;
- research;
- Context Compiler;
- provenance/lineage;
- industry packs;
- model replacement/bootstrap methods.

EVO App Platform remains authoritative for Package lifecycle, Eidos Experience contribution, public platform tools and Provider resolution.

## Package identity

```text
repository: jiangxng/Experience-Compiler
historical name: Experience Compiler / EC
target product/package: enterprise-agent
package type: AGENT
```

Repository identity and Package identity are intentionally different.

## Existing App Platform Agent work

The existing `agents/enterprise-agent` implementation is retained.

It is the host-side runtime/tool integration asset and is not a replacement for EC knowledge/memory/learning assets.

The two implementations converge through public contracts.

## LLM migration

EC currently contains an OpenAI-compatible model adapter, and App Platform contains an OpenAI Responses Agent adapter.

Both are retained as useful implementation evidence.

The target architecture is nevertheless Provider-based:

```text
Enterprise Agent
→ llm.inference capability
→ App Platform Provider resolution
→ LLM Provider plugin
```

No model vendor becomes part of the permanent Enterprise Agent identity.

## Integration rule

Do not bulk-copy EC Python modules into EVO App Platform.

Prefer:

- versioned service/API contracts;
- immutable/package data assets for Industry Packs where appropriate;
- explicit Context/Knowledge/Research ports;
- deployment adapters.

## Runtime independence

EVO + Eidos deterministic operation remains independent from EC/Enterprise Agent and any LLM.

Loss of Enterprise Agent degrades advisory intelligence, not authoritative business execution.

## Consequences

1. EC pluginization means package/lifecycle integration, not repository flattening.
2. Existing EC and App Platform Agent assets are both project capital.
3. Future work first proves the Package lifecycle, then LLM Provider resolution, then deeper EC service integration.
4. Historical EC releases remain preserved.
