# Section 08: SSO Security and Compliance

## Overview

SSO Security and Compliance encompasses the security controls, compliance certifications, and operational practices that protect the SSO integration and ensure it meets enterprise security requirements. Enterprise customers require that the platform's SSO implementation adheres to security best practices, supports compliance frameworks (SOC 2, ISO 27001, HIPAA, FedRAMP), and provides audit trails for all authentication events.

The security framework covers: secure token handling (JWT and SAML assertion validation), session management (timeout, refresh, revocation), cryptographic key management (certificate rotation, JWKS handling), audit logging (authentication events, mapping changes, provisioning operations), and compliance reporting (access reviews, user inventory reports, session activity logs). The framework also addresses emerging security requirements: phishing-resistant authentication (FIDO2/WebAuthn via IdP), token binding, and continuous access evaluation.

## Architecture

```
               SSO Security & Compliance

   IdP → Platform → Security Controls → Audit → Compliance
              |               |
   +----------------------------------------------------------+
   |           SSO Security & Compliance Framework           |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Token Security   |  | Session Security  |            |
   |  | • JWT validation |  | • Short-lived     |            |
   |  | • SAML assertion |  |   sessions (1h)   |            |
   |  |   verification   |  | • Refresh rotation |            |
   |  | • Replay protect |  | • Idle timeout     |            |
   |  | • Nonce/state    |  | • Concurrent limit |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Key Management   |  | Audit Logging     |            |
   |  | • Certificate    |  | • Auth events     |            |
   |  |   rotation       |  | • Provisioning    |            |
   |  | • JWKS caching   |  | • Mapping changes |            |
   |  | • HSM/KMS        |  | • Admin actions   |            |
   |  |   integration    |  +-------------------+            |
   |  +------------------+                                    |
   |  +------------------+  +-------------------+            |
   |  | Compliance       |  | Incident Response |             |
   |  | • SOC 2 controls |  | • Compromised     |            |
   |  | • Access reviews |  |   credential      |            |
   |  | • User inventory |  | • Suspicious      |            |
   |  | • Data retention |  |   activity        |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Session token (opaque) with short TTL and refresh rotation over long-lived JWT:** Instead of issuing long-lived JWTs (which cannot be revoked server-side without a blocklist), the platform issues an opaque session token (random string) with a 1-hour TTL. The token is stored server-side with the session metadata. Refresh tokens rotate on each use (old refresh token is invalidated when a new one is issued). This provides immediate session revocation (delete the server-side session record) without blocklist management. Trade-off: opaque tokens require a server-side lookup on each request but provide immediate revocation and no JWT blocklist complexity.

- **Layered validation with defense in depth over single-point validation:** Token/assertion validation is performed at multiple layers: (1) edge/API gateway validates token format and expiry, (2) SSO service validates IdP-specific signature and claims, (3) application layer validates permissions and scopes. Each layer provides progressively more detailed validation. If a token passes layer 1 but fails layer 2, the failure is logged and the request rejected. Trade-off: layered validation adds latency per request but provides defense in depth against token validation bypass.

- **Compliance automation via scheduled reports over manual evidence gathering:** The compliance framework automatically generates reports required for SOC 2, ISO 27001, and customer compliance questionnaires: user access inventory (all users and their roles), authentication activity (login events, failures, locations), SSO configuration changes (who changed what mapping when), and session activity (active sessions, idle time, concurrent sessions). Reports are generated on a configurable schedule and stored for the designated retention period. Trade-off: automated compliance reporting adds storage and processing overhead but eliminates manual evidence gathering for audits.

## Implementation Approach

```
interface SSOSecurityConfig {
  session: {
    ttlMs: number;
    idleTimeoutMs: number;
    refreshRotation: boolean;
    maxConcurrentSessions: number;
  };
  tokenValidation: {
    allowedSigningAlgorithms: string[];
    clockSkewMs: number;
    jwksCacheTTLMs: number;
    requireSignedAssertion: boolean;
    requireEncryptedAssertion: boolean;
  };
  compliance: {
    auditRetentionDays: number;
    accessReviewSchedule: 'weekly' | 'monthly' | 'quarterly';
    userInventoryEnabled: boolean;
    anomalyDetectionEnabled: boolean;
  };
}

class SSOSecurityService {
  private sessions = new Map<string, UserSession>();
  private auditLogger: AuditLogger;
  private anomalyDetector: AnomalyDetector;

  async createSession(userId: string, tenantId: string, params: {
    authMethod: string;
    idpUserId: string;
    metadata?: Record<string, any>;
  }): Promise<SessionResult> {
    const config = await this.getSecurityConfig(tenantId);

    // Enforce concurrent session limit
    const activeSessions = await this.countActiveSessions(userId);
    if (activeSessions >= config.session.maxConcurrentSessions) {
      // Revoke oldest session
      const oldest = await this.getOldestSession(userId);
      if (oldest) await this.revokeSession(oldest.id, 'Concurrent session limit reached');
    }

    const sessionId = crypto.randomUUID();
    const session: UserSession = {
      id: sessionId,
      userId,
      tenantId,
      authMethod: params.authMethod,
      idpUserId: params.idpUserId,
      createdAt: new Date(),
      expiresAt: new Date(Date.now() + config.session.ttlMs),
      lastActivityAt: new Date(),
      metadata: params.metadata || {},
      refreshToken: crypto.randomUUID(),
    };

    await this.db.sessions.insert(session);
    this.sessions.set(sessionId, session);

    await this.auditLogger.log({
      event: 'session.created',
      userId,
      tenantId,
      details: { authMethod: params.authMethod },
    });

    return {
      sessionToken: sessionId,
      refreshToken: session.refreshToken,
      expiresAt: session.expiresAt,
    };
  }

  async validateSession(sessionToken: string): Promise<UserSession | null> {
    const config = await this.getSecurityConfig();
    const session = this.sessions.get(sessionToken) || await this.db.sessions.findOne({ id: sessionToken });

    if (!session) return null;

    // Check expiry
    if (session.expiresAt < new Date()) {
      await this.revokeSession(session.id, 'Session expired');
      return null;
    }

    // Check idle timeout
    if (config.session.idleTimeoutMs > 0) {
      const idleTime = Date.now() - session.lastActivityAt.getTime();
      if (idleTime > config.session.idleTimeoutMs) {
        await this.revokeSession(session.id, 'Idle timeout');
        return null;
      }
    }

    // Check if revoked
    if (session.revoked) return null;

    // Update last activity (throttled to reduce writes)
    if (Date.now() - session.lastActivityAt.getTime() > 60000) {
      session.lastActivityAt = new Date();
      await this.db.sessions.update(session.id, { lastActivityAt: session.lastActivityAt });
    }

    return session;
  }

  async refreshSession(refreshToken: string): Promise<SessionResult | null> {
    const session = await this.db.sessions.findOne({ refreshToken });
    if (!session || session.revoked) return null;

    const config = await this.getSecurityConfig();

    if (config.session.refreshRotation) {
      // Invalidate old refresh token, issue new one
      session.refreshToken = crypto.randomUUID();
    }

    session.expiresAt = new Date(Date.now() + config.session.ttlMs);
    session.lastActivityAt = new Date();
    await this.db.sessions.update(session.id, {
      refreshToken: session.refreshToken,
      expiresAt: session.expiresAt,
      lastActivityAt: session.lastActivityAt,
    });

    this.sessions.set(session.id, session);

    return {
      sessionToken: session.id,
      refreshToken: session.refreshToken,
      expiresAt: session.expiresAt,
    };
  }

  async revokeSession(sessionId: string, reason: string): Promise<void> {
    const session = this.sessions.get(sessionId) || await this.db.sessions.findOne({ id: sessionId });
    if (!session) return;

    session.revoked = true;
    session.revokedAt = new Date();
    session.revokeReason = reason;

    await this.db.sessions.update(sessionId, { revoked: true, revokedAt: session.revokedAt, revokeReason: reason });
    this.sessions.delete(sessionId);

    await this.auditLogger.log({
      event: 'session.revoked',
      userId: session.userId,
      tenantId: session.tenantId,
      details: { reason, sessionId },
    });
  }

  async revokeAllUserSessions(userId: string, reason: string): Promise<number> {
    const sessions = await this.db.sessions.find({ userId, revoked: false });
    let count = 0;
    for (const session of sessions) {
      await this.revokeSession(session.id, reason);
      count++;
    }
    return count;
  }

  // Compliance reports
  async generateUserAccessReport(tenantId: string): Promise<ComplianceReport> {
    const users = await this.userService.listUsers(tenantId);
    const report: ComplianceReport = {
      generatedAt: new Date(),
      tenantId,
      totalUsers: users.length,
      activeUsers: users.filter(u => u.active).length,
      usersByRole: {} as Record<string, number>,
      usersByAuthMethod: {} as Record<string, number>,
      recentlyActive: 0,
    };

    for (const user of users) {
      report.usersByRole[user.role] = (report.usersByRole[user.role] || 0) + 1;
      report.usersByAuthMethod[user.authMethod || 'password'] = (report.usersByAuthMethod[user.authMethod || 'password'] || 0) + 1;

      const lastSession = await this.db.sessions.findOne({ userId: user.id, revoked: false }, { sort: { lastActivityAt: -1 } });
      if (lastSession && lastSession.lastActivityAt > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)) {
        report.recentlyActive++;
      }
    }

    return report;
  }

  async runSecurityScan(): Promise<SecurityScanResult> {
    const issues: SecurityIssue[] = [];

    // Check certificate expiry
    const certs = await this.getActiveCertificates();
    for (const cert of certs) {
      const daysUntilExpiry = (cert.expiresAt.getTime() - Date.now()) / (1000 * 60 * 60 * 24);
      if (daysUntilExpiry < 30) {
        issues.push({ severity: 'high', component: 'certificate', message: `Certificate ${cert.name} expires in ${Math.floor(daysUntilExpiry)} days` });
      }
    }

    // Check for stale sessions
    const staleConfigs = await this.db.samlConfigs.find({ lastUsed: { $lt: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000) } });
    for (const stale of staleConfigs) {
      issues.push({ severity: 'low', component: 'saml_config', message: `SAML config ${stale.id} not used in 90 days` });
    }

    // Check mapping conflicts
    const mappings = await this.db.rbacMappings.find({});
    const seenRoles = new Map<string, string[]>();
    for (const mapping of mappings) {
      for (const m of mapping.target) {  // Note: simplified
        const key = `${m.role}:${JSON.stringify(m.constraints)}`;
        if (!seenRoles.has(key)) seenRoles.set(key, []);
        seenRoles.get(key)!.push(mapping.id);
      }
    }
    for (const [key, ids] of seenRoles) {
      if (ids.length > 1) {
        issues.push({
          severity: 'medium', component: 'rbac',
          message: `Duplicate role mapping found for ${key}: ${ids.join(', ')}`,
        });
      }
    }

    return { issues, scannedAt: new Date() };
  }
}

// Security compliance configuration defaults
const DEFAULT_SECURITY_CONFIG: SSOSecurityConfig = {
  session: {
    ttlMs: 3600000,               // 1 hour
    idleTimeoutMs: 1800000,        // 30 minutes
    refreshRotation: true,
    maxConcurrentSessions: 5,
  },
  tokenValidation: {
    allowedSigningAlgorithms: ['RS256', 'RS384', 'RS512'],
    clockSkewMs: 300000,           // 5 minutes
    jwksCacheTTLMs: 3600000,       // 1 hour
    requireSignedAssertion: true,
    requireEncryptedAssertion: false,
  },
  compliance: {
    auditRetentionDays: 365,
    accessReviewSchedule: 'monthly',
    userInventoryEnabled: true,
    anomalyDetectionEnabled: true,
  },
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Helmet (MIT) | Node.js | HTTP security headers |
| express-rate-limit (MIT) | Node.js | Rate limiting auth endpoints |
| express-session (MIT) | Node.js | Session middleware |

## Production Considerations

**Scaling:** Session store must be shared across all application instances — use Redis with persistence for session data. Session validation happens on every authenticated request — optimize by caching session lookups in a local in-memory cache (1-minute TTL). Refresh token rotation creates database writes proportional to session refresh rate (typically every 30-60 minutes per active user). Session revocation events must propagate quickly — use a pub/sub mechanism (Redis Pub/Sub) to broadcast revocation events to all instances.

**Security:** Implement rate limiting on authentication endpoints (5 failed attempts per minute per IP). Use HTTP-only, Secure, SameSite=Strict cookies for session tokens. Never expose session tokens in URLs or logs. Implement anomaly detection: alert on logins from unusual geographic locations, multiple failed authentication attempts from the same user, logins from unusual user agents, and concurrent sessions from geographically distant locations.

**Monitoring:** Track authentication success/failure rates (by IdP, by user), session creation/expiry/revocation rates, refresh token rotation count, active sessions per user, session idle time distribution, and compliance report generation status. Alert on authentication failure spikes (possible brute force attack), session revocation events (admin-initiated or automatic), certificate expiry (30, 14, 7, and 1 day before), and compliance report generation failures.
