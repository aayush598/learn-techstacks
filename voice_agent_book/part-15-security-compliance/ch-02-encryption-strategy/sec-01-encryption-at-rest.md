# Section 01: Encryption at Rest (AES-256)

Encryption at rest protects stored data from unauthorized access if physical storage media is compromised. The platform encrypts all sensitive data at the database, file storage, and backup levels using AES-256 in GCM mode. Encryption keys are managed separately from the data they protect using a key management service (KMS).

Database encryption: PostgreSQL tablespace encryption (pg_tde or pgcrypto extension), column-level encryption for PII fields (email, phone, SSN using pgcrypto with AES-256), and Transparent Data Encryption (TDE) for full database files at rest. File storage encryption: S3 server-side encryption (SSE-S3 or SSE-KMS) for recordings and exports, with tenant-specific KMS keys for enterprise tier.

Backup encryption: all database backups are encrypted before leaving the server using GPG with AES-256. Backup encryption keys are stored in KMS with separate access control from production keys. Encryption is verified on restore. Key rotation is automated (quarterly for production keys, annually for backup keys).
