# Section 02: Backend Stack

## Technology Overview

The backend stack uses **Next.js API routes** for REST endpoints, **tRPC** for type-safe client-server communication, **Prisma ORM** for database access, **BullMQ** for job queues, and **Zod** for validation at every boundary.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND TECHNOLOGY STACK                         │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Runtime: Node.js 20 LTS (or Bun 1.x)                      │   │
│  │  Language: TypeScript 5 (strict mode)                      │   │
│  │                                                              │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │  Next.js API │ │   tRPC 10.x  │ │   Prisma ORM     │    │   │
│  │  │  Routes      │ │  (Type-safe  │ │   5.x            │    │   │
│  │  │  (REST)      │ │   RPC)       │ │  (PostgreSQL +   │    │   │
│  │  │              │ │              │ │   MongoDB)       │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │   BullMQ      │ │   Zod 3.x    │ │   Pino Logger    │    │   │
│  │  │  (Job Queue)  │ │  (Validation │ │  (Structured     │    │   │
│  │  │  + Redis)     │ │   at every   │ │   Logging)       │    │   │
│  │  │              │ │   boundary)  │ │                  │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │   Auth.js     │ │   OpenTele-  │ │   Sentry         │    │   │
│  │  │  (NextAuth v5)│ │   metry      │ │  (Error Tracking)│    │   │
│  │  │  (Auth)       │ │  (Tracing)   │ │                  │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Service Layer Architecture:                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Route Handler (Next.js API / tRPC)                        │   │
│  │         │                                                    │   │
│  │  ┌──────┴──────┐                                           │   │
│  │  │  Middleware   │  Auth, Validation, Rate Limit, Logging   │   │
│  │  └──────┬──────┘                                           │   │
│  │         │                                                    │   │
│  │  ┌──────┴──────┐                                           │   │
│  │  │  Service     │  Business logic, orchestration            │   │
│  │  │  Layer       │                                           │   │
│  │  └──────┬──────┘                                           │   │
│  │         │                                                    │   │
│  │  ┌──────┴──────┐                                           │   │
│  │  │  Repository  │  Prisma ORM, external API clients         │   │
│  │  │  Layer       │                                           │   │
│  │  └─────────────┘                                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Service Layer Pattern

```typescript
// Service layer with dependency injection
interface AgentService {
  listAgents(tenantId: string, params: PaginationParams): Promise<PaginatedResult<Agent>>;
  getAgent(id: string, tenantId: string): Promise<Agent>;
  createAgent(data: CreateAgentInput, tenantId: string, userId: string): Promise<Agent>;
  updateAgent(id: string, data: UpdateAgentInput, tenantId: string): Promise<Agent>;
  deleteAgent(id: string, tenantId: string): Promise<void>;
}

// Implementation using Prisma
class AgentServiceImpl implements AgentService {
  constructor(private db: PrismaClient, private queue: Queue) {}

  async listAgents(tenantId: string, params: PaginationParams): Promise<PaginatedResult<Agent>> {
    const [items, total] = await Promise.all([
      this.db.agent.findMany({
        where: { tenantId },
        skip: (params.page - 1) * params.pageSize,
        take: params.pageSize,
        orderBy: { createdAt: 'desc' },
      }),
      this.db.agent.count({ where: { tenantId } }),
    ]);

    return { items, total, page: params.page, pageSize: params.pageSize };
  }

  async createAgent(data: CreateAgentInput, tenantId: string, userId: string): Promise<Agent> {
    const agent = await this.db.agent.create({
      data: { ...data, tenantId, createdBy: userId },
    });

    // Publish event to Kafka
    await this.queue.publish('agent:created', agent);

    return agent;
  }
}
```

## BullMQ Job Queue

```typescript
// Queue definitions
import { Queue, Worker, QueueEvents } from 'bullmq';

const connection = { host: process.env.REDIS_HOST, port: 6379 };

// Voice processing queue
const voiceQueue = new Queue('voice-processing', { connection });

// Job types
interface VoiceJob {
  type: 'transcribe' | 'synthesize' | 'analyze_sentiment' | 'generate_summary';
  callId: string;
  audioUrl: string;
  options?: Record<string, unknown>;
}

// Worker
const voiceWorker = new Worker<VoiceJob>(
  'voice-processing',
  async (job) => {
    switch (job.data.type) {
      case 'transcribe':
        return await transcriptionService.transcribe(job.data.audioUrl);
      case 'synthesize':
        return await ttsService.synthesize(job.data.audioUrl);
    }
  },
  { connection, concurrency: 5 }
);

// Job scheduling with delays and retries
async function scheduleVoiceProcessing(callId: string, audioUrl: string) {
  await voiceQueue.add('transcribe-job', {
    type: 'transcribe',
    callId,
    audioUrl,
  }, {
    attempts: 3,
    backoff: { type: 'exponential', delay: 2000 },
    removeOnComplete: { age: 3600 * 24 },
  });
}
```

## Prisma Schema Example

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Agent {
  id             String   @id @default(cuid())
  tenantId       String
  name           String
  voiceSettings  Json     @default("{}")
  promptTemplate String
  temperature    Float    @default(0.7)
  isActive       Boolean  @default(true)
  createdAt      DateTime @default(now())
  updatedAt      DateTime @updatedAt

  tenant   Tenant  @relation(fields: [tenantId], references: [id])
  calls    Call[]

  @@index([tenantId])
  @@index([isActive])
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| API framework | Next.js API Routes + tRPC | REST for external, tRPC for internal type safety |
| ORM | Prisma | Type-safe queries, migrations, excellent DX |
| Job queue | BullMQ + Redis | Persistent, delayed jobs, rate limiting, scheduling |
| Validation | Zod at every boundary | API input, service input, database writes |
| Logging | Pino | Fast structured JSON logging, OpenTelemetry integration |
| Error tracking | Sentry | Source maps, breadcrumbs, performance monitoring |

## Integration Points

- **Ch 02 (Next.js Architecture)** — API routes follow structure defined in architecture
- **Ch 03 (Database)** — Prisma ORM maps to PostgreSQL schemas
- **Ch 05 (Microservices)** — BullMQ queues bridge service boundaries
- **Ch 08 (Frontend Stack)** — tRPC client consumed by frontend

## Production Considerations

- **Graceful Shutdown**: BullMQ workers handle SIGTERM — finish current job, stop accepting new ones
- **Connection Pooling**: Prisma uses PgBouncer-compatible mode with connection pooling
- **Job Monitoring**: BullMQ Dashboard for queue management and job retries
- **Rate Limiting per Worker**: Max 5 concurrent voice processing jobs per node
- **Memory**: Each voice job uses ~200MB RAM for audio processing; workers scale horizontally
