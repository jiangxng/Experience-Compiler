# Hardware and Capacity

Hardware depends more on data volume, retrieval latency and model hosting than source-code size.

## Development minimum
- 4 modern CPU cores
- 16 GB RAM
- 50 GB SSD
- Python 3.12
Runs core tests and in-memory demo.

## Serious local/integration workstation
- 12-24 CPU cores
- 64-128 GB RAM
- 2-4 TB NVMe
- optional NVIDIA GPU with 24+ GB VRAM for local embedding/smaller models
Runs PostgreSQL + search/vector + analytics profiles and sizeable development corpora.

## Initial production (small enterprise)
Separate failure domains rather than one huge server: 3 application/control nodes (8-16 cores, 32-64 GB each); HA PostgreSQL (primary + replica, 16-32 cores, 64-128 GB, enterprise NVMe); S3-compatible durable object storage; 3 search/vector nodes if required; independent backup target.

## Medium/large enterprise
Kubernetes or equivalent scheduler; 3+ availability-zone-aware data nodes per critical distributed service; 25/100 Gb networking when index/analytics traffic demands it; NVMe for hot indexes; object storage for warm/cold evidence; dedicated inference GPUs only when private model hosting is justified.

## GPU principle
EC does not require a GPU to preserve knowledge. GPU capacity is replaceable inference/embedding infrastructure. Never make knowledge unreadable without a specific accelerator generation.

## Capacity measurement
Measure: canonical record count/bytes, raw evidence bytes, vectors + dimensions, graph edges, daily ingestion, query QPS/P95/P99, context tokens/task, reasoning tokens/value class, replication factor, retention and rebuild time. Size from measured workload, not vendor defaults.
