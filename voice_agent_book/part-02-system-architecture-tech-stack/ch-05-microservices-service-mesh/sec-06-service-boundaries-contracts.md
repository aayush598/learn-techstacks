# Section 06: Service Boundaries & Contracts

## Service Ownership Map

Clear service boundaries prevent "distributed monolith" anti-patterns. Each service owns its domain data, has a well-defined API contract, and is independently deployable.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SERVICE BOUNDARIES & CONTRACTS                      │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  SERVICE         │ OWNS           │  API          │ DATA       │    │
│  │──────────────────┼────────────────┼───────────────┼────────────┤    │
│  │ Agent Service    │ Agent CRUD,    │ REST (3001)   │ PostgreSQL │    │
│  │                  │ Versions,      │ gRPC (50051)  │            │    │
│  │                  │ Prompts, Voices│               │            │    │
│  │──────────────────┼────────────────┼───────────────┼────────────┤    │
│  │ Call Service     │ Call lifecycle,│ REST (3002)   │ PostgreSQL │    │
│  │                  │ State machine, │ Kafka events  │ (partition)│    │
│  │                  │ Recording      │               │            │    │
│  │──────────────────┼────────────────┼───────────────┼────────────┤    │
│  │ Voice Service    │ STT, TTS, VAD,│ gRPC (50052)  │ Ephemeral  │    │
│  │                  │ Audio pipeline │ WebSocket     │ (in-memory)│    │
│  │──────────────────┼────────────────┼───────────────┼────────────┤    │
│  │ AI Service       │ LLM orchest.,  │ REST (3003)   │ PostgreSQL │    │
│  │                  │ RAG, Memory,   │ gRPC (50053)  │ + pgvector │    │
│  │                  │ Tool execution │               │            │    │
│  │──────────────────┼────────────────┼───────────────┼────────────┤    │
│  │ Campaign Service │ Campaigns,     │ REST (3004)   │ PostgreSQL │    │
│  │                  │ Contacts, DNC, │ BullMQ jobs   │            │    │
│  │                  │ Call attempts  │               │            │    │
│  │──────────────────┼────────────────┼───────────────┼────────────┤    │
│  │ Billing Service  │ Subscriptions, │ REST (3005)   │ PostgreSQL │    │
│  │                  │ Usage, Invoices│ Kafka events  │ + Redis    │    │
│  │                  │ Payments       │               │            │    │
│  │──────────────────┼────────────────┼───────────────┼────────────┤    │
│  │ Auth Service     │ Users, Roles,  │ REST (3006)   │ PostgreSQL │    │
│  │                  │ Sessions, MFA, │               │            │    │
│  │                  │ API Keys       │               │            │    │
│  │──────────────────┼────────────────┼───────────────┼────────────┤    │
│  │ Notification     │ Emails,        │ BullMQ jobs   │ PostgreSQL │    │
│  │ Service          │ Webhooks, SMS  │ Kafka events  │ + Redis    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## API Contract Definitions

```typescript
// Agent Service — OpenAPI 3.1 contract
// File: services/agent-service/api/openapi.yaml
// (TypeScript interfaces as source of truth)

export interface AgentServiceContract {
  // ── Agents ──
  createAgent(input: {
    name: string
    description?: string
    voiceId: string
    promptId: string
    language?: string
    config?: Partial<AgentConfig>
  }): Promise<Agent>

  updateAgent(id: string, input: Partial<{
    name: string
    description: string
    voiceId: string
    promptId: string
    language: string
    config: Partial<AgentConfig>
    status: AgentStatus
  }>): Promise<Agent>

  getAgent(id: string): Promise<Agent>
  listAgents(filter: {
    status?: AgentStatus
    search?: string
    page?: number
    limit?: number
  }): Promise<PaginatedResult<Agent>>

  deleteAgent(id: string): Promise<void>

  // ── Agent Versions ──
  deployAgent(id: string, note?: string): Promise<AgentVersion>
  getAgentVersions(id: string): Promise<AgentVersion[]>
  rollbackAgent(id: string, version: number): Promise<AgentVersion>

  // ── Prompts ──
  createPrompt(input: { name: string; content: string; variables?: string[] }): Promise<Prompt>
  updatePrompt(id: string, input: Partial<Prompt>): Promise<Prompt>
  listPrompts(): Promise<Prompt[]>

  // ── Voices ──
  listVoices(filter?: { provider?: string; language?: string }): Promise<Voice[]>
  createVoice(input: CreateVoiceInput): Promise<Voice>
}

// Agent Service internal API (for service-to-service calls)
export interface AgentServiceInternalContract {
  // Used by Call Service and AI Service
  getAgentConfig(agentId: string): Promise<AgentConfig>
  getPrompt(promptId: string): Promise<Prompt>
  getVoice(voiceId: string): Promise<Voice>
  resolveAgentForNumber(phoneNumber: string): Promise<Agent | null>
}

// Data ownership: Agent Service is the only service that writes to agents/voices/prompts tables
// Other services read via internal API only
```

## Data Ownership Matrix

```
TABLE             │ OWNER            │ READERS                  │ WRITE ACCESS
──────────────────┼──────────────────┼──────────────────────────┼──────────────
tenants           │ Auth Service     │ All services             │ Auth Service only
users             │ Auth Service     │ All services             │ Auth Service only
user_roles        │ Auth Service     │ Auth, API Gateway        │ Auth Service only
sessions          │ Auth Service     │ Auth Service only        │ Auth Service only
api_keys          │ Auth Service     │ API Gateway, Auth Service│ Auth Service only
──────────────────┼──────────────────┼──────────────────────────┼──────────────
agents            │ Agent Service    │ All services             │ Agent Service only
agent_versions    │ Agent Service    │ All services             │ Agent Service only
prompts           │ Agent Service    │ Call, AI Service         │ Agent Service only
voices            │ Agent Service    │ Call, Voice Service     │ Agent Service only
knowledge_bases   │ Agent Service    │ AI Service               │ Agent Service only
──────────────────┼──────────────────┼──────────────────────────┼──────────────
calls             │ Call Service     │ All services             │ Call Service only
conversation_ev.  │ Call Service     │ AI, Billing, Analytics   │ Call Service only
transcript_chunks │ Call Service     │ AI Service               │ Call Service only
call_recordings   │ Call Service     │ Billing, Analytics       │ Call Service only
──────────────────┼──────────────────┼──────────────────────────┼──────────────
campaigns         │ Campaign Service │ All services             │ Campaign Service only
contacts          │ Campaign Service │ Call Service             │ Campaign Service only
contact_lists     │ Campaign Service │ Campaign Service only    │ Campaign Service only
call_attempts     │ Campaign Service │ Call, Analytics          │ Campaign Service only
dnc_numbers       │ Campaign Service │ Call, Voice Service      │ Campaign Service only
──────────────────┼──────────────────┼──────────────────────────┼──────────────
plan_definitions  │ Billing Service  │ All services             │ Billing Service only
subscriptions     │ Billing Service  │ All services             │ Billing Service only
usage_records     │ Billing Service  │ Analytics                │ Billing Service only
invoices          │ Billing Service  │ Tenant (via API)         │ Billing Service only
payments          │ Billing Service  │ Tenant (via API)         │ Billing Service only
```

## Contract Versioning

```typescript
// API versioning strategy

// All REST APIs are versioned via URL path: /api/v1/agents
// Internal gRPC services use package versioning: voice.v1.VoiceService

export interface APIVersionPolicy {
  // Current version
  current: 'v1'
  // Deprecated (still functional but will be removed)
  deprecated: string[]
  // Sunset (no longer available)
  sunset: string[]

  // Minimum version supported
  minVersion: 'v1'
  // Maximum version planned
  maxVersion: 'v3'
}

// Backward compatibility rules:
// 1. Never remove fields from responses (add new fields as optional)
// 2. Never remove required fields from requests (add new fields as optional with defaults)
// 3. Never change the semantics of existing fields
// 4. Deprecate before removing (6-month sunset period)

// Contract testing
export async function verifyContractCompatibility(): Promise<void> {
  // Load previous contract
  const previousContract = await loadContract('v1.2.0')
  const currentContract = await loadContract('v1.3.0')

  // Verify backward compatibility
  const violations = checkBackwardCompatibility(previousContract, currentContract)
  if (violations.length > 0) {
    throw new Error(`Contract compatibility violations: ${violations.join(', ')}`)
  }
}
```

## Shared Kernel vs Bounded Context

```typescript
// Shared types (in monorepo package: @voice/shared)
// These types are shared across all services

// lib/shared/src/types.ts
export interface PaginatedResult<T> {
  data: T[]
  meta: {
    total: number
    page: number
    limit: number
    hasMore: boolean
  }
}

export interface ApiError {
  code: string
  message: string
  details?: unknown
  requestId?: string
}

// lib/shared/src/events.ts
// All event types shared here (see section 05)

// lib/shared/src/constants.ts
export const CALL_STATUSES = [
  'queued', 'ringing', 'connecting', 'in_progress',
  'paused', 'transferring', 'completed', 'failed',
  'no_answer', 'busy', 'voicemail', 'canceled', 'error'
] as const

export const PLAN_TIERS = ['free', 'starter', 'pro', 'business', 'enterprise'] as const

// Each service also has private types that are not shared
// Example: Voice Service private types
// services/voice-service/src/types.ts
export interface AudioPipelineConfig {
  sttModel: string
  sttLanguage: string
  sttComputeType: 'float16' | 'int8'
  ttsEngine: string
  ttsVoice: string
  vadThreshold: number
  maxSilenceMs: number
  sampleRate: 16000 | 24000 | 48000
  // This is private to Voice Service — not in shared package
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Boundary Definition | DDD Bounded Context | Clear ownership, no overlap |
| Data Sharing | Internal API (not shared DB) | Encapsulation, independent scaling |
| Contract Testing | OpenAPI + Protobuf compatibility | Automated CI verification |
| Versioning | URL-based (REST), package (gRPC) | Standard practices, tooling support |
| Shared Types | Monorepo package | Single source of truth, TypeScript types |

## Integration Points

- **Part 05 (Microservices)** — Boundaries enable independent deployment
- **Part 07 (API Gateway)** — Gateway routes to services by path
- **Part 03 (Database)** — Each service owns distinct tables
- **Part 19 (Testing)** — Contract tests verify service compatibility

## Production Considerations

- **Cross-Service Queries**: Minimize; use event-driven updates for denormalized data
- **Shared Database Access**: Never — leads to tight coupling and hidden dependencies
- **Internal API Latency**: Each internal hop adds ~5ms; batch requests when possible
- **Service Discovery**: Kubernetes DNS + Istio for reliable service resolution
- **SLA per Service**: Different SLAs for core vs supporting services
- **Ownership Handoff**: Documented with ADRs (Architecture Decision Records)
