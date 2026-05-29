# Section 05: Database Access Patterns

## Overview

Database access follows the Repository pattern with Prisma as the ORM layer. Controllers and services never call `prisma.model.findMany()` directly — they interact with typed repository classes that encapsulate query logic, transaction management, and relation loading. This abstraction enables testability, query optimization centralization, and N+1 prevention.

## Repository Pattern Architecture

```text
┌────────────────────────────────────────────────────────────┐
│                  Database Access Layers                      │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  Service Layer (Business Logic)                              │
│       │                                                      │
│       ▼                                                      │
│  Repository Layer (Data Access)                              │
│       │                                                      │
│       ├── VoiceCallRepository                                │
│       │   ├── findById(id)                                   │
│       │   ├── findByParticipant(participantId, opts)         │
│       │   ├── create(data)                                   │
│       │   ├── update(id, data)                               │
│       │   └── endCall(id)                                   │
│       │                                                      │
│       ├── TranscriptRepository                               │
│       │   ├── findByCallId(callId)                           │
│       │   ├── search(query, opts)                            │
│       │   └── createBatch(entries)                           │
│       │                                                      │
│       └── AnalyticsRepository                                │
│           ├── getCallMetrics(callId)                         │
│           ├── getAggregateStats(filters)                     │
│           └── getDailyUsage(days)                            │
│                                                              │
│       ▼                                                      │
│  Prisma Client (Generated ORM)                               │
│       │                                                      │
│       ▼                                                      │
│  PostgreSQL (with pgvector)                                  │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

## Repository Implementation

```typescript
// packages/db/src/repositories/voice-call.repository.ts
import { PrismaClient, Prisma } from '@prisma/client';
import { injectable } from 'tsyringe';

@injectable()
export class VoiceCallRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async findById(id: string, options?: FindOptions) {
    return this.prisma.voiceCall.findUnique({
      where: { id },
      include: this.buildIncludes(options),
    });
  }

  async findByParticipant(
    participantId: string,
    options?: PaginationOptions
  ) {
    return this.prisma.voiceCall.findMany({
      where: {
        participantIds: { has: participantId },
      },
      include: { transcript: true, analytics: true },
      orderBy: { createdAt: 'desc' },
      take: options?.limit ?? 20,
      skip: options?.cursor ? 1 : 0,
      ...(options?.cursor ? { cursor: { id: options.cursor } } : {}),
    });
  }

  async create(data: CreateVoiceCallData) {
    return this.prisma.voiceCall.create({
      data: {
        ...data,
        status: 'idle',
      },
      include: { participants: true },
    });
  }

  async update(id: string, data: UpdateVoiceCallData) {
    return this.prisma.voiceCall.update({
      where: { id },
      data,
    });
  }

  async endCall(id: string) {
    return this.prisma.voiceCall.update({
      where: { id },
      data: {
        status: 'disconnected',
        endedAt: new Date(),
      },
    });
  }

  private buildIncludes(options?: FindOptions) {
    const includes: Prisma.VoiceCallInclude = {};
    if (options?.includeTranscript) includes.transcript = true;
    if (options?.includeAnalytics) includes.analytics = true;
    if (options?.includeParticipants) includes.participants = true;
    return includes;
  }
}
```

**Design decision: Constructor injection over static methods**. Using `tsyringe` or `awilix` for dependency injection allows replacing the Prisma client with a mock in tests without monkey-patching. Static repository classes are simpler but require module-level mocking, which is fragile.

## Transaction Usage

Transactions wrap operations that span multiple repository calls:

```typescript
// packages/db/src/services/call-completion.service.ts
import { PrismaClient } from '@prisma/client';

export class CallCompletionService {
  constructor(
    private readonly prisma: PrismaClient,
    private readonly callRepo: VoiceCallRepository,
    private readonly transcriptRepo: TranscriptRepository,
    private readonly analyticsRepo: AnalyticsRepository
  ) {}

  async completeCall(callId: string, transcriptData: TranscriptData) {
    await this.prisma.$transaction(async (tx) => {
      // Use tx (transaction-scoped client) for all operations
      const txCallRepo = this.callRepo.withClient(tx);
      const txTranscriptRepo = this.transcriptRepo.withClient(tx);
      const txAnalyticsRepo = this.analyticsRepo.withClient(tx);

      await txCallRepo.endCall(callId);
      await txTranscriptRepo.create(callId, transcriptData);
      await txAnalyticsRepo.computeCallMetrics(callId);
    });
  }
}
```

The `$transaction` API provides automatic rollback if any operation fails. For long-running transactions, use the interactive API (shown above) with a timeout:

```typescript
await this.prisma.$transaction(
  async (tx) => { /* operations */ },
  { timeout: 10_000, maxWait: 5_000 }
);
```

## N+1 Prevention

The N+1 query problem is the most common performance issue in ORM-based applications. We enforce prevention through several mechanisms:

```typescript
// BAD — N+1 query (one query for the list, N queries for transcripts)
async function getCallsWithTranscripts(limit: number) {
  const calls = await this.prisma.voiceCall.findMany({ take: limit });
  for (const call of calls) {
    call.transcript = await this.prisma.transcript.findUnique({
      where: { callId: call.id },
    });
  }
  return calls;
}

// GOOD — Single query with eager loading
async function getCallsWithTranscripts(limit: number) {
  return this.prisma.voiceCall.findMany({
    take: limit,
    include: { transcript: true },
  });
}
```

Repository methods accept an `include` parameter to control relation loading:

```typescript
// Consumer decides what to load
const call = await callRepo.findById('call_123', {
  includeTranscript: true,
  includeAnalytics: true,
});
```

**Batch loading utility** for cases where eager loading isn't available:

```typescript
async function getCallsWithTranscripts(callIds: string[]) {
  const calls = await this.prisma.voiceCall.findMany({
    where: { id: { in: callIds } },
  });
  const transcripts = await this.prisma.transcript.findMany({
    where: { callId: { in: callIds } },
  });
  const transcriptMap = new Map(transcripts.map(t => [t.callId, t]));
  return calls.map(call => ({
    ...call,
    transcript: transcriptMap.get(call.id),
  }));
}
```

## Query Optimization

Prisma's `findMany` with large datasets requires explicit optimization strategies:

```typescript
// Pagination with cursor (efficient for large datasets)
const page = await this.prisma.voiceCall.findMany({
  take: 20,
  orderBy: { createdAt: 'desc' },
  where: { organizationId },
  ...(cursor ? { cursor: { id: cursor }, skip: 1 } : {}),
});

// Selective field loading (reduces data transfer)
const calls = await this.prisma.voiceCall.findMany({
  where: { status: 'connected' },
  select: {
    id: true,
    status: true,
    participantCount: true,
    createdAt: true,
  },
  take: 100,
});
```

**Index strategy**: Every `where`, `orderBy`, and `cursor` field must be indexed. Prisma's `db push` or migrations enforce these:

```prisma
model VoiceCall {
  id             String   @id @default(cuid())
  organizationId String
  status         CallStatus
  createdAt      DateTime @default(now())

  @@index([organizationId, status])
  @@index([organizationId, createdAt])
  @@index([status, createdAt])
}
```

## Seed Data Strategy

Seed data is critical for local development and CI test databases:

```typescript
// packages/db/prisma/seed.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function seed() {
  const org = await prisma.organization.create({
    data: {
      name: 'Acme Corp',
      slug: 'acme-corp',
    },
  });

  const calls = Array.from({ length: 50 }, (_, i) => ({
    organizationId: org.id,
    status: i < 40 ? 'disconnected' : 'connected',
    participantIds: [`user_${i % 10}`, `user_${(i + 1) % 10}`],
    createdAt: new Date(Date.now() - i * 3600000),
  }));

  await prisma.voiceCall.createMany({ data: calls });
  console.log(`Seeded ${calls.length} voice calls`);
}

seed()
  .catch((e) => { console.error(e); process.exit(1); })
  .finally(() => prisma.$disconnect());
```

## Integration Points

- **Prisma Client**: Generated from schema, provides type-safe queries
- **pgvector**: Vector similarity queries for voice fingerprinting and transcription search
- **Connection pooling**: `pgbouncer` or Prisma's built-in pooler for serverless deployments
- **Migration CI**: `prisma migrate deploy` runs as a pre-deployment step, not during app startup

## Production Considerations

1. **Connection pooling**: Prisma has a built-in connection pool. For serverless deployments, use Prisma Accelerate or a PgBouncer sidecar.
2. **Query logging**: Enable `log: ['query', 'info', 'warn', 'error']` in development. In production, log only slow queries (>100ms) to avoid log volume.
3. **Soft deletes**: Prefer a `deletedAt: DateTime?` column over hard deletes. Add `where: { deletedAt: null }` as a global middleware or default filter.
4. **Batch operations**: Use `createMany` and `updateMany` for bulk operations. Individual `create` in a loop is 100x slower.
5. **Read replicas**: Configure the Prisma client with a separate replica URL for read queries: `datasource.db.url(reads from replica)`. This is configured at the Prisma client level.
6. **Middleware hooks**: Use Prisma middleware for cross-cutting concerns like soft-delete filters, audit logging, and cache invalidation.
