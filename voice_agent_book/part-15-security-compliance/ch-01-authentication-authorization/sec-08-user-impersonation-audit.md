# Section 08: User Impersonation & Audit

User impersonation allows support staff to temporarily act as a tenant user for troubleshooting purposes. Impersonation is a high-security feature: it must be explicitly initiated, strictly audited, time-limited, and clearly indicated in the UI to prevent accidental actions as the impersonated user.

Impersonation flow: support agent identifies tenant issue → agent requests impersonation (select user, provide ticket number, reason) → approval (automatic for L2+ support, manager approval for sensitive tenants) → impersonation session starts → agent sees tenant's dashboard with prominent "Impersonating" banner → every action is logged with the agent's identity → session auto-ends after 30 minutes or on explicit stop.

Audit trail for impersonation: who impersonated (agent ID, name), who was impersonated (tenant ID, user ID), when (start and end timestamps), why (ticket reference), all actions performed during session (API calls, page views, changes). Reports are available for compliance review. Tenant notification (email) is sent when impersonation occurs for enterprise accounts.
