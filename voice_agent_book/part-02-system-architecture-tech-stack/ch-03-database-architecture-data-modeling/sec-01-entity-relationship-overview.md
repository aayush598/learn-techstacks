# Section 01: Entity Relationship Overview

## Core Domain Model

The database schema is organized around **eight core entities** that form the backbone of the AI Voice Agent platform. Each entity owns its data and relationships, with clear boundaries between domains.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CORE ENTITY RELATIONSHIP DIAGRAM                     │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                         TENANT                                  │    │
│  │  (Organization — top-level multi-tenant boundary)               │    │
│  └──────────┬────────────────────────────────────┬─────────────────┘    │
│             │                                    │                      │
│     ┌───────┴────────┐              ┌────────────┴──────────┐          │
│     ▼                 ▼              ▼                       ▼          │
│  ┌──────┐       ┌─────────┐   ┌──────────┐          ┌──────────┐      │
│  │ USER │       │  AGENT  │   │CAMPAIGN  │          │SUBSCRIPTION│     │
│  │      │       │         │   │          │          │           │      │
│  │ pk id│──┐    │ pk id   │   │ pk id    │          │ pk id     │      │
│  │ fk:  │  │    │ fk:     │   │ fk:      │          │ fk:       │      │
│  │tenant│  │    │tenant_id│   │tenant_id │          │tenant_id  │      │
│  └──┬───┘  │    └────┬────┘   └────┬─────┘          └───────────┘      │
│     │      │         │             │                                    │
│     │      │    ┌────┴────┐   ┌────┴──────┐                            │
│     │      └────┤-created │   │-contacts  │                            │
│     │           │-versions│   │-attempts  │                            │
│     │           └─────────┘   └───────────┘                            │
│     │                                                                  │
│     ▼                                                                  │
│  ┌────────────────────────────────────────────────────────┐            │
│  │                        CALL                            │            │
│  │  (Core transactional entity — each voice interaction)  │            │
│  │                                                         │            │
│  │  pk: id  |  fk: tenant_id  |  fk: agent_id              │            │
│  │  fk: campaign_id (nullable) | fk: created_by (user)     │            │
│  └──────────┬─────────────────────────────────────────────┘            │
│             │                                                          │
│     ┌───────┴───────────┐                                              │
│     ▼                   ▼                                              │
│  ┌─────────┐      ┌────────────┐                                      │
│  │RECORDING│      │CONVERSATION│                                      │
│  │         │      │  (Events)  │                                      │
│  │ pk id   │      │            │                                      │
│  │ fk:call │      │ pk id      │                                      │
│  │ fk:tenant│     │ fk: call   │                                      │
│  └─────────┘      └────────────┘                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Extended Entity Relationship Diagram

```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│     Tenant       │1────N─│      User        │1────N─│   UserRole      │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │       │ id (PK)         │
│ name             │       │ tenant_id (FK)    │       │ user_id (FK)    │
│ slug (UQ)        │       │ email (UQ)        │       │ role             │
│ config (JSON)    │       │ name              │       │ scope           │
│ status           │       │ password_hash     │       │ granted_by      │
│ created_at       │       │ avatar_url        │       │ granted_at      │
│ updated_at       │       │ last_login        │       └──────────────────┘
│                  │       │ status            │
│                  │       │ created_at        │        ┌──────────────────┐
│                  │       │ updated_at        │        │   Agent          │
└──────────────────┘       └──────────────────┘        ├──────────────────┤
       │                                                │ id (PK)         │
       │1                                               │ tenant_id (FK)   │
       │                                                │ name             │
       ▼                                                │ description      │
┌──────────────────┐                                    │ voice_id (FK)   │
│  PlanDefinition  │                                    │ prompt_id (FK)  │
├──────────────────┤                                    │ language         │
│ id (PK)          │                                    │ status           │
│ name             │                                    │ config (JSON)    │
│ tier             │                                    │ created_by (FK)  │
│ price_cents      │                                    │ deployed_at      │
│ features (JSON)  │                                    │ created_at       │
│ limits (JSON)    │                                    │ updated_at       │
│ is_active        │                                    └────────┬─────────┘
│ created_at       │                                             │1
│ updated_at       │                                             │
└──────────────────┘                                     ┌──────┴──────────┐
       │                                                   │                │
       │1                                                  ▼                ▼
       │                                         ┌────────────────┐ ┌──────────────┐
       ▼                                         │  AgentVersion  │ │    Prompt    │
┌──────────────────┐                            ├────────────────┤ ├──────────────┤
│  Subscription    │                            │ id (PK)        │ │ id (PK)     │
├──────────────────┤                            │ agent_id (FK)   │ │ tenant_id(FK)│
│ id (PK)          │                            │ version         │ │ name         │
│ tenant_id (FK)   │                            │ config (JSON)   │ │ content      │
│ plan_id (FK)     │                            │ publish_note    │ │ variables    │
│ status           │                            │ created_by (FK) │ │ created_by   │
│ current_period_  │                            │ created_at      │ │ created_at   │
│   start          │                            │ is_active       │ │ updated_at   │
│ current_period_  │                            └────────────────┘ └──────────────┘
│   end            │
│ canceled_at      │       ┌──────────────────┐
│ trial_end        │       │    Voice          │
│ created_at       │       ├──────────────────┤
│ updated_at       │       │ id (PK)          │
└──────────────────┘       │ tenant_id (FK)    │
       │                   │ name              │
       │1                  │ provider          │
       ▼                   │ voice_id          │
┌──────────────────┐       │ language          │
│  UsageRecord     │       │ gender            │
├──────────────────┤       │ preview_url       │
│ id (PK)          │       │ is_default        │
│ tenant_id (FK)   │       │ created_at        │
│ subscription_id  │       └──────────────────┘
│   (FK)           │
│ metric           │       ┌──────────────────┐
│ amount           │       │  Campaign         │
│ unit             │       ├──────────────────┤
│ recorded_at      │       │ id (PK)          │
│ source           │       │ tenant_id (FK)    │
└──────────────────┘       │ agent_id (FK)     │
                           │ name              │
┌──────────────────┐       │ type              │
│     Call          │       │ status            │
├──────────────────┤       │ schedule (JSON)   │
│ id (PK)          │       │ config (JSON)     │
│ tenant_id (FK)   │       │ started_at        │
│ agent_id (FK)    │       │ completed_at      │
│ campaign_id (FK) │       │ created_by (FK)   │
│ caller_number    │       │ created_at        │
│ called_number    │       │ updated_at        │
│ direction        │       └────────┬──────────┘
│ status           │                │
│ duration         │                ▼
│ cost_micro_us    │       ┌──────────────────┐       ┌──────────────────┐
│ stt_latency_ms   │       │   ContactList    │1────N─│    Contact       │
│ ai_latency_ms    │       ├──────────────────┤       ├──────────────────┤
│ tts_latency_ms   │       │ id (PK)          │       │ id (PK)          │
|| sentiment_score  │       │ tenant_id        │       │ contact_list_id  │
│ recording_url    │       │ campaign_id (FK)  │       │ phone            │
│ transcript_url   │       │ name              │       │ email            │
│ started_at       │       │ description       │       │ first_name       │
│ ended_at         │       │ created_by        │       │ last_name        │
│ created_at       │       │ created_at        │       │ metadata (JSON)  │
│ updated_at       │       │ updated_at        │       │ status           │
└──────────────────┘       └──────────────────┘       │ created_at       │
       │                                               │ updated_at       │
       ▼                                               └──────────────────┘
┌──────────────────┐       ┌──────────────────┐
│  Conversation    │       │  CallAttempt     │
│  Event           │       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ call_id (FK)     │       │ contact_id (FK)  │
│ agent_id (FK)    │       │ campaign_id (FK) │
│ type             │       │ call_id (FK)     │
│ payload (JSON)   │       │ attempt_number   │
│ timestamp        │       │ status           │
│ created_at       │       │ scheduled_at     │
└──────────────────┘       │ dialed_at        │
                           │ result           │
                           │ duration         │
┌──────────────────┐       │ notes            │
│   KnowledgeBase  │       │ created_at       │
├──────────────────┤       └──────────────────┘
│ id (PK)          │
│ tenant_id (FK)   │
│ agent_id (FK)    │
│ name             │
│ type             │
│ config (JSON)    │
│ chunk_count      │
│ status           │
│ created_by       │
│ created_at       │
│ updated_at       │
└──────────────────┘
```

## Prisma Schema (Core Models)

```prisma
// prisma/schema.prisma — Core entities

generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["postgresqlExtensions"]
}

datasource db {
  provider   = "postgresql"
  url        = env("DATABASE_URL")
  extensions = [pgvector, pgcrypto, pg_partman]
}

// ── Multi-Tenant Base ──
model Tenant {
  id        String   @id @default(uuid()) @db.Uuid
  slug      String   @unique @db.VarChar(100)
  name      String   @db.VarChar(255)
  config    Json     @default("{}")
  status    TenantStatus @default(active)
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  users         User[]
  agents        Agent[]
  calls         Call[]
  campaigns     Campaign[]
  voices        Voice[]
  prompts       Prompt[]
  subscriptions Subscription[]
  usageRecords  UsageRecord[]
  knowledgeBases KnowledgeBase[]

  @@map("tenants")
}

enum TenantStatus {
  active
  suspended
  canceled
  trial
}

model User {
  id           String    @id @default(uuid()) @db.Uuid
  tenantId     String    @map("tenant_id") @db.Uuid
  email        String    @unique @db.VarChar(255)
  name         String    @db.VarChar(255)
  passwordHash String?   @map("password_hash")
  avatarUrl    String?   @map("avatar_url") @db.VarChar(500)
  lastLogin    DateTime? @map("last_login")
  status       UserStatus @default(active)
  createdAt    DateTime  @default(now()) @map("created_at")
  updatedAt    DateTime  @updatedAt @map("updated_at")

  tenant       Tenant     @relation(fields: [tenantId], references: [id])
  roles        UserRole[]
  createdAgents Agent[]   @relation("AgentCreator")
  campaigns    Campaign[] @relation("CampaignCreator")

  @@unique([tenantId, email])
  @@map("users")
}

enum UserStatus {
  active
  invited
  disabled
  deleted
}

model UserRole {
  id        String   @id @default(uuid()) @db.Uuid
  userId    String   @map("user_id") @db.Uuid
  role      RoleType
  scope     String?  @db.VarChar(100)
  grantedBy String?  @map("granted_by") @db.Uuid
  grantedAt DateTime @default(now()) @map("granted_at")

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([userId, role, scope])
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

model Agent {
  id          String       @id @default(uuid()) @db.Uuid
  tenantId    String       @map("tenant_id") @db.Uuid
  name        String       @db.VarChar(255)
  description String?      @db.Text
  voiceId     String       @map("voice_id") @db.Uuid
  promptId    String       @map("prompt_id") @db.Uuid
  language    String       @default("en-US") @db.VarChar(10)
  status      AgentStatus  @default(draft)
  config      Json         @default("{}")
  createdBy   String       @map("created_by") @db.Uuid
  deployedAt  DateTime?    @map("deployed_at")
  createdAt   DateTime     @default(now()) @map("created_at")
  updatedAt   DateTime     @updatedAt @map("updated_at")

  tenant      Tenant       @relation(fields: [tenantId], references: [id])
  voice       Voice        @relation(fields: [voiceId], references: [id])
  prompt      Prompt       @relation(fields: [promptId], references: [id])
  createdByUser User       @relation("AgentCreator", fields: [createdBy], references: [id])
  versions    AgentVersion[]
  calls       Call[]
  campaigns   Campaign[]
  knowledgeBases KnowledgeBase[]

  @@index([tenantId, status])
  @@index([tenantId, createdAt])
  @@map("agents")
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Primary Keys | UUID v4 (not auto-increment) | Security (no sequential IDs), distributed generation |
| Timestamps | UTC with timezone | Consistent across geographic regions |
| Soft Deletes | status/deleted_at pattern | Audit trail, recovery capability |
| JSON Columns | Config, metadata fields | Flexible schema evolution without migrations |
| Index Strategy | Composite (tenant_id, created_at) | All queries filtered by tenant, sorted by time |

## Integration Points

- **Part 16 (User Management)** — User and role tables
- **Part 17 (Billing)** — Subscription and usage tables
- **Part 09 (Campaign Management)** — Campaign and contact tables
- **Part 04 (Core Voice)** — Call and conversation tables

## Production Considerations

- **Row-Level Security (RLS)**: All tables have RLS policies ensuring tenant isolation at the database level
- **Partitioning**: Large tables (calls, events, usage_records) are partitioned by month
- **Connection Pooling**: PgBouncer for connection management, max 500 connections per pool
- **Migration Strategy**: Prisma migrate with automated CI/CD validation
- **Backup**: WAL streaming to standby + daily pg_dump to MinIO
