# Backup Strategies for Recommendation Systems

## Overview

A production recommendation system depends on multiple data stores, trained models, feature pipelines, and configuration state. Loss of any component can degrade or disable recommendations entirely. This document covers comprehensive backup strategies across all system components, recovery procedures, and the planning framework for defining acceptable downtime and data loss.

## RTO/RPO Planning

### Definitions

- **Recovery Time Objective (RTO)**: Maximum acceptable time to restore service after a failure.
- **Recovery Point Objective (RPO)**: Maximum acceptable data loss measured in time.

### Target RTO/RPO by Component

| Component | RTO Target | RPO Target | Backup Frequency | Justification |
|-----------|------------|------------|------------------|---------------|
| PostgreSQL (user data) | 15 minutes | 1 minute | Continuous WAL archiving | Core user behavior data |
| PostgreSQL (catalog) | 1 hour | 15 minutes | Hourly snapshots | Item catalog changes infrequently |
| Redis (session cache) | 5 minutes | 5 minutes | RDB snapshots + AOF | Cache can be rebuilt from DB |
| Redis (precomputed recs) | 30 minutes | 1 hour | Hourly snapshots | Regenerable from training |
| Model Artifacts | 30 minutes | 24 hours | Daily + on-change | Models change infrequently |
| Feature Store | 30 minutes | 1 hour | Hourly snapshots | Regenerable from raw data |
| Configuration | 5 minutes | 0 (git) | Version control | All config in Git |
| Training Data | 1 hour | 24 hours | Daily snapshots | Large, rarely modified |

### Recovery Strategy Tiers

- **Tier 1 (Critical, <15 min RTO)**: PostgreSQL primary, Redis session cache, API endpoints.
- **Tier 2 (Important, <1 hour RTO)**: Feature store, precomputed recommendations, monitoring.
- **Tier 3 (Deferrable, <4 hours RTO)**: Training infrastructure, batch pipelines, analytics.
- **Tier 4 (Non-critical, <24 hours RTO)**: Development environments, historical data archives.

## Database Backup

### PostgreSQL Backup Strategy

**Continuous WAL Archiving**

- Enable WAL (Write-Archival Logging) archiving to S3 for continuous point-in-time recovery.
- Configure `archive_mode = on` and `archive_command` to copy WAL segments to S3.
- Retain WAL archives for the same duration as backup retention.
- WAL archiving enables recovery to any point in time within the retention window.

**pg_dump Logical Backups**

- Schedule daily `pg_dump` logical backups for full database snapshots.
- Use `--format=custom` for compressed, parallelizable backup format.
- Store backups in S3 with server-side encryption.
- Retain daily backups for 30 days, weekly backups for 12 weeks, monthly backups for 12 months.

**pgBackRest for Advanced Backup**

- Use pgBackRest for enterprise-grade backup management.
- Features: incremental backups, parallel compression, encrypted backups, parallel restore.
- Configure stanza for each database instance.
- Set up repository on S3 with lifecycle policies.
- Enable checksum verification on every backup.

**Backup Schedule**

| Backup Type | Frequency | Retention | Storage | Purpose |
|-------------|-----------|-----------|---------|---------|
| WAL Archiving | Continuous | 7 days | S3 Standard | Point-in-time recovery |
| pg_dump (full) | Daily 2:00 AM UTC | 30 days | S3 Standard | Full logical backup |
| pg_dump (full) | Weekly Sunday 2:00 AM UTC | 12 weeks | S3 IA | Weekly archive |
| pg_dump (full) | Monthly 1st 2:00 AM UTC | 12 months | S3 Glacier | Monthly archive |
| pg_basebackup | Daily 3:00 AM UTC | 14 days | S3 Standard | Physical backup |
| Replica snapshot | Every 6 hours | 7 days | S3 Standard | Read replica recovery |

**Backup Verification**

- Run automated restore tests weekly against a disposable RDS instance.
- Verify data integrity by comparing row counts and checksums.
- Test point-in-time recovery to random timestamps monthly.
- Document recovery time for each backup type and compare against RTO targets.

### Read Replica Strategy

- Maintain at least one read replica in the same region for read failover.
- Configure automatic failover promotion for the read replica (RDS Multi-AZ).
- Use synchronous replication for Tier 1 databases (zero data loss).
- Use asynchronous replication for Tier 2 databases (minimal latency impact).

## Redis Backup

### RDB (Snapshot) Backups

- Enable Redis RDB snapshots at regular intervals.
- Configure `save 900 1` (save if 1 keys changed in 900 seconds) for base protection.
- Store RDB files in S3 for durable backup.
- RDB provides point-in-time snapshots with minimal performance impact.

### AOF (Append-Only File) Persistence

- Enable AOF persistence for Redis with `appendfsync everysec`.
- AOF provides better durability than RDB alone (at most 1 second of data loss).
- Configure AOF rewrite policy to manage file size.
- Use AOF for recovery of recent writes that may not be captured in RDB snapshots.

### Redis Backup Schedule

| Backup Type | Frequency | Retention | Use Case |
|-------------|-----------|-----------|----------|
| RDB Snapshot | Every 5 minutes | 24 hours | Quick recovery |
| RDB to S3 | Every hour | 7 days | Durable backup |
| AOF | Continuous | Until rewrite | Maximum durability |
| Full Redis Export | Daily | 30 days | Complete restoration |

### Redis Recovery Procedures

1. **Cache Miss Recovery**: Simply restart Redis and let the cache warm from the database.
2. **Data Corruption Recovery**: Stop Redis, restore from RDB snapshot, replay AOF.
3. **Complete Loss Recovery**: Restore from S3 backup, verify data integrity, restart service.
4. **Partial Shard Failure**: Redis Cluster automatically rebalances; monitor and verify.

## Model Artifact Backup

### Model Registry Backup

- Store all model artifacts in a versioned S3 bucket.
- Enable versioning to prevent accidental overwrites.
- Replicate model artifacts to a secondary region for disaster recovery.
- Maintain a model metadata database (MLflow or custom) with backup strategy.

### Model Artifact Types

| Artifact | Size (Typical) | Change Frequency | Backup Priority |
|----------|----------------|------------------|-----------------|
| Trained Model (ONNX) | 100MB-2GB | Weekly | High |
| Model Weights (PyTorch) | 50MB-5GB | Weekly | High |
| Feature Pipeline Code | 10MB-100MB | Daily | Critical |
| Training Config | 1KB-100KB | Per experiment | Critical |
| Training Data Snapshots | 1GB-100GB | Daily | Medium |
| Validation Reports | 1MB-10MB | Per experiment | Low |

### Model Versioning Strategy

- Tag every model version with: commit SHA, training data hash, metrics, and timestamp.
- Store model lineage: which code version, data version, and hyperparameters produced it.
- Implement model rollback capability by keeping previous versions in the registry.
- Archive retired models to cold storage after 90 days.

## Configuration Backup

### Infrastructure Configuration

- All Terraform configurations are version-controlled in Git (inherent backup).
- Store Terraform state files in versioned S3 buckets.
- Back up Kubernetes manifests using Velero with daily schedules.
- Store Helm values files in Git for all environments.

### Application Configuration

- Store all application configuration in environment variables and ConfigMaps.
- Use AWS Secrets Manager or Vault for secrets with automatic rotation.
- Back up ConfigMaps and Secrets using Velero.
- Document all configuration dependencies and startup requirements.

### Monitoring Configuration

- Export Grafana dashboards as JSON and store in Git.
- Back up Prometheus alerting rules and recording rules.
- Store PagerDuty/Opsgenie escalation policies in version control.
- Document all monitoring thresholds and their rationale.

## Backup Testing

### Automated Recovery Tests

- Run weekly automated restore tests for PostgreSQL backups.
- Verify Redis backup integrity by restoring to a test instance and comparing data.
- Test model artifact restoration by loading and running inference against test data.
- Validate that restored configurations produce a functional system.

### Chaos Engineering

- Schedule monthly game days to simulate component failures.
- Test full-region failure scenarios quarterly with DR failover.
- Verify that backup systems function correctly under failure conditions.
- Document lessons learned and update procedures accordingly.

### Recovery Drill Schedule

| Test Type | Frequency | Scope | Duration |
|-----------|-----------|-------|----------|
| Database point-in-time restore | Weekly | PostgreSQL | 30 minutes |
| Full database restore | Monthly | PostgreSQL | 2 hours |
| Redis failover test | Monthly | Redis Cluster | 30 minutes |
| Model artifact restoration | Monthly | Model Registry | 1 hour |
| Full system DR failover | Quarterly | All components | 4 hours |
| Chaos engineering (random) | Monthly | Random component | 2 hours |

## Cross-Region Backup Replication

### Multi-Region Strategy

- Primary region: All production workloads with full backup infrastructure.
- Secondary region: Warm standby with scaled-down capacity and replicated data.
- Tertiary region: Cold storage for long-term archival (S3 Glacier Deep Archive).

### Replication Methods

| Component | Primary → Secondary | RPO | RPO Target |
|-----------|-------------------|-----|------------|
| PostgreSQL | Cross-region read replica | Seconds | <1 minute |
| Redis | Cross-region replication | Seconds | <5 minutes |
| S3 Model Artifacts | Cross-region replication | Minutes | <15 minutes |
| Configuration | Git (global) | 0 | Real-time |
| Secrets | Multi-region Secrets Manager | Seconds | <1 minute |

### Failover Procedures

1. **Detection**: Automated health checks detect primary region failure.
2. **DNS Failover**: Route53 health check triggers DNS failover to secondary region.
3. **Data Verification**: Verify replicated data consistency in secondary region.
4. **Capacity Scaling**: Scale up secondary region capacity to full production levels.
5. **Traffic Validation**: Monitor traffic flow and error rates post-failover.
6. **Stakeholder Notification**: Notify all stakeholders of the failover event.
7. **Post-Incident**: Conduct post-mortem and update failover procedures.

### Failback Procedures

1. **Primary Region Recovery**: Verify primary region infrastructure is fully operational.
2. **Data Resynchronization**: Reverse replication from secondary to primary.
3. **Validation**: Run comprehensive validation suite against primary region.
4. **Gradual Traffic Shift**: Move 10% → 25% → 50% → 100% of traffic back to primary.
5. **Re-establish Replication**: Resume normal replication from primary to secondary.
6. **Capacity Normalization**: Scale down secondary region to warm standby levels.

## Backup Security

### Encryption

- Encrypt all backups at rest using AES-256 or customer-managed KMS keys.
- Use separate KMS keys for backup encryption vs. production encryption.
- Rotate backup encryption keys annually.
- Verify encryption status of all backups as part of backup verification.

### Access Control

- Restrict backup access to dedicated backup service accounts.
- Implement MFA for all backup deletion operations.
- Enable S3 Object Lock for critical backups (WORM compliance).
- Audit all backup access and deletion via CloudTrail.

### Retention and Compliance

- Implement S3 lifecycle policies for automatic tiering and deletion.
- Maintain backup retention per compliance requirements (GDPR, SOC2, HIPAA).
- Implement data retention policies for user data backup deletion.
- Document all retention policies and obtain compliance team sign-off.
