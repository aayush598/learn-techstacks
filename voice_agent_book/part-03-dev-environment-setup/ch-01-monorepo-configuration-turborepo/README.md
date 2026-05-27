# Chapter 01: Monorepo Configuration with Turborepo

> **Part:** 03 - Development Environment & Project Setup

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Turborepo Initialization](sec-01-turborepo-initialization.md) | Project scaffolding, workspace configuration (pnpm), turbo.json pipeline definition |
| 02 | [Package Workspace Structure](sec-02-package-workspace-structure.md) | apps/web (Next.js), apps/api (Next.js API), packages/ui, packages/db, packages/voice, packages/ai, packages/config |
| 03 | [Build Pipeline Configuration](sec-03-build-pipeline-configuration.md) | Task dependencies, output caching, remote caching, parallel execution, inputs/outputs |
| 04 | [Shared TypeScript Package](sec-04-shared-typescript-package.md) | Common types, API contracts, Zod schemas, shared constants |
| 05 | [Database Package (Prisma)](sec-05-database-package-prisma.md) | Shared Prisma schema, client generation, migration scripts, seed data |
| 06 | [UI Component Package](sec-06-ui-component-package.md) | Shared component library, design system tokens, Storybook, tree-shaking |
| 07 | [Configuration Packages](sec-07-configuration-packages.md) | ESLint config, TypeScript config, Prettier config, Tailwind config — shared across workspaces |
| 08 | [Local Package Development](sec-08-local-package-development.md) | Linking, hot reload, versioning, publishing internal packages |

---

## Monorepo Structure

```
voice-agent-platform/
├── apps/
│   ├── web/              # Next.js dashboard (App Router)
│   └── api/              # Next.js API routes + edge functions
├── packages/
│   ├── ui/               # Shared component library
│   ├── db/               # Prisma schema + client
│   ├── voice/            # STT/TTS/VAD utilities
│   ├── ai/               # LLM abstraction, prompts, RAG
│   └── config/           # ESLint, TS, Prettier configs
├── docker/               # Docker Compose files
├── turbo.json            # Build pipeline
└── package.json          # Workspace root
```

---

## Key Takeaways

- Turborepo for fast, caching build system
- pnpm workspaces for efficient dependency management
- Shared packages for types, UI, database, and configuration
- Remote caching for CI speed (Vercel Remote Cache)
- Package-specific tsconfig extending root config
- Prisma client shared across apps via @voice-agent/db package
