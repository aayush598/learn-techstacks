# Default Permission Assignment

## Overview

Default permission assignment configures roles and permissions for new users at invitation time or upon first login. Assignments can be based on department, team, or role template, with optional escalation as the user completes onboarding.

## Assignment Configuration

```typescript
interface DefaultAssignmentConfig {
  tenantId: string;
  departmentDefaults: Record<string, {
    roleId: string;
    teamId?: string;
    additionalPermissions?: string[];
  }>;
  roleDefaults: Record<string, {
    permissions: string[];
    restrictions?: RoleRestriction[];
  }>;
  escalationRules: EscalationRule[];
}

interface EscalationRule {
  triggerStep: string;         // Onboarding step ID
  addPermissions: string[];
  newRoleId?: string;
  reason: string;
}
```

## Assignment Service

```typescript
class PermissionAssignmentService {
  async assignDefaults(userId: string, tenantId: string, departmentId?: string): Promise<void> {
    const config = await this.getDefaultConfig(tenantId);
    const user = await this.userService.getUser(userId);

    // Department-based defaults
    if (departmentId && config.departmentDefaults[departmentId]) {
      const deptDefault = config.departmentDefaults[departmentId];
      await this.roleService.assignRole(userId, deptDefault.roleId, 'system');
      if (deptDefault.teamId) {
        await this.teamService.addMember(deptDefault.teamId, userId, 'member');
      }
    } else {
      // Fallback to default role
      await this.roleService.assignRole(userId, config.defaultRoleId, 'system');
    }
  }
}
```

## Permission Escalation

```typescript
async function handleEscalation(userId: string, completedStepId: string): Promise<void> {
  const config = await getTenantConfig(getUserTenant(userId));
  const matchingRule = config.escalationRules.find(r => r.triggerStep === completedStepId);

  if (matchingRule) {
    if (matchingRule.newRoleId) {
      await roleService.assignRole(userId, matchingRule.newRoleId, 'system');
    }
    for (const perm of matchingRule.addPermissions) {
      await permissionService.grantPermission(userId, perm);
    }
  }
}
```

## Permission Progression

```
Day 1 (Invite): Team Member (basic permissions)
Day 3 (Training Complete): Agent (call handling)
Day 7 (10 Calls): Senior Agent (extended permissions)
Day 30 (Manager Approval): Team Lead (admin delegation)
```

## Open-Source Tools

- **Casbin** (Apache 2.0) — Dynamic permission assignment

## Production Considerations

- Allow override of defaults per user at invitation time
- Log all automatic permission assignments for audit
- Support retroactive application of new defaults to existing users
- Escalation rules should be additive only (never remove permissions)
- Provide admin dashboard to view current default configurations
