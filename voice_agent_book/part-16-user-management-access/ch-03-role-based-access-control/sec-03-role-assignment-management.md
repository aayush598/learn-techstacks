# Role Assignment Management

## Overview

Role assignment management handles the lifecycle of linking users to roles, including assignments, removals, temporary grants with expiration, role activation/deactivation, and bulk operations across teams or departments.

## Assignment Lifecycle

```
[Admin/System] → Assign Role to User
    │
    ▼
[Validation] → Does role exist?
    ├── No → Error
    └── Yes → Does user exist?
                ├── No → Error
                └── Yes → Check if already assigned
                            ├── Yes → Update (extend or modify)
                            └── No → Create assignment
                                     │
                                     ▼
                            [Record with metadata]
                              ├── assigned_by
                              ├── assigned_at
                              ├── expires_at (optional)
                              └── reason / justification
```

## Assignment Operations

```typescript
interface RoleAssignmentRequest {
  userId: string;
  roleId: string;
  assignedBy?: string;
  expiresAt?: Date;
  reason?: string;
  notifyUser?: boolean;
}

interface RoleAssignmentResult {
  success: boolean;
  assignment?: UserRoleAssignment;
  error?: string;
}

class RoleAssignmentService {
  async assignRole(request: RoleAssignmentRequest): Promise<RoleAssignmentResult> {
    // Validate role exists and is active
    const role = await this.roleStore.getRole(request.roleId);
    if (!role) {
      return { success: false, error: 'role_not_found' };
    }

    // Validate user exists and is active
    const user = await this.userStore.getUser(request.userId);
    if (!user || user.status !== 'active') {
      return { success: false, error: 'user_not_available' };
    }

    // Check for existing assignment
    const existing = await this.db.findOne('user_roles', {
      userId: request.userId,
      roleId: request.roleId,
    });

    if (existing) {
      // Update existing assignment
      if (request.expiresAt) {
        existing.expiresAt = request.expiresAt;
      }
      existing.assignedBy = request.assignedBy;
      existing.assignedAt = new Date();
      await this.db.update('user_roles', { id: existing.id }, existing);
      await this.invalidatePermissionCache(request.userId);

      if (request.notifyUser) {
        await this.notifyRoleAssigned(user, role, request.expiresAt);
      }

      return { success: true, assignment: existing };
    }

    // Create new assignment
    const assignment: UserRoleAssignment = {
      userId: request.userId,
      roleId: request.roleId,
      assignedBy: request.assignedBy,
      assignedAt: new Date(),
      expiresAt: request.expiresAt,
    };

    await this.db.insert('user_roles', assignment);
    await this.invalidatePermissionCache(request.userId);

    if (request.notifyUser) {
      await this.notifyRoleAssigned(user, role, request.expiresAt);
    }

    return { success: true, assignment };
  }

  async removeRole(userId: string, roleId: string, removedBy?: string): Promise<void> {
    const assignment = await this.db.findOne('user_roles', { userId, roleId });
    if (!assignment) return;

    await this.db.delete('user_roles', { userId, roleId });
    await this.invalidatePermissionCache(userId);

    // Log the removal
    await this.auditLog.record({
      action: 'role.removed',
      actor: removedBy || 'system',
      target: { userId, roleId },
      metadata: { previousAssignment: assignment },
    });

    const user = await this.userStore.getUser(userId);
    const role = await this.roleStore.getRole(roleId);
    await this.notifyRoleRemoved(user!, role!);
  }

  async getUserRoles(userId: string): Promise<UserRoleWithRole[]> {
    const assignments = await this.db.find('user_roles', { userId });
    const roles = await Promise.all(
      assignments.map(async a => {
        const role = await this.roleStore.getRole(a.roleId);
        return { ...a, role };
      })
    );
    return roles.filter(r => r.role !== null);
  }

  async getUsersByRole(roleId: string): Promise<User[]> {
    const assignments = await this.db.find('user_roles', { roleId });
    const userIds = assignments.map(a => a.userId);
    return this.userStore.getUsersByIds(userIds);
  }
}
```

## Temporary Role Grants

```typescript
interface TemporaryRoleGrant {
  userId: string;
  roleId: string;
  grantedAt: Date;
  expiresAt: Date;
  reason: string;
  grantedBy: string;
  autoRevoke: boolean;
}

class TemporaryRoleService {
  async grantTemporaryRole(
    grant: Omit<TemporaryRoleGrant, 'grantedAt' | 'autoRevoke'>
  ): Promise<void> {
    const { userId, roleId, expiresAt, reason } = grant;

    await this.assignmentService.assignRole({
      userId,
      roleId,
      assignedBy: grant.grantedBy,
      expiresAt,
      reason,
    });

    // Schedule automatic revocation
    if (expiresAt) {
      const delay = expiresAt.getTime() - Date.now();
      await this.scheduleRevocation(userId, roleId, delay);
    }

    await this.auditLog.record({
      action: 'role.temporary_grant',
      actor: grant.grantedBy,
      target: { userId, roleId },
      metadata: { expiresAt, reason },
    });
  }

  private async scheduleRevocation(
    userId: string, roleId: string, delayMs: number
  ): Promise<void> {
    await this.queue.schedule({
      type: 'revoke_temporary_role',
      payload: { userId, roleId },
      delay: delayMs,
    });
  }

  async extendTemporaryGrant(
    userId: string, roleId: string,
    newExpiry: Date, extendedBy: string
  ): Promise<void> {
    await this.db.update('user_roles', { userId, roleId }, {
      expiresAt: newExpiry,
    });

    // Re-schedule revocation
    await this.cancelRevocation(userId, roleId);
    const delay = newExpiry.getTime() - Date.now();
    await this.scheduleRevocation(userId, roleId, delay);

    await this.auditLog.record({
      action: 'role.temporary_extend',
      actor: extendedBy,
      target: { userId, roleId },
      metadata: { newExpiry },
    });
  }

  async processExpiredAssignments(): Promise<number> {
    const expired = await this.db.find('user_roles', {
      expiresAt: { $lte: new Date() },
    });

    for (const assignment of expired) {
      await this.assignmentService.removeRole(
        assignment.userId, assignment.roleId, 'system'
      );
    }

    return expired.length;
  }
}
```

## Bulk Role Assignment

```typescript
interface BulkRoleAssignmentRequest {
  userIds: string[];
  roleId: string;
  assignedBy: string;
  expiresAt?: Date;
  notifyUsers?: boolean;
}

interface BulkAssignmentResult {
  succeeded: number;
  failed: number;
  errors: Array<{ userId: string; error: string }>;
}

async function bulkAssignRole(
  request: BulkRoleAssignmentRequest
): Promise<BulkAssignmentResult> {
  const result: BulkAssignmentResult = { succeeded: 0, failed: 0, errors: [] };
  const batchSize = 50;

  for (let i = 0; i < request.userIds.length; i += batchSize) {
    const batch = request.userIds.slice(i, i + batchSize);
    const operations = batch.map(userId =>
      assignmentService.assignRole({
        userId,
        roleId: request.roleId,
        assignedBy: request.assignedBy,
        expiresAt: request.expiresAt,
        notifyUser: request.notifyUsers,
      })
    );

    const outcomes = await Promise.allSettled(operations);
    for (const outcome of outcomes) {
      if (outcome.status === 'fulfilled' && outcome.value.success) {
        result.succeeded++;
      } else {
        result.failed++;
        const failedUserId = batch[result.errors.length];
        result.errors.push({
          userId: failedUserId,
          error: outcome.status === 'rejected' ? outcome.reason.message : outcome.value.error!,
        });
      }
    }
  }

  return result;
}
```

## Open-Source Tools

- **BullMQ** (MIT) — Queue for scheduling role expiry revocation
- **casbin** (Apache 2.0) — Role management API

## Production Considerations

- Run a cron job every 5 minutes to process expired assignments (backup for queue-based revocation)
- Never assign roles directly to users without audit logging
- Require justification (reason field) for sensitive role assignments (admin, developer)
- Limit concurrent temporary role grants per user (max 3 active)
- Send email notification to user and manager when roles change
- Implement approval workflow for assigning admin roles (two-person rule)
