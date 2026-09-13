# Testing

## Current
Run `PYTHONPATH=src python -m unittest discover -s tests -v` and `python scripts/validate_repo.py`.

## Required future layers
Unit, contract/schema, deterministic golden, property tests, tenant-isolation, temporal correctness, adversarial retrieval, source poisoning, migration/replay, projection rebuild, chaos/failure, load, model conformance, industry benchmark and end-to-end EVO/Eidos scenarios.

Freeze Context Packs for model regression so a model upgrade can be compared against identical inputs.
