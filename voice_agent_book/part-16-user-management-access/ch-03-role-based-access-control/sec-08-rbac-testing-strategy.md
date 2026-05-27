# RBAC Testing Strategy

## Overview

Testing the RBAC system is critical for security and compliance. The testing strategy covers permission matrix validation, automated permission audits, negative testing for denial patterns, and regression test suites that catch unintended permission changes.

## Permission Matrix Testing

```typescript
interface PermissionMatrixTest {
  role: string;
  action: string;
  resource: string;
  resourceScope: string;
  expectedResult: boolean;
  description: string;
}

const DEFAULT_PERMISSION_MATRIX: PermissionMatrixTest[] = [
  // Admin permissions
  { role: 'admin', action: 'read', resource: 'agents', resourceScope: 'any', expectedResult: true, description: 'Admin can read any agent' },
  { role: 'admin', action: 'delete', resource: 'agents', resourceScope: 'any', expectedResult: true, description: 'Admin can delete any agent' },
  { role: 'admin', action: 'read', resource: 'billing', resourceScope: 'any', expectedResult: true, description: 'Admin can read billing' },
  { role: 'admin', action: 'read', resource: 'users', resourceScope: 'any', expectedResult: true, description: 'Admin can read users' },

  // Manager permissions
  { role: 'manager', action: 'read', resource: 'agents', resourceScope: 'team', expectedResult: true, description: 'Manager can read team agents' },
  { role: 'manager', action: 'delete', resource: 'agents', resourceScope: 'team', expectedResult: false, description: 'Manager cannot delete agents' },
  { role: 'manager', action: 'read', resource: 'billing', resourceScope: 'any', expectedResult: false, description: 'Manager cannot read billing' },
  { role: 'manager', action: 'create', resource: 'campaigns', resourceScope: 'team', expectedResult: true, description: 'Manager can create campaigns' },

  // Agent permissions
  { role: 'agent', action: 'read', resource: 'calls', resourceScope: 'self', expectedResult: true, description: 'Agent can read own calls' },
  { role: 'agent', action: 'read', resource: 'calls', resourceScope: 'other', expectedResult: false, description: 'Agent cannot read other calls' },
  { role: 'agent', action: 'create', resource: 'campaigns', resourceScope: 'any', expectedResult: false, description: 'Agent cannot create campaigns' },
  { role: 'agent', action: 'delete', resource: 'transcripts', resourceScope: 'self', expectedResult: false, description: 'Agent cannot delete transcripts' },

  // Viewer permissions
  { role: 'viewer', action: 'read', resource: 'dashboards', resourceScope: 'any', expectedResult: true, description: 'Viewer can read dashboards' },
  { role: 'viewer', action: 'create', resource: 'agents', resourceScope: 'any', expectedResult: false, description: 'Viewer cannot create agents' },
  { role: 'viewer', action: 'read', resource: 'users', resourceScope: 'any', expectedResult: false, description: 'Viewer cannot read users' },

  // Sensitive operations
  { role: 'admin', action: 'delete', resource: 'tenants', resourceScope: 'any', expectedResult: false, description: 'Even admin cannot delete tenant' },
  { role: 'developer', action: 'read', resource: 'api_keys', resourceScope: 'tenant', expectedResult: true, description: 'Developer can read API keys' },
];
```

## Automated Permission Audit

```typescript
class PermissionAudit {
  async runFullAudit(tenantId: string): Promise<AuditReport> {
    const roles = await this.roleStore.getTenantRoles(tenantId);
    const users = await this.userStore.getTenantUsers(tenantId);
    const results: AuditCheckResult[] = [];

    // Check 1: No role has excessive permissions
    for (const role of roles) {
      const wildcardPerms = role.permissions.filter(
        p => p.action === '*' || p.resource === '*'
      );
      if (wildcardPerms.length > 0 && !role.isBuiltin) {
        results.push({
          type: 'warning',
          message: `Custom role "${role.name}" has wildcard permissions`,
          roleId: role.id,
        });
      }
    }

    // Check 2: Sensitive permissions are restricted
    const sensitiveResources = ['billing', 'users', 'api_keys', 'settings'];
    for (const role of roles) {
      for (const resource of sensitiveResources) {
        const hasSensitiveAccess = role.permissions.some(
          p => p.resource === resource && p.effect === 'allow'
        );
        if (hasSensitiveAccess && !['admin', 'developer'].includes(role.name.toLowerCase())) {
          results.push({
            type: 'info',
            message: `Role "${role.name}" has access to sensitive resource "${resource}"`,
            roleId: role.id,
          });
        }
      }
    }

    // Check 3: Users with no roles
    const usersWithRoles = new Set(
      (await this.roleStore.getAllAssignments(tenantId)).map(a => a.userId)
    );
    for (const user of users) {
      if (!usersWithRoles.has(user.id)) {
        results.push({
          type: 'warning',
          message: `User ${user.email} has no roles assigned`,
          userId: user.id,
        });
      }
    }

    // Check 4: Expired assignments still active
    const expired = await this.db.find('user_roles', {
      expiresAt: { $lte: new Date() },
      tenantId,
    });
    for (const assignment of expired) {
      results.push({
        type: 'error',
        message: `Expired role assignment found for user ${assignment.userId}`,
        assignmentId: assignment.id,
      });
    }

    return {
      tenantId,
      timestamp: new Date(),
      totalChecks: results.length,
      errors: results.filter(r => r.type === 'error').length,
      warnings: results.filter(r => r.type === 'warning').length,
      results,
    };
  }
}
```

## Negative Testing

```typescript
describe('RBAC Negative Testing', () => {
  let engine: PermissionEngine;

  beforeEach(() => {
    engine = new PermissionEngine();
  });

  describe('Deny always wins', () => {
    it('deny overrides allow when both set for same resource', async () => {
      const result = await engine.check({
        userId: 'user1',
        tenantId: 'tenant1',
        action: 'delete',
        resource: 'agents',
      });

      expect(result.allowed).toBe(false);
      expect(result.reason).toBe('explicit_deny');
    });

    it('deny in parent role overrides allow in child role', async () => {
      const result = await engine.check({
        userId: 'user2',
        tenantId: 'tenant1',
        action: 'read',
        resource: 'billing',
      });
      // user2 has 'manager' (deny billing) and 'admin' (allow everything)
      // Manager deny should win
      expect(result.allowed).toBe(false);
    });
  });

  describe('Unassigned users', () => {
    it('returns denied for user with no roles', async () => {
      const result = await engine.check({
        userId: 'unassigned_user',
        tenantId: 'tenant1',
        action: 'read',
        resource: 'dashboards',
      });
      expect(result.allowed).toBe(false);
      expect(result.reason).toBe('no_roles_assigned');
    });
  });

  describe('Resource scope boundaries', () => {
    it('agent cannot access calls assigned to other agents', async () => {
      const result = await engine.check({
        userId: 'agent1',
        tenantId: 'tenant1',
        action: 'read',
        resource: 'calls',
        resourceId: 'call_agent2',
      });
      expect(result.allowed).toBe(false);
    });

    it('manager cannot access resources outside their department', async () => {
      const result = await engine.check({
        userId: 'manager_sales',
        tenantId: 'tenant1',
        action: 'read',
        resource: 'agents',
        resourceId: 'agent_support',
      });
      expect(result.allowed).toBe(false);
    });
  });
});
```

## Regression Test Suite

```typescript
class RBACRegressionTest {
  async runAll(): Promise<TestReport> {
    const tests = [
      ...this.basicPermissionTests(),
      ...this.hierarchyTests(),
      ...this.conditionTests(),
      ...this.scopeTests(),
      ...this.edgeCaseTests(),
    ];

    const results = await Promise.all(tests.map(t => t()));
    const failed = results.filter(r => !r.passed);

    return {
      total: results.length,
      passed: results.length - failed.length,
      failed: failed.length,
      failures: failed.map(f => ({ name: f.name, error: f.error })),
      timestamp: new Date(),
    };
  }

  private basicPermissionTests(): TestFn[] {
    return [
      async () => {
        // Verify admin still has full access after schema changes
        const result = await engine.check({
          userId: 'admin1', tenantId: 'tenant1',
          action: 'read', resource: 'agents',
        });
        return { name: 'admin_basic_access', passed: result.allowed };
      },
      async () => {
        // Verify viewer cannot perform destructive actions
        const result = await engine.check({
          userId: 'viewer1', tenantId: 'tenant1',
          action: 'delete', resource: 'campaigns',
        });
        return { name: 'viewer_no_delete', passed: !result.allowed };
      },
    ];
  }

  private edgeCaseTests(): TestFn[] {
    return [
      async () => ({
        name: 'case_insensitive_resource',
        passed: (await engine.check({
          userId: 'admin1', tenantId: 'tenant1',
          action: 'READ', resource: 'AGENTS',
        })).allowed,
      }),
      async () => ({
        name: 'non_existent_resource',
        passed: !(await engine.check({
          userId: 'admin1', tenantId: 'tenant1',
          action: 'read', resource: 'non_existent',
        })).allowed,
      }),
      async () => ({
        name: 'empty_action_and_resource',
        passed: !(await engine.check({
          userId: 'admin1', tenantId: 'tenant1',
          action: '', resource: '',
        })).allowed,
      }),
    ];
  }
}
```

## Open-Source Tools

- **Jest** (MIT) — Test runner for permission tests
- **Casbin** (Apache 2.0) — Built-in model testing utilities
- **Supertest** (MIT) — HTTP integration testing with permission middleware

## Production Considerations

- Run permission matrix tests in CI/CD pipeline before each deployment
- Alert on permission test failures immediately (security regression)
- Generate coverage reports showing which permission combinations are tested
- Include permission tests in security review process for each product change
- Maintain separate test suite for compliance-related permissions (SOC 2, HIPAA, PCI)
- Run permission audits on a schedule (daily) and deliver results to security team
- Version control permission matrices alongside code to track changes over time
