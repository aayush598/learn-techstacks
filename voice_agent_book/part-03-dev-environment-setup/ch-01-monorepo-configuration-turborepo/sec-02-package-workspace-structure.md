# Section 02: Package Workspace Structure

## Overview

The voice agent platform monorepo is organized into two categories: applications (apps) that compose the final product, and packages that provide reusable libraries. This structure maximizes code sharing while maintaining clear ownership boundaries.

## Workspace Topology

```text
voice-agent-platform/
├── apps/
│   ├── web/                          # Next.js frontend (App Router)
│   │   ├── src/
│   │   │   ├── app/                  # App Router pages
│   │   │   ├── components/           # Page-specific components
│   │   │   └── lib/                  # Client utilities
│   │   ├── next.config.js
│   │   ├── tailwind.config.ts
│   │   └── package.json
│   └── api/                          # Next.js API (API routes + edge)
│       ├── src/
│       │   ├── app/                  # API route handlers
│       │   ├── services/             # Business logic
│       │   └── middleware.ts         # Auth, rate limiting
│       ├── next.config.js
│       └── package.json
├── packages/
│   ├── ui/                           # Shared component library
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── tokens/              # Design tokens
│   │   │   └── hooks/
│   │   └── package.json
│   ├── db/                           # Database access (Prisma)
│   │   ├── prisma/
│   │   │   ├── schema.prisma
│   │   │   └── migrations/
│   │   ├── src/
│   │   │   ├── client.ts
│   │   │   └── seed.ts
│   │   └── package.json
│   ├── voice/                        # Voice processing
│   │   ├── src/
│   │   │   ├── stt/                 # Speech-to-text
│   │   │   ├── tts/                 # Text-to-speech
│   │   │   └── vad/                 # Voice activity detection
│   │   └── package.json
│   ├── ai/                           # AI/LLM utilities
│   │   ├── src/
│   │   │   ├── providers/           # OpenAI, Anthropic, etc.
│   │   │   ├── prompts/             # Prompt templates
│   │   │   └── rag/                 # RAG pipeline
│   │   └── package.json
│   └── config/                       # Shared configuration
│       ├── eslint/
│       ├── typescript/
│       ├── prettier/
│       └── tailwind/
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
├── turbo.json
├── pnpm-workspace.yaml
├── package.json
└── .gitignore
```

## Application Layer

### apps/web — Customer Dashboard

The web app provides the user-facing dashboard where customers configure voice agents, view analytics, and manage settings.

```jsonc
{
  "name": "@voice-agent/web",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "lint": "next lint",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@voice-agent/ui": "workspace:*",
    "@voice-agent/db": "workspace:*",
    "@voice-agent/ai": "workspace:*",
    "next": "^14.2.0",
    "react": "^18.3.0",
    "react-dom": "^18.3.0"
  },
  "devDependencies": {
    "@voice-agent/config-typescript": "workspace:*",
    "@voice-agent/config-eslint": "workspace:*",
    "@voice-agent/config-tailwind": "workspace:*"
  }
}
```

### apps/api — API Server

The API app handles all backend logic, webhook processing, real-time communication via WebSockets, and edge computing functions.

```jsonc
{
  "name": "@voice-agent/api",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "dev": "next dev -p 4000",
    "build": "next build",
    "lint": "next lint",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@voice-agent/db": "workspace:*",
    "@voice-agent/voice": "workspace:*",
    "@voice-agent/ai": "workspace:*",
    "next": "^14.2.0",
    "react": "^18.3.0"
  }
}
```

Running the API on port 4000 separates it from the frontend on port 3000, allowing independent development and testing.

## Package Layer

### packages/db — Database Package

The database package encapsulates Prisma schema, client, migrations, and seed logic. No application code outside this package should import Prisma directly.

```jsonc
{
  "name": "@voice-agent/db",
  "version": "0.0.1",
  "private": true,
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": "./dist/index.js",
    "./client": "./dist/client.js",
    "./types": "./dist/types.js"
  },
  "scripts": {
    "build": "tsc && prisma generate",
    "db:generate": "prisma generate",
    "db:migrate": "prisma migrate dev",
    "db:seed": "tsx src/seed.ts",
    "db:reset": "prisma migrate reset"
  },
  "dependencies": {
    "@prisma/client": "^5.12.0"
  },
  "devDependencies": {
    "prisma": "^5.12.0",
    "tsx": "^4.7.0"
  }
}
```

### packages/voice — Voice Processing Package

Contains speech-to-text, text-to-speech, and voice activity detection abstractions. Each module provides a provider-agnostic interface with concrete implementations.

```text
packages/voice/src/
├── stt/
│   ├── types.ts           # SpeechToTextProvider interface
│   ├── deepgram.ts        # Deepgram implementation
│   ├── assembly.ts        # AssemblyAI implementation
│   └── mock.ts            # Mock for testing
├── tts/
│   ├── types.ts           # TextToSpeechProvider interface
│   ├── elevenlabs.ts      # ElevenLabs implementation
│   ├── cartesia.ts        # Cartesia implementation
│   └── mock.ts
├── vad/
│   ├── types.ts           # VoiceActivityDetector interface
│   ├── silero.ts          # Silero VAD implementation
│   └── mock.ts
└── index.ts               # Barrel exports
```

### packages/ai — AI Abstraction Package

Provides LLM provider abstraction, prompt management, and RAG pipeline utilities. This is where the conversation with language models is orchestrated.

```text
packages/ai/src/
├── providers/
│   ├── types.ts           # LLMProvider interface
│   ├── openai.ts
│   ├── anthropic.ts
│   └── mock.ts
├── prompts/
│   ├── templates/         # Prompt templates directory
│   ├── manager.ts         # Prompt versioning and loading
│   └── types.ts
├── rag/
│   ├── embedder.ts        # Text embedding
│   ├── retriever.ts       # Vector search retrieval
│   └── pipeline.ts        # Full RAG pipeline
├── tools/
│   ├── registry.ts        # Function calling registry
│   └── definitions.ts     # Tool definitions
└── index.ts
```

### packages/ui — Component Library

Shared React components with design system tokens. Consumed by the web app and potentially by embedded widgets.

```jsonc
{
  "name": "@voice-agent/ui",
  "version": "0.0.1",
  "private": true,
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": "./dist/index.js",
    "./tokens": "./dist/tokens.js",
    "./styles": "./dist/styles.css"
  },
  "scripts": {
    "build": "tsc && tsc-alias",
    "dev": "tsc --watch",
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build"
  },
  "peerDependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "tailwindcss": "^3.4.0"
  }
}
```

### packages/config — Configuration Packages

Each config tool has its own package within the config directory, making it easy for apps to depend only on what they need:

- `@voice-agent/config-eslint` — ESLint flat config with shared rules
- `@voice-agent/config-typescript` — Base tsconfig with strict mode
- `@voice-agent/config-prettier` — Prettier configuration
- `@voice-agent/config-tailwind` — Tailwind preset with brand tokens

## Dependency Graph

Understanding the dependency graph is critical for build ordering:

```text
                  apps/web ──── apps/api
                     │              │
                     ├──────┬───────┤
                     │      │       │
                  packages/ui   packages/db
                     │              │
                     │              ├── packages/voice
                     │              └── packages/ai
                     │
               packages/config
            (eslint, typescript, prettier, tailwind)
```

The `config` packages are devDependencies and don't participate in the build graph. The `ui` package depends on React (peer dependency). Both apps depend on `db`, and `api` additionally depends on `voice` and `ai`.

## Design Decisions

**Colocation vs. separation**: Each package manages its own dependencies, scripts, and build configuration. This allows teams to work independently and packages to be extracted into separate repositories if needed.

**Private by default**: All packages set `"private": true` to prevent accidental publication to npm. Only packages intended for external use should remove this flag.

**Workspace protocol**: Using `"workspace:*"` ensures local packages always reference each other via the workspace protocol, never accidentally pulling from npm.

## Production Considerations

1. **Circular dependencies**: Turborepo detects and errors on circular workspace dependencies. Enforce a strict DAG
2. **Bundle size**: Monitor the `ui` package bundle size — tree-shaking requires proper ESM configuration
3. **Version alignment**: When packages depend on shared deps (React, Next.js), use peer dependencies to prevent duplicates
4. **Entry point consistency**: Each package should export a clean public API via index.ts — avoid deep imports across packages
