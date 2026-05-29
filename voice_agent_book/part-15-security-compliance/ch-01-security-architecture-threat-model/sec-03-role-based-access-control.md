# Section 03: Role-Based Access Control (RBAC)

RBAC assigns permissions to roles, and roles to users, simplifying permission management at scale. Users inherit permissions through their role assignments. Roles can be scoped to the tenant level (tenant admin, tenant viewer) or the platform level (platform admin, support agent).

Role structure: platform roles (super_admin, admin, support_agent, billing_manager), tenant roles (tenant_admin, agent_manager, analyst, viewer, api_key_manager). Each role has a set of permissions defined as actions on resources: calls:read, calls:write, agents:admin, billing:read, users:manage.

Permission enforcement: roles are stored in the database with their permission sets. The middleware checks the user's roles against the required permissions for each endpoint. Permission checks are cached in Redis with tenant-scoped keys. Role assignment is audited. Custom roles can be created by tenant admins for their organization.
