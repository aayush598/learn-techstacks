# Section 06: Directory Sync (SCIM)

## Overview

System for Cross-domain Identity Management (SCIM) enables automated user provisioning and deprovisioning between the voice agent platform and enterprise identity providers. When a user is added to or removed from an enterprise directory (Okta, Entra ID, OneLogin, Google Workspace), the SCIM integration automatically creates or deactivates the corresponding user account in the platform without manual intervention. SCIM 2.0 is the industry standard for identity lifecycle management.

The SCIM integration implements the server side of the SCIM 2.0 protocol (RFC 7643 and RFC 7644). The platform exposes SCIM 2.0 endpoints (`/Users`, `/Groups`, `/Schemas`, `/ServiceProviderConfig`) that identity providers call to synchronize user and group data. The integration handles the full CRUD lifecycle: Create (provision new user), Read (query user by ID or filter), Update (update user attributes), Patch (partial update), and Delete/Deactivate (deprovision user).

## Architecture

```
                 SCIM Directory Sync

   IdP → SCIM Endpoint → SCIM Controller → User Service
              |                    |
   +----------------------------------------------------------+
   |              SCIM 2.0 Server Components                  |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | SCIM Endpoints   |  | Schema Registry   |            |
   |  | • /Users         |  | • Core User       |            |
   |  | • /Groups        |  | • Core Group      |            |
   |  | • /Schemas       |  | • Enterprise User |            |
   |  | • /ServiceProvid-|  | • Custom          |            |
   |  |   erConfig       |  |   extensions      |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | User CRUD        |  | Group CRUD        |            |
   |  | • POST /Users    |  | • POST /Groups    |            |
   |  | • GET /Users/{id}|  | • GET /Groups/{id}|            |
   |  | • PUT /Users/{id}|  | • PUT /Groups/{id}|            |
   |  | • PATCH /Users   |  | • PATCH /Groups   |            |
   |  | • DELETE /Users  |  | • DELETE /Groups  |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Filter/Pagination|  | Auth              |             |
   |  | • Filter (eq, sw,|  | • Bearer Token    |            |
   |  |   co, pr)        |  | • OAuth2          |            |
   |  | • Pagination     |  | • IP allowlisting |            |
   |  | • Sorting        |  +-------------------+            |
   |  +------------------+                                    |
   +----------------------------------------------------------+
```

## Design Decisions

- **SCIM server over SCIM client pattern:** The platform implements the SCIM server, meaning IdPs push data to the platform rather than the platform pulling from the IdP. This is simpler — the platform does not need to manage connections to potentially hundreds of different IdPs. Each IdP is configured to call the platform's SCIM endpoint with a bearer token. Trade-off: the platform SCIM endpoint must be publicly accessible and authenticated, but the push model eliminates polling overhead and provides real-time provisioning.

- **Enterprise User Schema extension over core schema only:** The SCIM Core User Schema (id, userName, name, emails, phoneNumbers) is extended with the Enterprise User Schema extension (employeeNumber, department, manager, organization, division, costCenter). This enables enterprise customers to synchronize organizational attributes that may be used for reporting and access control. The extension is optional — SCIM clients that do not need it can omit the enterprise extension. Trade-off: extension support adds schema complexity but enables richer organizational data synchronization.

- **Soft delete (deactivate) over hard delete for user deprovisioning:** When an IdP sends a DELETE request or sets `active: false`, the SCIM integration deactivates the user account rather than deleting it. Deactivated users cannot log in but their data (call history, configurations) is preserved for audit and compliance. Hard deletion is available as a separate cleanup process (90 days after deactivation). Trade-off: soft delete requires data retention and eventual cleanup logic but prevents accidental data loss from SCIM operations.

## Implementation Approach

```
// SCIM 2.0 Core User Schema
interface SCIMUser {
  schemas: ['urn:ietf:params:scim:schemas:core:2.0:User'];
  id?: string;
  externalId?: string;
  userName: string;
  name?: {
    formatted?: string;
    familyName?: string;
    givenName?: string;
    middleName?: string;
  };
  displayName?: string;
  emails?: { value: string; type: 'work' | 'home' | 'other'; primary?: boolean }[];
  phoneNumbers?: { value: string; type: 'work' | 'mobile' | 'other' }[];
  active?: boolean;
  groups?: { value: string; display: string }[];
  roles?: { value: string; display: string }[];
  meta: {
    resourceType: 'User';
    created: string;
    lastModified: string;
    location: string;
  };
  'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User'?: {
    employeeNumber?: string;
    costCenter?: string;
    organization?: string;
    division?: string;
    department?: string;
    manager?: { value: string; displayName: string };
  };
}

interface SCIMGroup {
  schemas: ['urn:ietf:params:scim:schemas:core:2.0:Group'];
  id?: string;
  externalId?: string;
  displayName: string;
  members?: { value: string; display: string }[];
  meta: {
    resourceType: 'Group';
    created: string;
    lastModified: string;
    location: string;
  };
}

class SCIMServer {
  private tokenValidator: SCIMTokenValidator;

  // POST /Users — Create user
  async createUser(tenantId: string, userData: SCIMUser): Promise<SCIMUser> {
    const user = await this.userService.createUser({
      tenantId,
      email: userData.emails?.find(e => e.primary || e.type === 'work')?.value || userData.userName,
      name: userData.name?.formatted || `${userData.name?.givenName} ${userData.name?.familyName}`,
      externalId: userData.externalId,
      active: userData.active !== false,
      employeeNumber: userData['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User']?.employeeNumber,
      department: userData['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User']?.department,
    });

    const scimUser = this.mapToSCIMUser(user);
    return scimUser;
  }

  // GET /Users/{id} — Get user
  async getUser(tenantId: string, userId: string): Promise<SCIMUser | null> {
    const user = await this.userService.getUser(userId);
    if (!user || user.tenantId !== tenantId) return null;
    return this.mapToSCIMUser(user);
  }

  // GET /Users — List/Search users
  async listUsers(tenantId: string, params: SCIMListParams): Promise<SCIMListResponse<SCIMUser>> {
    const filter = this.parseFilter(params.filter);
    const result = await this.userService.listUsers({
      tenantId,
      filter,
      startIndex: params.startIndex || 1,
      count: params.count || 100,
    });

    return {
      schemas: ['urn:ietf:params:scim:api:messages:2.0:ListResponse'],
      totalResults: result.total,
      startIndex: params.startIndex || 1,
      itemsPerPage: result.items.length,
      Resources: result.items.map(u => this.mapToSCIMUser(u)),
    };
  }

  // PUT /Users/{id} — Full update
  async updateUser(tenantId: string, userId: string, userData: SCIMUser): Promise<SCIMUser> {
    const email = userData.emails?.find(e => e.primary)?.value || userData.userName;
    await this.userService.updateUser(userId, {
      email,
      name: userData.name?.formatted,
      active: userData.active,
      department: userData['urn:ietf:params:scim:schemas:extension:enterprise:2.0:User']?.department,
    });

    // Sync group membership if provided
    if (userData.groups) {
      await this.syncUserGroups(tenantId, userId, userData.groups);
    }

    return this.getUser(tenantId, userId)!;
  }

  // PATCH /Users/{id} — Partial update
  async patchUser(tenantId: string, userId: string, patchBody: SCIMPatchRequest): Promise<SCIMUser> {
    const updates: Record<string, any> = {};

    for (const op of patchBody.Operations) {
      if (op.op === 'replace') {
        if (op.path === 'active' || op.path === undefined && op.value.active !== undefined) {
          updates.active = op.path === 'active' ? op.value : op.value.active;
        }
        if (op.path === 'name.formatted') updates.name = op.value;
        if (op.path === 'emails' || (op.path === undefined && op.value.emails)) {
          const emails = op.path === 'emails' ? op.value : op.value.emails;
          const primary = emails?.find((e: any) => e.primary);
          if (primary) updates.email = primary.value;
        }
      }
      if (op.op === 'remove') {
        if (op.path === 'active' || op.path === 'urn:ietf:params:scim:api:messages:2.0:Enterprise:User:active') {
          updates.active = false;
        }
      }
    }

    if (Object.keys(updates).length > 0) {
      await this.userService.updateUser(userId, updates);
    }

    return this.getUser(tenantId, userId)!;
  }

  // DELETE /Users/{id} — Deactivate user
  async deleteUser(tenantId: string, userId: string): Promise<void> {
    await this.userService.deactivateUser(tenantId, userId);
  }

  // PATCH /Users/{id} with group membership
  private async syncUserGroups(tenantId: string, userId: string, groups: { value: string; display: string }[]): Promise<void> {
    for (const group of groups) {
      const platformGroup = await this.roleService.findOrCreateGroup(tenantId, group.display, group.value);
      if (platformGroup) {
        await this.roleService.addUserToGroup(userId, platformGroup.id);
      }
    }
  }

  private mapToSCIMUser(user: PlatformUser): SCIMUser {
    return {
      schemas: ['urn:ietf:params:scim:schemas:core:2.0:User', 'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User'],
      id: user.id,
      externalId: user.externalId,
      userName: user.email,
      name: {
        formatted: user.name,
        givenName: user.name?.split(' ')[0],
        familyName: user.name?.split(' ').slice(1).join(' '),
      },
      emails: [{ value: user.email, type: 'work', primary: true }],
      active: user.active,
      meta: {
        resourceType: 'User',
        created: user.createdAt.toISOString(),
        lastModified: user.updatedAt.toISOString(),
        location: `/scim/v2/Users/${user.id}`,
      },
      'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User': {
        employeeNumber: user.employeeNumber,
        department: user.department,
      },
    };
  }

  // POST /Groups — Create group
  async createGroup(tenantId: string, groupData: SCIMGroup): Promise<SCIMGroup> {
    const group = await this.roleService.createGroup(tenantId, {
      name: groupData.displayName,
      externalId: groupData.externalId,
    });

    if (groupData.members) {
      for (const member of groupData.members) {
        await this.roleService.addUserToGroup(member.value, group.id);
      }
    }

    return this.mapToSCIMGroup(group);
  }
}

// Middleware for SCIM authentication
function scimAuthMiddleware(tenantId: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const authHeader = req.headers['authorization'];
    if (!authHeader?.startsWith('Bearer ')) {
      res.status(401).json({ schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'], status: '401', detail: 'Missing authorization' });
      return;
    }

    const token = authHeader.slice(7);
    const valid = await validateSCIMToken(tenantId, token);
    if (!valid) {
      res.status(401).json({ schemas: ['urn:ietf:params:scim:api:messages:2.0:Error'], status: '401', detail: 'Invalid token' });
      return;
    }

    req.tenantId = tenantId;
    next();
  };
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| scim2-js (MIT) | Node.js | SCIM model + filter parser |
| Express SCIM middleware (MIT) | Node.js | SCIM routing |
| Zod (MIT) | Validation | SCIM payload validation |

## Production Considerations

**Scaling:** SCIM operations are low-volume (provisioning events, not API calls per user request). The SCIM server must handle IdP-initiated syncs that may push the entire user directory (thousands of users) during initial setup. Implement request throttling to prevent IdP bulk syncs from overwhelming the platform. SCIM responses must include accurate `totalResults` for IdPs that use pagination. Support for `PATCH` (partial update) is critical — most IdPs use PATCH for group membership changes rather than PUT.

**Security:** SCIM endpoints require bearer token authentication. Each tenant has a unique SCIM bearer token that is configured on both the platform and the IdP side. The SCIM token must have separate permissions from user API tokens (SCIM tokens only access SCIM endpoints). Log all SCIM operations with the source IP and IdP identifier for audit trails. IdP IP allowlisting is recommended for SCIM endpoints.

**Monitoring:** Track SCIM operation counts (create, read, update, delete, patch) by resource type (User, Group), operation success/failure rates, response times, IdP synchronization frequency, and user provisioning lag (time from IdP event to platform user creation). Alert on high SCIM failure rates (indicates configuration drift between IdP and platform), bulk sync failures, and unauthorized SCIM access attempts.
