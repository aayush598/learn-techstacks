# Section 04: Shared TypeScript Package

## Overview

The shared TypeScript package (`@voice-agent/types`) serves as the single source of truth for type definitions, API contracts, Zod schemas, and shared constants used across the platform. By centralizing these definitions, we prevent type drift between the frontend and backend, ensure API contract compliance, and reduce duplication.

## Package Structure

```text
packages/types/src/
├── api/
│   ├── contracts.ts        # API request/response shapes
│   ├── errors.ts           # Error response format
│   └── pagination.ts       # Pagination types
├── domain/
│   ├── agent.ts            # Agent entity types
│   ├── call.ts             # Call record types
│   ├── campaign.ts         # Campaign types
│   ├── contact.ts          # Contact/lead types
│   ├── organization.ts     # Tenant organization types
│   ├── transcript.ts       # Transcription types
│   └── user.ts             # User types
├── events/
│   ├── call-events.ts      # Call lifecycle events
│   └── system-events.ts    # System event types
├── schemas/
│   ├── agent-schema.ts     # Zod schemas for agent
│   ├── call-schema.ts      # Zod schemas for call
│   └── shared-schema.ts    # Common Zod utilities
├── constants/
│   ├── call-states.ts      # Call state enum + transitions
│   ├── roles.ts            # User roles and permissions
│   └── limits.ts           # Platform limits and quotas
├── utils/
│   ├── branded.ts          # Branded type utilities
│   └── guards.ts           # Type guard functions
└── index.ts                # Barrel exports
```

## Package Configuration

```jsonc
{
  "name": "@voice-agent/types",
  "version": "0.0.1",
  "private": true,
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": "./dist/index.js",
    "./api": "./dist/api/index.js",
    "./domain": "./dist/domain/index.js",
    "./schemas": "./dist/schemas/index.js",
    "./constants": "./dist/constants/index.js"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsc --watch",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "zod": "^3.22.0"
  },
  "devDependencies": {
    "@voice-agent/config-typescript": "workspace:*",
    "typescript": "^5.4.0"
  }
}
```

The package provides multiple entry points via the `exports` field, allowing consumers to import only what they need:

```typescript
// Import only API contracts
import type { CreateAgentRequest, AgentResponse } from "@voice-agent/types/api";

// Import domain types
import type { Agent, Call, Campaign } from "@voice-agent/types/domain";

// Import Zod schemas for runtime validation
import { agentSchema, callSchema } from "@voice-agent/types/schemas";

// Import constants
import { CALL_STATES, USER_ROLES } from "@voice-agent/types/constants";
```

## API Contract Definitions

```typescript
// packages/types/src/api/contracts.ts
import { z } from "zod";
import type { PaginatedResponse } from "./pagination";

// ── Request Schemas ──────────────────────────────────────────

export const CreateAgentSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(1000).optional(),
  voiceProvider: z.enum(["elevenlabs", "cartesia", "deepgram"]),
  voiceId: z.string(),
  greetingMessage: z.string().max(500),
  maxCallDuration: z.number().int().positive().max(14400),
  temperature: z.number().min(0).max(1).default(0.7),
  llmProvider: z.enum(["openai", "anthropic"]),
  llmModel: z.string(),
  knowledgeBaseIds: z.array(z.string().ulid()).optional(),
});

export const UpdateAgentSchema = CreateAgentSchema.partial();

// ── Response Types ───────────────────────────────────────────

export interface AgentResponse {
  id: string;
  name: string;
  description: string | null;
  voiceProvider: "elevenlabs" | "cartesia" | "deepgram";
  voiceId: string;
  greetingMessage: string;
  maxCallDuration: number;
  temperature: number;
  llmProvider: "openai" | "anthropic";
  llmModel: string;
  status: "draft" | "active" | "paused" | "archived";
  createdAt: string;
  updatedAt: string;
}

export type AgentListResponse = PaginatedResponse<AgentResponse>;

// ── Type Inference from Zod ─────────────────────────────────

export type CreateAgentRequest = z.infer<typeof CreateAgentSchema>;
export type UpdateAgentRequest = z.infer<typeof UpdateAgentSchema>;
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

export interface VoiceConfiguration {
  provider: "elevenlabs" | "cartesia" | "deepgram";
  voiceId: string;
  speed: number;
  stability: number;
  similarityBoost: number;
}

export interface LLMConfiguration {
  provider: "openai" | "anthropic";
  model: string;
  temperature: number;
  maxTokens: number;
  systemPrompt: string;
}
```

## Shared Constants

```typescript
// packages/types/src/constants/call-states.ts

export const CALL_STATES = {
  INITIATING: "initiating",
  RINGING: "ringing",
  IN_PROGRESS: "in_progress",
  TRANSFERRING: "transferring",
  COMPLETED: "completed",
  FAILED: "failed",
  BUSY: "busy",
  NO_ANSWER: "no_answer",
} as const;

export type CallState = (typeof CALL_STATES)[keyof typeof CALL_STATES];

// Valid state transitions
export const CALL_STATE_TRANSITIONS: Record<CallState, CallState[]> = {
  initiating: ["ringing", "failed"],
  ringing: ["in_progress", "busy", "no_answer", "failed"],
  in_progress: ["completed", "transferred", "failed"],
  transferring: ["in_progress", "completed", "failed"],
  completed: [],
  failed: [],
  busy: [],
  no_answer: [],
} as const;

export function isValidTransition(
  from: CallState,
  to: CallState
): boolean {
  return CALL_STATE_TRANSITIONS[from]?.includes(to) ?? false;
}
```

## Zod Schemas for Runtime Validation

```typescript
// packages/types/src/schemas/agent-schema.ts
import { z } from "zod";

export const agentSchema = z.object({
  id: z.string().ulid(),
  organizationId: z.string().ulid(),
  name: z.string().min(1).max(100),
  description: z.string().max(1000).nullable(),
  voiceConfig: z.object({
    provider: z.enum(["elevenlabs", "cartesia", "deepgram"]),
    voiceId: z.string(),
    speed: z.number().min(0.5).max(2.0),
    stability: z.number().min(0).max(1),
    similarityBoost: z.number().min(0).max(1),
  }),
  llmConfig: z.object({
    provider: z.enum(["openai", "anthropic"]),
    model: z.string(),
    temperature: z.number().min(0).max(1),
    maxTokens: z.number().int().positive().max(128000),
    systemPrompt: z.string().max(4000),
  }),
  status: z.enum(["draft", "active", "paused", "archived"]),
  createdAt: z.date(),
  updatedAt: z.date(),
});

export type AgentRecord = z.infer<typeof agentSchema>;
```

## Zod + OpenAPI Integration

```typescript
// packages/types/src/schemas/shared-schema.ts
import { z } from "zod";

// Extend Zod to generate OpenAPI metadata
export const ApiResponseSchema = <T extends z.ZodTypeAny>(data: T) =>
  z.object({
    success: z.boolean(),
    data: data.optional(),
    error: z
      .object({
        code: z.string(),
        message: z.string(),
        details: z.unknown().optional(),
      })
      .optional(),
    meta: z
      .object({
        requestId: z.string().ulid(),
        timestamp: z.string().datetime(),
      })
      .optional(),
  });

export type ApiResponse<T> = z.infer<ReturnType<typeof ApiResponseSchema<T>>>;
```

## Barrel Export Strategy

```typescript
// packages/types/src/index.ts
export * from "./domain";
export * from "./constants";
```

Using barrel exports provides clean import paths but must be balanced against tree-shaking concerns. For a types-only package, barrel exports are safe because TypeScript types are erased at compile time.

## Design Decisions

### Why a separate types package instead of inlining types?

1. **Type drift prevention**: Without a shared package, the frontend and backend inevitably diverge in their understanding of data shapes
2. **Package size**: Zod schemas and types add minimal bundle weight but provide maximum value when shared
3. **Versioning**: The types package can be versioned independently, allowing gradual API migration

### Trade-offs

1. **Build overhead**: The types package must be built before any dependent package, adding ~2 seconds to initial build
2. **Import complexity**: Developers must know which entry point to import from — mitigated by clear barrel exports
3. **Zod in the browser**: Zod schemas can be bundled to the frontend for form validation, adding ~30KB gzipped

## Integration Points

- **Prisma**: Domain types mirror the Prisma schema but provide frontend-safe shapes (dates as strings, no relational includes)
- **tRPC or Next.js API routes**: API contracts define the request/response shapes for all endpoints
- **React Query**: Query mutation types are derived from API contracts
- **Form validation**: Zod schemas are used both server-side (API validation) and client-side (form validation via react-hook-form)

## Production Considerations

1. **Breaking changes**: Always version the types package. Use `@voice-agent/types@1.0.0` vs `@voice-agent/types@2.0.0` for major API changes
2. **Deprecation strategy**: Mark deprecated fields with JSDoc `@deprecated` and maintain backward compatibility for at least one release cycle
3. **Circular dependencies**: Never import from apps or other packages into the types package — it must remain a leaf in the dependency graph
4. **Bundle analysis**: Periodically run `attw` (Are The Types Wrong) to verify package type correctness for all consumers
