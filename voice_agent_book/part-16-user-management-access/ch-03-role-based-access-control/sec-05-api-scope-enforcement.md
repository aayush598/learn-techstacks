# API Scope Enforcement

## Overview

API scope enforcement extends RBAC to the API layer, ensuring every request is validated against the caller's granted permissions at the route, parameter, and resource level. This covers API key scoping, route-level guards, parameter-level checks, and resource ownership validation.

## Scope Hierarchy

```
API Key / Token
    └── Scopes (e.g., "agents:read", "calls:*")
         └── Resources (e.g., "agents/agent_123")
              └── Fields (e.g., "agents.name", "agents.phone")
                   └── Operations (read, write, create, delete)
```

## Scope String Format

```typescript
type ScopePattern = `${string}:${string}`;
// Examples:
//   "agents:read"        - Read agents
//   "agents:*"           - All agent operations
//   "agents:read,write"  - Read and write agents
//   "calls:create"       - Create calls
//   "*:read"             - Read everything
//   "*:*"                - Full access

interface Scope {
  resource: string;
  actions: string[];
  restrictions?: ScopeRestriction[];
}

interface ScopeRestriction {
  field?: string;         // E.g., "phone", "billing_info"
  operator: 'eq' | 'in' | 'subset';
  value: unknown;
}

function parseScope(scope: string): Scope {
  const [resource, actionsStr] = scope.split(':');
  const actions = actionsStr.split(',').map(a => a.trim());

  return { resource, actions };
}

function matchScope(required: Scope, granted: Scope): boolean {
  // Wildcard match
  if (granted.resource === '*' || granted.resource === required.resource) {
    if (granted.actions.includes('*')) return true;
    return required.actions.every(a => granted.actions.includes(a));
  }
  return false;
}
```

## Route-Level Guard

```typescript
interface RouteScopeConfig {
  method: string;
  path: string;
  requiredScope: string;
  resourceType?: string;
  resourceIdParam?: string;
}

const ROUTE_SCOPE_MAP: RouteScopeConfig[] = [
  // Agent routes
  { method: 'GET', path: '/v1/agents', requiredScope: 'agents:read' },
  { method: 'POST', path: '/v1/agents', requiredScope: 'agents:create' },
  { method: 'GET', path: '/v1/agents/:id', requiredScope: 'agents:read', resourceType: 'agent', resourceIdParam: 'id' },
  { method: 'PATCH', path: '/v1/agents/:id', requiredScope: 'agents:write', resourceType: 'agent', resourceIdParam: 'id' },
  { method: 'DELETE', path: '/v1/agents/:id', requiredScope: 'agents:delete', resourceType: 'agent', resourceIdParam: 'id' },
  { method: 'POST', path: '/v1/agents/:id/deploy', requiredScope: 'agents:deploy' },

  // Call routes
  { method: 'GET', path: '/v1/calls', requiredScope: 'calls:read' },
  { method: 'POST', path: '/v1/calls', requiredScope: 'calls:create' },

  // Campaign routes
  { method: 'GET', path: '/v1/campaigns', requiredScope: 'campaigns:read' },
  { method: 'POST', path: '/v1/campaigns', requiredScope: 'campaigns:create' },
  { method: 'POST', path: '/v1/campaigns/:id/start', requiredScope: 'campaigns:start' },

  // Admin routes
  { method: 'GET', path: '/v1/users', requiredScope: 'users:read' },
  { method: 'POST', path: '/v1/users', requiredScope: 'users:create' },
  { method: 'GET', path: '/v1/billing', requiredScope: 'billing:read' },
];
```

## Dynamic Scope Middleware

```typescript
function scopeGuard(scopeMap: RouteScopeConfig[]) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;
    if (!user) return res.status(401).json({ error: 'Unauthorized' });

    // Find matching route config
    const routeConfig = findMatchingRoute(req.method, req.path, scopeMap);
    if (!routeConfig) {
      return next(); // No scope requirement = allow
    }

    // Check basic scope
    const grantedScopes = user.apiKey?.scopes || user.permissions || [];
    const requiredScope = parseScope(routeConfig.requiredScope);

    const hasScope = grantedScopes.some((s: string) =>
      matchScope(requiredScope, parseScope(s))
    );

    if (!hasScope) {
      return res.status(403).json({
        error: 'Insufficient scope',
        required: routeConfig.requiredScope,
      });
    }

    // Resource ownership check
    if (routeConfig.resourceIdParam) {
      const resourceId = req.params[routeConfig.resourceIdParam];
      if (resourceId) {
        const isOwner = await checkResourceOwnership(
          user,
          routeConfig.resourceType!,
          resourceId
        );

        if (!isOwner && !userHasTenantScope(user)) {
          return res.status(403).json({
            error: 'Resource access denied',
            resource: routeConfig.resourceType,
          });
        }
      }
    }

    next();
  };
}

function findMatchingRoute(
  method: string,
  path: string,
  scopeMap: RouteScopeConfig[]
): RouteScopeConfig | undefined {
  return scopeMap.find(config => {
    if (config.method !== method) return false;
    const pattern = config.path.replace(/:(\w+)/g, '([^/]+)');
    const regex = new RegExp(`^${pattern}$`);
    return regex.test(path);
  });
}
```

## Parameter-Level Access Control

```typescript
interface FieldLevelAccess {
  resourceType: string;
  fields: Record<string, 'read' | 'write' | 'none'>;
}

class FieldLevelAccessControl {
  private fieldPermissions: Map<string, FieldLevelAccess>;

  constructor() {
    this.fieldPermissions = new Map();
    this.initializeDefaults();
  }

  private initializeDefaults(): void {
    // Agents resource field-level access
    this.fieldPermissions.set('agents', {
      resourceType: 'agents',
      fields: {
        id: 'read',
        name: 'read',
        phone: 'read',
        email: 'read',
        status: 'read',
        // Sensitive fields
        api_key: 'none',
        billing_plan: 'none',
        payment_method: 'none',
        call_recordings: 'read',  // Restricted by separate permission
      },
    });
  }

  filterResponseFields<T extends Record<string, unknown>>(
    user: User,
    resourceType: string,
    data: T,
    operation: 'read' | 'write'
  ): Partial<T> {
    const access = this.fieldPermissions.get(resourceType);
    if (!access) return data;

    const filtered: Record<string, unknown> = {};
    const userPermissions = getUserPermissions(user);

    for (const [field, value] of Object.entries(data)) {
      const fieldPerm = access.fields[field];
      if (!fieldPerm) {
        // Unknown field - block by default
        continue;
      }

      if (fieldPerm === 'none') {
        // Check if user has explicit permission for this field
        const hasFieldPermission = userPermissions.some(
          (p: string) => p === `${resourceType}:${field}:${operation}` ||
                         p === `${resourceType}:sensitive:*`
        );
        if (!hasFieldPermission) continue;
      }

      filtered[field] = value;
    }

    return filtered as Partial<T>;
  }
}
```

## Resource Ownership Validation

```typescript
async function checkResourceOwnership(
  user: User,
  resourceType: string,
  resourceId: string
): Promise<boolean> {
  const resource = await resourceRegistry.getResource(resourceType, resourceId);
  if (!resource) return false;

  // Direct ownership
  if (resource.ownerId === user.id) return true;

  // Team-level access (resource belongs to user's team)
  if (resource.teamId && user.teamIds.includes(resource.teamId)) return true;

  // Department-level access
  if (resource.departmentId && user.departmentIds.includes(resource.departmentId)) return true;

  return false;
}

function userHasTenantScope(user: User): boolean {
  return user.roles.some(r =>
    ['admin', 'developer', 'manager'].includes(r)
  );
}
```

## Subscription Data Filtering

```typescript
class SubscriptionDataFilter {
  filterByAccessLevel<T extends Record<string, unknown>>(
    user: User,
    subscriptionId: string,
    data: T
  ): Partial<T> {
    const subscriptionAccess = user.subscriptionAccess || {};

    if (subscriptionAccess.role === 'billing_admin') {
      return data; // Full access to billing data
    }

    if (subscriptionAccess.role === 'viewer') {
      // Only show aggregate/read-only billing data
      const { payment_method, invoices, ...rest } = data as any;
      return { ...rest, payment_method: '***' } as Partial<T>;
    }

    return {}; // No billing access
  }
}
```

## Open-Source Tools

- **casbin** (Apache 2.0) — Scope matching and enforcement
- **express-routescan** (MIT) — Route-to-scope mapping generation

## Production Considerations

- Maintain a route-scope registry that's checked at application startup for completeness
- Log scope denials with the required scope information for debugging
- Cache resource ownership lookups in Redis with 30-second TTL
- Test scope enforcement with an automated probe that validates each route independently
- Apply field-level filtering at the serialization layer, not in business logic
- Support wildcard scope expansion (e.g., `campaigns:*` expands to all campaign actions)
