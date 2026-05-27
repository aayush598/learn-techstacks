# Built-in vs Custom Roles

## Overview

Built-in (system-defined) roles provide a reliable baseline of permissions for common user types, while custom roles allow tenants to define precise access patterns for their organizational needs. Proper coexistence ensures upgrade paths and data integrity.

## Role Coexistence Architecture

```
Role Types
├── Built-in (system)
│   ├── Admin         ─ Immutable name + description
│   ├── Manager       ─ Cloneable, but original always available
│   ├── Agent         ─ Permission set versioned with platform
│   ├── Developer     ─ Receives feature-specific updates
│   └── Viewer        ─ Cannot be deleted
│
├── Custom (tenant-defined)
│   ├── Senior Agent  ─ Based on Agent, with extensions
│   ├── Team Lead     ─ Fully independent permission set
│   └── QA Specialist ─ Cloned from system role + overrides
│
└── Hybrid
    ├── Locked (inherits from built-in, limited overrides)
    └── Extended (copies built-in, fully independent)
```

## Role Type Definition

```typescript
interface BuiltinRole {
  id: string;
  name: string;
  description: string;
  system: true;
  protected: true;          // Cannot be deleted
  upgradeable: boolean;      // Receives platform updates
  minCustomPermissions: number; // Custom roles must have at least these
}

const BUILT_IN_ROLES: Record<string, BuiltinRole> = {
  admin: {
    id: 'builtin_admin', name: 'Admin', description: 'Full system access',
    system: true, protected: true, upgradeable: true, minCustomPermissions: 0,
  },
  manager: {
    id: 'builtin_manager', name: 'Manager', description: 'Team management',
    system: true, protected: true, upgradeable: true, minCustomPermissions: 3,
  },
  agent: {
    id: 'builtin_agent', name: 'Agent', description: 'Call handling',
    system: true, protected: true, upgradeable: true, minCustomPermissions: 5,
  },
};

class BuiltinRoleManager {
  async createCustomFromBuiltin(
    tenantId: string,
    builtinRoleId: string,
    customName: string,
    customPermissions: RolePermission[]
  ): Promise<Role> {
    const builtin = this.getBuiltinRole(builtinRoleId);
    if (!builtin) throw new Error('Built-in role not found');

    // Validate minimum permission requirements
    if (customPermissions.length < builtin.minCustomPermissions) {
      throw new Error(
        `Custom roles based on "${builtin.name}" require at least ${builtin.minCustomPermissions} permissions`
      );
    }

    // Create custom role
    const role: Role = {
      id: generateId('role'),
      tenantId,
      name: customName,
      description: `Custom role derived from ${builtin.name}`,
      roleType: 'custom',
      isBuiltin: false,
      permissions: customPermissions,
      metadata: {
        builtinSource: builtinRoleId,
        version: 1,
      },
      createdAt: new Date(),
    };

    await this.db.insert('roles', role);
    return role;
  }

  async upgradeBuiltinRole(roleId: string, newPermissions: RolePermission[]): Promise<void> {
    const builtin = this.getBuiltinRole(roleId);
    if (!builtin || !builtin.upgradeable) {
      throw new Error('Role is not upgradeable');
    }

    // Update the built-in role definition
    await this.db.update('roles', { id: roleId, isBuiltin: true }, {
      permissions: newPermissions,
      metadata: { version: (builtin.metadata?.version || 0) + 1 },
      updatedAt: new Date(),
    });

    // Optionally propagate to derived custom roles
    const derivedRoles = await this.db.find('roles', {
      'metadata.builtinSource': roleId,
      tenantId: { $exists: true },
    });

    for (const derived of derivedRoles) {
      if (derived.metadata?.autoUpgrade !== false) {
        await this.propagateUpgrade(derived, newPermissions);
      }
    }

    // Record in changelog
    await this.changelog.record({
      type: 'builtin_role_upgraded',
      roleId,
      version: builtin.metadata?.version + 1,
      affectedRoles: derivedRoles.length,
    });
  }

  private async propagateUpgrade(
    customRole: Role,
    newBuiltinPermissions: RolePermission[]
  ): Promise<void> {
    // Merge strategy: add new permissions from builtin, keep custom overrides
    const mergedPermissions = this.mergePermissions(
      newBuiltinPermissions,
      customRole.permissions
    );

    await this.db.update('roles', { id: customRole.id }, {
      permissions: mergedPermissions,
      updatedAt: new Date(),
    });
  }

  private mergePermissions(
    base: RolePermission[],
    overrides: RolePermission[]
  ): RolePermission[] {
    const merged = new Map<string, RolePermission>();

    // Add base permissions
    for (const perm of base) {
      merged.set(`${perm.resource}:${perm.action}`, { ...perm, source: 'builtin' });
    }

    // Apply overrides (custom permissions win)
    for (const perm of overrides) {
      const key = `${perm.resource}:${perm.action}`;
      merged.set(key, { ...perm, source: 'custom' });
    }

    return Array.from(merged.values());
  }
}
```

## Protection Mechanisms

```typescript
class BuiltinRoleProtection {
  // Prevent deletion
  async deleteRole(roleId: string): Promise<boolean> {
    const role = await this.db.findOne('roles', { id: roleId });
    if (!role) throw new Error('Role not found');

    if (role.isBuiltin) {
      throw new Error('Cannot delete built-in role');
    }

    await this.db.update('roles', { id: roleId }, { status: 'deleted' });
    return true;
  }

  // Prevent renaming
  async renameRole(roleId: string, newName: string): Promise<void> {
    const role = await this.db.findOne('roles', { id: roleId });
    if (role?.isBuiltin) {
      throw new Error('Cannot rename built-in role');
    }
    await this.db.update('roles', { id: roleId }, { name: newName });
  }

  // Prevent permission reduction below minimum
  async validatePermissionSet(
    roleId: string, permissions: RolePermission[]
  ): Promise<ValidationResult> {
    const role = await this.db.findOne('roles', { id: roleId });
    if (!role) return { valid: true, errors: [] };

    const builtin = this.getBuiltinRoleById(roleId);
    if (!builtin) return { valid: true, errors: [] };

    const errors: string[] = [];
    const requiredPerms = this.getRequiredPermissions(builtin.name);

    for (const required of requiredPerms) {
      const hasRequired = permissions.some(
        p => p.resource === required.resource && p.action === required.action && p.effect === 'allow'
      );
      if (!hasRequired) {
        errors.push(`Built-in role "${builtin.name}" requires "${required.resource}:${required.action}"`);
      }
    }

    return { valid: errors.length === 0, errors };
  }
}
```

## Upgrade Management Dashboard

```
Built-in Role Updates
┌─────────────────────────────────────────────────────┐
│  Role: Agent                                         │
│  Current version: 3 (deployed 2 months ago)          │
│  Latest version: 4 (available)                       │
│  Change summary:                                     │
│    • Added: transcripts:export                       │
│    • Removed: settings:write                         │
│    • Modified: calls:duration limit from 240 to 360  │
│                                                      │
│  [Preview Changes] [Upgrade All Derived]             │
│  [Customize Per-Role] [Skip Version]                 │
│                                                      │
│  Derived Roles: 12                                   │
│  ├── Senior Agent (auto-upgrade: ON)                 │
│  ├── Quality Analyst (auto-upgrade: OFF)             │
│  └── ...                                             │
└─────────────────────────────────────────────────────┘
```

## Open-Source Tools

- **Casbin** (Apache 2.0) — Model-based role definitions with built-in vs custom distinction
- **Permit.io** (Apache 2.0) — Built-in role management in admin panel

## Production Considerations

- Built-in roles cannot be deleted, renamed, or have their core permission set removed
- Custom roles derived from built-ins can choose auto-upgrade or manual-upgrade mode
- Platform upgrades to built-in roles should be communicated via changelog with migration guide
- Users assigned built-in roles directly should be migrated to custom equivalent before built-in removal
- Version built-in role definitions and allow rollback for 30 days
- Provide migration tooling to convert built-in role assignments to custom role assignments
- Warn admins when custom role permissions diverge significantly from the built-in baseline
