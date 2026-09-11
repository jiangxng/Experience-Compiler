# Public API

## `compileForm(snapshot)`
Input: `EvoExperienceSnapshotV1`-compatible semantic snapshot.  
Output: `UidlFormV01`.

Guarantees:
- deterministic output;
- preserves command code and input version;
- preserves field key, label, semantic type, required/read-only status and supported validation;
- does not perform network I/O;
- throws an explicit error for unsupported semantic types.

## Contract files
- `contracts/evo-semantic/v1.schema.json`
- `contracts/uidl/v0.1/schema.json`
- `contracts/contract.manifest.json`

These files are part of the external compatibility surface.
