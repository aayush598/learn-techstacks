# Invitation Token Design

## Overview

Invitation tokens enable secure, time-limited user onboarding. Each token encodes the intended role, team, and expiration, and is cryptographically signed to prevent tampering. One-time use enforcement prevents replay attacks.

## Token Structure

```typescript
interface InvitationPayload {
  email: string;
  tenantId: string;
  roleId: string;
  teamId?: string;
  departmentId?: string;
  permissions?: string[];
  expiresAt: Date;
  maxUses: number;
  invitedBy: string;
  metadata?: Record<string, unknown>;
}

interface InvitationToken {
  id: string;
  token: string;           // Signed JWT or random string
  hash: string;            // SHA-256 of token for lookup
  payload: InvitationPayload;
  usedCount: number;
  maxUses: number;
  expiresAt: Date;
  revokedAt?: Date;
  createdAt: Date;
}
```

## Generation

```typescript
class InvitationTokenService {
  async generateToken(payload: InvitationPayload): Promise<string> {
    const tokenBytes = randomBytes(32);
    const rawToken = tokenBytes.toString('hex');
    const tokenHash = createHash('sha256').update(rawToken).digest('hex');

    const token = await this.db.insert('invitation_tokens', {
      id: generateId('invite'),
      token: tokenHash,
      payload,
      usedCount: 0,
      maxUses: payload.maxUses,
      expiresAt: payload.expiresAt,
      createdAt: new Date(),
    });

    // Return signed token for URL
    return this.signToken(rawToken);
  }

  private signToken(rawToken: string): string {
    const hmac = createHmac('sha256', process.env.INVITE_SECRET!);
    hmac.update(rawToken);
    const signature = hmac.digest('hex');
    return `${rawToken}.${signature}`;
  }

  async validateToken(signedToken: string): Promise<InvitationPayload | null> {
    const [rawToken, signature] = signedToken.split('.');

    // Verify signature
    const expectedSig = createHmac('sha256', process.env.INVITE_SECRET!)
      .update(rawToken)
      .digest('hex');

    if (!timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSig))) {
      return null;
    }

    // Look up token
    const tokenHash = createHash('sha256').update(rawToken).digest('hex');
    const stored = await this.db.findOne('invitation_tokens', { token: tokenHash });

    if (!stored) return null;
    if (stored.revokedAt) return null;
    if (stored.expiresAt < new Date()) return null;
    if (stored.usedCount >= stored.maxUses) return null;

    return stored.payload;
  }
}
```

## One-Time Use & Expiry

```typescript
async function consumeToken(tokenId: string): Promise<void> {
  await this.db.update('invitation_tokens', { id: tokenId }, {
    $inc: { usedCount: 1 },
    lastUsedAt: new Date(),
  });
}

// Cleanup expired tokens
async function cleanupExpiredTokens(): Promise<number> {
  const result = await this.db.delete('invitation_tokens', {
    expiresAt: { $lt: new Date() },
    usedCount: { $eq: 0 },
  });
  return result.deletedCount;
}
```

## Open-Source Tools

- **jsonwebtoken** (MIT) — JWT-based invitation tokens
- **nanoid** (MIT) — Secure random ID generation
- **bcrypt** (MIT) — Token hashing

## Production Considerations

- Default token expiry: 7 days; configurable per tenant (1-30 days)
- Max 3 uses per token (for resend scenarios)
- Store only hashed tokens in database
- Rate-limit token generation: max 10 per minute per admin user
- Log all token validation attempts for audit
- Support token revocation from admin panel
