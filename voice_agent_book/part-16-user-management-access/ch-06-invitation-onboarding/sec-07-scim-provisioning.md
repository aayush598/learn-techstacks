# SCIM Provisioning Standard

## Overview

SCIM 2.0 (System for Cross-domain Identity Management) enables automated user provisioning and group management from identity providers (Okta, Azure AD, Google Workspace). SCIM supports user creation, updates, deactivation, and group membership sync.

## SCIM Endpoints

```typescript
// SCIM 2.0 Core endpoints
const SCIM_ENDPOINTS = {
  '/scim/v2/Users': { methods: ['GET', 'POST'] },
  '/scim/v2/Users/:id': { methods: ['GET', 'PUT', 'PATCH', 'DELETE'] },
  '/scim/v2/Groups': { methods: ['GET', 'POST'] },
  '/scim/v2/Groups/:id': { methods: ['GET', 'PUT', 'PATCH', 'DELETE'] },
  '/scim/v2/ServiceProviderConfig': { methods: ['GET'] },
  '/scim/v2/Schemas': { methods: ['GET'] },
};
```

## User Provisioning

```typescript
class ScimUserController {
  async createUser(req: Request, res: Response): Promise<void> {
    const scimUser = req.body as ScimUser;

    const user = await this.userService.createUser({
      email: scimUser.userName,
      name: `${scimUser.name.givenName} ${scimUser.name.familyName}`,
      tenantId: req.tenantId,
      status: scimUser.active ? 'active' : 'inactive',
      externalId: scimUser.externalId,
    });

    // Assign default role if specified in groups
    if (scimUser.groups) {
      for (const group of scimUser.groups) {
        const role = await this.mapGroupToRole(group.value, req.tenantId);
        if (role) await this.roleService.assignRole(user.id, role.id, 'scim');
      }
    }

    const response = this.toScimUser(user);
    res.status(201).json(response);
  }

  async patchUser(req: Request, res: Response): Promise<void> {
    const { id } = req.params;
    const patchOp = req.body as ScimPatchOperation;

    const user = await this.userService.getUserByExternalId(id, req.tenantId);
    if (!user) { res.status(404).json({ error: 'User not found' }); return; }

    for (const op of patchOp.Operations) {
      if (op.path === 'active' && op.value === false) {
        await this.userService.deactivateUser(user.id, 'scim');
      } else if (op.path === 'name.givenName') {
        await this.userService.updateUser(user.id, { name: `${op.value} ${user.name.split(' ')[1]}` });
      }
    }

    res.status(200).json(this.toScimUser(await this.userService.getUser(user.id)!));
  }
}
```

## Group-to-Role Mapping

```typescript
interface GroupRoleMapping {
  tenantId: string;
  groupId: string;        // SCIM group ID from IdP
  groupName: string;
  roleId: string;
  createdAt: Date;
}

async function mapGroupToRole(scimGroupId: string, tenantId: string): Promise<Role | null> {
  const mapping = await db.findOne('group_role_mappings', { groupId: scimGroupId, tenantId });
  if (!mapping) return null;
  return roleService.getRole(mapping.roleId);
}
```

## Open-Source Tools

- **scim2** (MIT) — SCIM 2.0 server library
- **@scim2/server** (MIT) — Express middleware for SCIM
- **BetterCloud** (Commercial) — SCIM integration testing

## Production Considerations

- Support SCIM Bearer token authentication
- Rate-limit SCIM requests: 100/min per tenant
- IdP-initiated deactivation should suspend not hard-delete user accounts
- Sync groups bidirectionally (SCIM push groups from app to IdP)
- Log all SCIM operations for audit trail
- Support incremental sync via `startIndex` and `count` parameters
- Filter SCIM users by `filter` parameter (e.g., `userName eq "john"`)
