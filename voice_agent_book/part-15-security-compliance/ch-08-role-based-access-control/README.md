# Chapter 08: Role-Based Access Control (RBAC)

> **Part:** 15 - Security, Compliance & Governance

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [RBAC Model Design](sec-01-rbac-model-design.md) | Core RBAC (NIST model), user-role-permission relationships, role hierarchy, separation of duties |
| 02 | [Permission Definition Catalog](sec-02-permission-definition-catalog.md) | Resource-based permissions, action verbs (CRUD), permission naming conventions, wildcard matching |
| 03 | [Role Hierarchy & Inheritance](sec-03-role-hierarchy-inheritance.md) | Parent-child role relationships, permission inheritance, override semantics, cycle prevention |
| 04 | [User-Role Assignment](sec-04-user-role-assignment.md) | Direct assignment vs group-based, temporary role grants, role activation, session roles |
| 05 | [Attribute-Based Access Control (ABAC)](sec-05-abac-integration.md) | Combining RBAC with ABAC, attribute context (time, location, device), policy evaluation engine |
| 06 | [Policy-as-Code Implementation](sec-06-policy-as-code.md) | OPA/Rego policies, Casbin implementation, policy testing, versioned policies |
| 07 | [Access Review Automation](sec-07-access-review-automation.md) | Scheduled access reviews, certification campaigns, manager approval workflows, revocation automation |
| 08 | [RBAC Audit Logging](sec-08-rbac-audit-logging.md) | Permission change audit, access grant/revoke logging, privilege escalation detection |

---

## RBAC Data Model

```
User ─── UserRoleAssignment ─── Role ─── RolePermission ─── Permission
 │                                │
 │                          RoleHierarchy
 │                          (parent/child)
 │
UserAttributes ─────────── ABAC Policy ─── Context (time, IP, device)
                                              │
                                         Decision Engine
                                              │
                                         Allow/Deny
```

---

## Learning Objectives

- Design RBAC model following NIST standards
- Create comprehensive permission definition catalog
- Implement role hierarchy with inheritance and override
- Build user-role assignment with temporary grant support
- Combine RBAC with ABAC for contextual access decisions
- Implement policy-as-code using OPA/Casbin
- Automate access review and certification campaigns
- Build RBAC audit logging with privilege escalation detection
