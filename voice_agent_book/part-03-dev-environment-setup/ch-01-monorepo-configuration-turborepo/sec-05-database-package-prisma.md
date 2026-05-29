# Section 05: Database Package (Prisma)

## Overview

The database package (`@voice-agent/db`) encapsulates all database access logic, including the Prisma schema, client generation, migration scripts, and seed data. This package is the sole interface between application code and the database, enforcing a repository pattern and preventing direct Prisma usage in business logic.

## Package Architecture

```text
packages/db/
├── prisma/
│   ├── schema.prisma          # Main schema definition
│   ├── schema.voice.prisma    # Voice-related models (partial)
│   ├── schema.auth.prisma     # Auth-related models (partial)
│   ├── migrations/            # Auto-generated migrations
│   └── seed.ts                # Seed data script
├── src/
│   ├── client.ts              # Prisma client singleton
│   ├── repositories/          # Repository pattern implementations
│   │   ├── agent.repo.ts
│   │   ├── call.repo.ts
│   │   ├── campaign.repo.ts
│   │   ├── contact.repo.ts
│   │   └── organization.repo.ts
│   ├── types.ts               # Exported Prisma-generated types
│   ├── errors.ts              # Database-specific errors
│   ├── utils.ts               # Query helpers, pagination, etc.
│   └── index.ts               # Barrel exports
├── tsconfig.json
└── package.json
```

## Prisma Schema Design

```prisma
// packages/db/prisma/schema.prisma

generator client {
  provider        = "prisma-client-js"
  engineType      = "library"
  binaryTargets   = ["native", "linux-amd64"]
  previewFeatures = ["multiSchema", "postgresqlExtensions", "views"]
}

datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  extensions = [pgvector, postgis, uuid_ossp]
  schemas   = ["public", "voice", "analytics"]
}

// ── Organization / Multi-tenant ──────────────────────────────

model Organization {
  id        String   @id @default(ulid())
  name      String
  slug      String   @unique
  plan      PlanType @default(free)
  settings  Json?    @default("{}")
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  agents    Agent[]
  campaigns Campaign[]
  contacts  Contact[]

  @@map("organizations")
  @@schema("public")
}

enum PlanType {
  free
  starter
  professional
  enterprise
}

// ── Agent ────────────────────────────────────────────────────

model Agent {
  id              String   @id @default(ulid())
  organizationId  String
  name            String
  description     String?
  voiceProvider   String   @default("elevenlabs")
  voiceId         String
  greetingMessage String
  maxCallDuration Int      @default(600)
  temperature     Float    @default(0.7)
  llmProvider     String   @default("openai")
  llmModel        String   @default("gpt-4")
  status          String   @default("draft")
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt

  organization Organization @relation(fields: [organizationId], references: [id])
  campaigns    Campaign[]
  calls        Call[]

  @@index([organizationId])
  @@map("agents")
  @@schema("voice")
}

// ── Call ─────────────────────────────────────────────────────

model Call {
  id             String   @id @default(ulid())
  organizationId String
  agentId        String
  contactId      String?
  campaignId     String?
  status         CallStatus @default(initiating)
  direction      CallDirection
  fromNumber     String?
  toNumber       String?
  duration       Int?
  recordingUrl   String?
  transcriptUrl  String?
  cost           Decimal?  @db.Decimal(10, 6)
  startedAt      DateTime?
  endedAt        DateTime?
  createdAt      DateTime  @default(now())
  updatedAt      DateTime  @updatedAt

  organization Organization @relation(fields: [organizationId], references: [id])
  agent        Agent        @relation(fields: [agentId], references: [id])
  contact      Contact?     @relation(fields: [contactId], references: [id])
  campaign     Campaign?    @relation(fields: [campaignId], references: [id])

  @@index([organizationId, status])
  @@index([agentId, createdAt])
  @@index([createdAt])
  @@map("calls")
  @@schema("voice")
}

enum CallStatus {
  initiating
  ringing
  in_progress
  transferring
  completed
  failed
  busy
  no_answer
}

enum CallDirection {
  inbound
  outbound
}

// ── Contact ──────────────────────────────────────────────────

model Contact {
  id             String   @id @default(ulid())
  organizationId String
  firstName      String
  lastName       String
  email          String?
  phone          String
  tags           String[] @default([])
  customFields   Json?    @default("{}")
  createdAt      DateTime @default(now())
  updatedAt      DateTime @updatedAt

  organization Organization @relation(fields: [organizationId], references: [id])
  calls        Call[]

  @@index([organizationId, phone])
  @@index([organizationId, email])
  @@map("contacts")
  @@schema("public")
}

// ── Campaign ─────────────────────────────────────────────────

model Campaign {
  id             String        @id @default(ulid())
  organizationId String
  agentId        String
  name           String
  status         CampaignStatus @default(draft)
  schedule       Json?
  callWindow     Json?
  maxAttempts    Int           @default(3)
  createdAt      DateTime      @default(now())
  updatedAt      DateTime      @updatedAt

  organization Organization @relation(fields: [organizationId], references: [id])
  agent        Agent        @relation(fields: [agentId], references: [id])
  calls        Call[]

  @@index([organizationId, status])
  @@map("campaigns")
  @@schema("voice")
}

enum CampaignStatus {
  draft
  active
  paused
  completed
  archived
}
```

## Client Singleton

```typescript
// packages/db/src/client.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log:
      process.env.NODE_ENV === "development"
        ? ["query", "error", "warn"]
        : ["error"],
  });

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}
```

The singleton pattern prevents multiple Prisma client instances during hot reload in development. The global variable pattern is the officially recommended approach for Next.js.

## Repository Pattern

```typescript
// packages/db/src/repositories/agent.repo.ts
import { prisma } from "../client";
import type { Prisma } from "@prisma/client";
import { DatabaseError } from "../errors";

export class AgentRepository {
  async findById(id: string, organizationId: string) {
    try {
      return await prisma.agent.findFirst({
        where: { id, organizationId },
        include: {
          organization: { select: { name: true, plan: true } },
          _count: { select: { calls: true, campaigns: true } },
        },
      });
    } catch (error) {
      throw new DatabaseError("Failed to find agent", { cause: error });
    }
  }

  async findMany(params: {
    organizationId: string;
    status?: string;
    page?: number;
    pageSize?: number;
  }) {
    const { organizationId, status, page = 1, pageSize = 20 } = params;
    const skip = (page - 1) * pageSize;

    try {
      const [agents, total] = await Promise.all([
        prisma.agent.findMany({
          where: { organizationId, ...(status && { status }) },
          orderBy: { createdAt: "desc" },
          skip,
          take: pageSize,
        }),
        prisma.agent.count({
          where: { organizationId, ...(status && { status }) },
        }),
      ]);

      return { agents, total, page, pageSize, totalPages: Math.ceil(total / pageSize) };
    } catch (error) {
      throw new DatabaseError("Failed to query agents", { cause: error });
    }
  }

  async create(data: Prisma.AgentCreateInput) {
    try {
      return await prisma.agent.create({ data });
    } catch (error) {
      throw new DatabaseError("Failed to create agent", { cause: error });
    }
  }

  async update(id: string, organizationId: string, data: Prisma.AgentUpdateInput) {
    try {
      return await prisma.agent.update({
        where: { id, organizationId },
        data,
      });
    } catch (error) {
      throw new DatabaseError("Failed to update agent", { cause: error });
    }
  }

  async delete(id: string, organizationId: string) {
    try {
      await prisma.agent.update({
        where: { id, organizationId },
        data: { status: "archived" },
      });
    } catch (error) {
      throw new DatabaseError("Failed to archive agent", { cause: error });
    }
  }
}

export const agentRepository = new AgentRepository();
```

## Migration Scripts

```jsonc
{
  "scripts": {
    "db:generate": "prisma generate",
    "db:migrate": "prisma migrate dev",
    "db:migrate:prod": "prisma migrate deploy",
    "db:push": "prisma db push",
    "db:seed": "tsx prisma/seed.ts",
    "db:reset": "prisma migrate reset --force",
    "db:studio": "prisma studio",
    "db:validate": "prisma validate"
  }
}
```

### Migration Workflow

```text
Development Flow:
  prisma migrate dev --name add_call_duration_index
       │
       ▼
  Creates migration file → prisma/migrations/20240501_add_call_duration_index/
       │
       ▼
  Applies to local DB
       │
       ▼
  Generates updated Prisma client

Production Flow:
  prisma migrate deploy
       │
       ▼
  Applies pending migrations sequentially
       │
       ▼
  No client generation (done during build)
```

## Seed Data Strategy

```typescript
// packages/db/prisma/seed.ts
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  // Clean existing data
  await prisma.call.deleteMany();
  await prisma.campaign.deleteMany();
  await prisma.agent.deleteMany();
  await prisma.contact.deleteMany();
  await prisma.organization.deleteMany();

  // Create demo organization
  const org = await prisma.organization.create({
    data: {
      name: "Acme Corp",
      slug: "acme-corp",
      plan: "professional",
    },
  });

  // Create demo agent
  const agent = await prisma.agent.create({
    data: {
      organizationId: org.id,
      name: "Support Agent",
      voiceProvider: "elevenlabs",
      voiceId: "21m00Tcm4TlvDq8ikWAM",
      greetingMessage: "Hello! Thank you for calling Acme Corp support.",
      llmProvider: "openai",
      llmModel: "gpt-4",
      status: "active",
    },
  });

  // Create sample contacts
  await prisma.contact.createMany({
    data: [
      { organizationId: org.id, firstName: "John", lastName: "Doe", phone: "+15551234567" },
      { organizationId: org.id, firstName: "Jane", lastName: "Smith", phone: "+15557654321" },
      { organizationId: org.id, firstName: "Bob", lastName: "Johnson", phone: "+15559876543" },
    ],
  });

  // Create sample campaign
  await prisma.campaign.create({
    data: {
      organizationId: org.id,
      agentId: agent.id,
      name: "Q2 Outreach",
      status: "active",
    },
  });

  console.log("Seed data created successfully");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
```

## Design Decisions

### Why wrap Prisma in repositories?

Direct Prisma usage in controllers leads to:
- Tight coupling to Prisma's query API
- Difficulty mocking in tests
- Scattered query logic across the codebase
- No central place for cross-cutting concerns (soft deletes, audit logging, tenant isolation)

The repository pattern provides a clean seam for testing and a single place to enforce organizational policies.

### `schema.prisma` splitting

Using the `multiSchema` preview feature, we organize models into logical schemas (`public`, `voice`, `analytics`). This provides:
- Clear ownership boundaries
- Database-level schema isolation
- Migration independence for different domains

## Integration Points

- **apps/api**: Imports repositories to handle API requests
- **apps/web**: Imports repositories for server components and server actions
- **packages/voice**: May import for writing call records
- **packages/ai**: May import for reading agent configuration

## Production Considerations

1. **Connection pooling**: Use PgBouncer in production and configure Prisma for connection pooling with `?pgbouncer=true` in the DATABASE_URL
2. **Migration safety**: Run `prisma migrate deploy` as a separate step before deploying new application code — never auto-migrate in production
3. **Shadow database**: Prisma Migrate uses a shadow database to detect schema drift. Keep it in sync with the main database
4. **Query logging**: Enable query logging only in development — in production, log only errors and slow queries (>100ms)
5. **Type safety**: Always use Prisma-generated types rather than manually defining database types. This ensures type-safety is never out of sync with the actual schema
