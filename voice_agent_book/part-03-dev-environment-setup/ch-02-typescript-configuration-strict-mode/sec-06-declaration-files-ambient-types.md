# Section 06: Declaration Files & Ambient Types

## Overview

Declaration files (.d.ts) provide TypeScript with type information for code that doesn't have built-in type definitions — browser APIs, environment variables, global modules, and third-party libraries. This section covers how the voice agent platform manages ambient types to ensure a fully typed development experience.

## Ambient Type Categories

```text
┌─────────────────────────────────────────────────────────────┐
│                  Ambient Type Declarations                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Global Types                                          │   │
│  │  - Process.env type augmentation                     │   │
│  │  - Global utility types                              │   │
│  │  - Window extensions (analytics, feature flags)      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Module Declarations                                   │   │
│  │  - CSS/SCSS module imports                           │   │
│  │  - Image/asset imports                               │   │
│  │  - Untyped JavaScript libraries                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Third-Party Type Augmentations                       │   │
│  │  - Extending library types                           │   │
│  │  - Adding missing exports                            │   │
│  │  - Overriding incorrect types                        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Global Type Declarations

### Environment Variables

The most common ambient type declaration augments `ProcessEnv` to provide type information for application environment variables:

```typescript
// packages/types/src/ambient/env.d.ts

declare namespace NodeJS {
  interface ProcessEnv {
    // App
    NODE_ENV: "development" | "production" | "test";
    APP_NAME: string;
    APP_URL: string;
    API_URL: string;

    // Database
    DATABASE_URL: string;
    DATABASE_URL_READER: string;
    SHADOW_DATABASE_URL?: string;

    // Redis
    REDIS_URL: string;
    REDIS_PREFIX: string;

    // Kafka
    KAFKA_BROKERS: string;
    KAFKA_CLIENT_ID: string;
    KAFKA_GROUP_ID: string;

    // Storage
    MINIO_ENDPOINT: string;
    MINIO_PORT: string;
    MINIO_ACCESS_KEY: string;
    MINIO_SECRET_KEY: string;
    MINIO_BUCKET_RECORDINGS: string;
    MINIO_BUCKET_TRANSCRIPTS: string;

    // Voice Providers
    ELEVENLABS_API_KEY: string;
    DEEPGRAM_API_KEY: string;
    CARTESIA_API_KEY: string;

    // LLM Providers
    OPENAI_API_KEY: string;
    ANTHROPIC_API_KEY: string;

    // Auth
    JWT_SECRET: string;
    JWT_EXPIRES_IN: string;
    AUTH_REDIRECT_URL: string;

    // Monitoring
    SENTRY_DSN?: string;
    SENTRY_ENVIRONMENT: string;
    OTEL_EXPORTER_OTLP_ENDPOINT?: string;

    // Feature Flags
    FEATURE_VOICE_ANALYTICS?: "true" | "false";
    FEATURE_HUMAN_HANDOFF?: "true" | "false";
    FEATURE_CAMPAIGNS?: "true" | "false";

    // Optional
    LOG_LEVEL?: "debug" | "info" | "warn" | "error";
    DEBUG?: string;
  }
}
```

### Global Utility Types

```typescript
// packages/types/src/ambient/global.d.ts

// Make branded types available globally through the monorepo
declare global {
  // ── Utility Types ────────────────────────────────────────
  type DeepPartial<T> = T extends object
    ? { [P in keyof T]?: DeepPartial<T[P]> }
    : T;

  type AsyncReturnType<T extends (...args: unknown[]) => unknown> =
    T extends (...args: unknown[]) => Promise<infer R> ? R : never;

  type NonEmptyArray<T> = [T, ...T[]];

  // ── Callback aliases ─────────────────────────────────────
  type AsyncHandler<T = void> = () => Promise<T>;
  type SyncHandler<T = void> = () => T;

  // ── JSON-compatible types ────────────────────────────────
  type JsonValue = string | number | boolean | null | JsonObject | JsonArray;
  interface JsonObject {
    [key: string]: JsonValue;
  }
  type JsonArray = JsonValue[];
}

// Required for the `declare global` pattern to work
export {};
```

## Browser API Types

### Web Audio API

For voice processing on the frontend, augmentations for Web Audio API are needed:

```typescript
// packages/voice/src/ambient/audio.d.ts

// Extend AudioContext for our voice processing needs
declare global {
  interface AudioContext {
    // Custom method for voice activity detection
    createVoiceActivityDetector(): Promise<VoiceActivityDetector>;
  }

  interface VoiceActivityDetector {
    readonly speaking: boolean;
    readonly confidence: number;
    onEvent: (event: VADEvent) => void;
    start(): Promise<void>;
    stop(): void;
    destroy(): void;
  }

  interface VADEvent {
    type: "speech_start" | "speech_end" | "silence" | "error";
    timestamp: number;
    data?: unknown;
  }
}

export {};
```

### MediaStream Recording

```typescript
// packages/voice/src/ambient/mediarecorder.d.ts

// Extend MediaRecorder for our recording needs
declare global {
  interface MediaRecorder {
    // Custom property to track recording metadata
    recordingId?: string;
    callId?: string;
  }

  interface MediaRecorderEventMap {
    "segment": BlobEvent;
    "error": ErrorEvent;
  }
}

export {};
```

## Module Declarations

### Asset Imports

```typescript
// packages/config/typescript/ambient/assets.d.ts

// CSS modules
declare module "*.module.css" {
  const classes: { readonly [key: string]: string };
  export default classes;
}

declare module "*.module.scss" {
  const classes: { readonly [key: string]: string };
  export default classes;
}

// Static assets
declare module "*.svg" {
  const content: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
  export default content;
}

declare module "*.png" {
  const content: string;
  export default content;
}

declare module "*.jpg" {
  const content: string;
  export default content;
}

declare module "*.webp" {
  const content: string;
  export default content;
}

declare module "*.woff2" {
  const content: string;
  export default content;
}
```

### JSON Imports

```typescript
// packages/config/typescript/ambient/json.d.ts

// Enable importing JSON files with type safety
declare module "*.json" {
  const value: unknown;
  export default value;
}
```

## Third-Party Type Augmentations

### Extending Next.js Types

```typescript
// apps/web/src/types/next.d.ts

import type { OrganizationId } from "@voice-agent/types";

declare module "next" {
  interface NextApiRequest {
    organizationId: OrganizationId;
    userId: string;
  }
}

declare module "next/navigation" {
  interface AppRouterInstance {
    // Custom navigation methods
    pushWithParams(path: string, params?: Record<string, string>): void;
    replaceWithParams(path: string, params?: Record<string, string>): void;
  }
}
```

### Extending Express/Socket.io Types

```typescript
// apps/api/src/types/socket.d.ts

import type { AgentId, OrganizationId, UserId } from "@voice-agent/types";

declare module "socket.io" {
  interface Socket {
    userId: UserId;
    organizationId: OrganizationId;
    agentId?: AgentId;
  }
}
```

### Library Type Fixes

When a library has incomplete or incorrect types, augment locally:

```typescript
// apps/web/src/types/library-fixes.d.ts

// Example: Adding missing exports from a library
declare module "some-library" {
  export function missingFunction(param: string): Promise<void>;
}

// Example: Fixing incorrect types
declare module "incorrect-types-library" {
  interface FixedType {
    id: string;
    name: string;
    // Original library has this as optional, but it's always present
    status: string;
  }

  export function getEntity(id: string): Promise<FixedType>;
}
```

## Declaration File Organization

```text
packages/types/src/ambient/
├── env.d.ts               # ProcessEnv augmentations
├── global.d.ts            # Global utility types
├── api.d.ts               # API-related ambient types
└── events.d.ts            # Custom event types

apps/web/src/types/
├── next.d.ts              # Next.js type augmentations
├── assets.d.ts            # Asset import declarations
├── library-fixes.d.ts     # Third-party type patches
└── feature-flags.d.ts     # Feature flag types

apps/api/src/types/
├── socket.d.ts            # Socket.io augmentations
├── kafka.d.ts             # Kafka message types
└── middleware.d.ts        # Request context types
```

## TypeScript Configuration for Ambient Types

```jsonc
{
  "compilerOptions": {
    // Ambient declarations are included by default through
    // the `include` pattern or manually via `types`:
    "types": ["node", "jest"],
    "typeRoots": [
      "./node_modules/@types",
      "./src/types",           // App-specific ambient types
      "./packages/types/src/ambient" // Shared ambient types
    ]
  },
  "include": [
    "src/**/*.ts",
    "src/**/*.tsx",
    "src/types/**/*.d.ts"     // Include all declaration files
  ],
  "files": [
    "../../packages/types/src/ambient/env.d.ts" // Explicit reference for shared
  ]
}
```

## Design Decisions

### Global declarations vs. explicit imports

**Decision**: Use global declarations sparingly for truly universal types (process.env, global utilities). Prefer explicit imports for everything else.

**Rationale**: Global types are invisible — developers may not know where a type comes from. Explicit imports clarify dependencies and make code review easier. Global declarations should be reserved for:
- Environment variable typing
- Truly cross-cutting utility types
- Third-party library type augmentations

### Type augmentation vs. fork

When a library has incorrect types:
1. First try augmenting locally (`.d.ts` file)
2. If the types are fundamentally broken, create a thin wrapper module
3. Only fork the library as a last resort

## Integration Points

- **VS Code**: Ambient types are picked up automatically for IntelliSense
- **TypeScript compiler**: Reads all `*.d.ts` files in `include` paths
- **CI type checking**: Ambient types must be included in the `files` or `include` configuration for CI to use them
- **API documentation**: Some tools (TypeDoc) use ambient types for documentation generation

## Production Considerations

1. **TypeRoots ordering**: The order of `typeRoots` matters. If two type definitions conflict, the first match wins. List application types first to override library defaults
2. **Declaration file cleanup**: Remove unused ambient types. Stale declarations can hide type errors by providing incorrect type information
3. **Cross-package ambient types**: Shared ambient types (like env.d.ts) must be accessible to all packages. Include them via `files` in each package's tsconfig or use a shared config package
4. **Version conflicts**: When upgrading libraries, check if their built-in types now cover what you were augmenting. Remove redundant declarations
5. **Triple-slash directives**: Prefer `declare module` over `/// <reference>` directives. The reference directive is deprecated for most use cases
