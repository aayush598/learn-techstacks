# Key Rotation & Expiry

## Overview

Key rotation replaces existing API keys with new ones on a schedule or on-demand. Dual-key overlap allows seamless rotation without downtime. Expiry policies enforce key lifetime limits.

## Rotation Service

```typescript
interface KeyRotationPolicy {
  tenantId: string;
  maxKeyAge: number;           // Max days before rotation required
  gracePeriodDays: number;     // Old key remains valid after rotation
  notifyBeforeDays: number;    // Days before expiry to notify
  autoRotate: boolean;         // Auto-rotate keys at expiry
}

class KeyRotationService {
  async rotateKey(keyId: string, rotatedBy: string): Promise<KeyRotationResult> {
    const existingKey = await this.apiKeyStore.findById(keyId);
    if (!existingKey) throw new Error('Key not found');

    // Generate new key
    const newKey = await this.apiKeyStore.create({
      ...existingKey,
      id: generateId('key'),
      createdAt: new Date(),
      expiresAt: new Date(Date.now() + 90 * 86400000),
      rotatedFrom: keyId,
    });

    // Keep old key valid for grace period
    const policy = await this.getRotationPolicy(existingKey.tenantId);
    if (policy.gracePeriodDays > 0) {
      await this.apiKeyStore.updateExpiry(keyId,
        new Date(Date.now() + policy.gracePeriodDays * 86400000)
      );
    }

    await this.auditLog.record({
      action: 'api_key.rotated',
      actor: rotatedBy,
      target: { keyId },
      changes: { before: { keyId }, after: { newKeyId: newKey.id } },
    });

    return { newKey, oldKeyExpiry: existingKey.expiresAt, gracePeriodDays: policy.gracePeriodDays };
  }

  async findExpiredKeys(): Promise<StoredApiKey[]> {
    return this.db.find('api_keys', {
      expiresAt: { $lt: new Date() },
      revokedAt: null,
    });
  }
}
```

## Open-Source Tools

- **node-cron** (MIT) — Rotation scheduler
- **BullMQ** (MIT) — Rotation notification queue

## Production Considerations

- Default key expiry: 90 days (configurable: 30-365)
- Grace period: 7 days default (both old and new key work)
- Notify key owner at 14, 7, and 1 day before expiry
- Auto-rotate option creates new key and sends to webhook
- Keys older than max age cannot be used even if not expired
- Allow manual rotation with one-click in developer dashboard
- Log all rotation events for compliance audit
