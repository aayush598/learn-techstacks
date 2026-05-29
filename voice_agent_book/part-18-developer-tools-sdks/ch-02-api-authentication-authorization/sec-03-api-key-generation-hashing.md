# Section 03: API Key Generation & Hashing

## Overview

API keys are cryptographically random tokens that identify and authenticate tenants. Keys are generated with sufficient entropy to prevent guessing, prefixed for type identification, and hashed before storage. The system never stores raw keys — only bcrypt or SHA-256 hashes — ensuring that a database breach does not expose valid credentials.

## Architecture

```
API Key Lifecycle
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Key Generation:
  Entropy Source (crypto.randomBytes)
       │
  48 random bytes → base64url → "<PREFIX>_" + key_encoded
       │
  Result: "va_live_[48-char-base64url]" (e.g., "va_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f")

Key Storage:
  Raw Key ──→ bcrypt hash (cost 12) ──→ Stored in database
  Prefix ──→ Stored in plaintext  ──→ For key type routing
  Key ID ──→ Stored as lookup key ──→ "key_abc123"

Key Validation:
  User provides:   "va_live_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f"
                        │
  Parse prefix → "va_live" → lookup algorithm
  Extract key_id from prefix-stored mapping
                        ↓
  Load hash from DB → bcrypt.compare(raw, hash)
                        ↓
  Valid → Tenant + Scopes retrieved

  Constant-time comparison prevents timing attacks.
```

## Design Decisions

- **48 Random Bytes**: 384 bits of entropy — infeasible to guess even with quantum computing advances
- **Prefix Identification**: `va_live_` (production), `va_test_` (sandbox), `va_dev_` (development) — instant environment and key type identification
- **Bcrypt Over SHA-256**: Bcrypt includes salt and is deliberately slow (configurable cost) — slows brute force attacks
- **Key ID for Lookup**: A separate `key_` prefix identifier maps to the stored hash; avoids exposing the hash in error messages

## Implementation Approach

```typescript
import crypto from 'node:crypto';
import bcrypt from 'bcrypt';

// Key configuration
const KEY_CONFIG = {
  production: { prefix: 'va_live_', length: 48, cost: 12 },
  sandbox: { prefix: 'va_test_', length: 48, cost: 10 },
  development: { prefix: 'va_dev_', length: 32, cost: 8 },
} as const;

interface GeneratedApiKey {
  rawKey: string;       // Returned to user once
  keyId: string;        // Lookup identifier
  prefix: string;       // Key type prefix
  hash: string;         // bcrypt hash for storage
  environment: 'production' | 'sandbox' | 'development';
}

class ApiKeyService {
  async generateKey(
    environment: 'production' | 'sandbox' | 'development'
  ): Promise<GeneratedApiKey> {
    const config = KEY_CONFIG[environment];

    // Generate random bytes
    const randomBytes = crypto.randomBytes(config.length);
    const encoded = randomBytes
      .toString('base64url');

    const rawKey = `${config.prefix}${encoded}`;
    const keyId = `key_${crypto.randomBytes(8).toString('hex')}`;

    // Hash with bcrypt
    const hash = await bcrypt.hash(rawKey, config.cost);

    return {
      rawKey,
      keyId,
      prefix: config.prefix,
      hash,
      environment,
    };
  }

  async validateKey(rawKey: string): Promise<KeyValidationResult> {
    // Extract prefix
    const prefix = KEY_CONFIG.production.prefix;
    const testPrefix = KEY_CONFIG.sandbox.prefix;

    let environment: 'production' | 'sandbox';
    if (rawKey.startsWith(KEY_CONFIG.sandbox.prefix)) {
      environment = 'sandbox';
    } else if (rawKey.startsWith(KEY_CONFIG.production.prefix)) {
      environment = 'production';
    } else {
      throw new UnauthorizedError('Invalid API key format');
    }

    // Lookup key record by prefix + partial hash lookup
    // (We store a lookup hash for efficient querying)
    const lookupHash = crypto
      .createHash('sha256')
      .update(rawKey.slice(0, 20))
      .digest('hex');

    const keyRecord = await this.keyRepository.findByLookupHash(lookupHash);

    if (!keyRecord) {
      throw new UnauthorizedError('Invalid API key');
    }

    // Constant-time comparison
    const isValid = await bcrypt.compare(rawKey, keyRecord.hash);

    if (!isValid) {
      throw new UnauthorizedError('Invalid API key');
    }

    return {
      tenantId: keyRecord.tenantId,
      keyId: keyRecord.id,
      scopes: keyRecord.scopes,
      environment,
    };
  }
}

// Display helper — shows only last 4 characters
function maskApiKey(rawKey: string): string {
  const prefix = rawKey.slice(0, rawKey.lastIndexOf('_') + 1);
  const lastFour = rawKey.slice(-4);
  return `${prefix}${'•'.repeat(8)}${lastFour}`;
}
```

## Integration Points

- **Developer Portal**: Key generation UI calls ApiKeyService; raw key displayed once with copy-to-clipboard
- **Audit Logging**: Every key generation and revocation is logged with actor identity and timestamp
- **Key Rotation**: Scheduled job generates new keys for tenants approaching 90-day key age

## Production Considerations

- **Bcrypt Cost Tuning**: Cost 12 adds ~250ms to validation — acceptable for auth flow; cost 10 for sandbox (~50ms)
- **Key Revocation**: Immediate revocation via database flag; cached key validation respects ttl
- **Rate Limit on Auth**: Limit key validation attempts to 10 per second per IP to prevent brute force
- **Breach Response**: In case of hash exposure, all keys are rotated; bcrypt cost ensures window for rotation

## Open-Source Tools

- **bcrypt**: Industry-standard password hashing with configurable cost
- **Node crypto**: CSPRNG for secure random key generation
