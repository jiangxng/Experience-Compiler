# Backup and Disaster Recovery

Define RPO/RTO by data class. Raw evidence and canonical knowledge are irreplaceable; search/vector indexes should be rebuildable.

Minimum production practice: PITR for canonical DB, object-versioning/immutability where appropriate, encrypted off-site backups, regular restore drills, manifest/hash verification, documented key recovery, projection rebuild runbooks. A backup that has not been restored in a drill is not trusted.
