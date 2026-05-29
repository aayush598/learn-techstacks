# Section 04: Database Replication & Failover

Database replication ensures data durability and availability across failures. The platform uses PostgreSQL streaming replication with synchronous commit for critical transactions and asynchronous replication for cross-region disaster recovery. Failover is automated using Patroni or PostgreSQL's built-in tools.

Replication architecture: primary database handles read/write traffic. Local replicas (same region) provide read scaling and serve as failover targets. Remote replicas (standby region) receive WAL via streaming replication for DR. Synchronous replication: at least one local replica confirms every write for zero data loss on primary failure.

Failover process: automated health check detects primary failure (3 consecutive failed checks, 15-second interval) → Patroni promotes the most advanced replica to primary → application connection poolers (PgBouncer) update connection strings → DNS record updated (if using DNS-based routing) → streaming replication re-established from new primary → old primary restored as replica when recovered. Manual failover available for planned maintenance.
