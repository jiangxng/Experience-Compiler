# Agent / Enterprise Agent legacy branch reconciliation (2026-10-12)

The development-stage Agent history is being folded into this repository's current `main`, without reverting the newer and more authoritative architecture documents.

| Source branch | Pinned head | Reconciliation |
|---|---|---|
| `docs/align-enterprise-agent-boundaries-20260924` | `a5d86dc4e7666b140193b2c912aec419f096a50c` | Already an ancestor of `main`; no remaining delta |
| `docs/clarify-ec-vs-enterprise-agent-package` | `9e587bee1cacd641e8164a6140cbfa55e4d1fd05` | Diverged, but its architecture boundary document's meaningful lines are already in the longer `main` version; preserve `main` and attach legacy history |
| `evo/app-platform-agent-package-convergence-v0.1` | `bb3edbf24bd2084b7e432f81b5bbd21520ebe5db` | Preserve current `README.md`, `ARCHITECTURE.md`, `CONSTITUTION.md` and existing ADR 0005 rather than restoring the older package-convergence prose; attach legacy history |

### Semantic points retained from older proposals

- EVO remains authoritative for enterprise truth, deterministic commands, authorization and execution.
- Eidos owns deterministic UI interaction, validation and rendering.
- Experience Compiler owns knowledge, research, recommendations and governed proposals; it does not directly mutate EVO enterprise truth.
- Observations/proposals need explicit human or policy decisions and authorized EVO execution.
- The installable first-party `enterprise-agent` package belongs to EVO App Platform; EC may contribute learning/research services without owning the plugin lifecycle.

These are **historical conclusions**, not a mandate to replace later architecture. PR ancestry and exact current `main` document versions are the record of reconciliation. The legacy source refs should be retired only after the reconciliation PR is merged and ancestry is reverified. No business runtime was changed.
