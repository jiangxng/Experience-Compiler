# Data Import Experience Learning v0.1

**Status:** CURRENT_AUTHORITY  
**Owner:** Experience Compiler  
**First consumer:** EVO App Platform Data Import

## Purpose

Prove the smallest real Experience Compiler learning loop:

```text
EVO import evidence
  -> EC tenant-scoped experience
  -> EC advisory recommendation
  -> EVO Human review / deterministic execution
  -> new outcome evidence
```

The first acceptance case is intentionally narrow:

1. a Human confirms source field `编码` maps to `counterparty.subject.code`;
2. the import passes dry-run and commits successfully;
3. EC records the successful Human-confirmed experience;
4. a later import has a different overall table structure but still contains `编码`;
5. EC recommends `counterparty.subject.code` without relying on the old whole-table Recipe;
6. EVO presents/applies the recommendation for Human review;
7. EC never writes operational Counterparty data directly.

## Ownership

### EC owns

- persistent mapping experience;
- evidence/provenance linking the learned experience to the successful import job;
- tenant/object-scoped recommendation;
- confidence and contradiction handling;
- later consolidation/generalization of repeated experiences.

### EVO App Platform owns

- source-file handling;
- target object schema;
- deterministic mapping execution;
- dry-run;
- Human correction/confirmation;
- commit;
- Import Recipe as an executable deterministic artifact/cache;
- deciding when to request EC advisory help.

### Eidos owns

- Human presentation of recommendation, confidence, provenance and review controls.

## Learning eligibility

EC MUST NOT learn a reusable mapping from a guess alone.

v0.1 accepts experience only when all are true:

```text
Human final confirmation
AND dry-run passed
AND commit succeeded
```

The resulting learned pattern remains **tenant-scoped candidate intelligence**. It is not global truth and does not gain execution authority.

## Scope and anti-overfit rule

The learned key is conceptually:

```text
tenant
+ target object
+ normalized source term
-> target field
```

Therefore:

```text
Counterparty + 编码 -> code
```

does not imply:

```text
Item + 编码 -> code
Warehouse + 编码 -> code
global 编码 -> code
```

Cross-object or cross-tenant generalization requires a later governed learning step with its own evidence and evaluation.

## Recommendation safety

A recommendation is valid only when the target field still exists in the target schema supplied by the consumer.

Equal conflicting evidence fails closed: EC emits no preferred recommendation.

A recommendation is advisory-only. EVO may prefill a mapping for Human review, but EC cannot commit the import or mutate enterprise operational truth.

## Relationship to Import Recipe

Import Recipe and EC learning solve different problems.

```text
Import Recipe
= exact/sufficiently compatible whole-file execution pattern

EC mapping experience
= reusable semantic experience across different file structures
```

Recipe remains useful because it avoids unnecessary advisory work on known stable file formats. EC is consulted when deterministic reuse does not safely resolve the import.

## v0.1 non-goals

- synonym invention by an LLM;
- cross-enterprise/global promotion;
- automatic schema creation;
- automatic operational writes;
- semantic-vector retrieval;
- software-vendor fingerprinting;
- industry-wide alias dictionaries.

Those may be added after this narrow loop is measured.

## First hard test

Given a successful Human-confirmed import:

```text
文件 A
名称 | 编码 | 地址
       编码 -> Counterparty.code
```

A later file:

```text
文件 B
联系电话 | 编码 | 客户名称 | 开户行
          ^
```

must receive an EC recommendation:

```text
编码 -> Counterparty.code
confidence >= 0.90
supporting evidence = prior successful Human-confirmed import
```

without requiring the overall source-header fingerprint to match 文件 A.
