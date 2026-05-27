# RBAC Data Model

## Overview

The Role-Based Access Control (RBAC) data model defines the relationships between users, roles, permissions, and resources. A well-designed schema enables efficient permission evaluation, supports hierarchical role structures, and scales to thousands of permissions per tenant.

## Core Entities

```
┌──────────┐     ┌──────────┐     ┌──────────────┐
│  Users   │────→│  Roles   │←────│  Permissions  │
└──────────┘     └──────────┘     └──────────────┘
      │               │
      │        ┌──────┴──────┐
      │        ▼             ▼
      │  ┌──────────┐  ┌──────────┐
      │  │  Role    │  │  Role    │
      │  │  Assign. │  │  Inherit │
      │  └──────────┘  └──────────┘
      ▼
┌──────────┐
│  Tenant  │
└──────────┘
```

## Database Schema

```sql
-- Tenants table
CREATE TABLE tenants (
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  domain VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE users (
  id VARCHAR(64) PRIMARY KEY,
  tenant_id VARCHAR(64) NOT NULL,
  email VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  status VARCHAR(32) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  INDEX idx_tenant_id (tenant_id)
);

-- Roles table
CREATE TABLE roles (
  id VARCHAR(64) PRIMARY KEY,
  tenant_id VARCHAR(64) NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  role_type ENUM('system', 'custom') DEFAULT 'custom',
  is_builtin BOOLEAN DEFAULT FALSE,
  parent_role_id VARCHAR(64),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (tenant_id) REFERENCES tenants(id),
  FOREIGN KEY (parent_role_id) REFERENCES roles(id),
  UNIQUE KEY uk_tenant_role (tenant_id, name)
);

-- Permissions table (flat permission list)
CREATE TABLE permissions (
  id VARCHAR(64) PRIMARY KEY,
  resource VARCHAR(128) NOT NULL,
  action VARCHAR(64) NOT NULL,
  description TEXT,
  UNIQUE KEY uk_resource_action (resource, action)
);

-- Role-Permission assignments
CREATE TABLE role_permissions (
  role_id VARCHAR(64) NOT NULL,
  permission_id VARCHAR(64) NOT NULL,
  effect ENUM('allow', 'deny') DEFAULT 'allow',
  conditions JSON,
  PRIMARY KEY (role_id, permission_id),
  FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
  FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);

-- User-Role assignments
CREATE TABLE user_roles (
  user_id VARCHAR(64) NOT NULL,
  role_id VARCHAR(64) NOT NULL,
  assigned_by VARCHAR(64),
  assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NULL,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- Resource scope restrictions per role
CREATE TABLE role_resource_scopes (
  id VARCHAR(64) PRIMARY KEY,
  role_id VARCHAR(64) NOT NULL,
  resource_type VARCHAR(128) NOT NULL,
  scope_type ENUM('tenant', 'department', 'team', 'self') NOT NULL,
  scope_value VARCHAR(255),
  FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);
```

## TypeScript Models

```typescript
interface Tenant {
  id: string;
  name: string;
  domain?: string;
  createdAt: Date;
}

interface User {
  id: string;
  tenantId: string;
  email: string;
  name: string;
  status: 'active' | 'inactive' | 'suspended';
  createdAt: Date;
}

interface Role {
  id: string;
  tenantId: string;
  name: string;
  description?: string;
  roleType: 'system' | 'custom';
  isBuiltin: boolean;
  parentRoleId?: string;
  permissions: RolePermission[];
  resourceScopes: ResourceScope[];
  createdAt: Date;
}

interface RolePermission {
  roleId: string;
  resource: string;
  action: string;
  effect: 'allow' | 'deny';
  conditions?: PermissionCondition;
}

interface ResourceScope {
  resourceType: string;
  scopeType: 'tenant' | 'department' | 'team' | 'self';
  scopeValue?: string;
}

interface PermissionCondition {
  attribute: string;
  operator: 'eq' | 'neq' | 'in' | 'contains' | 'gt' | 'lt';
  value: unknown;
}

interface UserRoleAssignment {
  userId: string;
  roleId: string;
  assignedBy?: string;
  assignedAt: Date;
  expiresAt?: Date;
}
```

## Built-in Role Definitions

```typescript
const BUILT_IN_ROLES: Record<string, RoleDefinition> = {
  admin: {
    name: 'Admin',
    description: 'Full system access with all permissions',
    permissions: ['*:*'],
    scopes: [{ resourceType: '*', scopeType: 'tenant' }],
  },
  manager: {
    name: 'Manager',
    description: 'Manage agents, campaigns, and view team performance',
    permissions: [
      'agents:*', 'campaigns:*', 'calls:read',
      'reports:*', 'team:read', 'users:read',
    ],
    scopes: [{ resourceType: '*', scopeType: 'department' }],
  },
  agent: {
    name: 'Agent',
    description: 'Make and receive calls, view own analytics',
    permissions: [
      'calls:create', 'calls:read', 'calls:update',
      'agents:read', 'transcripts:read',
    ],
    scopes: [{ resourceType: '*', scopeType: 'self' }],
  },
  developer: {
    name: 'Developer',
    description: 'API access and agent configuration',
    permissions: [
      'agents:*', 'api_keys:*', 'webhooks:*',
      'logs:read', 'analytics:read',
    ],
    scopes: [{ resourceType: '*', scopeType: 'tenant' }],
  },
  viewer: {
    name: 'Viewer',
    description: 'Read-only access to dashboards and reports',
    permissions: [
      'dashboards:read', 'reports:read', 'analytics:read',
    ],
    scopes: [{ resourceType: '*', scopeType: 'tenant' }],
  },
};
```

## Open-Source Tools

- **Casbin** (Apache 2.0) — Authorization library supporting RBAC, ABAC, ACL models
- **Permit.io** (Apache 2.0) — Fine-grained authorization with RBAC support
- **Prisma** (MIT) — ORM for database schema management

## Production Considerations

- Cache role-permission mappings in Redis with TTL-based invalidation
- Index all foreign keys and query patterns (tenant_id + user_id lookups)
- Use soft deletes for roles and permissions to maintain audit trail
- Set a role depth limit (max 3 levels of parent-child inheritance) to prevent circular chains
- Precompute flat permission list for each user on role change
- Partition role data by tenant to ensure isolation in multi-tenant setup
