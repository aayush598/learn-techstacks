# Role Validation & Sanity Checks

## Overview

Role validation ensures custom roles meet minimum security requirements, prevent privilege escalation, avoid circular inheritance, and maintain consistency. Validation runs during role creation and modification to catch issues before they affect users.

## Validation Categories

```
Validation Checks
├── Minimum Permission Requirements
│   ├── Every role must have at least 1 permission
│   ├── Sensitive permissions require security review
│   └── Admin roles cannot be created from non-admin base
├── Privilege Escalation Prevention
│   ├── Custom role cannot exceed creator's permissions
│   ├── Cannot grant permissions the assigner doesn't have
│   └── Inheritance depth limit
├── Circular Inheritance Detection
│   ├── Role cannot inherit from itself (directly or transitively)
│   └── Max inheritance chain length (3 levels)
└── Consistency & Sanity
    ├── No contradictory permissions (allow + deny on same resource)
    ├── Valid resource references
    └── Restriction value bounds
```

## Validation Engine

```typescript
interface RoleValidationRequest {
  role: Role;
  context: {
    creatorUserId?: string;
    creatorPermissions?: string[];
    tenantId: string;
  };
}

interface RoleValidationResult {
  valid: boolean;
  checks: ValidationCheckResult[];
  overallRisk: 'low' | 'medium' | 'high';
  warnings: string[];
  errors: string[];
}

interface ValidationCheckResult {
  checkName: string;
  passed: boolean;
  severity: 'error' | 'warning' | 'info';
  message: string;
  details?: Record<string, unknown>;
}

class RoleValidator {
  async validate(request: RoleValidationRequest): Promise<RoleValidationResult> {
    const checks: ValidationCheckResult[] = [];

    checks.push(await this.checkMinimumPermissions(request));
    checks.push(await this.checkPrivilegeEscalation(request));
    checks.push(await this.checkCircularInheritance(request));
    checks.push(await this.checkPermissionConsistency(request));
    checks.push(await this.checkRestrictionBounds(request));
    checks.push(await this.checkSensitiveResources(request));

    const errors = checks.filter(c => !c.passed && c.severity === 'error');
    const warnings = checks.filter(c => !c.passed && c.severity === 'warning');
    const riskLevel = this.calculateRiskLevel(checks);

    return {
      valid: errors.length === 0,
      checks,
      overallRisk: riskLevel,
      warnings: warnings.map(w => w.message),
      errors: errors.map(e => e.message),
    };
  }

  private async checkMinimumPermissions(
    request: RoleValidationRequest
  ): Promise<ValidationCheckResult> {
    if (!request.role.permissions || request.role.permissions.length === 0) {
      return {
        checkName: 'minimum_permissions',
        passed: false,
        severity: 'error',
        message: 'Role must have at least one permission',
      };
    }

    const allowedPerms = request.role.permissions.filter(p => p.effect === 'allow');
    if (allowedPerms.length === 0) {
      return {
        checkName: 'minimum_permissions',
        passed: false,
        severity: 'error',
        message: 'Role must have at least one allowed permission (not just denials)',
      };
    }

    return {
      checkName: 'minimum_permissions',
      passed: true,
      severity: 'info',
      message: `Role has ${allowedPerms.length} allowed permissions`,
    };
  }

  private async checkPrivilegeEscalation(
    request: RoleValidationRequest
  ): Promise<ValidationCheckResult> {
    if (!request.context.creatorUserId || !request.context.creatorPermissions) {
      return {
        checkName: 'privilege_escalation',
        passed: true,
        severity: 'info',
        message: 'Privilege escalation check skipped (system context)',
      };
    }

    const creatorPerms = new Set(request.context.creatorPermissions);

    for (const perm of request.role.permissions) {
      if (perm.effect !== 'allow') continue;

      const permKey = `${perm.resource}:${perm.action}`;
      if (!creatorPerms.has(permKey) && !creatorPerms.has(`${perm.resource}:*`) && !creatorPerms.has('*:*')) {
        return {
          checkName: 'privilege_escalation',
          passed: false,
          severity: 'error',
          message: `Role grants ${permKey} which creator does not have`,
          details: { permission: permKey },
        };
      }
    }

    return {
      checkName: 'privilege_escalation',
      passed: true,
      severity: 'info',
      message: 'No privilege escalation detected',
    };
  }

  private async checkCircularInheritance(
    request: RoleValidationRequest
  ): Promise<ValidationCheckResult> {
    const visited = new Set<string>();
    let current: string | undefined = request.role.parentRoleId;
    let depth = 0;

    while (current) {
      if (visited.has(current)) {
        return {
          checkName: 'circular_inheritance',
          passed: false,
          severity: 'error',
          message: `Circular inheritance detected at depth ${depth}`,
          details: { cyclePath: Array.from(visited) },
        };
      }

      if (depth > 3) {
        return {
          checkName: 'circular_inheritance',
          passed: false,
          severity: 'error',
          message: 'Maximum inheritance depth exceeded (max 3)',
          details: { depth, maxDepth: 3 },
        };
      }

      visited.add(current);
      const parentRole = await this.roleStore.getRole(current);
      current = parentRole?.parentRoleId;
      depth++;
    }

    return {
      checkName: 'circular_inheritance',
      passed: true,
      severity: 'info',
      message: `Inheritance chain depth: ${depth}`,
    };
  }

  private async checkPermissionConsistency(
    request: RoleValidationRequest
  ): Promise<ValidationCheckResult> {
    const conflicts: string[] = [];

    for (let i = 0; i < request.role.permissions.length; i++) {
      for (let j = i + 1; j < request.role.permissions.length; j++) {
        const a = request.role.permissions[i];
        const b = request.role.permissions[j];

        if (a.resource === b.resource && a.action === b.action && a.effect !== b.effect) {
          conflicts.push(`${a.resource}:${a.action} (allow vs deny)`);
        }
      }
    }

    if (conflicts.length > 0) {
      return {
        checkName: 'permission_consistency',
        passed: false,
        severity: 'warning',
        message: `Contradictory permissions found: ${conflicts.join(', ')}`,
        details: { conflicts },
      };
    }

    return {
      checkName: 'permission_consistency',
      passed: true,
      severity: 'info',
      message: 'No permission conflicts',
    };
  }

  private async checkRestrictionBounds(
    request: RoleValidationRequest
  ): Promise<ValidationCheckResult> {
    const bounds = {
      maxConcurrentCalls: { min: 1, max: 100, default: 10 },
      callDurationLimitMinutes: { min: 1, max: 480, default: 120 },
      maxAgentsManaged: { min: 1, max: 500, default: 20 },
    };

    const errors: string[] = [];

    for (const restriction of request.role.restrictions || []) {
      const bound = (bounds as any)[restriction.type];
      if (!bound) {
        errors.push(`Unknown restriction type: ${restriction.type}`);
        continue;
      }

      if (typeof restriction.value === 'number') {
        if (restriction.value < bound.min || restriction.value > bound.max) {
          errors.push(
            `${restriction.type} value ${restriction.value} is out of bounds (${bound.min}-${bound.max})`
          );
        }
      }
    }

    return {
      checkName: 'restriction_bounds',
      passed: errors.length === 0,
      severity: errors.length > 0 ? 'error' : 'info',
      message: errors.length > 0 ? errors.join(', ') : 'All restrictions within bounds',
      details: { errors },
    };
  }

  private async checkSensitiveResources(
    request: RoleValidationRequest
  ): Promise<ValidationCheckResult> {
    const sensitiveResources = ['billing', 'api_keys', 'system_settings', 'users'];
    const sensitiveGrants: string[] = [];

    for (const perm of request.role.permissions) {
      if (perm.effect === 'allow' && sensitiveResources.includes(perm.resource)) {
        sensitiveGrants.push(`${perm.resource}:${perm.action}`);
      }
    }

    if (sensitiveGrants.length > 0 && !request.role.isBuiltin) {
      return {
        checkName: 'sensitive_resources',
        passed: false,
        severity: 'warning',
        message: `Custom role grants access to sensitive resources: ${sensitiveGrants.join(', ')}`,
        details: { sensitiveGrants },
      };
    }

    return {
      checkName: 'sensitive_resources',
      passed: true,
      severity: 'info',
      message: 'No sensitive resource access granted',
    };
  }

  private calculateRiskLevel(checks: ValidationCheckResult[]): 'low' | 'medium' | 'high' {
    const errors = checks.filter(c => !c.passed && c.severity === 'error');
    const warnings = checks.filter(c => !c.passed && c.severity === 'warning');

    if (errors.length > 0) return 'high';
    if (warnings.length > 2) return 'medium';
    return 'low';
  }
}
```

## Validation UI Integration

```typescript
function RoleValidationPanel({ result }: { result: RoleValidationResult }) {
  return (
    <div className={`validation-panel risk-${result.overallRisk}`}>
      <h3>Role Validation</h3>
      <div className="validation-summary">
        <span className={`badge ${result.valid ? 'success' : 'error'}`}>
          {result.valid ? 'Valid' : 'Invalid'}
        </span>
        <span className="risk-badge">{result.overallRisk}</span>
      </div>

      {result.errors.length > 0 && (
        <div className="validation-errors">
          <h4>Errors</h4>
          <ul>{result.errors.map((e, i) => <li key={i}>{e}</li>)}</ul>
        </div>
      )}

      {result.warnings.length > 0 && (
        <div className="validation-warnings">
          <h4>Warnings</h4>
          <ul>{result.warnings.map((w, i) => <li key={i}>{w}</li>)}</ul>
        </div>
      )}

      <div className="validation-checks">
        {result.checks.map(check => (
          <div key={check.checkName} className={`check ${check.passed ? 'pass' : 'fail'}`}>
            <span className="check-icon">{check.passed ? '✓' : '✗'}</span>
            <span className="check-message">{check.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Open-Source Tools

- **Zod** (MIT) — Schema validation for permission structures
- **Casbin** (Apache 2.0) — Built-in model validation

## Production Considerations

- Validate roles synchronously during creation/modification in the UI
- Run batch validation on existing roles during platform upgrades
- Add validation as a pre-commit hook in permission-as-code CI/CD pipelines
- Track validation failures with metrics to identify common configuration mistakes
- Allow override of validation warnings with explicit admin acknowledgment
- Maintain a validation rules registry that evolves with platform capabilities
- Provide remediation suggestions alongside validation errors
