# Session Expiry & Refresh

## Overview

Session expiry controls how long a session remains valid. Two models exist: absolute expiry (fixed lifetime) and sliding expiry (extended on activity). Idle timeout detects abandoned sessions, and forced re-auth protects sensitive actions.

## Expiry Configuration

```typescript
interface SessionExpiryConfig {
  absoluteMaxAge: number;        // Max session lifetime in seconds
  slidingExpiryEnabled: boolean;
  slidingWindow: number;         // Extend by this many seconds on activity
  idleTimeout: number;           // Max idle time before requiring re-auth
  sensitiveActionTimeout: number; // Max time since last MFA for sensitive ops
}

const DEFAULT_SESSION_EXPIRY: SessionExpiryConfig = {
  absoluteMaxAge: 7 * 86400,      // 7 days
  slidingExpiryEnabled: true,
  slidingWindow: 86400,           // Extend by 24h on activity
  idleTimeout: 3600,              // 1 hour idle timeout
  sensitiveActionTimeout: 900,    // 15 minutes for sensitive actions
};
```

## Expiry Service

```typescript
class SessionExpiryService {
  async validateSession(session: Session): Promise<SessionValidation> {
    const now = Date.now();

    // Absolute expiry check
    if (session.expiresAt.getTime() <= now) {
      await this.sessionStore.delete(session.id);
      return { valid: false, reason: 'session_expired' };
    }

    // Idle timeout check
    if (this.isIdleTimeoutExceeded(session, config.idleTimeout)) {
      await this.sessionStore.delete(session.id);
      return { valid: false, reason: 'idle_timeout' };
    }

    // Sliding expiry extension
    if (config.slidingExpiryEnabled) {
      const newExpiry = new Date(Math.min(
        now + config.slidingWindow * 1000,
        session.createdAt.getTime() + config.absoluteMaxAge * 1000
      ));
      session.expiresAt = newExpiry;
      await this.sessionStore.updateActivity(session.id);
    }

    return { valid: true, session };
  }

  async handleSensitiveAction(userId: string): Promise<boolean> {
    const session = await this.sessionStore.getCurrentSession(userId);
    if (!session) return false;

    const timeSinceMfa = session.mfaVerifiedAt
      ? (Date.now() - session.mfaVerifiedAt.getTime()) / 1000
      : Infinity;

    if (timeSinceMfa > config.sensitiveActionTimeout) {
      // Require step-up authentication
      return false;
    }

    return true;
  }

  async extendSession(sessionId: string, extensionSeconds: number): Promise<void> {
    const session = await this.sessionStore.findById(sessionId);
    if (!session) throw new Error('Session not found');

    const newExpiry = new Date(Math.min(
      session.expiresAt.getTime() + extensionSeconds * 1000,
      session.createdAt.getTime() + config.absoluteMaxAge * 1000
    ));

    session.expiresAt = newExpiry;
    await this.sessionStore.update(session);
  }
}
```

## Open-Source Tools

- **express-session** (MIT) — Session expiry middleware
- **ioredis** (MIT) — Redis TTL for automatic expiry

## Production Considerations

- Absolute max session: 7 days (configurable per tenant: 1-30 days)
- Sliding window: extend by session maxAge/4 on each request
- Idle timeout: 1 hour default, 15 minutes for sensitive data access
- Notify user 5 minutes before session expires
- Store session creation time to enforce absolute expiry
- Force re-auth for billing, API key management, security settings
