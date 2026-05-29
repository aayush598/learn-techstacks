# Section 01: Naming Conventions

## Overview

Consistent naming is the most visible aspect of code conventions. It reduces cognitive load during code review, makes grep-based search predictable, and enforces a mental model of the codebase's structure. This section defines naming rules for files, components, functions, types, constants, and database entities across the voice agent platform.

## Naming Convention Map

```text
┌──────────────────────────────────────────────────────────────────┐
│                    Naming Convention Reference                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Entity            │ Convention    │ Example                       │
│  ──────────────────┼───────────────┼──────────────────────────────│
│  Files/Directories │ kebab-case    │ voice-stream-manager.ts       │
│  React Components  │ PascalCase    │ VoiceCallPanel.tsx            │
│  Functions/Methods │ camelCase     │ connectToVoiceStream()        │
│  Variables         │ camelCase     │ activeCallCount               │
│  Classes           │ PascalCase    │ VoiceStreamManager            │
│  Interfaces        │ PascalCase    │ VoiceCallOptions              │
│  Types             │ PascalCase    │ CallStatus                    │
│  Enums             │ PascalCase    │ CallDisconnectReason          │
│  Enum Members      │ PascalCase    │ UserHungUp                    │
│  Constants         │ UPPER_CASE    │ MAX_RETRY_ATTEMPTS            │
│  Database tables   │ snake_case    │ voice_call_logs               │
│  Database columns  │ snake_case    │ call_duration_ms              │
│  Environment vars  │ UPPER_CASE    │ VOICE_API_KEY                 │
│  CSS classes       │ kebab-case    │ .voice-call-panel            │
│  Git branches      │ kebab-case    │ feat/voice-stream-retry       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## File and Directory Naming

All files and directories use **kebab-case**. This is the most portable naming convention — it works case-sensitively across macOS, Linux, and Windows without issues, and it's URL-friendly.

```
packages/
  ui/
    voice-call-panel/
      voice-call-panel.tsx
      voice-call-panel.test.tsx
      voice-call-panel.stories.tsx
      use-voice-call.ts
      voice-call-status.tsx
```

The one exception is `index.ts` barrel files — they retain the standard `index.ts` name rather than being renamed to the directory name. This follows the Node.js module resolution convention and keeps import paths clean.

**Design decision**: Some teams prefer PascalCase for component files to match the component name (`VoiceCallPanel.tsx`). We chose kebab-case because:
1. It's consistent across all file types (not just components)
2. Case-insensitive filesystems don't cause ambiguity
3. CLI tab-completion works predictably
4. URL-based import paths match the filesystem path

## Component Naming

React components use **PascalCase** for both the component function and the file name:

```typescript
// packages/ui/voice-call-panel/voice-call-panel.tsx
export function VoiceCallPanel({ callId, onEnd }: VoiceCallPanelProps) {
  return <div className="voice-call-panel">{/* ... */}</div>;
}
```

Hooks use **camelCase** prefixed with `use`:

```typescript
// packages/ui/voice-call-panel/use-voice-call.ts
export function useVoiceCall(callId: string) {
  const [status, setStatus] = useState<CallStatus>('idle');
  // ...
  return { status, connect, disconnect };
}
```

Higher-order components use **camelCase** prefixed with `with`:

```typescript
export function withVoiceCallTracking<T extends VoiceCallProps>(
  Component: React.ComponentType<T>
) {
  return function TrackedVoiceCall(props: T) {
    // ...
    return <Component {...props} />;
  };
}
```

## Type and Interface Naming

Types and interfaces use **PascalCase**. Interfaces are preferred for object shapes that represent public APIs; types are used for unions, intersections, and internal types:

```typescript
// Public API interface
export interface VoiceCallOptions {
  callId: string;
  participantIds: string[];
  recordingEnabled?: boolean;
  maxDurationSeconds: number;
}

// Internal union type
export type CallStatus =
  | 'idle'
  | 'connecting'
  | 'connected'
  | 'disconnected'
  | 'error';

// Generic constraint type
export type VoiceEventCallback<T = unknown> = (event: T) => void | Promise<void>;
```

A naming subtlety: we use **`Props` suffix** for component props types (`VoiceCallPanelProps`) and **`Options` suffix** for configuration objects (`VoiceCallOptions`). This disambiguates the two categories, which are often confused.

## Constant Naming

Constants use **UPPER_SNAKE_CASE** for module-level immutable values:

```typescript
// packages/voice/src/constants.ts
export const MAX_RETRY_ATTEMPTS = 3;
export const RECONNECT_BACKOFF_MS = 1000;
export const AUDIO_SAMPLE_RATE = 16000;
export const DEFAULT_VOICE_TIMEOUT_MS = 30_000;
export const SUPPORTED_AUDIO_FORMATS = ['pcm16', 'opus', 'mp3'] as const;
```

The `as const` assertion ensures TypeScript infers the literal type rather than `string[]`, enabling exhaustive type checks when consuming the constant.

**Trade-off**: Upper snake case makes constants visually distinct but is noisier for long names. We limit it to truly immutable values. Configuration variables read from `process.env` are not constants (they can change per environment) and use camelCase within their configuration object.

## Database Naming

Database entities use **snake_case** to align with PostgreSQL conventions:

```prisma
// packages/db/prisma/schema.prisma
model VoiceCallLog {
  id              String   @id @default(cuid())
  callId          String   @map("call_id")
  participantId   String   @map("participant_id")
  callDurationMs  Int      @map("call_duration_ms")
  status          CallStatus
  startedAt       DateTime @map("started_at") @default(now())
  endedAt         DateTime? @map("ended_at")
  createdAt       DateTime @map("created_at") @default(now())
  updatedAt       DateTime @updatedAt @map("updated_at")

  @@map("voice_call_logs")
}
```

The `@map` attribute exposes camelCase properties in TypeScript while keeping snake_case in the database. This gives TypeScript developers idiomatic JavaScript naming without sacrificing PostgreSQL convention adherence.

## Environment Variable Naming

Environment variables use **UPPER_SNAKE_CASE** with a project prefix:

```
VOICE_API_KEY=sk-...
VOICE_DATABASE_URL=postgres://...
VOICE_REDIS_URL=redis://...
VOICE_KAFKA_BROKERS=kafka:9092
VOICE_LOG_LEVEL=debug
NEXT_PUBLIC_VOICE_WS_URL=wss://...
```

The `VOICE_` prefix prevents collisions when the deployment environment has variables from multiple projects. `NEXT_PUBLIC_` follows Next.js convention for client-side environment exposure.

## Git Branch Naming

Branches follow the `type/short-description` pattern:

```
feat/voice-stream-retry
fix/audio-sync-offset
chore/update-deps-2024-06
docs/api-voice-endpoints
refactor/call-state-machine
```

The type prefix enables automated changelog generation and branch filtering in CI workflows. Type prefixes are limited to: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `perf`, `security`.

## Integration Points

- **ESLint**: `eslint-plugin-unicorn` enforces filename casing rules via `unicorn/filename-case`
- **Prettier**: Formats consistently but doesn't enforce naming conventions
- **TypeScript**: The `@typescript-eslint/naming-convention` rule enforces type/interface/class naming
- **Prisma**: Column maps and table maps enforce database naming separation
- **Git hooks**: Branch name validation via `commitlint` or a custom hook

## Production Considerations

1. **Migration cost**: Changing naming conventions mid-project is expensive. Establish these rules before writing the first line of application code.
2. **Code generation alignment**: Ensure scaffolding tools (Plop, Hygen) generate files that follow naming conventions automatically.
3. **Linter auto-fix**: Configure ESLint's `unicorn/filename-case` with `fix: true` to auto-rename files on save in supported editors.
4. **Review checklist**: Add a naming convention section to the PR review template to catch violations early.
5. **Gradual enforcement**: For existing codebases adopting these conventions, use a `// eslint-disable-next-line` comment with a TODO to allow gradual migration without blocking development.
