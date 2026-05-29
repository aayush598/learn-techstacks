# Section 05: Authentication & Session Security

## Session Architecture

User authentication uses **Auth.js** with database sessions, secure cookies, and session rotation. Brute force protection, account lockout, and MFA provide additional security layers.

```
┌─────────────────────────────────────────────────────────────────────┐
│               AUTHENTICATION & SESSION FLOW                         │
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌────────────┐   │
│  │  Browser │    │  Auth.js │    │ Database │    │   Redis    │   │
│  │          │    │          │    │          │    │            │   │
│  │──Login───→    │          │    │          │    │            │   │
│  │  (email/pw)   │──Verify──→    │          │    │            │   │
│  │               │←──User───    │          │    │            │   │
│  │               │              │          │    │            │   │
│  │               │──Create──→   │          │    │            │   │
│  │               │  Session     │          │    │            │   │
│  │               │─────────────── Session ──→  │            │   │
│  │               │              │    Token  │    │            │   │
│  │←Set Cookie───  │              │          │    │            │   │
│  │  (httpOnly,    │              │          │    │            │   │
│  │   sameSite)    │              │          │    │            │   │
│  │               │              │          │    │            │   │
│  │──API Call───→  │──Validate───→ │          │──Check──→     │   │
│  │  (cookie)      │  Middleware   │          │    │            │   │
│  │               │←──User───    │          │    │            │   │
│  │←Response───   │              │          │    │            │   │
│  └──────────┘    └──────────┘    └──────────┘    └────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Secure Cookie Configuration

```typescript
interface SessionConfig {
  cookieName: string;
  cookieOptions: {
    httpOnly: true;          // Not accessible via JavaScript
    secure: true;            // HTTPS only
    sameSite: 'lax';         // CSRF protection
    path: '/';
    maxAge: 60 * 60 * 24;    // 24 hours
    domain?: string;         // Set in production
  };
  sessionTTL: 60 * 60 * 24;               // 24 hours session
  refreshTokenTTL: 60 * 60 * 24 * 7;      // 7 days refresh
  rotationInterval: 60 * 60;              // Rotate session every hour
}

// Session token format
// Session tokens are opaque, high-entropy random strings
function generateSessionToken(): string {
  return crypto.randomBytes(64).toString('hex');
  // Example: "a7f3c9e8b1d2..."
}

// Hashed before storage (SHA-256)
async function hashSessionToken(token: string): Promise<string> {
  return crypto.createHash('sha256').update(token).digest('hex');
}
```

## Session Rotation

```typescript
class SessionManager {
  constructor(
    private db: PrismaClient,
    private redis: RedisClient
  ) {}

  async createSession(userId: string, tenantId: string): Promise<string> {
    const token = generateSessionToken();
    const hashedToken = await hashSessionToken(token);

    // Store session with expiry
    await this.db.session.create({
      data: {
        token: hashedToken,
        userId,
        tenantId,
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000),
        createdAt: new Date(),
      },
    });

    // Cache in Redis for fast lookup
    await this.redis.set(
      `session:${hashedToken}`,
      JSON.stringify({ userId, tenantId }),
      { EX: 24 * 60 * 60 }
    );

    return token;
  }

  async rotateSession(oldToken: string): Promise<string | null> {
    const hashedOld = await hashSessionToken(oldToken);
    const session = await this.db.session.findUnique({
      where: { token: hashedOld },
    });

    if (!session || session.expiresAt < new Date()) {
      return null;
    }

    // Delete old session
    await this.db.session.delete({ where: { id: session.id } });
    await this.redis.del(`session:${hashedOld}`);

    // Create new session (token rotation invalidates stolen tokens)
    return this.createSession(session.userId, session.tenantId);
  }

  async validateSession(token: string): Promise<SessionPayload | null> {
    const hashedToken = await hashSessionToken(token);

    // Check Redis cache first
    const cached = await this.redis.get(`session:${hashedToken}`);
    if (cached) {
      return JSON.parse(cached);
    }

    // Fallback to database
    const session = await this.db.session.findUnique({
      where: { token: hashedToken },
    });

    if (!session || session.expiresAt < new Date()) {
      return null;
    }

    return { userId: session.userId, tenantId: session.tenantId };
  }
}
```

## Brute Force Protection

```typescript
class BruteForceProtection {
  private readonly MAX_ATTEMPTS = 5;
  private readonly LOCKOUT_DURATION = 15 * 60 * 1000; // 15 minutes
  private readonly WINDOW_DURATION = 60 * 60 * 1000;  // 1 hour sliding window

  async recordFailedAttempt(identifier: string): Promise<void> {
    const attempts = await this.redis.incr(`auth:attempts:${identifier}`);

    if (attempts === 1) {
      await this.redis.expire(`auth:attempts:${identifier}`, this.WINDOW_DURATION / 1000);
    }

    if (attempts >= this.MAX_ATTEMPTS) {
      await this.redis.set(
        `auth:lockout:${identifier}`,
        '1',
        { EX: this.LOCKOUT_DURATION / 1000 }
      );

      // Alert security team on repeated lockouts
      const lockoutCount = await this.redis.incr(`auth:lockout_count:${identifier}`);
      if (lockoutCount >= 3) {
        await alertService.sendAlert({
          severity: 'high',
          title: 'Brute force attack detected',
          description: `Account ${identifier} locked out ${lockoutCount} times`,
        });
      }
    }

    return { attempts, remaining: Math.max(0, this.MAX_ATTEMPTS - attempts) };
  }

  async isLocked(identifier: string): Promise<boolean> {
    const locked = await this.redis.get(`auth:lockout:${identifier}`);
    return locked === '1';
  }

  async clearAttempts(identifier: string): Promise<void> {
    await this.redis.del(`auth:attempts:${identifier}`);
    await this.redis.del(`auth:lockout:${identifier}`);
  }
}
```

## Account Lockout

```typescript
// Progressive lockout durations
const LOCKOUT_DURATIONS = [15, 30, 60, 120, 240]; // minutes

async function getLockoutDuration(identifier: string): Promise<number> {
  const count = await getLockoutCount(identifier);
  const index = Math.min(count, LOCKOUT_DURATIONS.length - 1);
  return LOCKOUT_DURATIONS[index] * 60 * 1000;
}

// Self-service unlock via email verification
async function sendUnlockEmail(email: string): Promise<void> {
  const token = generateSessionToken();
  await redis.set(`unlock:token:${token}`, email, { EX: 60 * 30 }); // 30 min
  await emailService.send({
    to: email,
    subject: 'Account Unlock Request',
    body: `Click to unlock: https://app.voiceagent.dev/auth/unlock?token=${token}`,
  });
}
```

## Multi-Factor Authentication

```typescript
// TOTP-based MFA
import { authenticator } from 'otplib';

class MfaService {
  async generateSecret(userId: string): Promise<{ secret: string; qrCodeUrl: string }> {
    const secret = authenticator.generateSecret();
    const serviceName = 'VoiceAgent';

    // Store encrypted secret
    await this.vault.write(`secret/mfa/${userId}`, {
      secret: await encryptSecret(secret),
      enabled: false,
    });

    const qrCodeUrl = authenticator.keyuri(userId, serviceName, secret);
    return { secret, qrCodeUrl };
  }

  async verifyToken(userId: string, token: string): Promise<boolean> {
    const { secret } = await this.vault.read(`secret/mfa/${userId}`);
    return authenticator.verify({ token, secret });
  }

  async enable(userId: string, token: string): Promise<boolean> {
    const valid = await this.verifyToken(userId, token);
    if (valid) {
      await this.vault.write(`secret/mfa/${userId}`, { enabled: true });
    }
    return valid;
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Session storage | Database + Redis cache | Durable + fast lookup; cache bust on DB change |
| Session token | Opaque random string (not JWT) | Revocable, no payload exposure, no signature issues |
| Session rotation | Every hour + on privilege escalation | Limits stolen session window |
| Brute force | Sliding window + progressive lockout | Fair lockout, adaptive to attack patterns |
| MFA | TOTP (standard authenticator apps) | No SMS costs, works offline, widely supported |

## Integration Points

- **Ch 10 (API Security)** — Session validation in API middleware
- **Ch 07 (API Gateway)** — Auth middleware uses session manager
- **Ch 10 (Incident Response)** — Account compromise detection
- **Ch 03 (Database)** — Session table with TTL-based cleanup

## Production Considerations

- **Session Cleanup**: Background job deletes expired sessions every hour
- **Rate Limit on Login**: 5 attempts per minute per IP + per user
- **Concurrent Sessions**: Max 5 concurrent sessions per user; oldest session revoked
- **MFA Recovery**: 8 backup codes generated on MFA enable; stored encrypted in Vault
- **Password Policy**: Minimum 12 characters, zxcvbn strength check, no common passwords
