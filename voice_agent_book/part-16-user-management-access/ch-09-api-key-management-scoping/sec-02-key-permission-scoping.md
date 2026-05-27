# Key Permission Scoping

## Overview

API key scoping restricts what resources and actions a key can access. Scopes follow a resource:action pattern and can be limited to specific resources using resource-level restrictions.

## Scope Model

```typescript
interface ApiKeyScope {
  resource: string;       // e.g., "agents", "calls", "campaigns"
  actions: string[];      // e.g., ["read", "create"]
  restrictions?: ScopeRestriction[];
}

interface ScopeRestriction {
  type: 'resource_id' | 'team_id' | 'department_id' | 'attribute';
  field: string;
  operator: 'eq' | 'in' | 'contains';
  value: string | string[];
}

class ApiKeyScopeService {
  async validateScope(apiKey: StoredApiKey, requiredAction: string, requiredResource: string, resourceId?: string): Promise<boolean> {
    for (const scope of apiKey.scopes) {
      const scopeParts = scope.split(':');
      const [scopeResource, scopeActions] = [scopeParts[0], scopeParts[1] || ''];

      const resourceMatch = scopeResource === '*' || scopeResource === requiredResource;
      const actionMatch = scopeActions === '*' || scopeActions.split(',').includes(requiredAction);

      if (resourceMatch && actionMatch) return true;
    }

    return false;
  }
}
```

## Scope Patterns

```
agents:read             - Read agents only
agents:read,write       - Read and write agents
calls:*                 - All call operations
campaigns:read          - Read campaigns only
*:read                  - Read everything
team:sales:agents:read  - Read agents in sales team
```

## Open-Source Tools

- **Casbin** (Apache 2.0) — Scope-based authorization
- **Permit.io** (Apache 2.0) — Fine-grained API scoping

## Production Considerations

- Default-deny: keys have no scopes until explicitly granted
- Max 20 scopes per key to prevent complexity
- Scopes are additive (union of all scopes)
- Support wildcard and prefix matching for scopes
- Audit scope changes with before/after comparison
- Validate scopes against available resource types
- Allow scope templates for common patterns
