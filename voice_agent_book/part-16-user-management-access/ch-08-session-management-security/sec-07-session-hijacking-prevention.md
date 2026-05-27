# Session Hijacking Prevention

## Overview

Session hijacking occurs when an attacker steals a valid session token. Prevention combines secure cookie attributes, token binding to device/network characteristics, and active session monitoring.

## Secure Cookie Configuration

```typescript
const SECURE_COOKIE_OPTIONS = {
  httpOnly: true,           // Not accessible via JavaScript
  secure: true,             // HTTPS only
  sameSite: 'strict',       // Prevent CSRF via cross-site requests
  path: '/',
  maxAge: 7 * 86400,        // 7 days
  domain: '.voiceagent.com', // Subdomain scope
};

// Additional protection: __Host- prefix for path-bound cookies
// Set-Cookie: __Host-session=token; Path=/; Secure; HttpOnly; SameSite=Strict
```

## Token Binding

```typescript
class TokenBindingService {
  async bindTokenToDevice(session: Session, fingerprint: DeviceFingerprint): Promise<void> {
    const bindingTag = createHash('sha256')
      .update(`${session.token}:${fingerprint.hash}`)
      .digest('hex')
      .slice(0, 16);

    await this.sessionStore.updateMetadata(session.id, { bindingTag, deviceFingerprint: fingerprint.hash });
  }

  async validateBinding(session: Session, fingerprintHash: string): Promise<boolean> {
    if (!session.metadata?.bindingTag) return true; // Legacy session, no binding
    if (!session.metadata?.deviceFingerprint) return true;

    return session.metadata.deviceFingerprint === fingerprintHash;
  }

  async bindToIp(session: Session, ip: string): Promise<void> {
    await this.sessionStore.updateMetadata(session.id, {
      boundIp: ip,
      ipBoundAt: new Date(),
    });
  }

  async validateIpBinding(session: Session, currentIp: string): Promise<boolean> {
    if (!session.metadata?.boundIp) return true;

    const ipChanged = session.metadata.boundIp !== currentIp;
    if (ipChanged) {
      const timeSinceBind = (Date.now() - new Date(session.metadata.ipBoundAt).getTime()) / 3600000;
      if (timeSinceBind < 1) {
        // IP changed within an hour of binding - suspicious
        return false;
      }
    }

    return true;
  }
}
```

## CSRF Protection

```typescript
// Double Submit Cookie pattern
function csrfMiddleware(req: Request, res: Response, next: NextFunction) {
  const csrfCookie = req.cookies['csrf-token'];
  const csrfHeader = req.headers['x-csrf-token'];

  if (req.method !== 'GET' && req.method !== 'HEAD' && req.method !== 'OPTIONS') {
    if (!csrfCookie || !csrfHeader || csrfCookie !== csrfHeader) {
      return res.status(403).json({ error: 'CSRF validation failed' });
    }
  }

  next();
}
```

## Session Monitoring

```typescript
class SessionHijackMonitor {
  async detectHijack(session: Session, request: Request): Promise<HijackIndicator> {
    const indicators: string[] = [];

    // IP address change (without VPN/proxy)
    if (session.ipAddress !== request.ip) {
      indicators.push('ip_changed');
    }

    // User agent change
    if (session.userAgent !== request.headers['user-agent']) {
      indicators.push('user_agent_changed');
    }

    // Geographic distance
    if (session.ipAddress) {
      const distance = this.calculateDistance(session.ipAddress, request.ip);
      if (distance > 100) {
        indicators.push(`geographic_distance:${distance}km`);
      }
    }

    if (indicators.length > 0) {
      await this.flagSession(session.id, indicators);
    }

    return {
      suspicious: indicators.length >= 2, // 2+ indicators = likely hijack
      indicators,
      severity: indicators.length >= 3 ? 'critical' : indicators.length >= 2 ? 'high' : 'low',
    };
  }

  private async flagSession(sessionId: string, indicators: string[]): Promise<void> {
    await this.db.insert('session_flags', {
      sessionId,
      indicators,
      flaggedAt: new Date(),
      action: indicators.length >= 3 ? 'revoke' : 'monitor',
    });

    if (indicators.length >= 3) {
      await this.sessionService.revokeSession(
        sessionId, 'hijack_detected', 'system'
      );
    }
  }
}
```

## Open-Source Tools

- **helmet** (MIT) — Express security headers middleware
- **csrf-csrf** (MIT) — CSRF token generation and validation
- **express-rate-limit** (MIT) — Rate limiting on session validation failures

## Production Considerations

- Rotate session token on privilege escalation (login, MFA verification)
- Set session cookie `maxAge` to match session expiry
- Use `__Host-` prefix for cookies to prevent subdomain overwrite
- Monitor session validation failures as security metric
- Implement session token rotation every 24 hours for long-lived sessions
- Alert on 3+ hijack indicators within 5 minutes
- Provide user ability to view and terminate all active sessions
