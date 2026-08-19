# API Key Management

## 1. Overview

API keys provide a simple authentication mechanism for service-to-service communication,
partner integrations, and programmatic access to recommendation system APIs. Unlike JWTs
which carry rich claims, API keys are opaque identifiers mapped to permissions server-side.
This document covers key generation, rotation, scoping, storage, revocation, usage tracking,
and rate limiting for production recommendation systems.

### 1.1 API Key vs JWT

| Aspect | API Key | JWT |
|---|---|---|
| Structure | Opaque string | Structured (header.payload.signature) |
| Claims | None (server-side lookup) | Embedded in token |
| Validation | Database/cache lookup | Cryptographic verification |
| Use case | Service-to-service, partner access | User authentication |
| Lifetime | Long-lived (months-years) | Short-lived (minutes-hours) |
| Revocation | Instant (database lookup) | Blacklist or expiry |

### 1.2 API Key Use Cases

| Use Case | Key Type | Lifetime | Scope |
|---|---|---|---|
| Internal service communication | Service key | 90 days (rotated) | Per-service permissions |
| Partner integration | Partner key | 1 year (rotated) | Limited API access |
| Development/testing | Dev key | 30 days | Non-production environments |
| Batch processing | Batch key | 24 hours | Batch endpoints only |
| Monitoring/health check | Readonly key | Indefinite | Read-only metrics |

---

## 2. Key Generation

### 2.1 Key Format

API keys follow a structured format for easy identification and validation:

```
Prefix environment random_bytes checksum

Example: apikey_demo_xK9mB2nP4qR7sT1vW3yZ5fH8jL0oQ6eU

Where:
- sk        = "secret key" prefix
- _live     = environment (_live, _test, _dev)
- a1b2...   = 32 bytes of cryptographic randomness (hex-encoded)
- q7r8      = 4-byte checksum (CRC32)
```

### 2.2 Key Generation Process

```
1. Generate 32 bytes of cryptographic randomness (CSPRNG)
2. Encode as hexadecimal string (64 characters)
3. Prepend environment prefix
4. Compute and append checksum
5. Hash key with SHA-256 before storage
6. Store key metadata (id, prefix, scopes, creation date)
7. Return plaintext key to user (shown once)
```

### 2.3 Key Properties

| Property | Requirement | Rationale |
|---|---|---|
| Length | 32+ bytes of randomness | Prevent brute-force guessing |
| Uniqueness | Globally unique | No key collisions |
| Format | Prefix + randomness + checksum | Easy identification and validation |
| Entropy | 256 bits | Sufficient for production security |
| Generation | CSPRNG | Cryptographically secure randomness |

### 2.4 Key Format Examples by Provider

| Provider | Format | Example |
|---|---|---|
| Stripe | `sk_live_[64chars]` | `sk_live_a1b2c3d4...` |
| AWS | `AKIA[16chars]` | `AKIAIOSFODNN7EXAMPLE` |
| Google | `[39chars]` | `AIzaSyDExample1234567890` |
| Custom | `rec_[env]_[64chars]` | `rec_prod_a1b2c3d4...` |

---

## 3. Key Rotation

### 3.1 Rotation Strategy

| Strategy | Description | Downtime | Use Case |
|---|---|---|---|
| Graceful rotation | New + old key valid during overlap | Zero | Standard rotation |
| Emergency rotation | Old key immediately invalidated | Possible brief outage | Security incident |
| Automatic rotation | System generates new key periodically | Zero | Internal services |
| Manual rotation | User generates new key, updates systems | Zero (with planning) | Partner keys |

### 3.2 Graceful Rotation Process

```
Phase 1: Pre-rotation (T-7 days)
├── Notify key holders of upcoming rotation
├── Provide new key alongside old key
└── Document migration steps

Phase 2: Dual-key period (T-0 to T+7 days)
├── Generate new key, activate immediately
├── Old key remains valid for 7 days
├── Monitor usage: alert if old key still being used
└── Support both keys simultaneously

Phase 3: Old key deprecation (T+7 days)
├── Deactivate old key
├── Keep old key in database for 30 days (re-activation)
└── Final notification to key holders

Phase 4: Old key deletion (T+37 days)
├── Permanently delete old key from database
└── Archive key metadata for audit purposes
```

### 3.3 Automatic Rotation for Internal Services

- Services generate new key pair every 90 days
- New key registered in API key store automatically
- Old key remains valid for 14-day overlap period
- Services fetch new key from configuration service
- No manual intervention required

### 3.4 Rotation Monitoring

Track rotation compliance:

- **Key age alerting**: Alert when keys exceed maximum age
- **Rotation completion tracking**: Percentage of keys rotated on schedule
- **Usage after deprecation**: Alert if deprecated key is still being used
- **Partner key compliance**: Track partner rotation status

---

## 4. Key Scoping

### 4.1 Per-Service Scoping

Each service gets a key with permissions limited to its required operations:

| Service | Allowed Endpoints | Denied Endpoints |
|---|---|---|
| Recommendation API | GET /recommendations, /items | POST /models, DELETE /users |
| Feature Pipeline | POST /features, GET /features | GET /recommendations |
| Model Training | POST /models, GET /models | GET /recommendations |
| Analytics | GET /metrics, /reports | POST /models, /features |
| Admin | All endpoints | None |

### 4.2 Per-User Scoping

For partner API access, scope keys per user/partner:

| Scope | Description | Example |
|---|---|---|
| `read:recommendations` | Can read recommendations | Partner analytics |
| `read:items` | Can read item catalog | Content aggregator |
| `write:interactions` | Can record interactions | Event tracking service |
| `read:features` | Can read feature values | Feature debugging |
| `admin:*` | Full admin access | System administrators |

### 4.3 Scope Hierarchy

```
Global scopes
├── admin:*            → Full administrative access
├── service:*          → All service operations
├── read:*             → All read operations
├── write:*            → All write operations
└── user:*             → User management operations

Resource-specific scopes
├── recommendations:read    → Read recommendations only
├── recommendations:write   → Modify recommendation config
├── features:read           → Read feature values
├── features:write          → Modify feature pipeline
├── models:read             → Read model metadata
├── models:write            → Deploy/update models
└── analytics:read          → Read metrics and reports
```

### 4.4 Scope Enforcement

- **API Gateway**: Validates key scopes before routing to service
- **Service-level**: Each service validates required scopes for operation
- **Audit logging**: All scope-checked operations are logged
- **Scope violation**: Returns 403 Forbidden with required scope information

---

## 5. Key Storage

### 5.1 Storage Architecture

```
Key Storage Layers:
├── Plaintext key: NEVER stored (shown once at creation)
├── SHA-256 hash: Stored in primary database
├── Key prefix: Stored in index for lookup
├── Key metadata: Stored with hash (scopes, owner, expiry)
└── Revocation status: Stored in fast-lookup cache (Redis)
```

### 5.2 Hashed Key Storage

API keys are stored as SHA-256 hashes, never in plaintext:

| Property | Implementation |
|---|---|
| Hash algorithm | SHA-256 |
| Salting | Key prefix used as salt |
| Lookup | Hash incoming key, compare against stored hash |
| Irreversibility | Cannot recover plaintext from hash |
| Uniqueness | Collision probability negligible with SHA-256 |

### 5.3 Encrypted Key Storage

For keys requiring reversibility (e.g., forwarding to external services):

| Encryption | Use Case | Key Management |
|---|---|---|
| AES-256-GCM | Encrypted key storage | KMS-managed master key |
| Envelope encryption | Key encryption key + data key | Cloud KMS integration |
| HSM-backed | Maximum security requirements | Hardware security module |

### 5.4 Key Storage Security

- **Access control**: Only auth service can access key storage
- **Encryption at rest**: Database encryption enabled
- **Audit logging**: All key access logged
- **No plaintext logs**: Key values never logged (only hashes/prefixes)
- **Backup encryption**: Key backups encrypted separately
- **Separation of duties**: Key storage separated from key usage

---

## 6. Key Revocation

### 6.1 Revocation Methods

| Method | Speed | Scope | Use Case |
|---|---|---|---|
| Immediate invalidation | Instant | Single key | Compromised key |
| Batch revocation | < 1 minute | Multiple keys | Partner compromise |
| Scope reduction | Instant | Single key | Permission change |
| Owner revocation | Instant | All owner keys | User offboarding |

### 6.2 Revocation Flow

```
Revocation Request → Validation → Database Update → Cache Invalidation → Notification
       ↓               ↓              ↓                   ↓                ↓
   Admin/User      Verify         Mark key            Update Redis      Notify key
   request         authority      as revoked          revocation        holder
                                   in database         cache
```

### 6.3 Revocation Propagation

Revocation must propagate quickly across all API gateways:

- **Redis pub/sub**: Broadcast revocation events to all gateway instances
- **Local cache TTL**: Gateway caches revocation decisions for max 10 seconds
- **Consistency guarantee**: Revocation effective within 10 seconds cluster-wide
- **Audit trail**: All revocation events logged with timestamp and actor

---

## 7. Usage Tracking

### 7.1 Key Usage Metrics

Track per-key usage for security and billing:

| Metric | Description | Aggregation |
|---|---|---|
| Request count | Total API requests per key | Per minute/hour/day |
| Endpoint usage | Which endpoints are accessed | Per key per day |
| Error rate | Failed requests per key | Per minute |
| Latency distribution | Request latency per key | Per hour |
| Geographic origin | Where requests originate | Per day |
| Unique IPs | Number of distinct source IPs | Per hour |

### 7.2 Anomaly Detection

Automated detection of suspicious key usage:

| Anomaly | Detection Method | Response |
|---|---|---|
| Volume spike | > 3x normal usage rate | Alert + investigate |
| New geography | Request from unexpected region | Alert + verify |
| Endpoint abuse | Accessing endpoints outside normal pattern | Alert + possible revocation |
| Brute force | Many 401 errors from same key | Alert + possible block |
| Key sharing | Multiple IPs using same key simultaneously | Alert + investigate |

### 7.3 Usage Reporting

- **Real-time dashboard**: Live usage metrics per key
- **Daily summary**: Aggregated usage report per key owner
- **Monthly billing**: Usage-based billing for partner keys
- **Compliance report**: Audit trail of all key operations

---

## 8. Rate Limiting Per Key

### 8.1 Key-Based Rate Limits

Each API key has individual rate limits based on its tier:

| Key Tier | Requests/Second | Requests/Day | Burst Allowance |
|---|---|---|---|
| Internal service | 10,000 | Unlimited | 2x |
| Partner (premium) | 1,000 | 10,000,000 | 2x |
| Partner (standard) | 100 | 1,000,000 | 1.5x |
| Development | 10 | 100,000 | 1x |
| Monitoring | 1 | 10,000 | 1x |

### 8.2 Rate Limit Implementation

```
Request → Extract API Key → Look up Tier → Check Rate Limit → Allow/Deny
                              ↓                ↓
                         Redis lookup     Redis counter
                         (key → tier)     (key:window → count)
```

### 8.3 Rate Limit Headers

Response headers for rate-limited requests:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 742
X-RateLimit-Reset: 1705312800
X-RateLimit-Tier: partner_standard
X-RateLimit-Key-Id: key_a1b2c3d4
```

### 8.4 Rate Limit Overrides

- **Temporary overrides**: Increase limits for special events or partners
- **Emergency throttling**: Reduce all limits during incident
- **Per-endpoint limits**: Different limits for different endpoints
- **Time-based limits**: Different limits for peak vs off-peak hours
