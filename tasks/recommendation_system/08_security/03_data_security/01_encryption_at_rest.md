# Data Encryption at Rest for Recommendation Systems

## Overview

Encryption at rest protects recommendation system data — user interaction histories, feature
vectors, trained models, item metadata, and embeddings — when stored on disk, in databases,
or in object storage. This covers disk-level encryption, database encryption, object storage
encryption, key management with HashiCorp Vault, encryption algorithms, key rotation policies,
and HSM integration.

## Encryption Architecture Overview

```
Application Layer (Field-level encryption)
         │
    ┌────▼────┐
    │ Database │  Transparent Data Encryption (TDE)
    │  (Postgres)│  Column-level encryption for PII
    └────┬────┘
         │
    ┌────▼────┐
    │   Disk  │  LUKS / dm-crypt full-disk encryption
    │  Volume │  Encrypted filesystem layer
    └────┬────┘
         │
    ┌────▼────┐
    │   HSM   │  Hardware Security Module
    │ / Vault │  Key management and signing
    └─────────┘
```

## Disk Encryption (LUKS/dm-crypt)

### Full Disk Encryption

LUKS (Linux Unified Key Setup) provides full-disk encryption at the block device level:

- Encrypts entire partitions including swap space
- Transparent to applications — reads and writes are encrypted/decrypted automatically
- Performance overhead: 2-5% for modern CPUs with AES-NI instruction support
- Keys are derived from passphrase or key file stored in HSM/Vault

### LUKS Configuration for ML Workloads

ML workloads involve large temporary files (model checkpoints, intermediate embeddings):

| Partition       | Encryption | Rationale                                    |
|----------------|-----------|-----------------------------------------------|
| OS root        | LUKS      | Protect system configuration and secrets       |
| Data volume    | LUKS      | Protect training data and user interactions    |
| Model storage  | LUKS      | Protect trained model artifacts                |
| Swap space     | LUKS      | Prevent memory dump attacks                    |
| /tmp           | LUKS      | Protect temporary computation artifacts        |
| Scratch SSD    | Optional  | Performance-sensitive, non-sensitive intermediates |

### Performance Considerations

- AES-256-XTS with AES-NI: < 3% throughput reduction on NVMe SSDs
- Test encryption overhead with `fio` benchmark before deployment
- Monitor I/O latency during training to ensure encryption does not cause bottlenecks
- Consider hardware-accelerated encryption for GPU compute nodes

## Database Encryption

### PostgreSQL Transparent Data Encryption (TDE)

PostgreSQL TDE encrypts the entire database storage (WAL, data files, indexes):

**pg_tde Extension (Community)**:
- Encrypts data at the block level within PostgreSQL
- Key management integrated with external KMS
- Transparent to application code — no query changes required
- Supports per-table or per-database encryption

**Column-Level Encryption for PII**:
For sensitive fields like user email, demographic data:

- Use `pgcrypto` extension for application-level column encryption
- Encrypt before INSERT, decrypt after SELECT
- Encrypted columns cannot be indexed directly — use blind indexes (hash columns)
- Separate encryption keys per sensitive column type

### Encryption Scope for Recommendation Data

| Data Type               | Encryption Level | Method                     |
|------------------------|-----------------|----------------------------|
| User interaction logs  | TDE             | Full database encryption   |
| User profiles (PII)    | Column-level    | AES-256-GCM per field     |
| Item metadata          | TDE             | Full database encryption   |
| Feature vectors        | TDE             | Full database encryption   |
| Model weights          | TDE             | Full database encryption   |
| Audit logs             | TDE + column    | Full + field-level         |
| Session data           | TDE             | Full database encryption   |

## Object Storage Encryption (S3/MinIO)

### Server-Side Encryption Options

**SSE-S3 (Amazon S3 managed keys)**:
- AWS manages encryption keys entirely
- AES-256 encryption for all objects
- Simplest option, least control

**SSE-KMS (AWS KMS managed keys)**:
- Customer-managed keys in AWS KMS
- Fine-grained access policies per key
- CloudTrail audit log for every key usage
- Recommended for recommendation system data

**SSE-C (Customer-provided keys)**:
- Customer provides encryption key with each request
- AWS does not store the key
- Maximum control, highest operational complexity

### Object Storage Encryption Strategy

| Data Category          | Encryption Method | Key Management   | Retention    |
|-----------------------|-------------------|------------------|-------------|
| Training datasets     | SSE-KMS           | Dedicated KMS key| 90 days     |
| Model artifacts       | SSE-KMS           | Dedicated KMS key| Until replaced|
| User interaction logs | SSE-KMS           | Dedicated KMS key| 30 days     |
| Feature snapshots     | SSE-KMS           | Dedicated KMS key| 7 days      |
| Embedding caches      | SSE-S3            | AWS managed      | 24 hours    |
| Backup data           | SSE-KMS           | Dedicated KMS key| 1 year      |

### Client-Side Encryption

For maximum security, encrypt data before uploading to object storage:

1. Generate data encryption key (DEK) per object
2. Encrypt object with DEK using AES-256-GCM
3. Encrypt DEK with master key (KEK) from Vault/KMS
4. Store encrypted DEK alongside encrypted object
5. To decrypt: retrieve encrypted DEK, unwrap with KEK, decrypt object

## Key Management with HashiCorp Vault

### Vault Architecture for Recommendation Systems

```
Vault Server (HA mode, 3+ nodes)
├── Transit Engine (encryption as a service)
│   ├── rec-master-key       (AES-256-GCM)
│   ├── rec-pii-key          (AES-256-GCM, auto-rotate 30 days)
│   └── rec-model-key        (AES-256-GCM, manual rotation)
├── KV Engine (secrets storage)
│   ├── database/creds/rec-db (dynamic DB credentials)
│   ├── api-keys/             (third-party API keys)
│   └── tls/                  (certificate management)
├── PKI Engine (certificate authority)
│   ├── internal-ca          (service-to-service mTLS)
│   └── external-ca          (public TLS certificates)
└── Auth Methods
    ├── Kubernetes (service account auth)
    ├── AppRole (CI/CD pipeline auth)
    └── OIDC (human user auth)
```

### Transit Engine Usage

Vault's Transit engine provides encryption as a service without storing encrypted data in Vault:

- Application sends plaintext to Vault, receives ciphertext
- Vault never stores the data — only manages the keys
- Supports AES-256-GCM, RSA, ECDSA, and Ed25519
- Automatic key rotation with versioned keys
- Batching support for high-throughput encryption operations

### Dynamic Database Credentials

Vault can generate short-lived database credentials:

- Each recommendation service instance gets unique credentials
- Credentials automatically expire after configured TTL (e.g., 1 hour)
- No static database passwords in configuration files
- Automatic credential rotation without service restart

## Encryption Algorithms

### Algorithm Selection

| Algorithm       | Use Case                    | Key Size | Performance     |
|----------------|----------------------------|----------|-----------------|
| AES-256-GCM    | General data encryption     | 256-bit  | Fast (AES-NI)   |
| AES-256-XTS    | Full disk encryption        | 256-bit  | Fast (AES-NI)   |
| RSA-4096       | Key wrapping, signatures    | 4096-bit | Slow for bulk   |
| ChaCha20-Poly1305 | High-throughput stream  | 256-bit  | Fast (no AES-NI)|
| Ed25519        | Token signatures            | 256-bit  | Fast            |

### AES-256-GCM Recommended Configuration

- **Authentication**: Always use authenticated encryption (GCM mode)
- **IV/Nonce**: 96-bit random nonce, never reuse with same key
- **Tag length**: 128-bit authentication tag
- **AAD**: Include context (user_id, tenant_id) as additional authenticated data

### Key Hierarchy

```
Master Key (KEK) — stored in HSM/Vault, never exported
    │
    ├── Data Encryption Key (DEK) — per-database or per-storage
    │       └── Used to encrypt/decrypt actual data
    │
    ├── Model Encryption Key (MEK) — per-model-artifact
    │       └── Used to encrypt model weights and embeddings
    │
    └── Token Signing Key (TSK) — for JWT signing
            └── Used to sign and verify API tokens
```

## Key Rotation

### Rotation Schedule

| Key Type               | Rotation Period | Downtime Required | Method                  |
|------------------------|----------------|-------------------|-------------------------|
| Database encryption key | 90 days       | No                | Re-encrypt with new key |
| Object storage key     | 90 days        | No                | AWS re-encryption job   |
| JWT signing key        | 90 days        | No                | Dual-key publishing     |
| API secrets            | 180 days       | Rolling restart   | Secret versioning       |
| TLS certificates       | 90 days        | No                | Auto-renewal (certbot)  |

### Zero-Downtime Key Rotation Process

1. Add new key version to Vault transit engine (both old and new active)
2. Start re-encryption job reading with old key, writing with new key
3. Update application to encrypt new data with new key
4. Verify all data re-encrypted by attempting decryption with old key
5. Disable old key version after grace period

## HSM Integration

### Hardware Security Module Benefits

- Keys never leave the HSM hardware boundary
- Tamper-resistant and tamper-evident hardware
- FIPS 140-2 Level 3 certification for compliance
- High-performance cryptographic operations
- Physical access controls and audit logging

### HSM Integration Architecture

```
Application → Vault Server → HSM (PKCS#11 interface)
                 │
                 ├── Key generation (inside HSM)
                 ├── Signing operations (inside HSM)
                 ├── Decryption operations (inside HSM)
                 └── Key attestation (HSM-signed proof)
```

### Cloud HSM Options

| Provider     | Service          | Certification | Integration        |
|-------------|-----------------|---------------|--------------------|
| AWS         | CloudHSM        | FIPS 140-2 L3 | PKCS#11, JCE      |
| Azure       | Dedicated HSM   | FIPS 140-2 L3 | PKCS#11, JCE      |
| GCP         | Cloud HSM       | FIPS 140-2 L3 | PKCS#11            |
| HashiCorp   | Vault + CloudHSM| FIPS 140-2 L3 | Native integration |

## Compliance and Audit

### Encryption Audit Requirements

- Log all key access events (who, when, what operation)
- Track encryption/decryption operation counts per key
- Monitor key age and rotation compliance
- Alert on unauthorized key access attempts
- Maintain encryption inventory (what data is encrypted with what key)

### Regulatory Requirements

| Regulation | Encryption Requirement                              |
|-----------|-----------------------------------------------------|
| GDPR      | Encryption recommended for personal data protection |
| HIPAA     | Encryption required for PHI at rest and in transit  |
| PCI DSS   | AES-256 required for cardholder data                |
| SOC 2     | Encryption at rest and in transit demonstrated      |
| CCPA      | Encryption as reasonable security measure           |
