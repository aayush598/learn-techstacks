# Chapter 04: Custom Roles & Permissions

> **Part:** 16 - User Management & Access Control

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Custom Role Builder UI](sec-01-custom-role-builder-ui.md) | Drag-and-drop permission assignment, role configuration interface, visual permission matrix |
| 02 | [Permission Granularity Design](sec-02-permission-granularity-design.md) | Coarse vs fine-grained permissions, resource-level scoping, field-level access control |
| 03 | [Role Copy & Inheritance](sec-03-role-copy-inheritance.md) | Clone existing roles, inherit-and-override pattern, role versioning, parent role linking |
| 04 | [Permission Conflict Resolution](sec-04-permission-conflict-resolution.md) | Explicit deny priority, allow-override semantics, conflict detection, resolution visualization |
| 05 | [Built-in vs Custom Roles](sec-05-built-in-vs-custom-roles.md) | System-defined roles, custom roles coexistence, built-in role protection, upgrade preservation |
| 06 | [Role Validation & Sanity Checks](sec-06-role-validation-sanity-checks.md) | Minimum permission requirements, privilege escalation prevention, circular inheritance detection |
| 07 | [Permission Audit Trail](sec-07-permission-audit-trail.md) | Permission change logging, before/after snapshots, change approval workflow, audit reporting |
| 08 | [Custom Role Migration](sec-08-custom-role-migration.md) | Role schema versioning, migrating between versions, backward compatibility, role data integrity |

---

## Custom Role Editor Schema

```json
{
  "id": "custom_role_abc",
  "name": "Senior Agent",
  "base_role": "agent",
  "permissions": {
    "calls": { "read": true, "create": true, "update": true, "delete": false },
    "transcripts": { "read": true, "export": true },
    "agents": { "read": true, "create": false, "configure": false },
    "reports": { "view": true, "export": true, "schedule": false },
    "settings": { "read": true, "write": false }
  },
  "restrictions": {
    "max_concurrent_calls": 10,
    "call_duration_limit_minutes": 120
  }
}
```

---

## Learning Objectives

- Build custom role builder UI with permission matrix visualization
- Design permission granularity from coarse to field-level
- Implement role copy and inheritance patterns
- Handle permission conflict resolution with explicit deny
- Manage coexistence of built-in and custom roles
- Implement role validation with privilege escalation prevention
- Create permission change audit trail with approval workflow
- Support custom role migration across schema versions
