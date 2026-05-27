# Key Revocation Flow

## Overview

Key revocation immediately invalidates an API key, preventing further use. The flow handles cached key invalidation, in-flight request handling, and user notification.

## Revocation Service

```typescript
class ApiKeyRevocationService {
  async revokeKey(keyId: string, reason: string, revokedBy: string): Promise<void> {
    const key = await this.apiKeyStore.findById(keyId);
    if (!key || key.revokedAt) return;

    // Mark as revoked in database
    await this.db.update('api_keys', { id: keyId }, {
      revokedAt: new Date(),
      revokeReason: reason,
      revokedBy,
    });

    // Invalidate cache immediately
    await this.redis.del(`apikey:${key.hash}`);

    // Add to revocation list for cached middlewares
    await this.redis.sadd('revoked_keys', key.hash);
    await this.redis.pexpire('revoked_keys', 300000); // 5 min cleanup

    await this.auditLog.record({
      action: 'api_key.revoked',
      actor: revokedBy,
      target: { keyId },
      changes: { before: { status: 'active' }, after: { status: 'revoked' } },
      metadata: { reason, keyName: key.name },
    });

    // Notify key owner
    if (key.userId) {
      await this.notificationService.notify({
        type: 'api_key_revoked',
        userId: key.userId,
        data: { keyName: key.name, reason, revokedAt: new Date() },
      });
    }
  }

  async isKeyRevoked(keyHash: string): Promise<boolean> {
    // Check cache first
    const inRevokedList = await this.redis.sismember('revoked_keys', keyHash);
    if (inRevokedList) return true;

    // Check database
    const key = await this.db.findOne('api_keys', { hash: keyHash });
    return key?.revokedAt != null;
  }

  async handleInFlightRequests(keyId: string): Promise<void> {
    // Allow in-flight requests to complete (max 30 seconds)
    await this.redis.setex(`revoking:${keyId}`, 30, '1');
    await new Promise(resolve => setTimeout(resolve, 30000));
    await this.redis.del(`revoking:${keyId}`);
  }
}
```

## Cache Invalidation

```typescript
// API key cache middleware
async function cacheApiKey(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader?.startsWith('Bearer ')) return next();

  const key = authHeader.slice(7);
  const hash = createHash('sha256').update(key).digest('hex');

  // Check revocation list
  const isRevoked = await revocationService.isKeyRevoked(hash);
  if (isRevoked) {
    return res.status(401).json({ error: 'API key revoked' });
  }

  // Cache valid key for 5 minutes
  const cached = await redis.get(`apikey:${hash}`);
  if (cached) {
    req.apiKey = JSON.parse(cached);
    return next();
  }

  next();
}
```

## Open-Source Tools

- **ioredis** (MIT) — Cache invalidation

## Production Considerations

- Revocation takes effect immediately (sub-millisecond via Redis)
- In-flight requests complete with old key (30-second grace)
- Send revocation notification via email and in-app
- Allow bulk revocation of all keys for a user
- Provide revocation reason options (compromised, no longer needed, rotation)
- Never reuse revoked key names/prefixes
- Maintain revoked key hash list for audit purposes
