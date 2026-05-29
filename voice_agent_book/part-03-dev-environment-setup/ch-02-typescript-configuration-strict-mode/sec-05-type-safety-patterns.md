# Section 05: Type Safety Patterns

## Overview

Beyond basic strict mode, several advanced TypeScript patterns provide additional type safety for specific domains in the voice agent platform. Branded types prevent mixing up IDs of different entities, discriminated unions model state machines safely, and template literal types create type-safe route definitions.

## Branded Types for IDs

Branded types use TypeScript's type system to create nominally-typed wrappers around primitive types, preventing accidental misuse of IDs that share the same underlying type (all `string`).

```typescript
// packages/types/src/utils/branded.ts

declare const BRAND: unique symbol;

export type Brand<T, B extends string> = T & { [BRAND]: B };

// ── Entity IDs ────────────────────────────────────────────
export type AgentId = Brand<string, "AgentId">;
export type CallId = Brand<string, "CallId">;
export type OrganizationId = Brand<string, "OrganizationId">;
export type ContactId = Brand<string, "ContactId">;
export type CampaignId = Brand<string, "CampaignId">;
export type UserId = Brand<string, "UserId">;
export type RecordingId = Brand<string, "RecordingId">;

// ── Constructor helpers ───────────────────────────────────
export function toAgentId(id: string): AgentId {
  return id as AgentId;
}

export function toCallId(id: string): CallId {
  return id as CallId;
}

export function toOrganizationId(id: string): OrganizationId {
  return id as OrganizationId;
}

// ── Prisma JSON field types ───────────────────────────────
export type JsonValue = Brand<string, "JsonValue">;
```

### Usage in Practice

```typescript
// Without branded types — this compiles but is wrong
async function getCall(callId: string): Promise<Call | null>;
async function getAgent(agentId: string): Promise<Agent | null>;

const agentId = "01HXYZ...";
const call = await getCall(agentId); // Compiles! Runtime bug!

// With branded types — this is a compile error
async function getCall(callId: CallId): Promise<Call | null>;
async function getAgent(agentId: AgentId): Promise<Agent | null>;

const agentId = toAgentId("01HXYZ...");
const call = await getCall(agentId); // Error! AgentId != CallId
const call = await getCall(toCallId("01HXYZ...")); // Correct
```

### Runtime Behavior

Branded types are erased at runtime — `toAgentId(x)` simply returns the input string. The brand only exists during type checking:

```typescript
const id = toAgentId("abc123");
console.log(typeof id); // "string" — brand is compile-time only
console.log(id); // "abc123"
```

## Discriminated Unions for State Machines

Voice calls, campaigns, and agent lifecycle are naturally modeled as state machines. Discriminated unions provide compile-time guarantees that state transitions are valid:

```typescript
// packages/types/src/domain/call-state.ts

// ── Call State Machine ─────────────────────────────────────
export type CallState =
  | { status: "initiating"; startedAt: Date }
  | { status: "ringing"; ringStartedAt: Date; attempts: number }
  | {
      status: "in_progress";
      connectedAt: Date;
      transcriptId: string | null;
      recordingId: string | null;
    }
  | {
      status: "transferring";
      fromAgentId: string;
      toAgentId: string;
      initiatedAt: Date;
    }
  | {
      status: "completed";
      endedAt: Date;
      duration: number;
      recordingUrl: string | null;
    }
  | { status: "failed"; error: string; endedAt: Date }
  | { status: "busy"; endedAt: Date }
  | { status: "no_answer"; endedAt: Date; retryAllowed: boolean };

// ── Type-safe transition ───────────────────────────────────
export type CallTransition = {
  from: CallState["status"];
  to: CallState["status"];
};

export const ALLOWED_TRANSITIONS: CallTransition[] = [
  { from: "initiating", to: "ringing" },
  { from: "initiating", to: "failed" },
  { from: "ringing", to: "in_progress" },
  { from: "ringing", to: "busy" },
  { from: "ringing", to: "no_answer" },
  { from: "ringing", to: "failed" },
  { from: "in_progress", to: "completed" },
  { from: "in_progress", to: "transferring" },
  { from: "in_progress", to: "failed" },
  { from: "transferring", to: "in_progress" },
  { from: "transferring", to: "completed" },
  { from: "transferring", to: "failed" },
];

export function transitionCall(
  current: CallState,
  target: CallState["status"],
): CallState {
  const transition = ALLOWED_TRANSITIONS.find(
    (t) => t.from === current.status && t.to === target,
  );

  if (!transition) {
    throw new Error(
      `Invalid transition from ${current.status} to ${target}`,
    );
  }

  // TypeScript narrows based on the discriminated union
  switch (target) {
    case "in_progress":
      return { status: "in_progress", connectedAt: new Date(), transcriptId: null, recordingId: null };
    case "completed":
      return {
        status: "completed",
        endedAt: new Date(),
        duration: calculateDuration(current),
        recordingUrl: null,
      };
    case "failed":
      return { status: "failed", error: "Unknown error", endedAt: new Date() };
    default:
      throw new Error(`Transition to ${target} not implemented`);
  }
}
```

### Pattern Matching with Exhaustive Switch

```typescript
function handleCallState(state: CallState): string {
  // TypeScript enforces exhaustiveness — if a new state is added,
  // this switch will produce a compile error
  switch (state.status) {
    case "initiating":
      return "Call is being initiated";
    case "ringing":
      return `Ringing (attempt ${state.attempts})`;
    case "in_progress":
      return state.recordingId ? "Recording in progress" : "Call active";
    case "transferring":
      return `Transferring to agent ${state.toAgentId}`;
    case "completed":
      return `Completed, duration: ${state.duration}s`;
    case "failed":
      return `Failed: ${state.error}`;
    case "busy":
      return "Line was busy";
    case "no_answer":
      return state.retryAllowed ? "No answer, will retry" : "No answer";
  }
}
```

## Template Literal Types for Routes

```typescript
// packages/types/src/api/routes.ts

// ── Route Definitions ──────────────────────────────────────
export type ApiVersion = "v1" | "v2";

export type ApiRoutes = {
  agents: `/api/${ApiVersion}/agents`;
  agentById: `/api/${ApiVersion}/agents/${string}`;
  agentCalls: `/api/${ApiVersion}/agents/${string}/calls`;
  calls: `/api/${ApiVersion}/calls`;
  callById: `/api/${ApiVersion}/calls/${string}`;
  callTranscript: `/api/${ApiVersion}/calls/${string}/transcript`;
  campaigns: `/api/${ApiVersion}/campaigns`;
  campaignById: `/api/${ApiVersion}/campaigns/${string}`;
  contacts: `/api/${ApiVersion}/contacts`;
  contactById: `/api/${ApiVersion}/contacts/${string}`;
  analytics: `/api/${ApiVersion}/analytics`;
  webhooks: `/api/${ApiVersion}/webhooks`;
};

// ── Type-safe route builder ────────────────────────────────
export function buildRoute<T extends keyof ApiRoutes>(
  route: T,
  ...params: T extends "agentById" | "agentCalls"
    ? [string]
    : T extends "callById" | "callTranscript"
      ? [string]
      : T extends "campaignById"
        ? [string]
        : T extends "contactById"
          ? [string]
          : []
): ApiRoutes[T] {
  const base = "/api/v1" as const;

  switch (route) {
    case "agents":
      return `${base}/agents` as ApiRoutes[T];
    case "agentById":
    case "agentCalls": {
      const [id] = params as [string];
      const suffix = route === "agentCalls" ? "/calls" : "";
      return `${base}/agents/${id}${suffix}` as ApiRoutes[T];
    }
    case "calls":
      return `${base}/calls` as ApiRoutes[T];
    case "callById":
    case "callTranscript": {
      const [id] = params as [string];
      const suffix = route === "callTranscript" ? "/transcript" : "";
      return `${base}/calls/${id}${suffix}` as ApiRoutes[T];
    }
    case "campaigns":
      return `${base}/campaigns` as ApiRoutes[T];
    case "campaignById": {
      const [id] = params as [string];
      return `${base}/campaigns/${id}` as ApiRoutes[T];
    }
    default:
      throw new Error(`Unknown route: ${route}`);
  }
}

// Usage:
// const url = buildRoute("agentById", "01HXYZ...");
// // url type: `/api/v1/agents/${string}`
// // url value: "/api/v1/agents/01HXYZ..."
```

## Type-Safe Event Emitters

```typescript
// packages/types/src/events/emitter.ts

export interface EventMap {
  "call:initiated": { callId: CallId; agentId: AgentId; contactPhone: string };
  "call:completed": { callId: CallId; duration: number; cost: number };
  "call:failed": { callId: CallId; error: string };
  "agent:deployed": { agentId: AgentId; version: string };
  "agent:updated": { agentId: AgentId; changes: string[] };
  "transcript:ready": { callId: CallId; transcriptUrl: string };
}

export class TypedEmitter<T extends Record<string, unknown>> {
  private listeners = new Map<
    keyof T,
    Set<(data: T[keyof T]) => void>
  >();

  on<K extends keyof T>(event: K, listener: (data: T[K]) => void): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(listener as (data: T[keyof T]) => void);
  }

  emit<K extends keyof T>(event: K, data: T[K]): void {
    this.listeners.get(event)?.forEach((listener) => {
      listener(data as T[keyof T]);
    });
  }

  removeListener<K extends keyof T>(event: K, listener: (data: T[K]) => void): void {
    this.listeners.get(event)?.delete(listener as (data: T[keyof T]) => void);
  }
}

// Usage:
const emitter = new TypedEmitter<EventMap>();
emitter.on("call:initiated", (data) => {
  console.log(data.callId); // Type-safe!
});
```

## Type-Safe Configuration Objects

```typescript
// packages/types/src/domain/configuration.ts

type ProviderConfig = {
  elevenlabs: { apiKey: string; voiceId: string; stability: number };
  cartesia: { apiKey: string; voiceId: string; speed: number };
  deepgram: { apiKey: string; model: string; language: string };
};

export type VoiceConfig<P extends keyof ProviderConfig = keyof ProviderConfig> = {
  provider: P;
  config: ProviderConfig[P];
};

// Usage:
const config: VoiceConfig<"elevenlabs"> = {
  provider: "elevenlabs",
  config: {
    // TypeScript knows this must be ElevenLabs config
    apiKey: "...",
    voiceId: "...",
    stability: 0.8,
  },
};
```

## Design Decisions

### Branded Types vs. Classes vs. Symbols

| Approach | Runtime cost | Type safety | Ergonomics |
|----------|-------------|-------------|------------|
| Branded types | None (erased) | Compile-time only | Excellent |
| Classes with instanceof | Runtime memory | Both | Poor (verbose) |
| Symbols | Runtime lookup | Both | Moderate |

**Decision**: Branded types are the lightest-weight approach. They add zero runtime overhead and provide full compile-time protection.

### When NOT to use branded types

- **User-facing IDs**: If IDs are provided by the user or API, validate them at the boundary and then brand internally
- **Serialized data**: Branded types are lost in JSON serialization. Deserialize with validation on the receiving end
- **Performance-critical loops**: The branding function itself is zero-cost, but excessive use can make code harder to read

## Integration Points

- **API handlers**: Use branded IDs in request handlers after validation
- **Event system**: Branded types in event payloads prevent routing errors
- **Database layer**: Repository methods accept and return branded IDs
- **State machines**: Discriminated union states are used throughout call processing

## Production Considerations

1. **Branded type boundaries**: Brand at the system boundary (API → service), never in the database layer (Prisma returns plain strings)
2. **Validation**: Always validate that a plain string is a valid ID before branding. The brand is a compile-time guarantee, not a runtime one
3. **Testing**: Test state transitions exhaustively — the type system guarantees valid transitions at compile time, but runtime behavior must still be verified
4. **Third-party libraries**: When passing branded IDs to libraries, cast to the base type. Libraries don't know about our brands
