# Role Templates & Presets

## Overview

Role templates and presets provide pre-configured role definitions that can be applied with minimal customization. These include platform-defined built-in roles, industry-specific templates, and user-created reusable templates that streamline role setup for common organizational patterns.

## Template Architecture

```
┌─────────────────┐
│ Role Templates   │
├─────────────────┤
│ System Built-in │ ← Immutable, always available
│  - Admin        │
│  - Manager      │
│  - Agent        │
│  - Developer    │
│  - Viewer       │
├─────────────────┤
│ Industry        │ ← Pre-seeded for common verticals
│  - Healthcare   │
│  - Finance      │
│  - E-commerce   │
│  - Real Estate  │
├─────────────────┤
│ Custom Templates│ ← Created and shared by users
│  - Senior Agent │
│  - Team Lead    │
└─────────────────┘
```

## Template Data Model

```typescript
interface RoleTemplate {
  id: string;
  name: string;
  description: string;
  category: 'system' | 'industry' | 'custom';
  tenantId?: string;          // NULL for global templates
  isBuiltin: boolean;
  permissions: TemplatePermission[];
  resourceScopes: TemplateResourceScope[];
  restrictions?: RoleRestriction[];
  metadata: {
    version: number;
    industry?: string;
    useCase?: string;
    recommendedFor?: string[];
  };
  createdAt: Date;
  updatedAt: Date;
}

interface TemplatePermission {
  resource: string;
  actions: string[];           // 'read', 'write', 'create', 'delete', '*'
  effect: 'allow' | 'deny';
  conditions?: PermissionCondition[];
}

interface TemplateResourceScope {
  resourceType: string;
  scopeType: 'tenant' | 'department' | 'team' | 'self';
  defaultValue?: string;
}

interface RoleRestriction {
  type: 'max_concurrent_calls' | 'call_duration_limit' | 'max_agents' | 'feature_flag';
  value: number | boolean | string;
}
```

## Built-in Role Templates

```typescript
const BUILTIN_TEMPLATES: RoleTemplate[] = [
  {
    id: 'role-admin',
    name: 'Admin',
    description: 'Complete system access with all permissions across the tenant',
    category: 'system',
    isBuiltin: true,
    permissions: [
      { resource: '*', actions: ['*'], effect: 'allow' },
    ],
    resourceScopes: [
      { resourceType: '*', scopeType: 'tenant' },
    ],
    metadata: { version: 1, recommendedFor: ['system_administrators'] },
  },
  {
    id: 'role-manager',
    name: 'Manager',
    description: 'Manage agents, campaigns, and view team performance metrics',
    category: 'system',
    isBuiltin: true,
    permissions: [
      { resource: 'agents', actions: ['read', 'create', 'update'], effect: 'allow' },
      { resource: 'agents', actions: ['delete'], effect: 'deny' },
      { resource: 'campaigns', actions: ['*'], effect: 'allow' },
      { resource: 'calls', actions: ['read'], effect: 'allow' },
      { resource: 'reports', actions: ['*'], effect: 'allow' },
      { resource: 'users', actions: ['read'], effect: 'allow' },
      { resource: 'settings', actions: ['read'], effect: 'allow' },
      { resource: 'billing', actions: ['read'], effect: 'deny' },
    ],
    resourceScopes: [
      { resourceType: '*', scopeType: 'team' },
    ],
    metadata: { version: 1, recommendedFor: ['team_leads', 'department_heads'] },
  },
  {
    id: 'role-agent',
    name: 'Agent',
    description: 'Handle inbound/outbound calls and view personal performance',
    category: 'system',
    isBuiltin: true,
    permissions: [
      { resource: 'calls', actions: ['read', 'create', 'update'], effect: 'allow' },
      { resource: 'transcripts', actions: ['read'], effect: 'allow' },
      { resource: 'agents', actions: ['read'], effect: 'allow' },
      { resource: 'reports', actions: ['read'], effect: 'allow' },
      { resource: 'reports', actions: ['create', 'delete'], effect: 'deny' },
    ],
    resourceScopes: [
      { resourceType: 'calls', scopeType: 'self' },
      { resourceType: 'agents', scopeType: 'self' },
    ],
    restrictions: [
      { type: 'max_concurrent_calls', value: 5 },
      { type: 'call_duration_limit', value: 240 },
    ],
    metadata: { version: 1, recommendedFor: ['call_center_agents'] },
  },
];
```

## Industry Templates

```typescript
const INDUSTRY_TEMPLATES: Record<string, RoleTemplateModifier> = {
  healthcare: {
    additionalPermissions: [
      { resource: 'hipaa_compliance', actions: ['read'], effect: 'allow' },
      { resource: 'phi_data', actions: ['read'], effect: 'deny' },
    ],
    restrictions: [
      { type: 'feature_flag', value: true, description: 'hipaa_logging' },
    ],
  },
  finance: {
    additionalPermissions: [
      { resource: 'pci_compliance', actions: ['read'], effect: 'allow' },
      { resource: 'transcripts', actions: ['export'], effect: 'deny' },
    ],
    restrictions: [
      { type: 'call_recording', value: true },
      { type: 'feature_flag', value: true, description: 'compliance_audit_trail' },
    ],
  },
  ecommerce: {
    additionalPermissions: [
      { resource: 'orders', actions: ['read'], effect: 'allow' },
      { resource: 'crm', actions: ['read', 'write'], effect: 'allow' },
    ],
  },
};
```

## Template Application

```typescript
class RoleTemplateService {
  async applyTemplate(
    tenantId: string,
    templateId: string,
    customizations: TemplateCustomization
  ): Promise<Role> {
    const template = await this.getTemplate(templateId);
    if (!template) throw new Error('Template not found');

    // Create actual role from template
    const role: Role = {
      id: generateId('role'),
      tenantId,
      name: customizations.name || template.name,
      description: customizations.description || template.description,
      roleType: 'custom',
      isBuiltin: false,
      permissions: this.mergePermissions(template.permissions, customizations),
      resourceScopes: this.mergeScopes(template.resourceScopes, customizations),
      restrictions: template.restrictions,
      createdAt: new Date(),
    };

    await this.db.insert('roles', role);
    await this.invalidateTemplateCache(tenantId);
    return role;
  }

  private mergePermissions(
    templatePerms: TemplatePermission[],
    customizations: TemplateCustomization
  ): RolePermission[] {
    // Start with template permissions
    let perms = [...templatePerms];

    // Apply custom overrides
    if (customizations.overridePermissions) {
      for (const override of customizations.overridePermissions) {
        const existingIndex = perms.findIndex(
          p => p.resource === override.resource
        );

        if (existingIndex >= 0) {
          if (override.mode === 'add') {
            perms[existingIndex].actions = [
              ...new Set([...perms[existingIndex].actions, ...override.actions]),
            ];
          } else if (override.mode === 'remove') {
            perms[existingIndex].actions = perms[existingIndex].actions.filter(
              a => !override.actions.includes(a)
            );
          } else if (override.mode === 'replace') {
            perms[existingIndex] = { ...perms[existingIndex], actions: override.actions };
          }
        } else if (override.mode === 'add') {
          perms.push({
            resource: override.resource,
            actions: override.actions,
            effect: override.effect || 'allow',
          });
        }
      }
    }

    // Apply industry modifiers
    if (customizations.industry) {
      const industryMods = INDUSTRY_TEMPLATES[customizations.industry];
      if (industryMods) {
        perms.push(...industryMods.additionalPermissions.map(p => ({
          resource: p.resource,
          actions: p.actions,
          effect: p.effect,
        })));
      }
    }

    return perms;
  }

  private async invalidateTemplateCache(tenantId: string): Promise<void> {
    const keys = await this.redis.keys(`role_template:${tenantId}:*`);
    if (keys.length > 0) await this.redis.del(...keys);
  }
}

interface TemplateCustomization {
  name?: string;
  description?: string;
  overridePermissions?: TemplatePermissionOverride[];
  industry?: string;
}

interface TemplatePermissionOverride {
  resource: string;
  actions: string[];
  effect?: 'allow' | 'deny';
  mode: 'add' | 'remove' | 'replace';
}
```

## Template Versioning

```typescript
interface RoleTemplateVersion {
  templateId: string;
  version: number;
  permissions: TemplatePermission[];
  changelog: string;
  createdAt: Date;
  createdBy: string;
}

class TemplateVersionService {
  async createVersion(
    templateId: string,
    updatedPermissions: TemplatePermission[],
    changelog: string,
    userId: string
  ): Promise<RoleTemplateVersion> {
    const currentVersion = await this.getLatestVersion(templateId);
    const newVersionNumber = (currentVersion?.version || 0) + 1;

    const version: RoleTemplateVersion = {
      templateId,
      version: newVersionNumber,
      permissions: updatedPermissions,
      changelog,
      createdAt: new Date(),
      createdBy: userId,
    };

    await this.db.insert('role_template_versions', version);
    await this.db.update('role_templates', { id: templateId }, {
      metadata: { version: newVersionNumber },
      updatedAt: new Date(),
    });

    return version;
  }

  async getRolesUsingTemplate(templateId: string): Promise<Role[]> {
    return this.db.find('roles', {
      'metadata.templateId': templateId,
    });
  }
}
```

## Open-Source Tools

- **Casbin** (Apache 2.0) — Role template/model definitions in configuration files
- **Permit.io** (Apache 2.0) — Built-in role template library

## Production Considerations

- Lock built-in role templates from modification but allow clone-and-customize
- Show role template usage counts to help admins identify popular templates
- Allow bulk application of templates to multiple departments
- Version control all template changes with diff visualization
- Pre-seed industry templates based on tenant onboarding questionnaire
- Provide template preview showing effective permissions before applying
- Support role template marketplace for sharing custom templates between tenants
