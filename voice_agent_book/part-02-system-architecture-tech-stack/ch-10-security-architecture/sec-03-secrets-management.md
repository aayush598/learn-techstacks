# Section 03: Secrets Management

## Vault Architecture

All secrets — database credentials, API keys, TLS certificates, encryption keys — are stored in **HashiCorp Vault** with automatic rotation, audit logging, and dynamic secrets where possible. Secrets never exist in code, environment files, or configuration repositories.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SECRETS MANAGEMENT ARCHITECTURE                  │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    HASHICORP VAULT                          │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  Secret Engines                                       │   │   │
│  │  │                                                       │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐                  │   │   │
│  │  │  │  KV v2       │  │  Database    │   Static/dynamic │   │   │
│  │  │  │  (Static     │  │  (Dynamic    │   PG creds       │   │   │
│  │  │  │   Secrets)   │  │   Secrets)   │                  │   │   │
│  │  │  └──────────────┘  └──────────────┘                  │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐                  │   │   │
│  │  │  │  PKI         │  │  Transit     │   Encryption    │   │   │
│  │  │  │  (TLS Certs) │  │  (Encryption │   as a service   │   │   │
│  │  │  │              │  │   as Service)│                  │   │   │
│  │  │  └──────────────┘  └──────────────┘                  │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  Access Methods                                       │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │   │   │
│  │  │  │ Kubernetes   │  │  JWT/OIDC    │  │  Token     │  │   │   │
│  │  │  │ Auth         │  │  (Human)     │  │  (CI/CD)   │  │   │   │
│  │  │  └──────────────┘  └──────────────┘  └────────────┘  │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  Audit Log (all operations logged to ClickHouse)     │   │   │
│  │  │  • Who accessed what secret, when, from which IP    │   │   │
│  │  │  • Rotation events, lease creation, revocation      │   │   │
│  │  │  • Alerts on: root token usage, unauthorized access │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Integration: External Secrets Operator (Kubernetes)        │   │
│  │                                                              │   │
│  │  Vault ──→ ExternalSecrets Operator ──→ K8s Secret        │   │
│  │                                          ↓                  │   │
│  │                                     Pod mounts as           │   │
│  │                                     volume or env var       │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Dynamic Database Credentials

```typescript
// Vault database engine — generates short-lived PostgreSQL credentials
// Each service gets unique, time-limited credentials

interface DatabaseCredentials {
  username: string;  // v-token-call-svc-6h3k2a
  password: string;  // Auto-generated, 24-char
  ttl: number;       // 3600 seconds (1 hour)
}

async function getDatabaseCredentials(serviceName: string): Promise<DatabaseCredentials> {
  // Vault generates a new PG user with role-based permissions
  const result = await vault.write(`database/creds/${serviceName}-role`, {
    ttl: '1h',
  });

  return {
    username: result.data.username,
    password: result.data.password,
    ttl: result.data.ttl,
  };
}

// Database roles per service
// call-service-role: SELECT, INSERT, UPDATE on call_* tables
// billing-service-role: SELECT, INSERT, UPDATE on billing_* tables
// readonly-service-role: SELECT on all tables (analytics)
```

## Secret Structure

```typescript
// Vault secret paths follow a consistent naming convention
interface VaultPath {
  path: string;
  type: 'kv' | 'database' | 'pki' | 'transit';
  description: string;
  rotationPeriod: string; // How often the secret is rotated
}

const VAULT_SECRETS: VaultPath[] = [
  // Environment-level secrets
  { path: 'secret/production/database/url', type: 'database', description: 'PostgreSQL connection string', rotationPeriod: '1h' },
  { path: 'secret/production/redis/url', type: 'kv', description: 'Redis connection string', rotationPeriod: '24h' },
  { path: 'secret/production/kafka/brokers', type: 'kv', description: 'Kafka broker list', rotationPeriod: '24h' },

  // Third-party API keys
  { path: 'secret/production/api/openai/key', type: 'kv', description: 'OpenAI API key', rotationPeriod: '90d' },
  { path: 'secret/production/api/twilio/sid', type: 'kv', description: 'Twilio Account SID', rotationPeriod: '90d' },
  { path: 'secret/production/api/twilio/auth-token', type: 'kv', description: 'Twilio Auth Token', rotationPeriod: '90d' },
  { path: 'secret/production/api/stripe/key', type: 'kv', description: 'Stripe Secret Key', rotationPeriod: '90d' },

  // Encryption keys
  { path: 'transit/production/keys/call-records', type: 'transit', description: 'Encryption key for call recordings', rotationPeriod: '180d' },
  { path: 'transit/production/keys/pii', type: 'transit', description: 'Encryption key for PII data', rotationPeriod: '180d' },

  // TLS certificates (auto-renewed)
  { path: 'pki/production/issue/api-gateway', type: 'pki', description: 'API Gateway TLS cert', rotationPeriod: '24h' },
];
```

## External Secrets Operator

```yaml
# Kubernetes ExternalSecret resource
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: call-service-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: call-service-secrets  # K8s Secret name
    creationPolicy: Owner
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: secret/production/database/url
    - secretKey: REDIS_URL
      remoteRef:
        key: secret/production/redis/url
    - secretKey: OPENAI_API_KEY
      remoteRef:
        key: secret/production/api/openai/key
```

## Secret Rotation

```typescript
// Automated secret rotation
class SecretRotator {
  private readonly ROTATION_CHECKS = {
    'database': 60 * 60 * 1000,          // 1 hour
    'api-keys': 24 * 60 * 60 * 1000,     // 24 hours
    'encryption-keys': 180 * 24 * 60 * 60 * 1000, // 180 days
  };

  async rotateDatabaseCredentials(serviceName: string): Promise<void> {
    // Vault automatically rotates dynamic DB creds on lease expiry
    // No manual rotation needed for dynamic secrets
    console.log(`Database credentials for ${serviceName} rotated automatically by Vault`);
  }

  async rotateAPIKey(secretPath: string): Promise<void> {
    const oldKey = await vault.read(secretPath);

    // Generate new key via the provider's API
    const newKey = await apiProvider.rotateKey(oldKey.data.key_id);

    // Write new key to Vault
    await vault.write(secretPath, { key: newKey, rotated_at: new Date().toISOString() });

    // Keep old key valid for 24h for zero-downtime rotation
    await vault.write(`${secretPath}-previous`, {
      key: oldKey.data.key,
      expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
    });
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Secrets management | HashiCorp Vault | Industry standard, dynamic secrets, audit logging |
| Kubernetes integration | External Secrets Operator | Native K8s integration, auto-sync |
| Database credentials | Dynamic (Vault-generated) | Time-limited, per-service, no shared credentials |
| API key rotation | 90-day cycle with 24h overlap | Zero-downtime rotation with key overlap |
| Encryption keys | Vault Transit Engine | Keys never leave Vault; data encrypted/decrypted via API |

## Integration Points

- **Ch 10 (Zero-Trust)** — Service identity tied to Vault-issued certificates
- **Ch 10 (Container Security)** — Secrets mounted as volumes, not env vars
- **Ch 08 (DevOps)** — Terraform provisions Vault and configures secret engines
- **Ch 10 (Incident Response)** — Secret leak triggers emergency rotation

## Production Considerations

- **Vault HA**: 3-node Vault cluster with Raft storage backend; auto-unseal via KMS
- **Secret Caching**: Services cache secrets in-memory with 5-minute TTL to reduce Vault load
- **Disaster Recovery**: Vault snapshots to MinIO every hour; cross-region replication
- **Root Token**: Stored in offline HSM; used only for initial setup and disaster recovery
- **Audit Compliance**: All secret access logged to read-only audit sink; monthly review
