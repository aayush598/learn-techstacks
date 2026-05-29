# Section 06: Seed Data Strategy

## Overview

Seed data creates a realistic development environment that makes the application immediately useful after setup. A well-designed seed strategy includes demo organizations, sample agents with voice configurations, test contacts, fake call records with transcripts, and campaign data that exercises all application features.

## Seed Data Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              Seed Data Structure                              │
│                                                              │
│  1 Demo Organization                                          │
│  ├── 2 Users (admin + member)                               │
│  ├── 3 Agents (support, sales, survey)                      │
│  ├── 5 Contacts (diverse scenarios)                         │
│  ├── 2 Campaigns (active + completed)                       │
│  └── 20 Call Records (various statuses)                     │
│      ├── 5 completed calls                                  │
│      ├── 3 failed calls                                     │
│      ├── 2 in-progress calls                                │
│      └── 10 historical calls (for analytics)                │
│                                                              │
│  Factory functions for generating realistic data:            │
│  - faker.js for names, phones, emails                       │
│  - Random timestamps within reasonable ranges               │
│  - Realistic call durations (30s - 30min)                   │
│  - Various call outcomes (completed, failed, busy, etc.)    │
└─────────────────────────────────────────────────────────────┘
```

## Factory Functions

```typescript
// packages/db/prisma/factories.ts
import { faker } from "@faker-js/faker";

export function createOrganization(index: number = 1) {
  const companyName = faker.company.name();
  return {
    name: companyName,
    slug: faker.helpers.slugify(companyName).toLowerCase(),
    plan: faker.helpers.arrayElement([
      "free",
      "starter",
      "professional",
    ] as const),
    settings: {
      timezone: "America/New_York",
      language: "en-US",
      maxConcurrentCalls: faker.number.int({ min: 5, max: 50 }),
      notifications: {
        email: true,
        slack: faker.datatype.boolean(),
      },
    },
  };
}

export function createAgent(organizationId: string, index: number = 1) {
  const providers = {
    voice: ["elevenlabs", "cartesia", "deepgram"] as const,
    llm: ["openai", "anthropic"] as const,
  };

  const voiceProvider = faker.helpers.arrayElement(providers.voice);
  const llmProvider = faker.helpers.arrayElement(providers.llm);

  return {
    organizationId,
    name: faker.helpers.arrayElement([
      "Support Agent",
      "Sales Assistant",
      "Survey Bot",
      "Customer Success",
      "Tech Support",
    ]),
    description: faker.lorem.sentence(),
    voiceProvider,
    voiceId: faker.string.alphanumeric(20),
    voiceConfig: {
      stability: faker.number.float({ min: 0.5, max: 0.9 }),
      similarityBoost: faker.number.float({ min: 0.5, max: 0.9 }),
      speed: faker.number.float({ min: 0.8, max: 1.2 }),
    },
    llmProvider,
    llmModel: llmProvider === "openai" ? "gpt-4" : "claude-3-opus",
    llmConfig: {
      temperature: faker.number.float({ min: 0.3, max: 0.9 }),
      maxTokens: faker.number.int({ min: 512, max: 2048 }),
      systemPrompt: faker.lorem.paragraph(),
    },
    greetingMessage: faker.helpers.arrayElement([
      "Hello! Thank you for calling. How can I help you today?",
      "Welcome! I'm your virtual assistant. How may I assist you?",
      "Hi there! Thanks for reaching out. What can I do for you?",
    ]),
    maxCallDuration: faker.number.int({ min: 300, max: 3600 }),
    temperature: faker.number.float({ min: 0.3, max: 0.9 }),
    status: faker.helpers.arrayElement([
      "active",
      "active",
      "active",
      "paused",
      "draft",
    ] as const),
  };
}

export function createContact(organizationId: string, index: number = 1) {
  const firstName = faker.person.firstName();
  const lastName = faker.person.lastName();

  return {
    organizationId,
    firstName,
    lastName,
    email: faker.internet.email({ firstName, lastName }),
    phone: faker.phone.number({ style: "international" }),
    tags: faker.helpers.arrayElements(
      ["vip", "enterprise", "support", "sales", "returning", "new"],
      faker.number.int({ min: 1, max: 3 }),
    ),
    customFields: {
      company: faker.company.name(),
      position: faker.person.jobTitle(),
      notes: faker.lorem.sentence(),
    },
  };
}

export function createCallRecord(
  organizationId: string,
  agentId: string,
  contactId: string,
  status: string,
) {
  const isCompleted = status === "completed";
  const startTime = faker.date.recent({ days: 30 });
  const duration = isCompleted
    ? faker.number.int({ min: 30, max: 1800 })
    : null;
  const endTime = duration ? new Date(startTime.getTime() + duration * 1000) : null;

  return {
    organizationId,
    agentId,
    contactId,
    status,
    direction: faker.helpers.arrayElement(["inbound", "outbound"] as const),
    fromNumber: faker.phone.number({ style: "international" }),
    toNumber: faker.phone.number({ style: "international" }),
    duration,
    recordingUrl: isCompleted ? `recordings/${faker.string.uuid()}.wav` : null,
    transcriptUrl: isCompleted ? `transcripts/${faker.string.uuid()}.json` : null,
    cost: isCompleted ? faker.number.float({ min: 0.01, max: 5.0 }) : null,
    startedAt: startTime,
    endedAt: endTime,
  };
}
```

## Main Seed Script

```typescript
// packages/db/prisma/seed.ts
import { PrismaClient } from "@prisma/client";
import {
  createOrganization,
  createAgent,
  createContact,
  createCallRecord,
} from "./factories";

const prisma = new PrismaClient();

async function main() {
  console.log("🌱 Seeding database...");
  const startTime = Date.now();

  // Clean existing data in dependency order
  console.log("  Cleaning existing data...");
  await prisma.call.deleteMany();
  await prisma.campaign.deleteMany();
  await prisma.agent.deleteMany();
  await prisma.contact.deleteMany();
  await prisma.user.deleteMany();
  await prisma.organization.deleteMany();

  // Create demo organization
  console.log("  Creating organization...");
  const org = await prisma.organization.create({
    data: createOrganization(1),
  });

  // Create users
  console.log("  Creating users...");
  await prisma.user.createMany({
    data: [
      {
        organizationId: org.id,
        email: "admin@demo.voiceagent.dev",
        name: "Alice Admin",
        role: "admin",
      },
      {
        organizationId: org.id,
        email: "member@demo.voiceagent.dev",
        name: "Bob Member",
        role: "member",
      },
    ],
  });

  // Create agents
  console.log("  Creating agents...");
  const agentData = [createAgent(org.id, 1), createAgent(org.id, 2), createAgent(org.id, 3)];

  const agents = await Promise.all(
    agentData.map((data) => prisma.agent.create({ data })),
  );

  // Create contacts
  console.log("  Creating contacts...");
  const contactData = Array.from({ length: 5 }, (_, i) =>
    createContact(org.id, i + 1),
  );

  const contacts = await Promise.all(
    contactData.map((data) => prisma.contact.create({ data })),
  );

  // Create call records
  console.log("  Creating call records...");
  const statuses = [
    "completed",
    "completed",
    "completed",
    "completed",
    "completed",
    "failed",
    "failed",
    "failed",
    "in_progress",
    "in_progress",
    "completed",
    "completed",
    "completed",
    "completed",
    "completed",
    "completed",
    "completed",
    "completed",
    "completed",
    "completed",
  ];

  const callRecords = statuses.map((status, i) =>
    createCallRecord(
      org.id,
      faker.helpers.arrayElement(agents).id,
      faker.helpers.arrayElement(contacts).id,
      status,
    ),
  );

  await prisma.call.createMany({ data: callRecords });

  // Create campaigns
  console.log("  Creating campaigns...");
  await prisma.campaign.create({
    data: {
      organizationId: org.id,
      agentId: agents[0].id,
      name: "Q2 Customer Outreach",
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
      callWindow: {
        maxAttempts: 3,
        retryDelayMinutes: 60,
      },
      maxAttempts: 3,
    },
  });

  await prisma.campaign.create({
    data: {
      organizationId: org.id,
      agentId: agents[1].id,
      name: "Product Feedback Survey",
      status: "completed",
      schedule: {
        startDate: "2024-01-01",
        endDate: "2024-03-31",
        timezone: "America/New_York",
        windows: [
          { dayOfWeek: 1, startTime: "09:00", endTime: "17:00" },
          { dayOfWeek: 2, startTime: "09:00", endTime: "17:00" },
          { dayOfWeek: 3, startTime: "09:00", endTime: "17:00" },
          { dayOfWeek: 4, startTime: "09:00", endTime: "17:00" },
          { dayOfWeek: 5, startTime: "09:00", endTime: "17:00" },
        ],
      },
      maxAttempts: 2,
    },
  });

  const duration = Date.now() - startTime;
  console.log("");
  console.log("✅ Seed data created successfully!");
  console.log(`   Organization: ${org.name}`);
  console.log(`   Users: 2`);
  console.log(`   Agents: ${agents.length}`);
  console.log(`   Contacts: ${contacts.length}`);
  console.log(`   Calls: ${callRecords.length}`);
  console.log(`   Campaigns: 2`);
  console.log(`   Duration: ${duration}ms`);
  console.log("");
  console.log("📋 Demo login: admin@demo.voiceagent.dev");
}

main()
  .catch((e) => {
    console.error("❌ Seed failed:", e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
```

## Running Seed

```bash
# Run seed
pnpm --filter @voice-agent/db run db:seed

# Reset and re-seed
pnpm --filter @voice-agent/db run db:reset

# Seed specific data (using environment variable)
SEED_SIZE=large pnpm --filter @voice-agent/db run db:seed
```

## Design Decisions

### Factory functions vs. static seed data

**Decision**: Use factory functions with faker.js.

**Rationale**: Factory functions generate realistic, varied data that exercises different code paths. Static seed data is predictable and might not surface edge cases. Faker.js produces data that looks like real production data (names, phones, emails) without using real personal information.

### Why faker.js and not manual data?

Manual seed data is brittle — it doesn't change when the schema evolves. Factory functions adapt to schema changes with TypeScript's type checking. Re-running seed produces different data each time, which is closer to production conditions.

### Seed size

The default seed creates a small dataset (~30 records) suitable for development. For performance testing, a `SEED_SIZE=large` flag can generate thousands of records.

## Integration Points

- **Prisma migrate reset**: Calls seed automatically after reset
- **Local development**: Post-create command in DevContainers
- **CI**: Seed runs before integration tests
- **Demo environments**: Seed creates demo data for staging/preview

## Production Considerations

1. **Never seed production**: The seed script includes development-only data. Add a safety check: `if (process.env.NODE_ENV === 'production') { console.error('Cannot seed production'); process.exit(1); }`
2. **Idempotency**: Seed should be idempotent — running it twice produces the same result (or detects existing data and skips)
3. **Performance**: Large seeds can be slow. Use `createMany` for bulk inserts and batch transactions
4. **Data cleanup**: The seed script should clean existing data before inserting. In development, this is acceptable. Never run seed on a database with customer data
5. **Realistic data**: Use faker.js locale support for internationalization. Demo data should reflect the expected production data profile
