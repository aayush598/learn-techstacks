# Permission Audit Trail

## Overview

The permission audit trail records every change to roles, permissions, and assignments with before/after snapshots for complete accountability. This meets compliance requirements (SOC 2, SOX) and provides traceability for permission-related incidents.

## Event Schema

```typescript
interface PermissionAuditEvent {
  id: string;
  timestamp: Date;
  actor: {
    id: string;
    type: 'user' | 'system' | 'api' | 'scim';
    email?: string;
    ipAddress?: string;
  };
  action: PermissionAuditAction;
  target: {
    type: 'role' | 'permission' | 'assignment' | 'scope';
    id: string;
    name?: string;
  };
  changes: {
    before: Record<string, unknown> | null;
    after: Record<string, unknown> | null;
  };
  metadata: {
    tenantId: string;
    source: 'admin_ui' | 'api' | 'scim' | 'system';
    reason?: string;
    correlationId?: string;
  };
}

type PermissionAuditAction =
  | 'role.created'
  | 'role.updated'
  | 'role.deleted'
  | 'permission.added'
  | 'permission.removed'
  | 'permission.modified'
  | 'role.assigned'
  | 'role.unassigned'
  | 'scope.changed'
  | 'role.cloned'
  | 'role.inheritance_changed';
```

## Audit Trail Service

```typescript
class PermissionAuditService {
  async recordEvent(event: Omit<PermissionAuditEvent, 'id' | 'timestamp'>): Promise<void> {
    const fullEvent: PermissionAuditEvent = {
      ...event,
      id: generateId('audit'),
      timestamp: new Date(),
    };

    // Store in primary audit log
    await this.db.insert('permission_audit_log', fullEvent);

    // Publish to event bus for real-time monitoring
    await this.eventBus.publish('permission.audit', fullEvent);

    // Check for suspicious patterns
    await this.anomalyDetector.analyze(fullEvent);
  }

  async recordRoleChange(
    actor: PermissionAuditEvent['actor'],
    role: Role,
    beforePermissions: RolePermission[],
    afterPermissions: RolePermission[],
    metadata: Partial<PermissionAuditEvent['metadata']>
  ): Promise<void> {
    await this.recordEvent({
      actor,
      action: 'role.updated',
      target: { type: 'role', id: role.id, name: role.name },
      changes: {
        before: { permissions: beforePermissions, restrictions: role.restrictions },
        after: { permissions: afterPermissions, restrictions: role.restrictions },
      },
      metadata: {
        tenantId: role.tenantId,
        source: metadata.source || 'admin_ui',
        reason: metadata.reason,
        correlationId: metadata.correlationId,
      },
    });
  }

  async recordAssignment(
    actor: PermissionAuditEvent['actor'],
    userId: string,
    roleId: string,
    action: 'role.assigned' | 'role.unassigned',
    metadata: Partial<PermissionAuditEvent['metadata']>
  ): Promise<void> {
    await this.recordEvent({
      actor,
      action,
      target: { type: 'assignment', id: `${userId}:${roleId}` },
      changes: {
        before: action === 'role.assigned' ? null : { userId, roleId },
        after: action === 'role.assigned' ? { userId, roleId } : null,
      },
      metadata: {
        tenantId: metadata.tenantId || 'unknown',
        source: metadata.source || 'admin_ui',
        reason: metadata.reason,
      },
    });
  }

  async getRoleChangeHistory(roleId: string, limit: number = 50): Promise<PermissionAuditEvent[]> {
    return this.db.find('permission_audit_log', {
      'target.id': roleId,
      'target.type': 'role',
    }, { sort: { timestamp: -1 }, limit });
  }

  async getUserAssignmentHistory(userId: string, limit: number = 50): Promise<PermissionAuditEvent[]> {
    return this.db.find('permission_audit_log', {
      $or: [
        { 'changes.after.userId': userId },
        { 'changes.before.userId': userId },
      ],
      action: { $in: ['role.assigned', 'role.unassigned'] },
    }, { sort: { timestamp: -1 }, limit });
  }
}
```

## Change Approval Workflow

```typescript
interface PermissionChangeRequest {
  id: string;
  requesterId: string;
  requestedChanges: PermissionChange[];
  status: 'pending' | 'approved' | 'rejected' | 'cancelled';
  reviewerId?: string;
  reviewNotes?: string;
  requestedAt: Date;
  reviewedAt?: Date;
  expiresAt: Date;
}

interface PermissionChange {
  type: 'role_modify' | 'assign_role' | 'create_role' | 'delete_role';
  targetId: string;
  description: string;
  diff: string; // Human-readable change description
}

class PermissionChangeApproval {
  async requestChange(
    requesterId: string,
    changes: PermissionChange[],
    reason: string
  ): Promise<PermissionChangeRequest> {
    // Check if changes require approval
    const requiresApproval = changes.some(c =>
      this.isSensitiveChange(c) || this.isHighImpactChange(c)
    );

    if (!requiresApproval) {
      // Auto-approve low-impact changes
      return this.applyAndRecord(requesterId, changes, reason, 'system');
    }

    const request: PermissionChangeRequest = {
      id: generateId('pcr'),
      requesterId,
      requestedChanges: changes,
      status: 'pending',
      requestedAt: new Date(),
      expiresAt: new Date(Date.now() + 7 * 86400000), // 7 days
    };

    await this.db.insert('permission_change_requests', request);

    // Notify reviewers
    const reviewers = await this.getReviewersForChange(changes);
    await this.notificationService.notifyReviewers(request, reviewers);

    return request;
  }

  private isSensitiveChange(change: PermissionChange): boolean {
    const sensitivePatterns = [
      /billing/, /api_key/, /system_settings/,
      /admin_role/, /delete.*role/,
    ];
    return sensitivePatterns.some(p => p.test(change.description));
  }

  private isHighImpactChange(change: PermissionChange): boolean {
    const highImpactPatterns = [
      /wildcard/, /\*:(\*|all)/,
      /tenant.*scope/, /all.*users/,
    ];
    return highImpactPatterns.some(p => p.test(change.description));
  }

  async approve(requestId: string, reviewerId: string, notes?: string): Promise<void> {
    const request = await this.db.findOne('permission_change_requests', { id: requestId });
    if (!request || request.status !== 'pending') {
      throw new Error('Request not found or already processed');
    }

    request.status = 'approved';
    request.reviewerId = reviewerId;
    request.reviewNotes = notes;
    request.reviewedAt = new Date();

    await this.db.update('permission_change_requests', { id: requestId }, request);
    await this.applyChanges(request);
    await this.notificationService.notifyRequester(request);
  }

  private async applyChanges(request: PermissionChangeRequest): Promise<void> {
    for (const change of request.requestedChanges) {
      // Apply each change and audit
      await this.permissionService.applyChange(change, {
        id: request.requesterId,
        type: 'user',
      });
    }
  }
}
```

## Anomaly Detection

```typescript
class PermissionAnomalyDetector {
  async analyze(event: PermissionAuditEvent): Promise<void> {
    const anomalies: string[] = [];

    // Mass assignment detection
    if (event.action === 'role.assigned') {
      const recentAssignments = await this.getRecentAssignments(
        event.metadata.tenantId, 60000 // 1 minute
      );
      if (recentAssignments > 100) {
        anomalies.push('Mass role assignment detected');
        await this.alertHighSeverity('mass_assignment', event);
      }
    }

    // Unusual timing
    const hour = new Date().getHours();
    if (hour >= 0 && hour <= 5) {
      anomalies.push('Permission change during off-hours');
    }

    // Escalation detection
    if (event.action === 'role.assigned' || event.action === 'permission.added') {
      const newPermissions = event.changes.after as any;
      if (newPermissions?.permissions?.some((p: any) =>
        p.resource === 'billing' || p.action === '*'
      )) {
        anomalies.push('Permission escalation to sensitive resource');
      }
    }

    if (anomalies.length > 0) {
      await this.alertService.send({
        type: 'permission_anomaly',
        severity: anomalies.length > 1 ? 'high' : 'medium',
        event,
        anomalies,
      });
    }
  }
}
```

## Open-Source Tools

- **Elasticsearch** — Audit log storage and search
- **Grafana Loki** — Log aggregation for permission events
- **TimescaleDB** — Time-series audit storage

## Production Considerations

- Retain permission audit logs for minimum 3 years (compliance requirement)
- Never overwrite audit records; use append-only storage
- Index audit events by tenant, actor, target, and timestamp for fast querying
- Implement audit log integrity checks (hash chain) to prevent tampering
- Provide downloadable audit reports in CSV/PDF format for compliance reviews
- Rate-limit audit event creation to prevent log flooding
- Encrypt audit records at rest and in transit
- Include correlation IDs to link permission changes to support tickets
