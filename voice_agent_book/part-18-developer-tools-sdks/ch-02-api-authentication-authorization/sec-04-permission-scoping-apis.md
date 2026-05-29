# Section 04: Permission Scoping for APIs

## Overview

Permission scopes define what actions an API credential can perform. Scopes are strings following the `resource:action` pattern — `agents:read`, `calls:write`, `campaigns:*`. The permission system supports wildcard scopes, resource-level restrictions, and scope intersection during authorization. Both API keys and OAuth2 tokens resolve to the same scope structure.

## Architecture

```
Scope Design
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scope Syntax:
  {resource}:{action}[:{constraint}]

Resources:
  agents     → Agent CRUD and deployment
  calls      → Call management and monitoring
  campaigns  → Campaign management
  analytics  → Analytics data access
  webhooks   → Webhook configuration
  transcripts → Transcription access
  recordings → Recording access

Actions:
  read      → Read/list resources
  write     → Create/update resources
  delete    → Delete resources
  admin     → All actions on resource

Examples:
  agents:read            → List and get agents
  calls:write            → Create and update calls
  campaigns:*           → All campaign actions
  agents:read:ag_12345  → Read specific agent only
  analytics:read:realtime → Analytics with constraint

Authorization Flow:
  [Request] → [Auth Middleware] → [Scope Validation]
                                      │
  Required: agents:write              │
  Token has: agents:*                 │
  Result: ✓ Match (wildcard)          │
                                      │
  Required: agents:delete             │
  Token has: agents:read,agents:write │
  Result: ✗ No match                  │
```

## Design Decisions

- **Resource:Action Pattern**: Simple, predictable, and scalable — easy to add new resources and actions
- **Wildcard Scopes**: `agents:*` grants all actions on agents; `*:*` is full access (root scope)
- **Resource-Level Constraints**: Scopes can restrict to specific resource instances — `agents:read:ag_12345`
- **Scope Intersection**: Final permission is the intersection of all token scopes and any API key restrictions

## Implementation Approach

```typescript
// Scope definitions
interface Scope {
  resource: string;
  action: string;
  constraint?: string;
}

interface PermissionCheck {
  allowed: boolean;
  matchedScope?: string;
  reason?: string;
}

class ScopeValidator {
  // Parse scope string into components
  parse(scopeString: string): Scope {
    const parts = scopeString.split(':');

    return {
      resource: parts[0] || '',
      action: parts[1] || '',
      constraint: parts[2],
    };
  }

  // Check if a set of scopes grants a required permission
  check(scopes: string[], required: string): PermissionCheck {
    const requiredScope = this.parse(required);

    for (const scopeStr of scopes) {
      if (this.scopeMatches(scopeStr, requiredScope)) {
        return { allowed: true, matchedScope: scopeStr };
      }
    }

    return { allowed: false, reason: `Missing required scope: ${required}` };
  }

  // Check if a scope string matches a required scope
  private scopeMatches(scopeStr: string, required: Scope): boolean {
    const granted = this.parse(scopeStr);

    // Full wildcard
    if (granted.resource === '*' && granted.action === '*') {
      return true;
    }

    // Resource wildcard
    if (granted.resource !== '*' && granted.resource !== required.resource) {
      return false;
    }

    // Action wildcard or exact match
    if (granted.action !== '*' && granted.action !== required.action) {
      return false;
    }

    // Constraint check — if no constraint required, any level works
    if (required.constraint && granted.constraint) {
      return granted.constraint === required.constraint;
    }

    return true;
  }

  // Filter resources by scope constraints
  filterByScope<T extends { id: string }>(
    items: T[],
    scopes: string[],
    resource: string,
  ): T[] {
    const resourceScopes = scopes
      .map(s => this.parse(s))
      .filter(s => s.resource === resource || s.resource === '*');

    const hasWildcard = resourceScopes.some(s => !s.constraint);

    if (hasWildcard) {
      return items; // Full access
    }

    // Constraint-based filtering
    const allowedIds = resourceScopes
      .filter(s => s.constraint)
      .map(s => s.constraint!);

    return items.filter(item => allowedIds.includes(item.id));
  }
}

// Authorization middleware factory
function requireScope(...requiredScopes: string[]) {
  return async (c: Context, next: Next) => {
    const authContext: AuthContext = c.get('authContext');

    const validator = new ScopeValidator();

    for (const scope of requiredScopes) {
      const result = validator.check(authContext.scopes, scope);
      if (!result.allowed) {
        throw new ForbiddenError(result.reason || 'Insufficient permissions');
      }
    }

    await next();
  };
}

// Route usage
app.get('/v1/agents',
  authenticate(validator),
  requireScope('agents:read'),
  agentsController.list,
);

app.post('/v1/agents',
  authenticate(validator),
  requireScope('agents:write'),
  agentsController.create,
);

app.delete('/v1/agents/:id',
  authenticate(validator),
  requireScope('agents:delete'),
  agentsController.delete,
);
```

## Integration Points

- **API Key Management**: Key creation UI allows scope selection — presented as checkboxes grouped by resource
- **OAuth2 Consent**: Scope list displayed during OAuth2 authorization consent screen
- **SDK**: Scopes are enforced client-side for early feedback; server-side is authoritative

## Production Considerations

- **Least Privilege**: New API keys default to minimal scopes; users must explicitly request elevated access
- **Scope Audit**: Track scope usage patterns to detect unused scopes and suggest reduction
- **Scope Documentation**: Every endpoint in the OpenAPI spec documents required scopes
- **Temporary Scope Elevation**: Support time-bound scope grants for emergency access with automatic revocation

## Open-Source Tools

- **CASL**: Ability-based authorization library compatible with scope patterns
