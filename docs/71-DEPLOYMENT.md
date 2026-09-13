# Deployment

Development can run entirely in-memory. `deploy/docker-compose.yml` is an integration convenience, not HA production. Production should separate stateless services and stateful data systems, use orchestration, disruption budgets, anti-affinity, rolling upgrades and encrypted service identity. Air-gapped deployment must package models/indexes/industry packs with signed manifests.
