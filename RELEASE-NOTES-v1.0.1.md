# EC v1.0.1 — Windows Compatibility Fix

Patch release over EC v1.0 Manufacturing Intelligence Reference System.

## Fixed
- Deterministic SQLite connection release on Windows.
- Temporary SQLite test databases no longer rely on interpreter/GC timing.
- Repository now exposes `close()` and context-manager ownership.
- Added SQLite file-release regression coverage.
- Added Windows one-click bootstrap/validation script.
- `.venv/` remains explicitly Git-ignored.

## Validation profile
- Reference runtime: Python 3.12 / 3.13 on Windows.
- Python 3.14 is intentionally not claimed as Windows-certified by this patch until a real Windows regression run is completed.

## Maturity
Reference System patch; not Production Certified.
