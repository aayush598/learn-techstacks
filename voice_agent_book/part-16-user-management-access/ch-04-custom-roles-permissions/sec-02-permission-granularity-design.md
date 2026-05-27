# Permission Granularity Design

## Overview

Permission granularity defines the level of detail at which access controls operate. From coarse (full module access) to fine-grained (field-level read/write), the design choices affect security posture, administrative complexity, and system performance.

## Granularity Levels

```
Level 1: Module Access
  agents:read          → Can access the Agents module (read-only)
  agents:write         → Can modify anything in Agents

Level 2: Resource Access
  agents:read          → Can read agent list
  agents:read:detail   → Can read agent details
  agents:create        → Can create new agents
  agents:update        → Can update existing agents  
  agents:delete        → Can delete agents

Level 3: Resource + Field Access
  agents:read:name     → Can read agent name
  agents:read:phone    → Can read agent phone number
  agents:read:api_key  → Cannot read API key (denied explicitly)

Level 4: Scoped Resource Access
  agents:read:team     → Can read agents in own team
  agents:read:dept     → Can read agents in own department
  agents:read:tenant   → Can read all agents in tenant

Level 5: Conditional Access
  agents:read           → Can read agents only if:
    condition: status == 'active' AND created_by == current_user
```

## Granularity Decision Framework

```typescript
interface GranularityDecision {
  resourceType: string;
  level: 1 | 2 | 3 | 4 | 5;
  fields: string[];        // Fields to expose at this granularity
  sensitiveFields: string[]; // Fields requiring Level 3+
  defaultActions: string[];

  rationale: {
    security: string;      // Security justification
    usability: string;     // UX impact
    performance: string;   // Performance considerations
  };
}

const GRANULARITY_DECISIONS: Record<string, GranularityDecision> = {
  agents: {
    resourceType: 'agents',
    level: 2,              // Resource-level access
    fields: ['name', 'email', 'phone', 'status', 'createdAt'],
    sensitiveFields: ['api_key', 'billing_plan', 'payment_method'],
    defaultActions: ['read', 'create', 'update'],
    rationale: {
      security: 'Agent configuration contains sensitive keys and billing data',
      usability: 'Most users only need read/create on agents',
      performance: 'Field-level filtering adds ~2ms overhead per request',
    },
  },
  calls: {
    resourceType: 'calls',
    level: 4,              // Scoped resource access
    fields: ['id', 'status', 'duration', 'transcript', 'recording'],
    sensitiveFields: ['recording', 'transcript'],
    defaultActions: ['read', 'create'],
    rationale: {
      security: 'Call recordings contain PII and require strict scoping',
      usability: 'Agents should only see their own calls',
      performance: 'Scope filtering is index-covered',
    },
  },
  reports: {
    resourceType: 'reports',
    level: 2,
    fields: ['name', 'type', 'data', 'schedule'],
    sensitiveFields: [],
    defaultActions: ['read', 'create', 'export'],
    rationale: {
      security: 'Reports contain aggregated data, limited sensitivity',
      usability: 'Managers need full report access',
      performance: 'No field-level overhead',
    },
  },
};
```

## Field-Level Access Control

```typescript
class FieldLevelAccess {
  private fieldPermissions: Map<string, FieldAccessDef>;

  constructor() {
    this.fieldPermissions = new Map();
    this.registerDefaultFields();
  }

  registerField(resource: string, field: string, sensitivity: 'public' | 'internal' | 'sensitive' | 'restricted'): void {
    const key = `${resource}:${field}`;
    this.fieldPermissions.set(key, { resource, field, sensitivity });

    if (sensitivity === 'sensitive' || sensitivity === 'restricted') {
      this.registerSensitiveAccessPermission(resource, field);
    }
  }

  canAccessField(user: User, resource: string, field: string, operation: 'read' | 'write'): boolean {
    const def = this.fieldPermissions.get(`${resource}:${field}`);
    if (!def) return false;

    switch (def.sensitivity) {
      case 'public':
        return true;
      case 'internal':
        return user.roles.some(r => ['admin', 'manager', 'developer'].includes(r));
      case 'sensitive':
        return user.permissions.includes(`${resource}:${field}:${operation}`) ||
               user.permissions.includes(`${resource}:sensitive:*`);
      case 'restricted':
        return user.permissions.includes(`${resource}:${field}:${operation}`);
      default:
        return false;
    }
  }

  filterFields<T extends Record<string, unknown>>(
    user: User,
    resource: string,
    data: T,
    operation: 'read' | 'write'
  ): Partial<T> {
    const result: Record<string, unknown> = {};

    for (const [field, value] of Object.entries(data)) {
      if (this.canAccessField(user, resource, field, operation)) {
        result[field] = value;
      }
    }

    return result as Partial<T>;
  }
}
```

## Performance Considerations

```typescript
interface GranularityPerformance {
  level1: { overhead: '0-1ms', cacheable: true, storage: 'minimal' };
  level2: { overhead: '1-3ms', cacheable: true, storage: 'low' };
  level3: { overhead: '3-8ms', cacheable: 'partial', storage: 'medium' };
  level4: { overhead: '2-5ms', cacheable: true, storage: 'low' };
  level5: { overhead: '5-20ms', cacheable: 'depends', storage: 'high' };
}

// Strategies to minimize overhead
class GranularityOptimizer {
  // Pre-compute effective field access for a user session
  async computeFieldAccessMap(user: User): Promise<Map<string, Set<string>>> {
    const accessMap = new Map<string, Set<string>>();
    const start = Date.now();

    for (const [resource, def] of GRANULARITY_DECISIONS) {
      const accessible = new Set<string>();

      for (const field of def.fields) {
        if (this.canAccessField(user, resource, field, 'read')) {
          accessible.add(field);
        }
      }

      accessMap.set(resource, accessible);
    }

    const duration = Date.now() - start;
    metrics.record('field_access_compute_ms', duration);

    return accessMap;
  }
}
```

## Open-Source Tools

- **Casbin** (Apache 2.0) — Supports field-level ABAC (Attribute-Based Access Control)
- **Permit.io** (Apache 2.0) — Fine-grained permissions with field-level ReBAC

## Production Considerations

- Start coarse and add granularity only where security requirements demand it
- Profile field-level filtering overhead; batch field access checks for lists
- Document granularity decisions in a central permission catalog
- Allow tenant admins to choose their desired granularity level per resource
- Provide migration path between granularity levels as needs evolve
- Cache computed field access maps per user session to reduce per-request overhead
- Audit and log sensitive field access for compliance (e.g., financial or health data)
