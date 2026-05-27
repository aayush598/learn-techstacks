# Chapter 03: Role-Based Access Control

> **Part:** 16 - User Management & Access Control

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [RBAC Data Model](sec-01-rbac-data-model.md) | Users, roles, permissions, role assignments, permission assignment tables, schema design |
| 02 | [Permission Evaluation Engine](sec-02-permission-evaluation-engine.md) | Permission check algorithm, role hierarchy resolution, cached evaluation, bulk permission checks |
| 03 | [Role Assignment Management](sec-03-role-assignment-management.md) | Assign/unassign roles, role activation/deactivation, temporary assignments, expiry dates |
| 04 | [Permission Checking Middleware](sec-04-permission-checking-middleware.md) | Express/Next.js middleware pattern, decorator-based approach, GraphQL directive guards |
| 05 | [API Scope Enforcement](sec-05-api-scope-enforcement.md) | API key scoping, route-level guards, parameter-level checks, resource ownership validation |
| 06 | [UI Element Visibility](sec-06-ui-element-visibility.md) | Component-level permission checks, menu filtering, action button visibility, conditional rendering |
| 07 | [Role Templates & Presets](sec-07-role-templates-presets.md) | Predefined roles (admin, manager, agent, viewer), industry-specific templates, role cloning |
| 08 | [RBAC Testing Strategy](sec-08-rbac-testing-strategy.md) | Permission matrix testing, automated permission audits, negative testing, regression test suite |

---

## Permission Check Middleware

```typescript
// Next.js API route middleware
function requirePermission(action: string, resource: string) {
  return async (req: NextRequest, context: HandlerContext) => {
    const user = await getAuthUser(req);
    const hasPermission = await permissionEngine.check({
      userId: user.id,
      tenantId: user.tenantId,
      action,
      resource,
    });
    if (!hasPermission) {
      return NextResponse.json(
        { error: 'Forbidden', code: 'INSUFFICIENT_PERMISSIONS' },
        { status: 403 }
      );
    }
    return context.next();
  };
}
```

---

## Learning Objectives

- Design RBAC data model with users, roles, and permissions
- Implement permission evaluation engine with caching
- Build role assignment management with temporary grants
- Create permission checking middleware for API routes
- Enforce API scope with parameter-level checks
- Implement UI element visibility based on permissions
- Create role templates and presets for quick setup
- Develop comprehensive RBAC testing strategy
