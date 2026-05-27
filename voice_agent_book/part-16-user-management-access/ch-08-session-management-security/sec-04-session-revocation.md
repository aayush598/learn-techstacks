# Session Revocation

## Overview

Session revocation terminates active sessions immediately. Revocation can be admin-initiated (for security incidents), user-initiated (logout all devices), or triggered by security events (role change, password change).

## Revocation Types

```typescript
type RevocationReason =
  | 'user_logout'
  | 'admin_revoke'
  | 'password_changed'
  | 'role_changed'
  | 'account_disabled'
  | 'security_incident'
  | 'device_lost'
  | 'suspicious_activity'
  | 'session_expired';

interface SessionRevocation {
  sessionId: string;
  userId: string;
  reason: RevocationReason;
  initiatedBy: string;
  initiatedAt: Date;
  metadata?: Record<string, unknown>;
}
```

## Revocation Service

```typescript
class SessionRevocationService {
  async revokeSession(sessionId: string, reason: RevocationReason, initiatedBy: string): Promise<void> {
    const session = await this.sessionStore.findById(sessionId);
    if (!session) return;

    await this.sessionStore.delete(sessionId);

    await this.auditLog.record({
      action: 'session.revoked',
      actor: initiatedBy,
      target: { sessionId, userId: session.userId },
      changes: { before: { active: true }, after: { active: false } },
      metadata: { reason },
    });

    if (reason === 'security_incident') {
      await this.notificationService.notify({
        type: 'session_revoked_security',
        userId: session.userId,
        data: { reason, deviceInfo: session.userAgent, ip: session.ipAddress },
      });
    }
  }

  async revokeAllUserSessions(userId: string, reason: RevocationReason, initiatedBy: string): Promise<number> {
    const sessions = await this.sessionStore.getUserSessions(userId);
    let count = 0;

    for (const session of sessions) {
      await this.revokeSession(session.id, reason, initiatedBy);
      count++;
    }

    return count;
  }

  async revokeByUserIds(userIds: string[], reason: RevocationReason, initiatedBy: string): Promise<number> {
    let total = 0;
    for (const userId of userIds) {
      total += await this.revokeAllUserSessions(userId, reason, initiatedBy);
    }
    return total;
  }

  async handlePasswordChange(userId: string): Promise<void> {
    // Revoke all sessions except current one
    const currentSessionId = await this.getCurrentSessionId();
    const sessions = await this.sessionStore.getUserSessions(userId);

    for (const session of sessions) {
      if (session.id !== currentSessionId) {
        await this.revokeSession(session.id, 'password_changed', userId);
      }
    }
  }

  async handleRoleChange(userId: string, oldRole: string, newRole: string): Promise<void> {
    const sessions = await this.sessionStore.getUserSessions(userId);

    // Revoke sessions when user loses admin/manager role
    const isDemotion = isHigherRole(oldRole, newRole);
    if (isDemotion) {
      for (const session of sessions) {
        await this.revokeSession(session.id, 'role_changed', 'system');
      }
    }
  }

  async getActiveSessions(userId: string): Promise<Session[]> {
    const sessions = await this.sessionStore.getUserSessions(userId);
    return sessions.filter(s => s.expiresAt > new Date());
  }

  async countActiveSessions(userId: string): Promise<number> {
    return (await this.getActiveSessions(userId)).length;
  }
}
```

## Immediate Invalidation

```typescript
// Invalidate cached sessions in middleware
async function sessionRevocationMiddleware(req: Request, res: Response, next: NextFunction) {
  const token = req.cookies.session_token || req.headers.authorization?.split(' ')[1];
  if (!token) return next();

  const session = await sessionStore.findByToken(token);
  if (!session) {
    res.clearCookie('session_token');
    return res.status(401).json({ error: 'Session revoked' });
  }

  req.session = session;
  next();
}
```

## Open-Source Tools

- **ioredis** (MIT) — Immediate key deletion for session invalidation
- **BullMQ** (MIT) — Queue for bulk session revocation

## Production Considerations

- Cache session blacklist in Redis for immediate revocation enforcement
- Maximum 5-minute delay for session revocation propagation in distributed systems
- Provide admin "revoke all sessions for user" with confirmation dialog
- Send email notification for security-triggered revocations
- Allow partial revocation (selective sessions) from user settings
- Maintain revoked session ID list for 2x session TTL to prevent reuse
- Audit log all revocations with IP, reason, and admin identity
