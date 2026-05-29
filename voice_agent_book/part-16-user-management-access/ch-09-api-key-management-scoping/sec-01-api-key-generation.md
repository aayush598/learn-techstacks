# API Key Generation

## Overview

Secure API key generation produces cryptographically random keys with a structured format that includes prefixes for identification. Keys are hashed before storage and never stored in plaintext.

## Key Format

```
va_live_EXAMPLE_KEY_FOR_DOCS_ONLY
├── Prefix ─┘    ├── Tenant ──┘   ├── Secret (60+ bits entropy)
```

## Implementation

```typescript
interface GeneratedApiKey {
  key: string;       // Full key returned to user (shown once)
  hash: string;      // SHA-256 hash for storage
  prefix: string;    // First few chars for identification
}

class ApiKeyGenerator {
  generate(tenantId: string, environment: 'live' | 'test' = 'live'): GeneratedApiKey {
    const env = environment === 'live' ? 'live' : 'test';
    const tenantPrefix = tenantId.slice(0, 8);
    const keyPrefix = `va_${env}_${tenantPrefix}_`;

    const secret = randomBytes(32).toString('hex');
    const key = keyPrefix + secret;
    const hash = createHash('sha256').update(key).digest('hex');

    return { key, hash, prefix: key.slice(0, 12) + '...' };
  }

  validateKeyFormat(key: string): boolean {
    return /^va_(live|test)_[a-z0-9]{8}_[a-f0-9]{64}$/.test(key);
  }

  hashKey(key: string): string {
    return createHash('sha256').update(key).digest('hex');
  }
}
```

## Storage

```typescript
interface StoredApiKey {
  id: string;
  name: string;
  hash: string;
  prefix: string;
  tenantId: string;
  userId: string;
  environment: 'live' | 'test';
  scopes: string[];
  expiresAt?: Date;
  lastUsedAt?: Date;
  createdAt: Date;
  revokedAt?: Date;
  metadata?: Record<string, unknown>;
}
```

## Open-Source Tools

- **nanoid** (MIT) — Secure random ID generation
- **uuid** (MIT) — UUID v4 for key identifiers

## Production Considerations

- Minimum 256 bits of entropy for secret portion
- Show full key only once at creation
- Store only SHA-256 hash, never plaintext
- Support key prefix for database lookups (partial match)
- Rate-limit key generation: max 10 per user per hour
- Validate key format before hashing to prevent storage errors
