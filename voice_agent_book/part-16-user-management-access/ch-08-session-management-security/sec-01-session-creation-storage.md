# Session Creation & Storage

## Overview

Sessions maintain authentication state across HTTP requests. This section covers session token generation, server-side vs client-side storage strategies, Redis-backed session stores, and the session data model.

## Session Token Generation

```typescript
interface Session {
  id: string;
  userId: string;
  tenantId: string;
  token: string;             // Hashed session token
  refreshToken?: string;     // Hashed refresh token
  createdAt: Date;
  lastActivity: Date;
  expiresAt: Date;
  ipAddress: string;
  userAgent: string;
  deviceFingerprint?: string;
  mfaVerified: boolean;
  mfaVerifiedAt?: Date;
  metadata: Record<string, unknown>;
}

function generateSessionToken(): { raw: string; hash: string } {
  const raw = randomBytes(48).toString('hex');
  const hash = createHash('sha256').update(raw).digest('hex');
  return { raw, hash };
}
```

## Session Storage

```typescript
class SessionStore {
  private redis: Redis;

  constructor() {
    this.redis = new Redis({
      host: process.env.REDIS_HOST,
      enableAutoPipelining: true,
    });
  }

  async create(session: Session): Promise<void> {
    const key = `session:${session.token}`;
    await this.redis.setex(key, this.getTtl(session.expiresAt), JSON.stringify(session));

    // Indexes for lookup
    await this.redis.sadd(`user_sessions:${session.userId}`, session.id);
    await this.redis.setex(`session_id:${session.id}`, this.getTtl(session.expiresAt), session.token);
  }

  async findByToken(token: string): Promise<Session | null> {
    const hash = createHash('sha256').update(token).digest('hex');
    const key = `session:${hash}`;
    const data = await this.redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  async findById(sessionId: string): Promise<Session | null> {
    const tokenKey = await this.redis.get(`session_id:${sessionId}`);
    if (!tokenKey) return null;
    return this.findByToken(tokenKey);
  }

  async updateActivity(sessionId: string): Promise<void> {
    const session = await this.findById(sessionId);
    if (!session) return;

    session.lastActivity = new Date();

    // Extend TTL if sliding expiry
    const key = `session:${session.token}`;
    await this.redis.setex(key, this.getTtl(session.expiresAt), JSON.stringify(session));
  }

  async delete(sessionId: string): Promise<void> {
    const session = await this.findById(sessionId);
    if (!session) return;

    await this.redis.del(`session:${session.token}`);
    await this.redis.del(`session_id:${session.id}`);
    await this.redis.srem(`user_sessions:${session.userId}`, session.id);
  }

  async deleteAllForUser(userId: string): Promise<number> {
    const sessionIds = await this.redis.smembers(`user_sessions:${userId}`);
    await Promise.all(sessionIds.map(id => this.delete(id)));
    return sessionIds.length;
  }

  private getTtl(expiresAt: Date): number {
    return Math.max(1, Math.floor((expiresAt.getTime() - Date.now()) / 1000));
  }
}
```

## Session Cookie Configuration

```typescript
const SESSION_COOKIE_CONFIG = {
  httpOnly: true,
  secure: true,
  sameSite: 'lax' as const,
  path: '/',
  maxAge: 7 * 24 * 60 * 60, // 7 days in seconds
};
```

## Open-Source Tools

- **ioredis** (MIT) — Redis client with session store
- **express-session** (MIT) — Session middleware (with Redis store)
- **iron-session** (MIT) — Encrypted cookie sessions

## Production Considerations

- Use Redis Cluster for distributed session storage across regions
- Set session ID length to at least 128 bits of entropy
- Hash session tokens before storing (never store raw tokens)
- Implement session ID rotation on privilege escalation
- Monitor session store memory usage; set Redis maxmemory-policy to allkeys-lru
- Backup session data to database for disaster recovery
