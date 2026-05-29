# Section 02: User & Tenant Schema

## Multi-Tenant Data Model

The platform uses a **shared-database, row-level-security** approach to multi-tenancy. All tenants share the same database tables, but Row-Level Security (RLS) policies ensure complete data isolation at the database level.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      TENANT & USER SCHEMA                               │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      TENANT (Organization)                      │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  Tenant A    │  │  Tenant B    │  │  Tenant C    │          │    │
│  │  │  (Acme Corp) │  │  (Beta Inc)  │  │  (Gamma LLC) │          │    │
│  │  │              │  │              │  │              │          │    │
│  │  │  slug: acme  │  │  slug: beta  │  │  slug: gamma │          │    │
│  │  │  plan: pro   │  │  plan: free  │  │  plan:enterpr│          │    │
│  │  │  users: 15   │  │  users: 3    │  │  users: 150  │          │    │
│  │  │  agents: 5   │  │  agents: 1   │  │  agents: 50  │          │    │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │    │
│  └─────────┼──────────────────┼──────────────────┼──────────────────┘    │
│            │                  │                  │                       │
│  ┌─────────┴──────────────────┴──────────────────┴──────────────────┐    │
│  │                          USERS TABLE                              │    │
│  │                                                                   │    │
│  │  ┌─────────┬──────────┬──────────┬──────────┬────────────────┐    │    │
│  │  │  id     │ tenant_id│  email   │  name    │  status         │    │    │
│  │  ├─────────┼──────────┼──────────┼──────────┼────────────────┤    │    │
│  │  │ u1      │ t_acme   │ alice@.. │ Alice   │ active          │    │    │
│  │  │ u2      │ t_acme   │ bob@..   │ Bob     │ active          │    │    │
│  │  │ u3      │ t_beta   │ charlie@ │ Charlie │ active          │    │    │
│  │  │ u4      │ t_acme   │ dave@..  │ Dave     │ invited         │    │    │
│  │  │ u5      │ t_gamma  │ eve@..   │ Eve     │ active          │    │    │
│  │  └─────────┴──────────┴──────────┴──────────┴────────────────┘    │    │
│  │                                                                   │    │
│  │  RLS Policy: WHERE tenant_id = current_setting('app.tenant_id')   │    │
│  └───────────────────────────────────────────────────────────────────┘    │
│                                                                           │
│  ┌───────────────────────────────────────────────────────────────────┐    │
│  │                    USER ROLES TABLE                               │    │
│  │                                                                   │    │
│  │  ┌─────────┬──────────┬─────────────┬───────────┬────────────────┐│    │
│  │  │  id     │ user_id  │  role        │  scope    │  granted_at    ││    │
│  │  ├─────────┼──────────┼─────────────┼───────────┼────────────────┤│    │
│  │  │ r1      │ u1       │ admin        │ *         │ 2024-01-15     ││    │
│  │  │ r2      │ u2       │ agent_manager│ *         │ 2024-01-15     ││    │
│  │  │ r3      │ u5       │ call_viewer  │ agents:5  │ 2024-02-01     ││    │
│  │  │ r4      │ u5       │ analytics_   │ *         │ 2024-02-01     ││    │
│  │  │         │          │ viewer       │           │                ││    │
│  │  └─────────┴──────────┴─────────────┴───────────┴────────────────┘│    │
│  └───────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Prisma Schema

```prisma
// Tenant model with configuration
model Tenant {
  id        String       @id @default(uuid()) @db.Uuid
  slug      String       @unique @db.VarChar(100)
  name      String       @db.VarChar(255)
  config    Json         @default("{}")
  status    TenantStatus @default(active)
  createdAt DateTime     @default(now()) @map("created_at")
  updatedAt DateTime     @updatedAt @map("updated_at")

  users         User[]
  agents        Agent[]
  calls         Call[]
  campaigns     Campaign[]
  voices        Voice[]
  prompts       Prompt[]
  subscriptions Subscription[]
  usageRecords  UsageRecord[]
  knowledgeBases           KnowledgeBase[]
  webhookEndpoints         WebhookEndpoint[]
  apiKeys                  ApiKey[]
  auditLogs                AuditLog[]
  notificationPreferences  NotificationPreference[]

  @@map("tenants")
}

enum TenantStatus {
  active
  suspended
  canceled
  trial
}

// Tenant configuration shape
// {
//   "features": {
//     "advanced_analytics": true,
//     "custom_voices": false,
//     "white_label": true,
//     "sla_tier": "standard"
//   },
//   "limits": {
//     "max_agents": 50,
//     "max_calls_per_day": 10000,
//     "max_team_members": 150,
//     "storage_gb": 500
//   },
//   "branding": {
//     "primary_color": "#6366f1",
//     "logo_url": "https://cdn...",
//     "favicon_url": "https://cdn...",
//     "custom_domain": "voice.acme.com"
//   },
//   "security": {
//     "sso_enabled": true,
//     "sso_provider": "saml",
//     "sso_config": { ... },
//     "password_policy": {
//       "min_length": 12,
//       "require_special": true,
//       "require_mfa": true
//     }
//   }
// }

// User model
model User {
  id           String     @id @default(uuid()) @db.Uuid
  tenantId     String     @map("tenant_id") @db.Uuid
  email        String     @db.VarChar(255)
  name         String     @db.VarChar(255)
  passwordHash String?    @map("password_hash")
  avatarUrl    String?    @map("avatar_url") @db.VarChar(500)
  timezone     String     @default("UTC") @db.VarChar(50)
  locale       String     @default("en-US") @db.VarChar(10)
  lastLogin    DateTime?  @map("last_login")
  lastIp       String?    @map("last_ip") @db.VarChar(45)
  status       UserStatus @default(active)
  createdAt    DateTime   @default(now()) @map("created_at")
  updatedAt    DateTime   @updatedAt @map("updated_at")

  tenant              Tenant        @relation(fields: [tenantId], references: [id])
  roles               UserRole[]
  createdAgents       Agent[]        @relation("AgentCreator")
  campaigns           Campaign[]     @relation("CampaignCreator")
  auditLogs           AuditLog[]     @relation("AuditLogActor")
  apiKeys             ApiKey[]
  notificationPreferences NotificationPreference[]
  sessions            Session[]

  @@unique([tenantId, email])
  @@index([tenantId, status])
  @@index([email])
  @@map("users")
}

enum UserStatus {
  active
  invited
  disabled
  deleted
}

// User roles with scoped permissions
model UserRole {
  id        String   @id @default(uuid()) @db.Uuid
  userId    String   @map("user_id") @db.Uuid
  role      RoleType
  scope     String?  @db.VarChar(100)  // "*" for all, "agents:5" for specific agent
  grantedBy String?  @map("granted_by") @db.Uuid
  grantedAt DateTime @default(now()) @map("granted_at")

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([userId, role, scope])
  @@index([userId])
  @@map("user_roles")
}

enum RoleType {
  owner
  admin
  agent_manager
  call_viewer
  analytics_viewer
  developer
  billing_admin
}

// Session management
model Session {
  id        String   @id @default(uuid()) @db.Uuid
  userId    String   @map("user_id") @db.Uuid
  token     String   @unique @db.VarChar(500)
  ipAddress String?  @map("ip_address") @db.VarChar(45)
  userAgent String?  @map("user_agent") @db.Text
  expiresAt DateTime @map("expires_at")
  createdAt DateTime @default(now()) @map("created_at")
  lastUsed  DateTime? @map("last_used")

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([token])
  @@index([expiresAt])
  @@map("sessions")
}

// Invite model for team invitations
model Invite {
  id         String       @id @default(uuid()) @db.Uuid
  tenantId   String       @map("tenant_id") @db.Uuid
  email      String       @db.VarChar(255)
  role       RoleType
  invitedBy  String       @map("invited_by") @db.Uuid
  token      String       @unique @db.VarChar(500)
  status     InviteStatus @default(pending)
  expiresAt  DateTime     @map("expires_at")
  acceptedAt DateTime?    @map("accepted_at")
  createdAt  DateTime     @default(now()) @map("created_at")

  tenant    Tenant @relation(fields: [tenantId], references: [id])

  @@index([tenantId])
  @@index([token])
  @@map("invites")
}

enum InviteStatus {
  pending
  accepted
  expired
  revoked
}
```

## Row-Level Security (RLS) Implementation

```sql
-- RLS policies enforced at the database level

-- Enable RLS on all tenant-scoped tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE calls ENABLE ROW LEVEL SECURITY;
-- ... all other tables

-- Create policy function
CREATE OR REPLACE FUNCTION app.current_tenant_id()
RETURNS UUID AS $$
  SELECT NULLIF(
    current_setting('app.tenant_id', TRUE),
    ''
  )::UUID;
$$ LANGUAGE SQL STABLE;

-- Tenant isolation policy
CREATE POLICY tenant_isolation ON users
  FOR ALL
  USING (tenant_id = app.current_tenant_id())
  WITH CHECK (tenant_id = app.current_tenant_id());

CREATE POLICY tenant_isolation ON agents
  FOR ALL
  USING (tenant_id = app.current_tenant_id())
  WITH CHECK (tenant_id = app.current_tenant_id());

-- Cross-tenant admin access (for platform admin)
CREATE POLICY admin_access ON users
  FOR SELECT
  USING (
    app.current_tenant_id() IS NULL  -- No tenant context = admin
    OR tenant_id = app.current_tenant_id()
  );
```

## Team Invitation Flow

```typescript
// lib/team/invite.ts
import { prisma } from '@/lib/db'
import { sendEmail } from '@/lib/email'
import { createToken } from '@/lib/crypto'
import { revalidatePath } from 'next/cache'

export async function inviteTeamMember(
  tenantId: string,
  invitedByUserId: string,
  email: string,
  role: RoleType
) {
  // 1. Check if user already exists in tenant
  const existingUser = await prisma.user.findFirst({
    where: { tenantId, email }
  })
  if (existingUser) {
    throw new Error('User already belongs to this tenant')
  }

  // 2. Check invite limit
  const activeInvites = await prisma.invite.count({
    where: {
      tenantId,
      status: 'pending',
      expiresAt: { gt: new Date() }
    }
  })
  const tenantConfig = await prisma.tenant.findUnique({
    where: { id: tenantId },
    select: { config: true }
  })
  const maxTeamMembers = (tenantConfig?.config as any)?.limits?.max_team_members ?? 10
  if (activeInvites >= maxTeamMembers) {
    throw new Error('Team member limit reached')
  }

  // 3. Create invite
  const token = await createToken(48) // 48 character token
  const invite = await prisma.invite.create({
    data: {
      tenantId,
      email,
      role,
      invitedBy: invitedByUserId,
      token,
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7 days
    }
  })

  // 4. Send invitation email
  await sendEmail({
    to: email,
    template: 'team-invite',
    data: {
      inviteUrl: `${process.env.APP_URL}/auth/accept-invite?token=${token}`,
      expiresIn: '7 days',
      role
    }
  })

  return { success: true, inviteId: invite.id }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Multi-Tenancy | Row-Level Security (shared DB) | Lower operational cost, simpler schema |
| User ID | UUID v4 | No enumeration, distributed-safe |
| Password | bcrypt hash (cost 12) | Industry standard for password storage |
| Sessions | Separate session table | Revocable, refreshable, audit trail |
| Roles | Scoped permissions | Fine-grained access control per resource |
| Invites | Token-based with expiry | Secure onboarding, automatic cleanup |

## Integration Points

- **Part 16 (User Management)** — Full user management implementation
- **Part 15 (Security)** — RLS is a critical security control
- **Part 10 (Integrations)** — API keys linked to users via tenant context

## Production Considerations

- **RLS Performance**: Ensure `tenant_id` is indexed on all tables; RLS adds ~5% overhead
- **Connection Pooling**: Set `app.tenant_id` at connection pool level to avoid per-query overhead
- **Rate Limiting**: Max 10 invites per hour per tenant to prevent abuse
- **Cleanup**: Expired invites cleaned up via pg_cron nightly
- **Audit Trail**: All role changes logged in audit_log table
- **MFA**: Multi-factor authentication enforced via tenant config for enterprise tenants
