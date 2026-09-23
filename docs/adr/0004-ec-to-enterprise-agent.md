# ADR-0004: Experience Compiler transitions to Enterprise Agent

**Status:** Accepted  
**Date:** 2026-09-23

## Context

The original EC / Experience Compiler concept evolved from a durable enterprise knowledge, learning and advisory system.

The current system architecture now separates responsibilities more clearly:

- EVO provides enterprise computation/runtime capabilities;
- Eidos provides the pure frontend framework and App Host;
- EVO App Platform manages package/application lifecycle;
- the former EC responsibility is best expressed as a durable LLM Agent that uses those capabilities.

The name **Experience Compiler** no longer describes the target role accurately.

## Decision

EC is redefined as an **Enterprise Agent**.

> Enterprise Agent is a durable enterprise LLM Agent whose underlying model is replaceable while its role, memory, knowledge, methods and tool contracts remain persistent.

The Agent may:

- understand enterprise and industry context;
- plan and recommend;
- discover/select/configure applications;
- invoke public tools/APIs when authorized;
- learn from outcomes;
- preserve durable enterprise knowledge, experience and methods.

The Agent is not:

- EVO Core;
- Eidos Core;
- App Manager;
- enterprise operational truth;
- unrestricted execution authority.

## Package model

Enterprise Agent is expected to become an `AGENT` Package in the EVO App Platform package model.

The canonical package-model authority lives in the EVO-App-Platform repository:

`docs/architecture/AGENT-PACKAGE-MODEL-v0.1.md`

This repository remains the authority for the historical transition and migration of existing EC assets.

## Assets retained

The following EC assets remain valuable and should be preserved/reused where applicable:

- enterprise/industry knowledge models;
- memory and knowledge persistence;
- provenance and lineage;
- learning strategies;
- model-replacement mechanisms;
- context compilation;
- research acquisition;
- evaluation and reasoning methods;
- historical decisions and experience.

These assets become durable capabilities used by the Enterprise Agent rather than defining EC as a separate platform product.

## Superseded product identity

The target product identity "Experience Compiler" is superseded.

Historical documents and releases remain historical evidence and must not be rewritten to pretend the old design never existed.

When older documents conflict with this ADR about the product's current identity, this ADR wins for future architecture work.

## Repository decision deferred

This ADR does **not** decide whether:

- this repository will be renamed;
- a new Enterprise Agent repository will be created;
- implementation will be migrated into EVO-App-Platform;
- knowledge/memory will later be split into an independent service.

Those are separate engineering decisions.

## Model replacement

ADR-0003 remains valid.

A change of LLM/provider does not create a new Enterprise Agent identity. Durable role, memory, knowledge, methods, authority rules and tool contracts must survive model replacement.

## Consequences

Future work should:

1. stop expanding Experience Compiler as an independent platform identity;
2. evaluate existing EC implementation as reusable Enterprise Agent assets;
3. define public tool contracts to EVO, Eidos and App Platform;
4. preserve knowledge provenance and learning continuity;
5. avoid creating a separate Knowledge Platform until an independent lifecycle/ownership need exists.
