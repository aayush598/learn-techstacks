# Section 01: Environment Variable Strategy

## Overview

A robust environment variable strategy ensures that the voice agent platform runs correctly across development, testing, staging, and production environments. This section covers the `.env` file hierarchy, precedence rules, variable scoping, and best practices for managing configuration through environment variables.

## Environment Variable Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              Environment Variable Precedence                  │
│                                                              │
│  Higher Priority                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. Runtime environment (shell export)                  │  │
│  │    export DATABASE_URL="..."                           │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ 2. .env.local (local overrides, gitignored)            │  │
│  │    # Machine-specific, secrets                         │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ 3. .env.development / .env.production (per env)        │  │
│  │    # Environment-specific defaults                     │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ 4. .env (shared defaults, committed)                   │  │
│  │    # Safe defaults for all environments                │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ 5. .env.*.local (lowest priority, gitignored)          │  │
│  └───────────────────────────────────────────────────────┘  │
│  Lower Priority                                             │
└─────────────────────────────────────────────────────────────┘
```

## File Hierarchy

```text
voice-agent-platform/
├── .env                        # Committed — safe defaults
├── .env.local                  # Gitignored — local overrides
├── .env.development            # Committed — dev defaults
├── .env.production             # Committed — prod defaults
├── .env.test                   # Committed — test defaults
├── .env.development.local      # Gitignored — local dev overrides
├── .env.production.local       # Gitignored — local prod overrides
└── apps/
    ├── web/
    │   ├── .env                # Web-specific env vars
    │   └── .env.local
    └── api/
        ├── .env                # API-specific env vars
        └── .env.local
```

### .gitignore Rules

```gitignore
# .gitignore
.env.local
.env.*.local
*.env.local

# Keep .env (shared defaults)
# Keep .env.development, .env.production, .env.test
```

## File Contents

### .env (Shared Defaults)

```bash
# .env — Safe defaults for all environments
# These values are safe to commit (no secrets)

# App
APP_NAME=Voice Agent Platform
APP_URL=http://localhost:3000
API_URL=http://localhost:4000
NODE_ENV=development

# Logging
LOG_LEVEL=debug

# Feature Flags
FEATURE_VOICE_ANALYTICS=true
FEATURE_HUMAN_HANDOFF=true
FEATURE_CAMPAIGNS=false
```

### .env.development

```bash
# .env.development — Development environment defaults

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/voice_agent_dev
DATABASE_URL_READER=postgresql://postgres:postgres@localhost:5432/voice_agent_dev

# Redis
REDIS_URL=redis://localhost:6379
REDIS_PREFIX=dev:

# Kafka
KAFKA_BROKERS=localhost:9092
KAFKA_CLIENT_ID=voice-agent-dev
KAFKA_GROUP_ID=voice-agent-dev-group

# Storage (MinIO)
MINIO_ENDPOINT=localhost
MINIO_PORT=9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_RECORDINGS=dev-recordings
MINIO_BUCKET_TRANSCRIPTS=dev-transcripts
MINIO_USE_SSL=false

# Voice Providers (mock in development)
ELEVENLABS_API_KEY=mock-key
DEEPGRAM_API_KEY=mock-key
CARTESIA_API_KEY=mock-key

# LLM Providers (mock in development)
OPENAI_API_KEY=mock-key
ANTHROPIC_API_KEY=mock-key

# Auth
JWT_SECRET=dev-jwt-secret-not-for-production
JWT_EXPIRES_IN=7d
AUTH_REDIRECT_URL=http://localhost:3000/auth/callback

# Monitoring
SENTRY_DSN=
SENTRY_ENVIRONMENT=development
```

### .env.production

```bash
# .env.production — Production environment defaults
# Secret values are injected via CI/CD or Vault, not committed

# Database
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:5432/voice_agent_prod
DATABASE_URL_READER=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_READER_HOST}:5432/voice_agent_prod

# Redis
REDIS_URL=redis://:${REDIS_PASSWORD}@${REDIS_HOST}:6379
REDIS_PREFIX=prod:

# Kafka
KAFKA_BROKERS=${KAFKA_BROKER1}:9092,${KAFKA_BROKER2}:9092
KAFKA_CLIENT_ID=voice-agent-prod
KAFKA_GROUP_ID=voice-agent-prod-group

# Storage (S3-compatible)
MINIO_ENDPOINT=${S3_ENDPOINT}
MINIO_PORT=443
MINIO_ACCESS_KEY=${S3_ACCESS_KEY}
MINIO_SECRET_KEY=${S3_SECRET_KEY}
MINIO_BUCKET_RECORDINGS=prod-recordings
MINIO_BUCKET_TRANSCRIPTS=prod-transcripts
MINIO_USE_SSL=true

# Logging
LOG_LEVEL=info

# Auth
JWT_EXPIRES_IN=1h
AUTH_REDIRECT_URL=https://app.voiceagent.example.com/auth/callback

# Monitoring
SENTRY_ENVIRONMENT=production
```

### .env.test

```bash
# .env.test — Test environment defaults

# Database (Testcontainers overrides this)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/voice_agent_test

# Redis
REDIS_URL=redis://localhost:6379

# Disable external services in tests
ELEVENLABS_API_KEY=test-key
DEEPGRAM_API_KEY=test-key
OPENAI_API_KEY=test-key

# Feature flags for testing
FEATURE_VOICE_ANALYTICS=true
FEATURE_HUMAN_HANDOFF=true

# Logging
LOG_LEVEL=silent

# Monitoring — disabled in tests
SENTRY_DSN=
```

## Variable Scoping

### Application-Level vs. Package-Level

```typescript
// apps/web/next.config.js
const nextConfig = {
  // Environment variables exposed to the browser
  env: {
    NEXT_PUBLIC_APP_URL: process.env.APP_URL,
    NEXT_PUBLIC_API_URL: process.env.API_URL,
    NEXT_PUBLIC_SENTRY_DSN: process.env.SENTRY_DSN,
  },
};
```

**NEXT_PUBLIC_ convention**: Variables prefixed with `NEXT_PUBLIC_` are inlined into the client-side JavaScript bundle at build time. Never put secrets in `NEXT_PUBLIC_` variables.

## Loading Strategy

```typescript
// packages/config/src/env.ts
import { config } from "dotenv";
import { expand } from "dotenv-expand";
import { resolve } from "path";

const ENV_FILE_ORDER = [
  ".env",
  ".env.local",
  `.env.${process.env.NODE_ENV}`,
  `.env.${process.env.NODE_ENV}.local`,
];

export function loadEnv(): void {
  for (const file of ENV_FILE_ORDER) {
    const filePath = resolve(process.cwd(), file);
    const result = config({ path: filePath, override: true });
    if (result.error) continue; // File doesn't exist
    expand(result); // Expand ${VAR} references
  }
}
```

## Next.js Built-in Loading

Next.js automatically loads `.env` files in the correct order. No additional configuration needed:

```bash
# Next.js loads in this order:
# 1. .env.local (always, gitignored)
# 2. .env.development or .env.production (depending on NODE_ENV)
# 3. .env (shared defaults)
```

## Design Decisions

### Why commit .env files?

Committed `.env` files serve as documentation and provide safe defaults that make the project runnable immediately after checkout. Only `.env.local` and `.*.env.local` files are gitignored for secrets.

### Why not a single .env file?

Multiple files with clear precedence allow separation of concerns:
- **Shared defaults** (`.env`): Safe, committed
- **Environment-specific** (`.env.development`): Service URLs, ports
- **Local overrides** (`.env.local`): API keys, secrets, machine-specific config
- **CI overrides** (injected via CI variables): Production secrets

### Variable expansion

Using `dotenv-expand`, we can reference variables within `.env` files:
```bash
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@localhost:5432/voice_agent
```
This prevents duplication and makes environment-specific files more maintainable.

## Integration Points

- **Next.js**: Auto-loads `.env` files in correct order
- **Docker Compose**: Uses `env_file` directive to load `.env` files
- **CI/CD**: Injects environment-specific values via GitHub Actions secrets
- **Prisma**: Reads `DATABASE_URL` from environment
- **Zod validation**: Validates all env vars at startup (see Section 02)

## Production Considerations

1. **Secret scanning**: Use `git-secrets` or `talisman` pre-commit hooks to prevent accidentally committing secrets
2. **Environment audit**: Log which environment file was loaded (without logging values) during startup for debugging
3. **Build-time vs. runtime**: `NEXT_PUBLIC_*` vars are baked at build time — they require a rebuild to change. All other vars are read at runtime
4. **Validation failures**: If required env vars are missing, fail fast at startup with a clear error message listing the missing variables
5. **Rotation readiness**: Design the env var loading to support hot-reload of secrets (see Section 03 on rotation)
