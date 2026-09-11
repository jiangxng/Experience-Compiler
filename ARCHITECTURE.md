# Architecture

```text
EVO (or another semantic source)
        |
        | Semantic Snapshot v1
        v
+-----------------------+
| Experience Compiler   |
|  compiler-core        |
|  form compiler (M0)   |
+-----------------------+
        |
        | UIDL 0.1
        v
Eidos (or another runtime)
```

Dependency direction is one-way. The compiler does not read the EVO database and does not import Eidos runtime internals.

M0 modules:
- `src/contracts.ts`: public transport types.
- `src/compile-form.ts`: deterministic form compilation.
- `src/validate.ts`: fail-closed semantic validation.
- `contracts/`: machine-readable protocol artifacts.
- `tests/`: executable specification.

Future packages may include report, chart, workspace and AI interaction planning, but those are not M0 runtime commitments.
