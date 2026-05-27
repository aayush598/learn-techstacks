# Custom Role Migration

## Overview

Custom role migration handles the evolution of role schemas over time as the platform adds new resources, actions, and permission models. This includes versioning, backward compatibility, schema transformations, and data integrity during migration.

## Schema Versioning

```typescript
interface RoleSchemaVersion {
  version: number;
  changes: SchemaChange[];
  createdAt: Date;
  migrationScript?: string;
  backwardCompatible: boolean;
}

interface SchemaChange {
  type: 'permission_added' | 'permission_removed' | 'resource_renamed' | 'action_renamed'
      | 'restriction_added' | 'restriction_removed' | 'schema_field_added';
  description: string;
  affectedResources: string[];
}

const ROLE_SCHEMA_VERSIONS: RoleSchemaVersion[] = [
  {
    version: 1,
    changes: [{ type: 'schema_field_added', description: 'Initial schema', affectedResources: ['*'] }],
    createdAt: new Date('2025-01-01'),
    backwardCompatible: true,
  },
  {
    version: 2,
    changes: [
      { type: 'permission_added', description: 'Added transcripts:export permission', affectedResources: ['transcripts'] },
      { type: 'restriction_added', description: 'Added max_concurrent_calls restriction', affectedResources: ['agents'] },
    ],
    createdAt: new Date('2025-03-15'),
    backwardCompatible: true,
  },
  {
    version: 3,
    changes: [
      { type: 'resource_renamed', description: 'Renamed "reports" to "analytics"', affectedResources: ['reports'] },
      { type: 'action_renamed', description: 'Renamed "write" to "update"', affectedResources: ['*'] },
    ],
    createdAt: new Date('2025-06-01'),
    backwardCompatible: false, // Breaking change
  },
];
```

## Migration Service

```typescript
interface RoleMigration {
  id: string;
  tenantId: string;
  roleId: string;
  fromVersion: number;
  toVersion: number;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'rolled_back';
  startedAt?: Date;
  completedAt?: Date;
  error?: string;
  changes: SchemaChange[];
}

class RoleMigrationService {
  async migrateRole(roleId: string, targetVersion: number): Promise<RoleMigration> {
    const role = await this.roleStore.getRole(roleId);
    if (!role) throw new Error('Role not found');

    const currentVersion = role.metadata?.schemaVersion || 1;
    if (currentVersion >= targetVersion) {
      throw new Error(`Role already at schema version ${currentVersion}`);
    }

    const migration: RoleMigration = {
      id: generateId('migration'),
      tenantId: role.tenantId,
      roleId,
      fromVersion: currentVersion,
      toVersion: targetVersion,
      status: 'running',
      startedAt: new Date(),
      changes: [],
    };

    await this.db.insert('role_migrations', migration);

    try {
      for (let v = currentVersion; v < targetVersion; v++) {
        await this.applyMigrationStep(role, v, v + 1, migration);
      }

      migration.status = 'completed';
      migration.completedAt = new Date();
      await this.db.update('role_migrations', { id: migration.id }, migration);

      // Update role schema version
      await this.db.update('roles', { id: roleId }, {
        'metadata.schemaVersion': targetVersion,
        updatedAt: new Date(),
      });

    } catch (error) {
      migration.status = 'failed';
      migration.error = String(error);
      await this.db.update('role_migrations', { id: migration.id }, migration);

      if (!ROLE_SCHEMA_VERSIONS[v - 1]?.backwardCompatible) {
        await this.rollbackMigration(migration);
      }
    }

    return migration;
  }

  private async applyMigrationStep(
    role: Role,
    fromVersion: number,
    toVersion: number,
    migration: RoleMigration
  ): Promise<void> {
    const versionChanges = ROLE_SCHEMA_VERSIONS[toVersion - 1];
    if (!versionChanges) throw new Error(`Schema version ${toVersion} not found`);

    for (const change of versionChanges.changes) {
      switch (change.type) {
        case 'permission_added':
          // Add new permission with default deny
          if (!role.permissions.some(p =>
            p.resource === change.affectedResources[0]
          )) {
            role.permissions.push({
              resource: change.affectedResources[0],
              action: change.description.split(' ')[1],
              effect: 'deny',
            });
          }
          break;

        case 'permission_removed':
          // Remove deprecated permissions
          role.permissions = role.permissions.filter(p =>
            !(change.affectedResources.includes(p.resource) &&
              p.action === change.description.split(' ')[1])
          );
          break;

        case 'resource_renamed':
          // Migrate old resource name to new
          const [oldName, , newName] = change.description.match(/"([^"]+)"/g)!.map(s => s.replace(/"/g, ''));
          for (const perm of role.permissions) {
            if (perm.resource === oldName) {
              perm.resource = newName;
            }
          }
          break;

        case 'restriction_added':
          // Add default restriction if applicable
          if (!role.restrictions) role.restrictions = [];
          break;
      }

      migration.changes.push(change);
    }
  }

  private async rollbackMigration(migration: RoleMigration): Promise<void> {
    migration.status = 'rolled_back';
    migration.error = (migration.error || '') + ' - Auto-rollback initiated';

    await this.db.update('role_migrations', { id: migration.id }, migration);

    // Attempt to revert to previous version
    const backup = await this.db.findOne('role_backups', {
      roleId: migration.roleId,
      version: migration.fromVersion,
    });
    if (backup) {
      await this.db.update('roles', { id: migration.roleId }, backup.data);
    }
  }
}
```

## Pre-Migration Validation

```typescript
class PreMigrationValidator {
  async validateMigrationFeasibility(
    tenantId: string,
    targetVersion: number
  ): Promise<MigrationValidationReport> {
    const roles = await this.roleStore.getTenantRoles(tenantId);
    const checks: MigrationCheck[] = [];

    for (const role of roles) {
      const currentVersion = role.metadata?.schemaVersion || 1;

      // Check if direct migration path exists
      if (currentVersion > targetVersion) {
        checks.push({
          roleId: role.id,
          roleName: role.name,
          feasible: false,
          reason: `Role version ${currentVersion} exceeds target ${targetVersion}`,
        });
        continue;
      }

      // Check for breaking changes in the migration path
      let hasBreakingChanges = false;
      for (let v = currentVersion; v < targetVersion; v++) {
        const versionDef = ROLE_SCHEMA_VERSIONS[v];
        if (versionDef && !versionDef.backwardCompatible) {
          hasBreakingChanges = true;
          break;
        }
      }

      checks.push({
        roleId: role.id,
        roleName: role.name,
        feasible: true,
        breakingChanges: hasBreakingChanges,
        fromVersion: currentVersion,
        recommendedAction: hasBreakingChanges
          ? 'Manual review recommended before migration'
          : 'Auto-migration available',
      });
    }

    return {
      tenantId,
      targetVersion,
      totalRoles: checks.length,
      autoMigratable: checks.filter(c => c.feasible && !c.breakingChanges).length,
      requiresReview: checks.filter(c => c.breakingChanges).length,
      infeasible: checks.filter(c => !c.feasible).length,
      checks,
    };
  }
}

interface MigrationValidationReport {
  tenantId: string;
  targetVersion: number;
  totalRoles: number;
  autoMigratable: number;
  requiresReview: number;
  infeasible: number;
  checks: MigrationCheck[];
}
```

## Tenant-Wide Migration

```typescript
class TenantMigrationOrchestrator {
  async migrateTenant(tenantId: string, targetVersion: number): Promise<TenantMigrationResult> {
    const roles = await this.roleStore.getTenantRoles(tenantId);
    const migrations: RoleMigration[] = [];
    const errors: Array<{ roleId: string; error: string }> = [];

    // Create backup first
    await this.createTenantBackup(tenantId, targetVersion);

    // Migrate roles sequentially (respect dependency order)
    for (const role of roles) {
      try {
        const migration = await this.migrationService.migrateRole(role.id, targetVersion);
        migrations.push(migration);
      } catch (error) {
        errors.push({ roleId: role.id, error: String(error) });
      }
    }

    return {
      tenantId,
      targetVersion,
      totalRoles: roles.length,
      migrated: migrations.filter(m => m.status === 'completed').length,
      failed: errors.length,
      errors,
      migrations,
    };
  }

  private async createTenantBackup(tenantId: string, version: number): Promise<void> {
    const roles = await this.roleStore.getTenantRoles(tenantId);
    for (const role of roles) {
      await this.db.insert('role_backups', {
        roleId: role.id,
        tenantId,
        version: role.metadata?.schemaVersion || 1,
        data: role,
        createdAt: new Date(),
      });
    }
  }
}
```

## Open-Source Tools

- **node-pg-migrate** (MIT) — Database migration patterns adaptable for role schemas
- **umzug** (MIT) — Programmatic migration framework

## Production Considerations

- Always create backups before running migrations
- Test migrations in sandbox environment first
- Schedule migrations during maintenance windows for breaking changes
- Communicate migration timeline to tenants with affected custom roles
- Monitor migration success rate and provide rollback capability
- Maintain a migration changelog visible in the admin dashboard
- Allow tenants to postpone non-critical migrations for up to 30 days
- Automatically resolve backward-compatible migrations without notification
