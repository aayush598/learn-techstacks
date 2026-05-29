# Section 03: Shared Type Definitions

## Overview

Shared type definitions provide a contract-driven approach to building the voice agent platform. By centralizing domain types, API contracts, and database types in the `@voice-agent/types` package, we ensure that every layer of the application shares the same understanding of data shapes.

## Type Definition Architecture

```text
@voice-agent/types
│
├── Domain Types (entities, value objects)
│   ├── Agent, Organization, Call, Campaign, Contact, User
│   └── Value Objects: PhoneNumber, EmailAddress, Duration, Money
│
├── API Contracts (request/response)
│   ├── CreateAgentRequest, AgentResponse, CallListResponse
│   └── ApiError, PaginationParams, PaginatedResponse<T>
│
├── Database Types (Prisma-generated)
│   ├── Prisma.AgentGetPayload, Prisma.CallSelect
│   └── Input types: Prisma.AgentCreateInput
│
├── Event Types (message bus)
│   ├── CallStartedEvent, CallEndedEvent, AgentDeployedEvent
│   └── Event envelope: { id, type, timestamp, data, metadata }
│
└── Configuration Types
    ├── VoiceConfig, LLMConfig, CampaignConfig
    └── AppConfig (env-derived)
```

## Domain Types

```typescript
// packages/types/src/domain/agent.ts
export interface Agent {
  id: AgentId;
  organizationId: OrganizationId;
  name: string;
  description: string | null;
  voiceConfig: VoiceConfiguration;
  llmConfig: LLMConfiguration;
  greetingMessage: string;
  maxCallDuration: number;
  status: AgentStatus;
  createdAt: Date;
  updatedAt: Date;
}

export type AgentStatus = "draft" | "active" | "paused" | "archived";

export type AgentSummary = Pick<
  Agent,
  "id" | "name" | "status" | "createdAt"
>;

// packages/types/src/domain/call.ts
export interface Call {
  id: CallId;
  organizationId: OrganizationId;
  agentId: AgentId;
  contactId: ContactId | null;
  campaignId: CampaignId | null;
  status: CallStatus;
  direction: CallDirection;
  fromNumber: string;
  toNumber: string;
  duration: number | null;
  recordingUrl: string | null;
  transcriptUrl: string | null;
  cost: number | null;
  startedAt: Date | null;
  endedAt: Date | null;
  createdAt: Date;
  updatedAt: Date;
}

export type CallStatus =
  | "initiating"
  | "ringing"
  | "in_progress"
  | "transferring"
  | "completed"
  | "failed"
  | "busy"
  | "no_answer";

export type CallDirection = "inbound" | "outbound";

// ── State machine definition ────────────────────────────────
export const CALL_TRANSITIONS: Record<CallStatus, CallStatus[]> = {
  initiating: ["ringing", "failed"],
  ringing: ["in_progress", "busy", "no_answer", "failed"],
  in_progress: ["completed", "transferring", "failed"],
  transferring: ["in_progress", "completed", "failed"],
  completed: [],
  failed: [],
  busy: [],
  no_answer: [],
} as const;

export function canTransition(from: CallStatus, to: CallStatus): boolean {
  return CALL_TRANSITIONS[from].includes(to);
}
```

## API Contract Types

```typescript
// packages/types/src/api/pagination.ts
export interface PaginationParams {
  page?: number;
  pageSize?: number;
  cursor?: string;
  orderBy?: "asc" | "desc";
}

export interface PaginatedResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    pageSize: number;
    totalPages: number;
    hasNext: boolean;
    hasPrevious: boolean;
  };
}

export interface CursorPaginatedResponse<T> {
  data: T[];
  meta: {
    nextCursor: string | null;
    hasMore: boolean;
  };
}

// packages/types/src/api/errors.ts
export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string[]>;
  requestId: string;
}

export class AppError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly statusCode: number = 500,
    public readonly details?: Record<string, string[]>,
  ) {
    super(message);
    this.name = "AppError";
  }
}

// packages/types/src/api/contracts.ts
export interface CreateAgentRequest {
  name: string;
  description?: string;
  voiceProvider: "elevenlabs" | "cartesia" | "deepgram";
  voiceId: string;
  greetingMessage: string;
  maxCallDuration: number;
  temperature: number;
  llmProvider: "openai" | "anthropic";
  llmModel: string;
}

export interface AgentResponse {
  id: string;
  name: string;
  status: AgentStatus;
  createdAt: string;
  updatedAt: string;
}
```

## Database Types (Prisma Integration)

```typescript
// packages/types/src/db.ts
// Re-export Prisma-generated types with domain-specific wrappers

import type { Agent, Call, Campaign, Contact, Organization } from "@prisma/client";

// Prisma-generated types are used directly
export type { Agent, Call, Campaign, Contact, Organization };

// Extended types with relations
export type AgentWithRelations = Agent & {
  organization: Pick<Organization, "id" | "name" | "plan">;
  _count: {
    calls: number;
    campaigns: number;
  };
};

// Create input types (for repository layer)
export type CreateAgentInput = Pick<
  Agent,
  | "name"
  | "voiceProvider"
  | "voiceId"
  | "greetingMessage"
  | "maxCallDuration"
  | "temperature"
  | "llmProvider"
  | "llmModel"
> & { description?: string };
```

## Event Types

```typescript
// packages/types/src/events/call-events.ts
export interface CallEventEnvelope {
  id: string;
  type: CallEventType;
  timestamp: string;
  source: string;
  data: Record<string, unknown>;
  metadata: {
    organizationId: string;
    correlationId: string;
    causationId?: string;
  };
}

export type CallEventType =
  | "call.initiated"
  | "call.ringing"
  | "call.connected"
  | "call.transferred"
  | "call.completed"
  | "call.failed"
  | "call.recording.ready"
  | "call.transcript.ready";

export interface CallInitiatedEvent {
  callId: string;
  agentId: string;
  contactPhone: string;
  direction: CallDirection;
  campaignId?: string;
}
```

## Configuration Types

```typescript
// packages/types/src/domain/configuration.ts
export interface VoiceConfiguration {
  provider: "elevenlabs" | "cartesia" | "deepgram";
  voiceId: string;
  speed: number;
  stability: number;
  similarityBoost: number;
  optimizeLatency: number;
}

export interface LLMConfiguration {
  provider: "openai" | "anthropic";
  model: string;
  temperature: number;
  maxTokens: number;
  topP: number;
  frequencyPenalty: number;
  presencePenalty: number;
  systemPrompt: string;
}
```

## Type Organization Principles

### 1. Domain Types are Entity-Centric

Each domain type corresponds to a business entity. They should be the single representation of that concept across all layers:

```typescript
// ✅ One Agent type used everywhere
import type { Agent } from "@voice-agent/types/domain";

// ❌ No per-layer Agent types
// - types/api/agent.ts
// - types/db/agent.ts
// - types/domain/agent.ts
```

### 2. API Contracts are Transformations

API types differ from domain types in serialization concerns (dates as strings, omitted fields, renamed properties):

```typescript
// Domain type (internal)
interface Agent {
  createdAt: Date;
  updatedAt: Date;
}

// API type (serialized)
interface AgentResponse {
  createdAt: string; // ISO 8601
  updatedAt: string;
}
```

### 3. Database Types are Prisma-Generated

Never manually write types that mirror the database schema. Let Prisma generate them and re-export as needed. This ensures the types are always in sync with migrations.

## Design Decisions

### Why a separate types package instead of per-package types?

A centralized package prevents circular dependencies. If `packages/voice` defined its own types and `packages/ai` needed those types, they'd cross-import. With a shared types package, both import from the same leaf dependency.

### Prisma types vs. manual interfaces

Prisma-generated types are comprehensive but sometimes include fields that shouldn't be exposed (e.g., `passwordHash`). The repository layer should map Prisma types to domain types, stripping internal fields.

## Integration Points

- **API routes**: Use API contract types for request validation and response serialization
- **React components**: Use domain types for props and state
- **Event producers/consumers**: Share event types across microservices
- **Database repositories**: Use Prisma-generated types internally, map to domain types for consumers

## Production Considerations

1. **Breaking changes**: When a domain type changes, all consumers must update. Use versioned exports or create new types with a `V2` suffix to migrate gradually
2. **Type inflation**: It's easy to create too many types. Follow the YAGNI principle — don't create a type until it's consumed in at least two places
3. **Circular imports**: Domain types importing API types or vice versa creates cycles. Keep a strict dependency direction: API → Domain → Prisma
4. **Documentation**: Add JSDoc comments to public types. TypeScript's `--declaration` generates `.d.ts` files that serve as documentation for package consumers
