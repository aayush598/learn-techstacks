# Team Admin Delegation

## Overview

Team admin delegation allows team leads and department heads to manage their teams without full tenant admin access. Delegated admin roles provide scoped permissions for user management, resource allocation, and team configuration within their organizational unit.

## Delegated Admin Roles

```typescript
interface DelegatedAdminRole {
  id: string;
  tenantId: string;
  name: string;
  scope: 'team' | 'department' | 'multi_team';
  permissions: DelegatedPermission[];
  restrictions: DelegatedRestriction[];
}

interface DelegatedPermission {
  action: 'manage_members' | 'manage_resources' | 'view_analytics' | 'manage_settings'
       | 'assign_roles' | 'view_reports' | 'manage_billing' | 'approve_requests';
  enabled: boolean;
  constraints?: {
    maxRoleLevel?: string;     // Cannot assign roles above this level
    requireApproval?: boolean; // Changes need approval
    maxResourceQuota?: number;
  };
}

interface DelegatedRestriction {
  type: 'max_team_size' | 'max_resource_allocation' | 'budget_limit'
      | 'sensitive_actions_require_approval';
  value: number | boolean;
}
```

## Delegated Admin Service

```typescript
class TeamAdminDelegationService {
  async assignTeamAdmin(
    userId: string,
    teamId: string,
    role: DelegatedAdminRole,
    grantedBy: string
  ): Promise<void> {
    const team = await this.teamService.getTeam(teamId);
    if (!team) throw new Error('Team not found');

    const existingAdmins = await this.db.find('team_admins', { teamId });
    if (existingAdmins.length >= MAX_ADMINS_PER_TEAM) {
      throw new Error(`Maximum team admins (${MAX_ADMINS_PER_TEAM}) reached`);
    }

    await this.db.insert('team_admins', {
      userId,
      teamId,
      roleId: role.id,
      grantedBy,
      grantedAt: new Date(),
      isActive: true,
    });

    await this.auditLog.record({
      action: 'team.admin_assigned',
      actor: grantedBy,
      target: { userId, teamId },
      metadata: { roleName: role.name, scope: role.scope },
    });
  }

  async getDelegatedPermissions(
    userId: string,
    teamId: string
  ): Promise<DelegatedPermission[]> {
    const adminEntries = await this.db.find('team_admins', {
      userId,
      isActive: true,
      $or: [
        { teamId },
        { scopeType: 'department', scopeValue: (await this.teamService.getTeam(teamId))?.departmentId },
      ],
    });

    const permissions: DelegatedPermission[] = [];
    for (const entry of adminEntries) {
      const role = await this.db.findOne('delegated_admin_roles', { id: entry.roleId });
      if (role) {
        permissions.push(...role.permissions);
      }
    }

    return this.deduplicatePermissions(permissions);
  }

  async validateDelegatedAction(
    userId: string,
    teamId: string,
    action: string
  ): Promise<boolean> {
    const permissions = await this.getDelegatedPermissions(userId, teamId);
    const matching = permissions.find(p => p.action === action);
    if (!matching || !matching.enabled) return false;

    // Check restrictions
    if (action === 'assign_roles') {
      const adminEntry = await this.db.findOne('team_admins', { userId, teamId });
      const role = await this.db.findOne('delegated_admin_roles', { id: adminEntry?.roleId });
      if (role?.restrictions?.some(r => r.type === 'sensitive_actions_require_approval')) {
        return false; // Needs approval workflow
      }
    }

    return true;
  }
}
```

## Approval Workflow for Delegated Actions

```typescript
interface DelegatedActionRequest {
  id: string;
  requesterId: string;
  action: string;
  teamId: string;
  details: Record<string, unknown>;
  status: 'pending' | 'approved' | 'rejected';
  reviewerId?: string;
  reviewNotes?: string;
  createdAt: Date;
  reviewedAt?: Date;
}

class DelegatedActionApproval {
  async requestAction(
    requesterId: string,
    action: string,
    teamId: string,
    details: Record<string, unknown>
  ): Promise<DelegatedActionRequest> {
    // Check if action requires approval
    const requiresApproval = await this.isActionSensitive(action, teamId);

    const request: DelegatedActionRequest = {
      id: generateId('dar'),
      requesterId,
      action,
      teamId,
      details,
      status: requiresApproval ? 'pending' : 'approved',
      createdAt: new Date(),
    };

    if (!requiresApproval) {
      request.reviewedAt = new Date();
      await this.executeAction(request);
    } else {
      // Notify team lead or department head
      const reviewers = await this.getReviewers(teamId);
      await this.notificationService.notify({
        type: 'delegated_action_approval',
        recipients: reviewers,
        data: request,
      });
    }

    await this.db.insert('delegated_action_requests', request);
    return request;
  }

  private async isActionSensitive(action: string, teamId: string): Promise<boolean> {
    const sensitiveActions = ['delete_team', 'increase_quota', 'assign_admin_role', 'modify_budget'];
    return sensitiveActions.includes(action);
  }
}
```

## Scoped Admin Dashboard

```
Team Admin Dashboard (Sales Team)
┌────────────────────────────────────────────────┐
│  You are team admin for: Sales Team             │
│  Role: Team Lead (Delegated Admin)              │
├────────────────────────────────────────────────┤
│  Quick Actions                                  │
│  ├── + Add Team Member                          │
│  ├──   Remove Team Member [requires approval]   │
│  ├──   Adjust Resource Quota [requires approval]│
│  └──   View Team Analytics                       │
├────────────────────────────────────────────────┤
│  Team Members (12)                              │
│  ├── Alice (Agent) ─ active                     │
│  ├── Bob (Agent) ─ active                       │
│  └── ...                                        │
│  [Invite Member]                                │
├────────────────────────────────────────────────┤
│  Pending Approvals (2)                          │
│  ├── Charlie requested quota increase           │
│  └── Diana requested role change                │
└────────────────────────────────────────────────┘
```

## Open-Source Tools

- **Permit.io** (Apache 2.0) — Delegated admin with scoped permissions
- **Casbin** (Apache 2.0) — Role hierarchy with admin delegation patterns

## Production Considerations

- Maximum 5 delegated admins per team to prevent admin sprawl
- Require approval for destructive actions (delete team, remove members, change budget)
- Log all delegated admin actions with the scope of their authority
- Allow tenant admins to view all delegated admins across teams
- Provide monthly report of delegated admin activities to tenant admin
- Support emergency override of delegated admin restrictions by tenant admin
- Auto-revoke delegated admin when user leaves the team or changes role
