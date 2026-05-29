# Section 02: Prisma Schema & Migrations

## Overview

Prisma provides the database layer for the voice agent platform, handling schema definition, migration generation, and type-safe client generation. This section covers schema design patterns, migration workflows, seeding strategies, and best practices for managing database changes across development environments.

## Schema Architecture

```text
packages/db/prisma/
├── schema.prisma              # Main schema
├── schema.voice.prisma        # Voice-related models
├── schema.auth.prisma         # Authentication models
├── schema.analytics.prisma    # Analytics models
├── migrations/                # Generated migrations
│   ├── 20240501000000_init/
│   ├── 20240515000000_add_calls/
│   └── 20240601000000_add_vector/
└── seed.ts                    # Seed data
```

## Prisma Schema

```prisma
// packages/db/prisma/schema.prisma
generator client {
  provider        = "prisma-client-js"
  engineType      = "library"
  binaryTargets   = ["native", "linux-amd64", "darwin-arm64"]
  previewFeatures = ["multiSchema", "postgresqlExtensions"]
}

datasource db {
  provider   = "postgresql"
  url        = env("DATABASE_URL")
  extensions = [pgvector, uuid_ossp, pg_stat_statements]
  schemas    = ["public", "voice", "analytics"]
}

// ── Organization ──────────────────────────────────────────
model Organization {
  id        String   @id @default(ulid())
  name      String
  slug      String   @unique
  plan      PlanType @default(free)
  settings  Json?    @default("{}")
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  agents     Agent[]
  campaigns  Campaign[]
  contacts   Contact[]
  users      User[]

  @@map("organizations")
  @@schema("public")
}

enum PlanType {
  free
  starter
  professional
  enterprise
}

// ── User ──────────────────────────────────────────────────
model User {
  id             String   @id @default(ulid())
  organizationId String
  email          String   @unique
  name           String?
  role           UserRole @default(member)
  avatarUrl      String?
  lastLoginAt    DateTime?
  createdAt      DateTime @default(now())
  updatedAt      DateTime @updatedAt

  organization Organization @relation(fields: [organizationId], references: [id])

  @@index([organizationId])
  @@map("users")
  @@schema("public")
}

enum UserRole {
  owner
  admin
  member
  viewer
}

// ── Agent ─────────────────────────────────────────────────
model Agent {
  id              String   @id @default(ulid())
  organizationId  String
  name            String
  description     String?
  voiceProvider   String   @default("elevenlabs")
  voiceId         String
  voiceConfig     Json?    @default("{}")
  llmProvider     String   @default("openai")
  llmModel        String   @default("gpt-4")
  llmConfig       Json?    @default("{}")
  greetingMessage String   @default("Hello!")
  maxCallDuration Int      @default(600)
  temperature     Float    @default(0.7)
  status          String   @default("draft")
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt

  organization Organization @relation(fields: [organizationId], references: [id])
  campaigns    Campaign[]
  calls        Call[]

  @@index([organizationId])
  @@index([status])
  @@map("agents")
  @@schema("voice")
}
```

## Migration Workflow

```bash
# 1. Make schema changes
# Edit schema.prisma to add/modify models

# 2. Generate migration
pnpm --filter @voice-agent/db run db:migrate --name add_call_recording_url

# 3. Review the generated migration
# Check prisma/migrations/20240501_add_call_recording_url/migration.sql

# 4. Apply migration to local database
pnpm --filter @voice-agent/db run db:migrate

# 5. Generate Prisma client
pnpm --filter @voice-agent/db run db:generate

# 6. Commit migration files
git add prisma/migrations/
git commit -m "feat(db): add recording URL to calls"
```

### Generated Migration

```sql
-- prisma/migrations/20240501000001_add_call_recording_url/migration.sql
-- Migration: Add recording URL to calls table

ALTER TABLE voice.calls ADD COLUMN IF NOT EXISTS "recordingUrl" TEXT;
ALTER TABLE voice.calls ADD COLUMN IF NOT EXISTS "transcriptUrl" TEXT;

-- Create index for common queries
CREATE INDEX IF NOT EXISTS idx_calls_recording_url
  ON voice.calls ("recordingUrl")
  WHERE "recordingUrl" IS NOT NULL;
```

## Migration Scripts

```jsonc
{
  "scripts": {
    "db:generate": "prisma generate",
    "db:migrate": "prisma migrate dev",
    "db:migrate:prod": "prisma migrate deploy",
    "db:push": "prisma db push",
    "db:pull": "prisma db pull",
    "db:seed": "tsx prisma/seed.ts",
    "db:reset": "prisma migrate reset --force",
    "db:studio": "prisma studio",
    "db:validate": "prisma validate",
    "db:format": "prisma format"
  }
}
```

## Seed Data Strategy

```typescript
// packages/db/prisma/seed.ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  console.log("🌱 Seeding database...");

  // Clean existing data in dependency order
  await prisma.call.deleteMany();
  await prisma.campaign.deleteMany();
  await prisma.agent.deleteMany();
  await prisma.contact.deleteMany();
  await prisma.user.deleteMany();
  await prisma.organization.deleteMany();

  // Create demo organization
  const org = await prisma.organization.create({
    data: {
      name: "Acme Corp",
      slug: "acme-corp",
      plan: "professional",
      settings: {
        timezone: "America/New_York",
        language: "en-US",
        maxConcurrentCalls: 10,
      },
    },
  });

  // Create admin user
  await prisma.user.create({
    data: {
      organizationId: org.id,
      email: "admin@acme-corp.com",
      name: "Alice Admin",
      role: "admin",
    },
  });

  // Create demo agent
  const agent = await prisma.agent.create({
    data: {
      organizationId: org.id,
      name: "Support Agent",
      voiceProvider: "elevenlabs",
      voiceId: "21m00Tcm4TlvDq8ikWAM",
      voiceConfig: {
        stability: 0.7,
        similarityBoost: 0.8,
        speed: 1.0,
      },
      llmProvider: "openai",
      llmModel: "gpt-4",
      llmConfig: {
        temperature: 0.7,
        maxTokens: 1024,
        systemPrompt: "You are a helpful support agent...",
      },
      greetingMessage: "Hello! Thank you for calling Acme Corp support.",
      status: "active",
    },
  });

  // Create sample contacts
  const contacts = await Promise.all([
    prisma.contact.create({
      data: {
        organizationId: org.id,
        firstName: "John",
        lastName: "Doe",
        email: "john@example.com",
        phone: "+15551234567",
        tags: ["vip", "support"],
      },
    }),
    prisma.contact.create({
      data: {
        organizationId: org.id,
        firstName: "Jane",
        lastName: "Smith",
        email: "jane@example.com",
        phone: "+15557654321",
        tags: ["enterprise"],
      },
    }),
  ]);

  // Create sample campaign
  await prisma.campaign.create({
    data: {
      organizationId: org.id,
      agentId: agent.id,
      name: "Q2 Outreach",
      status: "active",
      schedule: {
        startDate: "2024-04-01",
        endDate: "2024-06-30",
        timezone: "America/New_York",
        windows: [
          { dayOfWeek: 1, startTime: "09:00", endTime: "17:00" },
          { dayOfWeek: 2, startTime: "09:00", endTime: "17:00" },
          { dayOfWeek: 3, startTime: "09:00", endTime: "17:00" },
          { dayOfWeek: 4, startTime: "09:00", endTime: "17:00" },
          { dayOfWeek: 5, startTime: "09:00", endTime: "17:00" },
        ],
      },
    },
  });

  console.log("✅ Seed data created successfully");
  console.log(`  Organization: ${org.name} (${org.id})`);
  console.log(`  Agent: ${agent.name}`);
  console.log(`  Contacts: ${contacts.length}`);
}

main()
  .catch((e) => {
    console.error("❌ Seed failed:", e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
```

## Migration Best Practices

### Naming Conventions

```bash
# Good — descriptive, follows convention
pnpm db:migrate --name add_call_duration_index
pnpm db:migrate --name create_voice_schema
pnpm db:migrate --name add_organization_id_to_calls

# Bad — non-descriptive
pnpm db:migrate --name fix
pnpm db:migrate --name wip
pnpm db:migrate --name updates
```

### Migration Safety

```sql
-- Always use IF NOT EXISTS / IF EXISTS for idempotency
ALTER TABLE voice.calls ADD COLUMN IF NOT EXISTS "recordingUrl" TEXT;

-- Don't drop columns without checking usage
-- Instead, mark as deprecated first, then drop in a later migration

-- For large tables, use NOT VALID + VALIDATE
ALTER TABLE voice.calls ADD CONSTRAINT fk_agent
  FOREIGN KEY ("agentId") REFERENCES voice.agents(id)
  NOT VALID;
ALTER TABLE voice.calls VALIDATE CONSTRAINT fk_agent;
```

## Design Decisions

### Why multiSchema?

The `multiSchema` preview feature organizes models into logical schemas (`public`, `voice`, `analytics`). This provides:
- Database-level schema isolation
- Clear ownership boundaries (voice team owns `voice` schema)
- Independent migration timelines per schema
- Easier compliance (PII in `public`, events in `analytics`)

### ULID vs. UUID vs. Auto-increment

**Decision**: ULID (Universally Unique Lexicographically Sortable Identifier).

**Rationale**: ULIDs are sortable by creation time (unlike UUIDv4), which improves B-tree index performance for time-ordered queries. They're also URL-safe and shorter than UUIDs. Prisma supports `@default(ulid())` natively.

## Integration Points

- **Prisma Client**: Generated from schema, used by repository layer
- **Migration files**: Checked into version control for reproducibility
- **Seed script**: Creates demo data for local development
- **CI/CD**: `prisma migrate deploy` runs during deployment

## Production Considerations

1. **Shadow database**: Prisma Migrate uses a shadow database to detect schema drift. Keep the shadow DB URL in sync with the primary database
2. **Migration locking**: Prisma acquires a lock on the migration table during migrations. For concurrent deployments, use a separate migration runner
3. **Zero-downtime migrations**: Use `db push` with care. For production, always generate explicit migrations and deploy them with `prisma migrate deploy` as a separate step before the application deployment
4. **Migration validation**: Run `prisma migrate deploy --preview-feature --create-only` to generate the SQL without applying it. Review the SQL manually before deployment
5. **Rollback**: Prisma doesn't support rollback. Always create a "down" migration manually if rollback capability is needed
