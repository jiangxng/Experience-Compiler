# v1.0 Readiness Gate

Do not call EC v1.0 Manufacturing Intelligence Reference System until all mandatory gates pass.

Mandatory:
- production PostgreSQL integration test against a real PostgreSQL service
- durable evidence/object-storage adapter and restore drill
- real model-provider evaluation with frozen benchmark corpus
- authoritative EVO public-contract integration
- authoritative Eidos public-contract integration
- manufacturing ontology/process/decision corpus review
- end-to-end manufacturing scenarios covering shortage, capacity, quality, maintenance and fulfillment
- tenant isolation/security tests
- migration/rollback rehearsal
- load/performance baseline and observability
- decision→outcome→lesson regression evidence

v0.9 provides the executable reference lifecycle needed to begin these gates.
