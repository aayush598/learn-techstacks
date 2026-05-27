# Permission Conflict Resolution

## Overview

When a user has multiple roles with overlapping or contradictory permissions, conflict resolution rules determine the effective access. The system must prioritize explicit denials, handle resource-level specificity, and provide clear conflict visualization.

## Conflict Resolution Rules

```
Rule 1: Explicit Deny Overrides Allow (DENY > ALLOW)
  Role A: allow agents:delete
  Role B: deny agents:delete
  Result: DENY

Rule 2: Specific Resource Overrides Wildcard
  Role A: allow agents:*
  Role B: deny agents:delete
  Result: DENY agents:delete, ALLOW everything else on agents

Rule 3: Direct Assignment Overrides Inheritance
  User assigned Role A directly: cannot delete agents
  User assigned Role B (inherits from A): can delete agents
  Result: DENY (direct assignment wins)

Rule 4: Most Restrictive Scope Wins
  Role A: allow agents:read scope=tenant
  Role B: allow agents:read scope=self  
  Result: ALLOW scope=self only (most restrictive)
```

## Conflict Detection

```typescript
interface PermissionConflict {
  userId?: string;
  roleId?: string;
  resource: string;
  action: string;
  conflictingPermissions: ConflictingPermission[];
  resolution: 'deny_wins' | 'specific_wins' | 'direct_wins' | 'restrictive_wins';
  resolvedEffect: 'allow' | 'deny';
}

interface ConflictingPermission {
  roleId: string;
  roleName: string;
  effect: 'allow' | 'deny';
  specificity: number;
  isDirect: boolean;
  scope: ResourceScope;
}

class ConflictResolver {
  resolveForUser(userId: string, request: PermissionRequest): PermissionResult {
    const userRoles = this.getUserRoles(userId);
    const matchingPermissions = this.findMatchingPermissions(userRoles, request);

    if (matchingPermissions.length === 0) {
      return { allowed: false, reason: 'no_matching_permission' };
    }

    // Step 1: Check for explicit denials
    const explicitDenies = matchingPermissions.filter(p => p.effect === 'deny');
    if (explicitDenies.length > 0) {
      return {
        allowed: false,
        reason: 'explicit_deny',
        matchedRole: explicitDenies[0].roleName,
        conflict: this.buildConflict(matchingPermissions),
      };
    }

    // Step 2: Most specific matching permission wins
    const sorted = this.sortBySpecificity(matchingPermissions);

    // Step 3: If ties, direct assignment > inherited
    const bestMatch = sorted[0];

    return {
      allowed: bestMatch.effect === 'allow',
      matchedRole: bestMatch.roleName,
    };
  }

  private findMatchingPermissions(
    userRoles: UserRoleWithRole[],
    request: PermissionRequest
  ): RolePermission[] {
    const allPermissions: RolePermission[] = [];

    for (const { role } of userRoles) {
      const effectivePerms = this.getEffectivePermissions(role!);
      for (const perm of effectivePerms) {
        if (this.permissionMatches(perm, request)) {
          allPermissions.push({
            ...perm,
            roleId: role!.id,
            roleName: role!.name,
            isDirect: userRoles.some(r => r.roleId === role!.id),
            specificity: this.calculateSpecificity(perm, request),
          });
        }
      }
    }

    return allPermissions;
  }

  private permissionMatches(perm: RolePermission, request: PermissionRequest): boolean {
    const resourceMatch = perm.resource === '*' || perm.resource === request.resource;
    const actionMatch = perm.action === '*' || perm.action === request.action;
    return resourceMatch && actionMatch;
  }

  private calculateSpecificity(perm: RolePermission, request: PermissionRequest): number {
    let score = 0;
    if (perm.resource !== '*') score += 10;
    if (perm.resource === request.resource) score += 5;
    if (perm.action !== '*') score += 10;
    if (perm.action === request.action) score += 5;
    if (perm.conditions) score += 3; // Conditional permissions are more specific
    return score;
  }

  private sortBySpecificity(permissions: RolePermission[]): RolePermission[] {
    return permissions.sort((a, b) => {
      const specDiff = b.specificity - a.specificity;
      if (specDiff !== 0) return specDiff;
      // Direct assignments over inherited
      if (a.isDirect !== b.isDirect) return a.isDirect ? -1 : 1;
      return 0;
    });
  }

  private buildConflict(permissions: ConflictingPermission[]): PermissionConflict {
    return {
      resource: permissions[0].resource,
      action: permissions[0].action,
      conflictingPermissions: permissions,
      resolution: this.determineResolution(permissions),
      resolvedEffect: this.resolveEffect(permissions),
    };
  }

  private determineResolution(permissions: ConflictingPermission[]): PermissionConflict['resolution'] {
    if (permissions.some(p => p.effect === 'deny')) return 'deny_wins';
    if (new Set(permissions.map(p => p.specificity)).size > 1) return 'specific_wins';
    if (permissions.some(p => p.isDirect) && permissions.some(p => !p.isDirect)) return 'direct_wins';
    return 'restrictive_wins';
  }
}
```

## Conflict Visualization

```typescript
function ConflictResolutionView({ conflicts }: { conflicts: PermissionConflict[] }) {
  return (
    <div className="conflict-list">
      {conflicts.map(conflict => (
        <div key={`${conflict.resource}:${conflict.action}`} className="conflict-card">
          <h4>{conflict.resource}:{conflict.action}</h4>
          <div className="conflict-permissions">
            {conflict.conflictingPermissions.map(perm => (
              <div key={perm.roleId} className={`perm-row ${perm.effect}`}>
                <span className="role-name">{perm.roleName}</span>
                <PermissionBadge effect={perm.effect} />
                <span className="specificity">Specificity: {perm.specificity}</span>
                <span className={perm.isDirect ? 'direct' : 'inherited'}>
                  {perm.isDirect ? 'Direct' : 'Inherited'}
                </span>
              </div>
            ))}
          </div>
          <div className="resolution">
            Resolution: <strong>{conflict.resolution}</strong>
            → <PermissionBadge effect={conflict.resolvedEffect} />
          </div>
        </div>
      ))}
    </div>
  );
}

function PermissionBadge({ effect }: { effect: 'allow' | 'deny' }) {
  return (
    <span className={`badge ${effect}`}>
      {effect === 'allow' ? '✓ Allow' : '✗ Deny'}
    </span>
  );
}
```

## Conflict Prevention

```typescript
class ConflictPreventionService {
  async validateNewRole(role: Role): Promise<ValidationResult> {
    const errors: string[] = [];

    // Check for conflicts within the same role
    const selfConflicts = this.findSelfConflicts(role.permissions);
    for (const conflict of selfConflicts) {
      errors.push(`Self-conflict: ${conflict.resource}:${conflict.action}`);
    }

    // Check for conflicts with existing roles
    if (role.parentRoleId) {
      const parent = await this.roleStore.getRole(role.parentRoleId);
      if (parent) {
        const parentConflicts = this.findConflictsWithParent(role.permissions, parent.permissions);
        for (const conflict of parentConflicts) {
          errors.push(`Inheritance conflict: ${conflict.description}`);
        }
      }
    }

    // Check for ambiguous wildcards
    const wildcards = role.permissions.filter(p => p.resource === '*' || p.action === '*');
    if (wildcards.length > 1) {
      errors.push('Multiple wildcard permissions may create ambiguous access');
    }

    return { valid: errors.length === 0, errors };
  }

  private findSelfConflicts(permissions: RolePermission[]): SelfConflict[] {
    const conflicts: SelfConflict[] = [];
    const seen = new Map<string, RolePermission>();

    for (const perm of permissions) {
      const key = `${perm.resource}:${perm.action}`;
      if (seen.has(key)) {
        const existing = seen.get(key)!;
        if (existing.effect !== perm.effect) {
          conflicts.push({
            resource: perm.resource,
            action: perm.action,
            conflictingPerms: [existing, perm],
            description: `Permission ${key} has both allow and deny`,
          });
        }
      }
      seen.set(key, perm);
    }

    return conflicts;
  }
}
```

## Open-Source Tools

- **Casbin** (Apache 2.0) — Built-in conflict resolution with priority model
- **Open Policy Agent** (Apache 2.0) — Policy-based conflict resolution

## Production Considerations

- Perform conflict detection when roles are created or modified, not at runtime
- Warn administrators about conflicts during role configuration
- Provide an override flag for explicit deny/allow to intentionally resolve conflicts
- Add conflict detection to CI/CD pipeline for automated permission management
- Maintain a conflict registry for audit and debugging purposes
- Limit the number of roles per user (recommended max 5) to reduce conflict complexity
