# Admin Audit Trail

## Overview

The admin audit trail records all configuration changes and sensitive operations performed by administrators. This is critical for compliance (SOC 2, SOX, HIPAA) and provides accountability for admin actions.

## Admin Actions Tracked

```typescript
const ADMIN_AUDITED_ACTIONS = [
  'user.created', 'user.deleted', 'user.suspended',
  'role.created', 'role.modified', 'role.deleted',
  'role.assigned', 'role.unassigned',
  'permission.granted', 'permission.revoked',
  'api_key.created', 'api_key.revoked', 'api_key.rotated',
  'billing.plan_changed', 'billing.invoice_voided',
  'settings.modified', 'security.settings_changed',
  'team.created', 'team.merged', 'team.deleted',
  'sso.config_changed', 'saml.certificate_updated',
  'session.override_started', 'session.override_ended',
  'audit.export', 'compliance.report_generated',
];
```

## Admin Audit Service

```typescript
class AdminAuditService {
  async recordAdminAction(adminUser: User, action: string, target: any, changes?: { before?: any; after?: any }): Promise<void> {
    if (!ADMIN_AUDITED_ACTIONS.includes(action)) return;

    const event: ActivityEvent = {
      id: generateId('audit'),
      timestamp: new Date(),
      actor: {
        id: adminUser.id,
        type: 'user',
        email: adminUser.email,
        ipAddress: adminUser.lastIp,
      },
      action,
      target,
      changes: changes || null,
      context: {
        tenantId: adminUser.tenantId,
        sessionId: adminUser.sessionId,
        source: 'admin',
      },
      severity: this.getSeverity(action),
    };

    // Write to immutable audit store
    await this.immutableStore.append(event);

    // Also write to standard activity log
    await this.captureService.logEvent(event);
  }

  async getAdminAuditTrail(tenantId: string, query: AuditQuery): Promise<PaginatedResult<ActivityEvent>> {
    const events = await this.immutableStore.query({
      tenantId,
      actions: query.actions || ADMIN_AUDITED_ACTIONS,
      startDate: query.startDate,
      endDate: query.endDate,
      actorIds: query.actorIds,
      limit: query.limit,
    });

    return {
      data: events,
      total: events.length,
      cursor: null,
    };
  }

  private getSeverity(action: string): 'info' | 'warning' | 'critical' {
    const criticalActions = ['user.deleted', 'api_key.revoked', 'session.override_started', 'billing.invoice_voided'];
    const warningActions = ['role.modified', 'permission.granted', 'settings.modified'];

    if (criticalActions.includes(action)) return 'critical';
    if (warningActions.includes(action)) return 'warning';
    return 'info';
  }
}
```

## Audit Trail Viewer

```
Admin Audit Trail
┌─────────────────────────────────────────────────────────────────────┐
│ Date Range: [Last 30 days ▼]  │  Search: [🔍]                      │
├────────┬──────────┬───────────┬──────────────────┬──────────────────┤
│ Time   │ Admin    │ Action    │ Target            │ Changes         │
├────────┼──────────┼───────────┼──────────────────┼──────────────────┤
│ 2:30PM │ Alice    │ role.mod  │ Role: Senior     │ +campaigns:read  │
│        │          │ ified     │ Agent            │ +calls:write     │
│ 1:15PM │ Alice    │ api_key.  │ Key: "Prod API"  │ Revoked          │
│        │          │ revoked   │                  │                  │
│ 11AM   │ Bob      │ user.sus  │ User: john@co    │ Status: active → │
│        │          │ pended    │                  │ suspended        │
│ ...    │ ...      │ ...       │ ...              │ ...              │
└────────┴──────────┴───────────┴──────────────────┴──────────────────┘
```

## Open-Source Tools

- **AWS S3 / S3-compatible** — Immutable audit log storage
- **Elasticsearch** — Searchable audit index

## Production Considerations

- Write to append-only/immutable storage (S3, immutable DB table)
- Retain admin audit records for minimum 3 years (compliance)
- Index by tenant, admin, action, and timestamp
- Include before/after snapshots for all configuration changes
- Alert on critical admin actions (user deletion, billing changes)
- Generate compliance reports from audit trail
- Support CSV/JSON export for auditor review
- Hash-chain audit records to detect tampering
