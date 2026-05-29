# Section 05: Backup Strategy & Verification

The backup strategy covers all data stores with appropriate frequency, retention, and verification. Backups are encrypted, stored in separate geographic regions, and tested regularly. The strategy follows the 3-2-1 rule: at least 3 copies of data, on 2 different media types, with 1 copy offsite.

Backup schedule: continuous WAL archiving (every 5 minutes), full database backup (daily, with weekly/monthly/yearly retention), object storage replication (continuous cross-region replication of recordings), configuration backups (after every change, versioned in Git), and application state backups (Redis snapshot every 6 hours). Retention: daily backups 30 days, weekly 3 months, monthly 1 year, yearly 7 years.

Backup verification: automated integrity checks after each backup (checksum verification, restore test to isolated environment). Quarterly full restore test: restore entire production environment from backups to a test environment, run smoke tests, verify data integrity, and document results. Failed restore tests are treated as critical incidents. Backup monitoring: success/failure metrics, age of latest backup, and storage usage trends.
