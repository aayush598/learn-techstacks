# Section 07: HIPAA-Compliant Backup & Disaster Recovery

Backup and disaster recovery for HIPAA environments must ensure ePHI is recoverable and protected at all stages. Backups are encrypted, tested regularly, and stored in secure geo-redundant locations. Disaster recovery plans are documented, tested annually, and include procedures for protecting ePHI during recovery.

Backup requirements: encrypted at rest (AES-256), encrypted in transit (TLS), stored in a geographically separate facility, regular testing (quarterly restore tests), and retention policy (6-year minimum for HIPAA). Backup verification: SHA-256 checksums automatically verified after backup completion. Corrupted backups are detected and reported immediately.

Disaster recovery: HIPAA-specific DR plan includes: prioritized recovery of ePHI systems (RTO: 4 hours, RPO: 15 minutes for critical systems), communication plan for notifying covered entities during extended outages, alternate processing arrangements (standby environment with latest backup), and post-recovery PHI integrity verification. Annual DR tests include HIPAA-specific scenarios.
