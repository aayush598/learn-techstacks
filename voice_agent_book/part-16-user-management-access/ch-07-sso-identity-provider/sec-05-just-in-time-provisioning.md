# Just-In-Time Provisioning

## Overview

JIT provisioning creates user accounts automatically on first SSO login, eliminating the need for pre-provisioning. Attributes from the IdP (name, email, groups) populate the user profile and determine role assignments.

## Provisioning Flow

```
SSO Login → User Not Found → JIT Enabled?
    ├── No → Error: Contact Admin
    └── Yes → Create User
              ├── Map IdP attributes to user profile
              ├── Determine role from IdP groups/attributes
              ├── Assign to default team
              └── Send welcome email
```

## Implementation

```typescript
class JitProvisioningService {
  async provisionUser(attributes: SamlAttributes | OidcClaims, config: SsoConfig): Promise<User> {
    const email = attributes[config.attributeMapping.email] as string;
    if (!email) throw new Error('Email not provided by IdP');

    // Check if user was previously deactivated
    const existing = await this.userService.findByEmailIncludingInactive(email, config.tenantId);
    if (existing) {
      if (existing.status === 'inactive') {
        await this.userService.reactivateUser(existing.id);
        return this.userService.getUser(existing.id)!;
      }
      return existing; // Should not happen if called correctly
    }

    const firstName = attributes[config.attributeMapping.firstName] as string || email.split('@')[0];
    const lastName = attributes[config.attributeMapping.lastName] as string || '';

    // Create user
    const user = await this.userService.createUser({
      email,
      name: `${firstName} ${lastName}`.trim(),
      tenantId: config.tenantId,
      status: 'active',
      authProvider: config.provider,
      externalId: attributes.sub || attributes.nameId,
      emailVerified: true,
    });

    // Determine role from IdP groups
    const role = await this.determineRole(attributes, config);
    if (role) {
      await this.roleService.assignRole(user.id, role.id, 'scim');
    }

    // Map department if provided
    if (config.attributeMapping.department && attributes[config.attributeMapping.department]) {
      const deptName = attributes[config.attributeMapping.department] as string;
      const department = await this.departmentService.findOrCreateByName(deptName, config.tenantId);
      if (department) {
        await this.userService.updateUser(user.id, { departmentId: department.id });
      }
    }

    // Send welcome email
    await this.notificationService.sendWelcome(user);

    return user;
  }

  private async determineRole(attributes: any, config: SsoConfig): Promise<Role | null> {
    // Check group-to-role mapping
    if (config.attributeMapping.groups && attributes[config.attributeMapping.groups]) {
      const groups = Array.isArray(attributes[config.attributeMapping.groups])
        ? attributes[config.attributeMapping.groups]
        : [attributes[config.attributeMapping.groups]];

      for (const group of groups) {
        const mapping = await this.db.findOne('group_role_mappings', {
          groupName: group,
          tenantId: config.tenantId,
        });
        if (mapping) {
          return this.roleService.getRole(mapping.roleId);
        }
      }
    }

    // Fall back to default role
    if (config.provisioning.defaultRoleId) {
      return this.roleService.getRole(config.provisioning.defaultRoleId);
    }

    return null;
  }
}
```

## Open-Source Tools

- **NextAuth.js** (ISC) — JIT provisioning with adapters
- **Clerk** (Commercial) — JIT user creation

## Production Considerations

- Disable JIT for tenants that require pre-approval
- Rate-limit JIT user creation (max 100 per hour per tenant)
- Audit all JIT-created users with IdP session ID
- Sync IdP attribute changes on each login (not just first)
- Allow admin to set default team and role for JIT users
- Send new user notification to tenant admin
- Store original IdP attributes in user metadata for troubleshooting
