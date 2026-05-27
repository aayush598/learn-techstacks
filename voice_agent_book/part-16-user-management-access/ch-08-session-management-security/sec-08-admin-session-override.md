# Admin Session Override

## Overview

Admin session override allows authorized support or admin staff to temporarily access a user's account for troubleshooting, with a complete audit trail and user notification. This supports support access and compliance requirements.

## Override Model

```typescript
interface SessionOverride {
  id: string;
  adminUserId: string;
  targetUserId: string;
  reason: string;
  supportTicketId?: string;
  status: 'active' | 'completed' | 'revoked';
  permissions: OverridePermission[];
  startedAt: Date;
  expiresAt: Date;
  lastActivity: Date;
  auditTrail: OverrideAction[];
  sessionToken?: string;      // Temporary override token
}

interface OverridePermission {
  resource: string;
  actions: string[];
  readOnly: boolean;          // Read-only mode by default
}

interface OverrideAction {
  timestamp: Date;
  action: string;
  resource: string;
  details: string;
}
```

## Override Service

```typescript
class AdminOverrideService {
  async createOverride(
    adminUserId: string,
    targetUserId: string,
    reason: string,
    durationMinutes: number = 30
  ): Promise<SessionOverride> {
    // Validate admin has override permission
    const admin = await this.userService.getUser(adminUserId);
    if (!admin?.roles.includes('admin') && !admin?.permissions.includes('session:override')) {
      throw new Error('Insufficient permissions for session override');
    }

    const originalAdminSession = await this.sessionStore.getCurrentSession(adminUserId);

    const override: SessionOverride = {
      id: generateId('override'),
      adminUserId,
      targetUserId,
      reason,
      supportTicketId: null,
      status: 'active',
      permissions: [{ resource: '*', actions: ['read'], readOnly: true }],
      startedAt: new Date(),
      expiresAt: new Date(Date.now() + durationMinutes * 60000),
      lastActivity: new Date(),
      auditTrail: [],
    };

    await this.db.insert('session_overrides', override);

    // Create temporary override session
    const token = generateSessionToken();
    await this.sessionStore.create({
      id: `override_${override.id}`,
      userId: targetUserId,
      tenantId: admin.tenantId,
      token: token.hash,
      createdAt: new Date(),
      lastActivity: new Date(),
      expiresAt: override.expiresAt,
      ipAddress: originalAdminSession?.ipAddress || '',
      userAgent: originalAdminSession?.userAgent || '',
      mfaVerified: true,
      metadata: { isOverride: true, originalAdminId: adminUserId, overrideId: override.id },
    });

    // Notify target user
    await this.notificationService.notify({
      type: 'session_override_started',
      userId: targetUserId,
      data: { reason, adminName: admin.name, expiresAt: override.expiresAt },
    });

    return { ...override, sessionToken: token.raw };
  }

  async recordAction(overrideId: string, action: string, resource: string, details: string): Promise<void> {
    const override = await this.db.findOne('session_overrides', { id: overrideId });
    if (!override || override.status !== 'active') return;

    override.auditTrail.push({
      timestamp: new Date(),
      action,
      resource,
      details,
    });
    override.lastActivity = new Date();

    await this.db.update('session_overrides', { id: overrideId }, override);

    // If sensitive action, notify user
    if (this.isSensitiveAction(action, resource)) {
      await this.notificationService.notify({
        type: 'session_override_action',
        userId: override.targetUserId,
        data: { action, resource, details, adminId: override.adminUserId },
      });
    }
  }

  async terminateOverride(overrideId: string): Promise<void> {
    const override = await this.db.findOne('session_overrides', { id: overrideId });
    if (!override) return;

    override.status = 'completed';
    await this.db.update('session_overrides', { id: overrideId }, override);

    // Revoke override session
    await this.sessionStore.delete(`override_${overrideId}`);

    // Notify user
    await this.notificationService.notify({
      type: 'session_override_ended',
      userId: override.targetUserId,
      data: { duration: Math.round((Date.now() - override.startedAt.getTime()) / 60000) },
    });
  }

  private isSensitiveAction(action: string, resource: string): boolean {
    const sensitive = ['billing', 'api_keys', 'users', 'security_settings', 'delete'];
    return sensitive.some(s => action.includes(s) || resource.includes(s));
  }

  async getOverrideHistory(targetUserId: string): Promise<SessionOverride[]> {
    return this.db.find('session_overrides', { targetUserId })
      .sort({ startedAt: -1 })
      .limit(50);
  }
}
```

## User Notification

```
Security Alert
┌──────────────────────────────────────────────────┐
│  Admin Access to Your Account                     │
│                                                   │
│  Admin: Alice (alice@company.com)                  │
│  Reason: Investigating call quality issue          │
│  Started: Today, 2:30 PM                          │
│  Expires: Today, 3:00 PM                          │
│  Actions: Read-only mode                          │
│                                                   │
│  If you didn't request this, contact support       │
│  or [Terminate Access Immediately]                │
└──────────────────────────────────────────────────┘
```

## Audit Trail

```
Admin Override Audit (Ticket #TKT-4521)
Date: 2025-06-15
Admin: Alice Johnson (alice@company.com)
Target: Bob Smith (bob@company.com)
Reason: Investigating call quality complaint
Duration: 22 minutes

Actions:
  10:30:00  Override started
  10:30:15  Viewed agent configuration
  10:31:20  Viewed call history (last 5 calls)
  10:35:40  Reviewed call recording (call_789)
  10:42:10  Viewed transcript (call_789)
  10:50:00  Viewed billing settings (SENSITIVE)
  10:52:00  Override ended
```

## Open-Source Tools

- **ioredis** (MIT) — Temporary override session storage
- **BullMQ** (MIT) — Auto-expiry job for override timeout

## Production Considerations

- Override duration limited to 15-60 minutes, auto-expire
- Default to read-only; write access requires explicit privilege
- Record every action during override with full audit trail
- Notify user via email and in-app immediately on override start
- Allow user to terminate override from their security settings
- Max 3 concurrent overrides per admin
- All override actions logged to immutable audit store
- Require MFA for admin initiating override
