# GuardrailZ - Project Overview

## What is GuardrailZ?

GuardrailZ is a **production-grade LLM safety & moderation platform** built with Next.js 14. It provides a multi-layered guardrail engine that validates both **input** (user prompts) and **output** (model responses) for AI systems, enforcing safety, security, compliance, and quality policies.

The platform exposes a **REST API** for programmatic use, a **dashboard** for management, a **marketplace/hub** for discovering guardrails, and bundled **TypeScript SDK** for easy integration.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | Next.js 14 (App Router) |
| **Language** | TypeScript (strict) |
| **Database** | PostgreSQL (via Drizzle ORM + postgres.js) |
| **Auth** | Clerk (with custom abstraction layer) |
| **Styling** | Tailwind CSS, shadcn/ui (Radix primitives) |
| **Payments** | Razorpay |
| **Validation** | Zod, AJV (JSON Schema) |
| **SDK Build** | tsup (TypeScript bundler) |
| **Docs** | MDX, rehype-pretty-code, MiniSearch |
| **Animation** | Framer Motion |
| **Testing** | Vitest |
| **Infrastructure** | Docker, Docker Compose |

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────┐
│                   Frontend (Next.js App Router)       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Marketing │  │Dashboard │  │   Docs   │           │
│  │  Pages    │  │  Pages   │  │  (MDX)   │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│         │            │               │               │
│  ┌──────┴────────────┴───────────────┴──────┐        │
│  │         API Routes (Next.js)              │        │
│  │   /api/validate | /api/profiles | ...     │        │
│  └────────────────┬──────────────────────────┘        │
└───────────────────┼───────────────────────────────────┘
                    │
┌───────────────────┼───────────────────────────────────┐
│                   ▼                                   │
│  ┌──────────────────────────────────────────┐         │
│  │         Guardrail Engine (Core)          │         │
│  │  ┌─────────┐ ┌──────────┐ ┌───────────┐  │         │
│  │  │Registry │ │ Executor │ │  Context   │  │         │
│  │  └─────────┘ └──────────┘ └───────────┘  │         │
│  │  ┌──────────────────────────────────┐    │         │
│  │  │ 40+ Guardrail Implementations    │    │         │
│  │  │ Input | Output | Tool | Content  │    │         │
│  │  │ Operational | Security | General │    │         │
│  │  └──────────────────────────────────┘    │         │
│  └──────────────────────────────────────────┘         │
│                    │                                   │
│  ┌─────────────────┴──────────────────────────┐       │
│  │         Profiles Module                    │       │
│  │  Built-in profiles | Compiler | Resolver   │       │
│  └─────────────────┬──────────────────────────┘       │
│                    │                                   │
│  ┌─────────────────┴──────────────────────────┐       │
│  │    Analytics | Auth | Rate Limiting        │       │
│  └─────────────────┬──────────────────────────┘       │
│                    │                                   │
│  ┌─────────────────┴──────────────────────────┐       │
│  │         PostgreSQL (Drizzle ORM)           │       │
│  └────────────────────────────────────────────┘       │
└───────────────────────────────────────────────────────┘
```

## Core Concepts

### 1. Guardrails
Atomic, composable safety checks that inspect text and return a result. Each guardrail extends `BaseGuardrail` and executes against a `GuardrailContext`.

### 2. Stages
Guardrails operate at different stages:
- **input**: Validate user prompts before they reach the LLM (23 guards)
- **output**: Validate model responses before sending to user (13 guards)
- **content**: Content policy checks (defamation, medical advice, violence)
- **tool**: Validate tool/function invocations (5 guards)
- **operational**: Rate limiting, cost control, model pinning, telemetry (4 guards)
- **security**: Key rotation triggers (1 guard)
- **general**: Cross-cutting concerns like retention checks (1 guard)

### 3. Actions
Each guardrail result produces one of four actions:
- **ALLOW**: Content passed all checks
- **WARN**: Content triggered a soft violation (passes but flagged)
- **BLOCK**: Content violated policy (fails)
- **MODIFY**: Content was modified/redacted (passes with changes)

### 4. Profiles
Named collections of guardrail configurations. Users can use built-in profiles (default, enterprise, healthcare, etc.) or create custom ones.

### 5. API Keys
Every request must authenticate via an API key. Keys have per-minute and per-day rate limits.

---

## Directory Structure

```
guardrailz/
├── app/                          # Next.js App Router
│   ├── (marketing)/              # Public marketing pages
│   │   ├── _components/          # Landing page components
│   │   ├── blogs/                # Blog section
│   │   ├── hub/                  # Guardrails hub / marketplace
│   │   ├── pricing/              # Pricing page
│   │   ├── layout.tsx            # Marketing layout
│   │   └── page.tsx              # Landing page (hero)
│   ├── api/                      # API routes
│   │   ├── analytics/            # GET analytics data
│   │   ├── dashboard/stats/      # GET dashboard stats
│   │   ├── guardrails/catalog/   # GET registered guardrails
│   │   ├── keys/                 # CRUD API keys
│   │   ├── payments/            # Razorpay order & verify
│   │   ├── profiles/            # CRUD profiles
│   │   ├── usage/               # GET usage stats
│   │   └── validate/            # POST validate (main endpoint)
│   ├── dashboard/               # Dashboard pages
│   │   ├── analytics/           # Analytics charts
│   │   ├── api-keys/            # API key management
│   │   ├── playground/          # Playground for testing
│   │   ├── profiles/            # Profile management
│   │   └── settings/            # User settings
│   ├── docs/                    # Documentation (MDX)
│   │   ├── _components/         # Custom doc components
│   │   ├── _config/             # Doc navigation & config
│   │   ├── _content/            # MDX content files
│   │   ├── _search/             # Full-text search (MiniSearch)
│   │   └── _utils/              # MDX utils
│   ├── globals.css
│   ├── layout.tsx               # Root layout
│   └── middleware.ts            # Clerk middleware
├── modules/                     # Domain modules (DDD)
│   ├── analytics/               # Analytics CQRS module
│   │   ├── domain/              # Domain models
│   │   ├── events/              # Event types
│   │   ├── ingestion/           # Event ingestion
│   │   ├── mappers/             # Row-to-domain mappers
│   │   ├── queries/             # Query handlers
│   │   ├── repository/          # Data access
│   │   ├── service/             # Business logic
│   │   └── utils/               # Type guards
│   ├── guardrails/              # Core guardrail engine
│   │   ├── contracts/           # Zod validation schemas
│   │   ├── descriptors/         # Normalizer & types
│   │   ├── engine/              # Core engine
│   │   │   ├── base.guardrails.ts
│   │   │   ├── context.ts
│   │   │   ├── errors.ts
│   │   │   ├── executor.ts
│   │   │   ├── registry.ts
│   │   │   └── types.ts
│   │   ├── guards/              # All guard implementations
│   │   │   ├── content/         # 3 guards
│   │   │   ├── general/         # 1 guard
│   │   │   ├── input/           # 17 guards
│   │   │   ├── operational/     # 4 guards
│   │   │   ├── output/          # 10 guards
│   │   │   ├── security/        # 1 guard
│   │   │   └── tool/            # 5 guards
│   │   ├── registry/            # Registry bootstrap files
│   │   ├── service/             # Execution & validation
│   │   └── types/               # Shared types
│   ├── hub/                     # Guardrails hub/catalog
│   │   ├── data/                # Catalog data
│   │   ├── domain/              # Hub domain models
│   │   ├── service/             # Query & stats services
│   │   └── ui/                  # Hub components
│   └── profiles/                # Profiles module
│       ├── builtins/            # 6 built-in profiles
│       ├── compiler/            # Profile compilation
│       ├── domain/              # Domain models
│       ├── repository/          # Data access
│       ├── service/             # Business logic
│       └── types/               # UI types
├── shared/                      # Shared infrastructure
│   ├── auth/                    # Auth abstraction
│   │   ├── domain/              # Auth domain models
│   │   ├── guards/              # require-auth guard
│   │   ├── providers/           # Clerk provider
│   │   └── service/             # Auth + user sync
│   ├── db/                      # Database
│   │   ├── schema/              # Drizzle schema (8 tables)
│   │   ├── client.ts            # DB client
│   │   └── types.ts
│   ├── hooks/                   # React hooks
│   ├── types/                   # Shared types
│   └── ui/                      # Shared UI components (shadcn)
├── sdk/                         # TypeScript SDK
│   ├── core/                    # HTTP client
│   ├── guardrails/              # Validate method
│   └── index.ts                 # Exports
├── lib/                         # Utility libraries
│   ├── api-key.ts               # Key generation
│   ├── rate-limit.ts            # Rate limit service
│   └── utils.js                 # Misc utilities
├── tests/                       # Test suite
│   ├── fixtures/                # Test fixtures
│   ├── guardrails/              # Individual guard tests
│   ├── integration/             # Integration tests
│   └── unit/                    # Unit tests
├── drizzle/                     # Drizzle migrations
├── public/                      # Static assets
├── Dockerfile
├── docker-compose.yml
├── package.json
└── next.config.cjs
```

---

## Data Flow: Request Validation

```
                    ┌──────────────┐
                    │   Client     │
                    │  (SDK/Curl)  │
                    └──────┬───────┘
                           │ POST /api/validate
                           │ x-api-key: grd_live_...
                           │ { text, profileName, validationType }
                           ▼
                    ┌──────────────┐
                    │  middleware  │  Clerk auth check (public route)
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │  validate/   │ Zod schema validation
                    │  route.ts    │
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │ validateReq  │
                    │  uest()      │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │ Auth Key │ │RateLimit │ │ Resolve  │
       │ Check    │ │ Check    │ │ Profile  │
       └──────────┘ └──────────┘ └──────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ runGuardrails│
                    │              │
                    │ 1. Normalize │
                    │    descriptors
                    │ 2. Create    │
                    │    instances │
                    │ 3. Execute   │
                    │    sequentially
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Log to DB   │
                    │  (executions)│
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Response   │
                    │ { passed,    │
                    │   results[], │
                    │   summary }  │
                    └──────────────┘
```
