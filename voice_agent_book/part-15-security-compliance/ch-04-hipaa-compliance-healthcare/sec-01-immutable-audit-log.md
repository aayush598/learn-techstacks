# Section 01: Immutable Audit Log System

An immutable audit log captures all security-relevant events in a tamper-proof store. Once written, logs cannot be modified or deleted, even by administrators. This ensures the audit trail is admissible as evidence in security investigations and compliance audits. The system uses write-once, read-many (WORM) storage with cryptographic chain verification.

WORM architecture: events are written to append-only storage (AWS S3 Object Lock with retention mode COMPLIANCE, Azure Blob Storage immutability policy, or Apache Kafka with log compaction disabled). Each event has a SHA-256 hash, and events are linked in a hash chain: each event includes the hash of the previous event, forming a blockchain-like structure.

Verification: the hash chain can be verified at any time to ensure no events have been modified, deleted, or reordered. Periodic validation jobs run the chain verification and alert on anomalies. Audit logs are replicated to a separate account/region for disaster recovery and independence from the main platform operations.
