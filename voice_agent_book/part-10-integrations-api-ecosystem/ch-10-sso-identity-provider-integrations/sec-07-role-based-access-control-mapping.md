# Section 07: Role-Based Access Control Mapping

## Overview

Role-Based Access Control (RBAC) mapping translates identity provider group memberships and roles into the platform's internal permission model. When a user authenticates via SSO (SAML or OIDC), the RBAC mapping engine takes the groups and roles from the IdP assertion, maps them to platform roles and permissions, and applies the appropriate access controls for the user's session. This ensures that enterprise customers can manage platform access entirely from their identity provider.

The RBAC mapping supports multiple mapping strategies: direct group-to-role mapping (IdP group "VoiceAgent-Admins" maps to platform "admin" role), attribute-based mapping (users with department="Engineering" get "developer" role), and claims-based mapping (specific SAML/OIDC claims determine permissions). The mapping engine evaluates all applicable mappings and computes the union of permissions for each user.

## Architecture

```
                 RBAC Mapping Architecture

   IdP → RBAC Engine → Permission Evaluator → Resource Access
              |
   +----------------------------------------------------------+
   |              RBAC Mapping Components                    |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Mapping Registry |  | Identity Source    |            |
   |  | • Group → Role   |  | • SAML attributes  |            |
   |  | • Attribute →    |  | • OIDC claims      |            |
   |  |   Role           |  | • SCIM groups      |            |
   |  | • Claim →        |  +-------------------+            |
   |  |   Permission     |                                   |
   |  +------------------+                                   |
   |  +------------------+  +-------------------+            |
   |  | Role Hierarchy   |  | Permission        |             |
   |  | • Inheritance    |  | Evaluation        |            |
   |  | • Role merging   |  | • Role →            |            |
   |  | • Precedence     |  |   permissions     |            |
   |  |   rules          |  | • Resource-level  |            |
   |  +------------------+  |   scoping         |            |
   |  +------------------+  +-------------------+            |
   |  | Audit Trail      |  | Mapping UI        |             |
   |  | • User → Role    |  | • Create mapping  |            |
   |  |   history        |  | • Test mapping    |            |
   |  | • Mapping        |  | • Conflict detect |            |
   |  |   changes        |  +-------------------+            |
   |  | • Permission     |                                    |
   |  |   grants         |                                    |
   |  +------------------+                                    |
   +----------------------------------------------------------+
```

## Design Decisions

- **Explicit mapping rules over dynamic role computation:** All role mappings are explicitly defined by the tenant admin through a mapping configuration interface. There is no automatic role inference — an IdP group only grants platform roles if there is an explicit mapping rule. This prevents accidental privilege escalation from IdP-side group name changes. Mapping rules include a source (SAML attribute, OIDC claim, or SCIM group), a matcher (exact match, regex, prefix), and a target platform role. Trade-off: explicit mapping requires admin effort to configure but provides security and predictability.

- **Role hierarchy with permission inheritance over flat role assignments:** Platform roles follow a hierarchical model (superadmin > admin > manager > agent > viewer) where higher roles inherit permissions from lower roles. A mapping to "admin" automatically includes all "agent" and "viewer" permissions. This simplifies mapping configuration — the admin only maps top-level roles and inheritance handles the rest. Trade-off: role hierarchies require careful design to avoid permission gaps or excessive inheritance but reduce the number of mapping rules needed.

- **Resource-level scoping via role constraints over global-only roles:** In addition to role assignment, the RBAC system supports resource-level scoping constraints. A user might have the "agent" role but scoped to "department=sales" — they can only access resources belonging to the sales department. Scoping rules are defined as key-value pairs in the mapping configuration (e.g., `constraints: { department: '{idp.department}' }`). Variables in curly braces are resolved from IdP attributes. Trade-off: scoping adds complexity to permission evaluation but enables fine-grained access control without role proliferation.

## Implementation Approach

```
interface RBACMappingRule {
  id: string;
  tenantId: string;
  name: string;
  priority: number;
  source: {
    type: 'saml_attribute' | 'oidc_claim' | 'scim_group';
    attribute: string;      // e.g., "groups" or "department"
    matcher: {
      type: 'exact' | 'prefix' | 'regex' | 'all';
      value: string;        // e.g., "VoiceAgent-Admins" or "admin-*"
    };
  };
  target: {
    role: string;           // Platform role name
    constraints?: Record<string, string>;  // Resource scoping
  };
}

interface ResolvedRole {
  roleName: string;
  permissions: string[];
  constraints: Record<string, string>;
  sourceRule: string;
}

class RBACMapper {
  private roleRegistry: RoleRegistry;

  async resolveUserRoles(tenantId: string, identity: IdentityData): Promise<ResolvedRole[]> {
    const mappings = await this.db.rbacMappings.find({ tenantId });

    const resolved: ResolvedRole[] = [];

    for (const mapping of mappings.sort((a, b) => a.priority - b.priority)) {
      const matched = this.evaluateMatcher(mapping.source, identity);
      if (!matched) continue;

      const role = this.roleRegistry.getRole(mapping.target.role);
      if (!role) {
        logger.warn('RBAC mapping references unknown role', { mappingId: mapping.id, role: mapping.target.role });
        continue;
      }

      // Resolve constraints with variable substitution
      const constraints: Record<string, string> = {};
      for (const [key, valueTemplate] of Object.entries(mapping.target.constraints || {})) {
        constraints[key] = this.resolveVariables(valueTemplate, identity.attributes);
      }

      resolved.push({
        roleName: role.name,
        permissions: this.getInheritedPermissions(role),
        constraints,
        sourceRule: mapping.id,
      });
    }

    return this.mergeRoles(resolved);
  }

  private evaluateMatcher(source: RBACMappingRule['source'], identity: IdentityData): boolean {
    let value: any = identity.attributes[source.attribute];

    if (!value) return false;
    if (!Array.isArray(value)) value = [value];

    for (const v of value) {
      switch (source.matcher.type) {
        case 'exact':
          if (v === source.matcher.value) return true;
          break;
        case 'prefix':
          if (v.startsWith(source.matcher.value)) return true;
          break;
        case 'regex':
          if (new RegExp(source.matcher.value).test(v)) return true;
          break;
        case 'all':
          return true;
      }
    }

    return false;
  }

  private resolveVariables(template: string, attributes: Record<string, any>): string {
    return template.replace(/\{([^}]+)\}/g, (_, key) => {
      const value = attributes[key];
      return value !== undefined ? String(value) : `{${key}}`;
    });
  }

  private mergeRoles(resolved: ResolvedRole[]): ResolvedRole[] {
    // Merge roles: combine permissions, deduplicate, keep highest priority role
    const merged = new Map<string, ResolvedRole>();

    for (const role of resolved) {
      const existing = merged.get(role.roleName);
      if (!existing) {
        merged.set(role.roleName, { ...role });
      } else {
        // Merge constraints (later rules override earlier)
        existing.constraints = { ...existing.constraints, ...role.constraints };
      }
    }

    return Array.from(merged.values());
  }

  private getInheritedPermissions(role: Role): string[] {
    const permissions = new Set<string>(role.permissions);
    let parent = role.parentRole;

    while (parent) {
      const parentRole = this.roleRegistry.getRole(parent);
      if (!parentRole) break;
      parentRole.permissions.forEach(p => permissions.add(p));
      parent = parentRole.parentRole;
    }

    return Array.from(permissions);
  }

  checkPermission(permissions: string[], requiredPermission: string): boolean {
    // Direct match or wildcard support
    return permissions.some(p =>
      p === requiredPermission ||
      p.endsWith(':*') && requiredPermission.startsWith(p.slice(0, -2))
    );
  }

  checkScopedPermission(
    permissions: string[],
    constraints: Record<string, string>,
    resource: ResourceContext
  ): boolean {
    if (!this.checkPermission(permissions, resource.requiredPermission)) {
      return false;
    }

    // Check constraints
    for (const [key, value] of Object.entries(constraints)) {
      if (resource.attributes[key] !== value) {
        return false;
      }
    }

    return true;
  }
}

// Example mapping configurations
const EXAMPLE_MAPPINGS: RBACMappingRule[] = [
  {
    id: 'm1',
    tenantId: 'tenant_abc',
    name: 'Admin group → Admin role',
    priority: 100,
    source: {
      type: 'saml_attribute',
      attribute: 'groups',
      matcher: { type: 'exact', value: 'VoiceAgent-Admins' },
    },
    target: { role: 'admin' },
  },
  {
    id: 'm2',
    tenantId: 'tenant_abc',
    name: 'Agent group → Agent role with department scope',
    priority: 200,
    source: {
      type: 'saml_attribute',
      attribute: 'groups',
      matcher: { type: 'prefix', value: 'VoiceAgent-' },
    },
    target: {
      role: 'agent',
      constraints: { department: '{department}' },
    },
  },
  {
    id: 'm3',
    tenantId: 'tenant_abc',
    name: 'All authenticated users → Viewer role',
    priority: 999,
    source: {
      type: 'saml_attribute',
      attribute: 'sub',
      matcher: { type: 'all', value: '' },
    },
    target: { role: 'viewer' },
  },
];
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| CASL (MIT) | Node.js | Permission management library |
| Zod (MIT) | Validation | Mapping rule validation |

## Production Considerations

**Scaling:** RBAC mapping evaluation happens on every user session creation and optionally on every API request (for resource-level authorization). Cache resolved roles in the session store (JWT or Redis) to avoid re-evaluating mappings on every request. Mapping rules are stored in the database and cached in memory with 5-minute TTL. Mapping changes take effect within the cache TTL — for immediate effect, invalidate user sessions.

**Security:** Always apply the principle of least privilege — the default mapping for unauthenticated or unknown groups should be the most restrictive role (viewer). Priority-based evaluation ensures specific mappings override catch-all mappings. Audit all mapping changes with admin identity and timestamp. Implement a mapping test tool that lets admins simulate a user's resolved roles based on test identity attributes.

**Monitoring:** Track RBAC mapping evaluation counts, role distribution (how many users have each role), mapping-to-role resolution rates, unmapped users (users with no matching mapping), and constraint evaluation results. Alert on users with no resolved roles (they will have no access), mapping rule conflicts, and sudden changes in role distribution that may indicate configuration errors.
