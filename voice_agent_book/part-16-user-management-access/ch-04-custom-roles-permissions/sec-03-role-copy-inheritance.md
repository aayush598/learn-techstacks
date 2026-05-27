# Role Copy & Inheritance

## Overview

Role copy and inheritance enables efficient creation of new roles by cloning existing configurations. The inherit-and-override pattern allows roles to derive permissions from a parent role while customizing specific areas, reducing administrative overhead and ensuring consistency.

## Inheritance Patterns

```
Pattern 1: Direct Clone
  Source: Agent → Clone → Senior Agent (fully independent copy)

Pattern 2: Parent Inheritance
  Base: Agent (parent)
    ├── Senior Agent (inherits agent + overrides)
    │   ├── Override: add "campaigns:read"  
    │   └── Override: increase call limit to 10
    └── Quality Analyst (inherits agent + overrides)
        ├── Override: add "calls:read" for all agents
        └── Override: add "transcripts:export"

Pattern 3: Multi-Level Inheritance
  Base: Viewer
    └── Report Viewer (inherits viewer + override)
        └── Advanced Report Viewer (inherits Report Viewer + override)
```

## Implementation

```typescript
interface RoleCloneOptions {
  sourceRoleId: string;
  newName: string;
  newDescription?: string;
  cloneType: 'copy' | 'inherit';
  permissionOverrides?: PermissionOverride[];
  scopeOverrides?: ScopeOverride[];
  restrictionOverrides?: RestrictionOverride[];
  copyMetadata?: boolean;
}

interface PermissionOverride {
  resource: string;
  action: string;
  mode: 'add' | 'remove' | 'override';
  value: boolean;
  effect: 'allow' | 'deny';
}

class RoleCloneService {
  async cloneRole(tenantId: string, options: RoleCloneOptions): Promise<Role> {
    const sourceRole = await this.roleStore.getRole(options.sourceRoleId);
    if (!sourceRole) throw new Error('Source role not found');

    const newRole: Role = {
      id: generateId('role'),
      tenantId,
      name: options.newName,
      description: options.newDescription || `Clone of ${sourceRole.name}`,
      roleType: 'custom',
      isBuiltin: false,
      parentRoleId: options.cloneType === 'inherit' ? sourceRole.id : undefined,
      createdAt: new Date(),
    };

    if (options.cloneType === 'copy') {
      newRole.permissions = this.clonePermissions(sourceRole.permissions);
      newRole.resourceScopes = [...sourceRole.resourceScopes];
      newRole.restrictions = sourceRole.restrictions ? [...sourceRole.restrictions] : undefined;
    } else {
      // Inheritance: only store overrides, reference parent for base permissions
      newRole.permissions = this.applyPermissionOverrides(
        sourceRole.permissions,
        options.permissionOverrides || []
      );
      newRole.resourceScopes = this.applyScopeOverrides(
        sourceRole.resourceScopes,
        options.scopeOverrides || []
      );
    }

    await this.db.insert('roles', newRole);
    await this.invalidatePermissionCache(tenantId);

    return newRole;
  }

  private clonePermissions(permissions: RolePermission[]): RolePermission[] {
    return permissions.map(p => ({ ...p }));
  }

  private applyPermissionOverrides(
    basePermissions: RolePermission[],
    overrides: PermissionOverride[]
  ): RolePermission[] {
    const result = [...basePermissions];

    for (const override of overrides) {
      const existingIndex = result.findIndex(
        p => p.resource === override.resource && p.action === override.action
      );

      switch (override.mode) {
        case 'add':
          if (existingIndex >= 0) {
            result[existingIndex].effect = override.effect;
          } else {
            result.push({
              resource: override.resource,
              action: override.action,
              effect: override.effect,
            });
          }
          break;
        case 'remove':
          if (existingIndex >= 0) {
            result.splice(existingIndex, 1);
          }
          break;
        case 'override':
          if (existingIndex >= 0) {
            result[existingIndex] = {
              ...result[existingIndex],
              effect: override.effect,
            };
          }
          break;
      }
    }

    return result;
  }

  async getEffectivePermissions(roleId: string): Promise<RolePermission[]> {
    const role = await this.roleStore.getRole(roleId);
    if (!role) return [];

    // If role has a parent, merge inheritance chain
    if (role.parentRoleId) {
      const parentPermissions = await this.getEffectivePermissions(role.parentRoleId);
      return this.mergePermissions(parentPermissions, role.permissions);
    }

    return role.permissions;
  }

  private mergePermissions(
    parent: RolePermission[],
    child: RolePermission[]
  ): RolePermission[] {
    const merged = new Map<string, RolePermission>();

    // Add parent permissions
    for (const perm of parent) {
      const key = `${perm.resource}:${perm.action}`;
      merged.set(key, perm);
    }

    // Child overrides (with higher priority)
    for (const perm of child) {
      const key = `${perm.resource}:${perm.action}`;
      if (perm.mode === 'remove') {
        merged.delete(key);
      } else {
        merged.set(key, { ...perm, inheritedFrom: undefined });
      }
    }

    return Array.from(merged.values());
  }
}
```

## Versioning & Change Propagation

```typescript
interface InheritedRoleChange {
  roleId: string;
  parentRoleId: string;
  changeType: 'permission_added' | 'permission_removed' | 'permission_modified';
  resource: string;
  action: string;
  timestamp: Date;
  applied: boolean;
}

class InheritanceChangePropagator {
  async propagateParentChange(parentRoleId: string, change: RoleChange): Promise<void> {
    // Find all roles inheriting from this parent
    const childRoles = await this.db.find('roles', {
      parentRoleId,
      tenantId: change.tenantId,
    });

    const results: InheritedRoleChange[] = [];

    for (const childRole of childRoles) {
      const effectivePerms = await this.roleCloneService.getEffectivePermissions(childRole.id);

      // Check if child has explicit override that conflicts
      const childOverride = childRole.permissions.find(
        p => p.resource === change.resource && p.action === change.action
      );

      if (childOverride) {
        // Child has explicit override - skip propagation
        results.push({
          roleId: childRole.id,
          parentRoleId,
          changeType: this.mapChangeType(change),
          resource: change.resource,
          action: change.action,
          timestamp: new Date(),
          applied: false, // Skipped due to override
        });
      } else {
        // No override - automatically propagate
        results.push({
          roleId: childRole.id,
          parentRoleId,
          changeType: this.mapChangeType(change),
          resource: change.resource,
          action: change.action,
          timestamp: new Date(),
          applied: true,
        });
      }
    }

    // Log propagation results
    await this.auditLog.record({
      action: 'role.inheritance_propagation',
      target: { parentRoleId },
      metadata: { changes: results, childCount: childRoles.length },
    });
  }

  async getInheritanceTree(roleId: string): Promise<InheritanceNode> {
    const role = await this.roleStore.getRole(roleId);
    const children = await this.db.find('roles', { parentRoleId: roleId });

    return {
      role: role!,
      children: await Promise.all(
        children.map(c => this.getInheritanceTree(c.id))
      ),
    };
  }
}

interface InheritanceNode {
  role: Role;
  children: InheritanceNode[];
}
```

## UI for Inheritance Visualization

```
Role Inheritance Tree
  Agent (base)
  ├── Senior Agent (inherits + overrides)
  │   └── (changes: +campaigns:read, +calls:write)
  └── Quality Analyst (inherits + overrides)
      └── (changes: +calls:read_all, +transcripts:export)
```

## Open-Source Tools

- **Casbin** (Apache 2.0) — Role hierarchy with inheritance support
- **Permit.io** (Apache 2.0) — Built-in role inheritance in UI

## Production Considerations

- Maximum inheritance depth of 3 to prevent complexity and performance issues
- Detect and prevent circular inheritance chains
- Show effective (inherited + overridden) vs actual (stored) permissions in UI
- Parent role changes should optionally propagate or require explicit confirmation
- Notify child role owners when parent role changes
- Cache effective permissions per role with cache invalidation on parent/child changes
- Soft-delete roles to preserve inheritance history for audit
