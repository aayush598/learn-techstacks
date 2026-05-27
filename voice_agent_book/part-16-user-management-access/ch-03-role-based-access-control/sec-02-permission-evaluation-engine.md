# Permission Evaluation Engine

## Overview

The permission evaluation engine determines whether a user has access to perform a specific action on a given resource. It resolves role hierarchies, evaluates conditions, applies deny precedence, and returns cached results for performance.

## Evaluation Algorithm

```
User Request (userId, action, resource)
    │
    ▼
Load User Roles (cached)
    │
    ▼
Resolve Role Hierarchy
    │
    ├── For each assigned role:
    │   ├── Collect direct permissions
    │   └── Collect inherited permissions (recursive)
    │
    ▼
Merge Permissions
    ├── Deny always wins (explicit deny overrides allow)
    ├── More specific resource > less specific
    └── Direct assignment > inherited
    │
    ▼
Evaluate Conditions
    ├── Attribute-based conditions
    └── Resource-level restrictions
    │
    ▼
Return: Allow / Deny
```

## Engine Implementation

```typescript
interface PermissionRequest {
  userId: string;
  tenantId: string;
  action: string;
  resource: string;
  resourceId?: string;
  attributes?: Record<string, unknown>;
}

interface PermissionResult {
  allowed: boolean;
  matchedRule?: string;
  matchedRole?: string;
  reason?: string;
}

class PermissionEngine {
  private cache: PermissionCache;
  private roleStore: RoleStore;
  private conditionEvaluator: ConditionEvaluator;

  constructor() {
    this.cache = new PermissionCache();
    this.roleStore = new RoleStore();
    this.conditionEvaluator = new ConditionEvaluator();
  }

  async check(request: PermissionRequest): Promise<PermissionResult> {
    // Check cache first
    const cached = await this.cache.get(request);
    if (cached) return cached;

    // Get user's roles
    const roleAssignments = await this.roleStore.getUserRoles(
      request.userId, request.tenantId
    );
    if (roleAssignments.length === 0) {
      const result: PermissionResult = {
        allowed: false,
        reason: 'no_roles_assigned',
      };
      return result;
    }

    // Collect all permissions from roles (resolving hierarchy)
    const allPermissions = await this.collectPermissions(roleAssignments);
    if (allPermissions.length === 0) {
      return { allowed: false, reason: 'no_permissions' };
    }

    // Evaluate permissions from most specific to least
    const sortedPermissions = this.sortPermissionsBySpecificity(
      allPermissions, request.action, request.resource
    );

    for (const perm of sortedPermissions) {
      // Check explicit deny first
      if (perm.effect === 'deny') {
        return {
          allowed: false,
          matchedRule: `${perm.resource}:${perm.action}`,
          matchedRole: perm.roleName,
          reason: 'explicit_deny',
        };
      }

      // Evaluate conditions
      if (perm.conditions && !await this.conditionEvaluator.evaluate(
        perm.conditions, request.attributes || {}
      )) {
        continue; // Skip this permission, conditions not met
      }

      return {
        allowed: true,
        matchedRule: `${perm.resource}:${perm.action}`,
        matchedRole: perm.roleName,
      };
    }

    return { allowed: false, reason: 'no_matching_permission' };
  }

  async collectPermissions(
    assignments: UserRoleAssignment[]
  ): Promise<ResolvedPermission[]> {
    const allPermissions: ResolvedPermission[] = [];

    for (const assignment of assignments) {
      const role = await this.roleStore.getRole(assignment.roleId);
      if (!role) continue;

      // Add direct permissions
      allPermissions.push(...role.permissions.map(p => ({
        ...p,
        roleName: role.name,
        hierarchyLevel: 0,
      })));

      // Recursively add parent role permissions
      await this.collectInheritedPermissions(role, allPermissions, 1);
    }

    return allPermissions;
  }

  private async collectInheritedPermissions(
    role: Role,
    collection: ResolvedPermission[],
    level: number
  ): Promise<void> {
    if (!role.parentRoleId || level > 3) return; // Max depth

    const parentRole = await this.roleStore.getRole(role.parentRoleId);
    if (!parentRole) return;

    collection.push(...parentRole.permissions.map(p => ({
      ...p,
      roleName: parentRole.name,
      hierarchyLevel: level,
    })));

    await this.collectInheritedPermissions(parentRole, collection, level + 1);
  }

  private sortPermissionsBySpecificity(
    permissions: ResolvedPermission[],
    action: string,
    resource: string
  ): ResolvedPermission[] {
    return permissions.sort((a, b) => {
      // Compute specificity score (higher = more specific match)
      const scoreA = this.computeSpecificity(a, action, resource);
      const scoreB = this.computeSpecificity(b, action, resource);
      return scoreB - scoreA;
    });
  }

  private computeSpecificity(
    perm: ResolvedPermission,
    action: string,
    resource: string
  ): number {
    let score = 0;

    // Exact resource match is most specific
    if (perm.resource === resource) score += 100;
    else if (perm.resource === '*') score += 0;
    else if (resource.startsWith(perm.resource.replace('*', ''))) score += 50;

    // Exact action match
    if (perm.action === action) score += 50;
    else if (perm.action === '*') score += 0;
    else if (perm.action.replace('*', '') === action) score += 25;

    // Direct permission > inherited
    if (perm.hierarchyLevel === 0) score += 20;

    return score;
  }

  async bulkCheck(requests: PermissionRequest[]): Promise<PermissionResult[]> {
    return Promise.all(requests.map(r => this.check(r)));
  }
}
```

## Caching Strategy

```typescript
class PermissionCache {
  private redis: Redis;

  async get(request: PermissionRequest): Promise<PermissionResult | null> {
    const key = this.buildCacheKey(request);
    const cached = await this.redis.get(key);
    return cached ? JSON.parse(cached) : null;
  }

  async set(request: PermissionRequest, result: PermissionResult): Promise<void> {
    const key = this.buildCacheKey(request);
    await this.redis.setex(key, 60, JSON.stringify(result)); // 60-second TTL
  }

  async invalidateUser(userId: string): Promise<void> {
    const pattern = `perm:${userId}:*`;
    const keys = await this.redis.keys(pattern);
    if (keys.length > 0) {
      await this.redis.del(...keys);
    }
  }

  private buildCacheKey(request: PermissionRequest): string {
    return `perm:${request.userId}:${request.tenantId}:${request.action}:${request.resource}:${request.resourceId || '*'}`;
  }
}
```

## Condition Evaluator

```typescript
class ConditionEvaluator {
  async evaluate(
    conditions: PermissionCondition[],
    attributes: Record<string, unknown>
  ): Promise<boolean> {
    return conditions.every(condition => {
      const attrValue = attributes[condition.attribute];
      if (attrValue === undefined) return false;

      switch (condition.operator) {
        case 'eq': return attrValue === condition.value;
        case 'neq': return attrValue !== condition.value;
        case 'in': return (condition.value as unknown[]).includes(attrValue);
        case 'contains': return String(attrValue).includes(String(condition.value));
        case 'gt': return Number(attrValue) > Number(condition.value);
        case 'lt': return Number(attrValue) < Number(condition.value);
        default: return false;
      }
    });
  }
}
```

## Open-Source Tools

- **Casbin** (Apache 2.0) — Permission evaluation engine with multiple modeling languages
- **node-cache-manager** (MIT) — Multi-layer caching
- **ioredis** (MIT) — Redis client for distributed caching

## Production Considerations

- Warm permission cache on user login to avoid cold-start latency
- Implement cache invalidation on role/permission changes for affected users
- Use Redis Cluster for distributed caching across multiple app instances
- Monitor permission evaluation latency (target <5ms p99)
- Rate-limit permission checks per user to prevent cache flooding attacks
- Log denied requests for security monitoring, but sample them to avoid log flooding
