# SCIM User Sync

## Overview

SCIM 2.0 enables automated user and group synchronization from identity providers. This covers user provisioning, group membership sync, attribute updates, and deactivation flows initiated by the IdP.

## SCIM Sync Architecture

```
[IdP (Okta/Azure AD)] ──SCIM──→ [SCIM Server]
    │ Push: Create/Update/Delete Users & Groups
    │ Pull: GET /Users, GET /Groups
    ↓
[SCIM Server] → [User Service] → [Role Service] → [Department Service]
```

## User Sync Implementation

```typescript
class ScimSyncService {
  async syncUser(scimUser: ScimUser, tenantId: string): Promise<User> {
    const existing = await this.userService.findByExternalId(scimUser.externalId, tenantId);

    if (existing) {
      // Update existing user
      const updates: Partial<User> = {
        name: `${scimUser.name.givenName} ${scimUser.name.familyName}`,
        email: scimUser.userName,
      };

      if (scimUser.active === false) {
        await this.userService.deactivateUser(existing.id, 'scim');
        return this.userService.getUser(existing.id)!;
      }

      await this.userService.updateUser(existing.id, updates);
      return this.userService.getUser(existing.id)!;
    }

    // Create new user
    if (!scimUser.active) return null; // Don't create inactive users

    return this.userService.createUser({
      email: scimUser.userName,
      name: `${scimUser.name.givenName} ${scimUser.name.familyName}`,
      tenantId,
      externalId: scimUser.externalId,
      status: 'active',
      authProvider: 'scim',
    });
  }

  async syncGroupMembership(groupId: string, memberExternalIds: string[], tenantId: string): Promise<void> {
    const groupMapping = await this.db.findOne('group_role_mappings', { groupId, tenantId });
    if (!groupMapping) return;

    const roleId = groupMapping.roleId;
    const currentMembers = await this.roleService.getUsersByRole(roleId);
    const currentExternalIds = new Set(currentMembers.map(u => u.externalId).filter(Boolean));

    const targetExternalIds = new Set(memberExternalIds);

    // Remove users no longer in group
    for (const externalId of currentExternalIds) {
      if (!targetExternalIds.has(externalId)) {
        const user = await this.userService.findByExternalId(externalId, tenantId);
        if (user) await this.roleService.removeRole(user.id, roleId, 'scim');
      }
    }

    // Add new group members
    for (const externalId of targetExternalIds) {
      if (!currentExternalIds.has(externalId)) {
        const user = await this.userService.findByExternalId(externalId, tenantId);
        if (user) await this.roleService.assignRole(user.id, roleId, 'scim');
      }
    }
  }
}
```

## Open-Source Tools

- **scim2** (MIT) — SCIM 2.0 server implementation
- **@scim2/server** (MIT) — Express middleware

## Production Considerations

- Support both push (IdP-initiated) and pull (app-initiated) sync
- Batch sync operations for large directories (max 200 per batch)
- Log all SCIM sync operations with before/after state
- Handle IdP user deactivation as suspension (not hard delete)
- Support delta sync using SCIM `externalId` as stable identifier
- Rate-limit SCIM syncs to prevent cascading updates
- Validate SCIM payload attributes against schema definition
