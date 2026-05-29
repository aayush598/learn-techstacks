# Section 02: Folder Structure Standards

## Overview

A well-defined folder structure makes the codebase navigable, enforces separation of concerns, and scales predictably as the team grows. Our structure follows a feature-based organization within a monorepo, with colocated tests, barrel exports, and clear boundaries between application code, shared packages, and infrastructure configuration.

## Monorepo Top-Level Structure

```
voice-agent-platform/
├── apps/
│   ├── web/                  # Next.js frontend
│   └── api/                  # Express/Fastify backend
├── packages/
│   ├── ui/                   # Shared React component library
│   ├── db/                   # Prisma schema, migrations, client
│   ├── voice/                # Voice streaming, WebSocket management
│   ├── ai/                   # LLM integration, prompt templates
│   ├── config/               # Shared ESLint, TypeScript configs
│   └── shared/               # Types, utilities, validation schemas
├── docker/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   └── development/
│       ├── Dockerfile
│       └── Dockerfile.prod
├── .github/
│   ├── actions/
│   │   └── setup/action.yml
│   └── workflows/
│       ├── ci.yml
│       ├── deploy.yml
│       └── nightly.yml
├── scripts/
│   ├── deploy-staging.sh
│   ├── seed-database.ts
│   └── health-check.sh
├── turbo.json
├── pnpm-workspace.yaml
└── tsconfig.base.json
```

The top level separates **apps** (deployable units) from **packages** (shared libraries). This split ensures that application-specific concerns don't leak into shared code.

## Feature-Based Package Structure

Within each package, code is organized by feature, not by technical concern:

```
packages/voice/
├── src/
│   ├── streaming/
│   │   ├── voice-stream-manager.ts
│   │   ├── voice-stream-manager.test.ts
│   │   ├── audio-buffer.ts
│   │   └── audio-buffer.test.ts
│   ├── websocket/
│   │   ├── websocket-client.ts
│   │   ├── websocket-client.test.ts
│   │   ├── connection-manager.ts
│   │   └── reconnection-strategy.ts
│   ├── transcription/
│   │   ├── transcription-service.ts
│   │   ├── transcription-service.test.ts
│   │   ├── stt-provider.ts
│   │   └── stt-provider.test.ts
│   ├── types/
│   │   ├── voice-types.ts
│   │   └── events.ts
│   ├── constants.ts
│   └── index.ts
├── package.json
├── tsconfig.json
└── vitest.config.ts
```

**Design decision: Feature-based over layer-based**. A layer-based structure (having `src/controllers/`, `src/services/`, `src/models/`) scatters related code across directories. When adding a new feature like "transcription", you'd touch four directories. Feature-based grouping keeps all transcription code in one directory, making it easy to reason about a feature's full implementation.

The trade-off is that cross-cutting concerns (logging, metrics, error handling) must be implemented consistently across features rather than enforced by a shared layer.

## Colocated Tests

Tests live next to the source they test, never in a separate `__tests__` directory:

```
packages/voice/src/streaming/
├── voice-stream-manager.ts
├── voice-stream-manager.test.ts     # Unit tests
├── voice-stream-manager.integration.test.ts  # Integration tests
├── audio-buffer.ts
└── audio-buffer.test.ts
```

Colocation provides several advantages:
1. **Discoverability**: Tests are immediately visible when opening a feature directory
2. **Refactoring confidence**: Deleting a feature directory removes both source and tests
3. **Import paths**: Relative imports from test to source are short and clear

Integration tests get the `.integration.test.ts` suffix to differentiate them from unit tests, allowing CI to run them separately.

## Barrel Exports

Each package exposes a public API through an `index.ts` barrel file:

```typescript
// packages/voice/src/index.ts
export { VoiceStreamManager } from './streaming/voice-stream-manager';
export { WebSocketClient } from './websocket/websocket-client';
export { TranscriptionService } from './transcription/transcription-service';
export type { VoiceCallOptions, CallStatus } from './types/voice-types';
export type { VoiceEvent, VoiceEventHandler } from './types/events';
export { MAX_RETRY_ATTEMPTS, RECONNECT_BACKOFF_MS } from './constants';
```

The barrel file is the **only** entry point for external consumers. Internal imports within the package use deep paths:

```typescript
// Internal import (within packages/voice)
import { AudioBuffer } from './streaming/audio-buffer';

// External import (from apps/web)
import { VoiceStreamManager } from '@voice-agent/voice';
```

This boundary prevents internal refactoring from breaking consumers. If `audio-buffer.ts` is renamed to `audio-buffer-utils.ts`, only the barrel file needs updating — external consumers are unaffected.

## Application Structure

Applications follow the same feature-based pattern with additional Next.js conventions:

```
apps/web/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── (dashboard)/
│   │   │   ├── calls/
│   │   │   ├── analytics/
│   │   │   └── settings/
│   │   ├── api/
│   │   │   ├── voice/
│   │   │   └── auth/
│   │   └── layout.tsx
│   ├── components/
│   │   ├── voice-call/
│   │   ├── analytics/
│   │   └── shared/
│   ├── lib/
│   │   ├── api-client.ts
│   │   └── websocket-context.ts
│   ├── hooks/
│   │   ├── use-voice-call.ts
│   │   └── use-analytics.ts
│   └── styles/
│       ├── globals.css
│       └── variables.css
├── e2e/
│   ├── voice-call.spec.ts
│   └── auth.spec.ts
├── package.json
├── next.config.js
├── playwright.config.ts
└── tailwind.config.ts
```

The `app/` directory follows Next.js App Router conventions where folder nesting defines URL routes. Pages are minimal — they compose components from `components/` and use hooks from `hooks/`. Business logic lives in feature packages, not in the app layer.

## Configuration Packages

Shared configuration is extracted into `packages/config/`:

```
packages/config/
├── eslint/
│   ├── package.json
│   ├── base.js
│   ├── react.js
│   └── node.js
├── typescript/
│   ├── package.json
│   ├── tsconfig.base.json
│   ├── tsconfig.nextjs.json
│   └── tsconfig.node.json
└── vitest/
    ├── package.json
    └── vitest.base.ts
```

Each config is a package that can be referenced by name in its respective tool:

```jsonc
// apps/web/package.json (example)
{
  "eslintConfig": {
    "extends": ["@voice-agent/eslint-config/react"]
  }
}
```

## Integration Points

- **Turborepo**: Package topology determines build order based on inter-package dependencies
- **TypeScript**: Path aliases in `tsconfig.base.json` map `@voice-agent/*` to package directories
- **Testing**: Vitest configuration includes aliases and glob patterns matching the colocation convention
- **Docker**: Each app has its own Dockerfile that builds only its dependency graph using Turborepo scoping

## Production Considerations

1. **Monorepo tooling**: pnpm + Turborepo is the minimum viable combination. Adding Nx or Lage provides additional structure but increases complexity.
2. **Boundary enforcement**: Use ESLint's `import/no-restricted-paths` to prevent apps from importing from other apps or from the wrong package depth.
3. **Circular dependency detection**: Use Madge or a custom Turborepo plugin to detect circular package dependencies.
4. **Migration guide**: When reorganizing, do it in phases. First create the new structure, then move files gradually using git moves (not copy-paste) to preserve history.
5. **Generated code**: Generated code (Prisma client, GraphQL types) goes in a `__generated__` directory or is gitignored and regenerated during setup.
