# Self-Registration Approval

## Overview

Self-registration allows users to sign up without an invitation, with optional admin approval. Configurable rules include domain whitelisting, auto-approval for known domains, and an admin approval queue for unknown domains.

## Registration Modes

```typescript
type RegistrationMode = 'open' | 'domain_whitelist' | 'approval_required' | 'invite_only';

interface RegistrationConfig {
  tenantId: string;
  mode: RegistrationMode;
  whitelistedDomains: string[];       // Auto-approve these domains
  blacklistedDomains: string[];       // Always reject these domains
  defaultRoleId: string;
  defaultTeamId?: string;
  requireEmailVerification: boolean;
  requirePhoneVerification: boolean;
  approvalRequiredForRoles: string[]; // Roles requiring manual approval
  maxPendingApprovals: number;
}
```

## Registration Flow

```typescript
class SelfRegistrationService {
  async register(email: string, password: string, name: string, tenantId: string): Promise<RegistrationResult> {
    const config = await this.getRegistrationConfig(tenantId);
    const domain = email.split('@')[1];

    // Check blacklist
    if (config.blacklistedDomains.includes(domain)) {
      return { success: false, reason: 'Domain not allowed' };
    }

    let requiresApproval = false;

    switch (config.mode) {
      case 'invite_only':
        return { success: false, reason: 'Registration closed. Contact admin for invitation.' };

      case 'approval_required':
        requiresApproval = true;
        break;

      case 'domain_whitelist':
        if (config.whitelistedDomains.includes(domain)) {
          requiresApproval = false;
        } else {
          requiresApproval = true;
        }
        break;

      case 'open':
        requiresApproval = false;
        break;
    }

    // Create user account
    const user = await this.userService.createUser({
      email, name, tenantId, status: requiresApproval ? 'pending' : 'active',
    });

    if (requiresApproval) {
      await this.createApprovalRequest(user.id, tenantId);
      return { success: true, requiresApproval: true };
    }

    // Auto-assign default role and team
    await this.roleService.assignRole(user.id, config.defaultRoleId, 'system');
    if (config.defaultTeamId) {
      await this.teamService.addMember(config.defaultTeamId, user.id, 'member');
    }

    return { success: true, user };
  }
}
```

## Approval Queue

```
Admin Dashboard → Users → Pending Approvals
├── John Doe (john@unknown-company.com) - 2 hours ago
│   [Approve] [Reject] [View Details]
├── Jane Smith (jane@partner.com) - 5 hours ago
│   [Approve] [Reject] [View Details]
└── Bulk Actions: [Approve All] [Reject All] [Export]
```

## Open-Source Tools

- **Auth.js** (ISC) — Built-in registration flows
- **Zod** (MIT) — Registration input validation

## Production Considerations

- Rate-limit registration attempts per IP (max 3/hour)
- Email domain validation (check MX records for domain existence)
- Manual approval requests expire after 48 hours
- Notify admins via Slack/email when approval is pending
- Allow bulk approve/reject for large queues
