# Section 02: Zod Validation Schema

## Overview

Runtime environment variable validation with Zod prevents configuration errors from reaching production. By defining a Zod schema for all environment variables, we ensure that every required variable is present, every value has the correct type, and the application fails fast at startup with actionable error messages.

## The Problem

```typescript
// Without validation — silent failures
const dbUrl = process.env.DATABASE_URL;
// If undefined, Prisma connects to nowhere and throws a cryptic error
// If misspelled as DATABASE_URL_TYPO, application uses a default

const apiKey = process.env.OPENAI_API_KEY;
// If undefined, OpenAI calls fail with "401 Unauthorized"
// Debugging requires checking if the env var is set
```

## Zod Schema Definition

```typescript
// packages/config/src/env-schema.ts
import { z } from "zod";

// ── Nested schema for logical grouping ──────────────────────
const appSchema = z.object({
  NODE_ENV: z
    .enum(["development", "production", "test"])
    .default("development"),
  APP_NAME: z.string().default("Voice Agent Platform"),
  APP_URL: z.string().url(),
  API_URL: z.string().url(),
  LOG_LEVEL: z
    .enum(["debug", "info", "warn", "error", "silent"])
    .default("info"),
});

const databaseSchema = z.object({
  DATABASE_URL: z.string().url(),
  DATABASE_URL_READER: z.string().url().optional(),
});

const redisSchema = z.object({
  REDIS_URL: z.string().url(),
  REDIS_PREFIX: z.string().default("va:"),
});

const kafkaSchema = z.object({
  KAFKA_BROKERS: z.string(),
  KAFKA_CLIENT_ID: z.string(),
  KAFKA_GROUP_ID: z.string(),
});

const storageSchema = z.object({
  MINIO_ENDPOINT: z.string(),
  MINIO_PORT: z.string().regex(/^\d+$/),
  MINIO_ACCESS_KEY: z.string().min(1),
  MINIO_SECRET_KEY: z.string().min(8),
  MINIO_BUCKET_RECORDINGS: z.string().default("recordings"),
  MINIO_BUCKET_TRANSCRIPTS: z.string().default("transcripts"),
  MINIO_USE_SSL: z
    .string()
    .transform((v) => v === "true")
    .default("false"),
});

const voiceSchema = z.object({
  ELEVENLABS_API_KEY: z.string().min(1),
  DEEPGRAM_API_KEY: z.string().min(1),
  CARTESIA_API_KEY: z.string().min(1),
});

const llmSchema = z.object({
  OPENAI_API_KEY: z.string().min(1),
  ANTHROPIC_API_KEY: z.string().min(1),
});

const authSchema = z.object({
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRES_IN: z.string().default("7d"),
  AUTH_REDIRECT_URL: z.string().url(),
});

const monitoringSchema = z.object({
  SENTRY_DSN: z.string().url().optional(),
  SENTRY_ENVIRONMENT: z
    .enum(["development", "staging", "production"])
    .default("development"),
  OTEL_EXPORTER_OTLP_ENDPOINT: z.string().url().optional(),
});

const featureFlagsSchema = z.object({
  FEATURE_VOICE_ANALYTICS: z
    .string()
    .transform((v) => v === "true")
    .default("true"),
  FEATURE_HUMAN_HANDOFF: z
    .string()
    .transform((v) => v === "true")
    .default("true"),
  FEATURE_CAMPAIGNS: z
    .string()
    .transform((v) => v === "true")
    .default("false"),
});

// ── Combined schema ─────────────────────────────────────────
export const envSchema = z.object({
  ...appSchema.shape,
  ...databaseSchema.shape,
  ...redisSchema.shape,
  ...kafkaSchema.shape,
  ...storageSchema.shape,
  ...voiceSchema.shape,
  ...llmSchema.shape,
  ...authSchema.shape,
  ...monitoringSchema.shape,
  ...featureFlagsSchema.shape,
});

export type Env = z.infer<typeof envSchema>;
```

## Validation at Startup

```typescript
// packages/config/src/env-validator.ts
import { envSchema, type Env } from "./env-schema";
import { loadEnv } from "./env";

// Singleton validated environment
let validatedEnv: Env | null = null;

export function validateEnv(): Env {
  if (validatedEnv) {
    return validatedEnv;
  }

  loadEnv();

  const result = envSchema.safeParse(process.env);

  if (!result.success) {
    const errors = result.error.flatten();
    const errorMessages = [
      "Environment variable validation failed:",
      "",
      ...errors.fieldErrors.flatMap(([key, messages]) =>
        messages.map((msg) => `  ❌ ${key}: ${msg}`)
      ),
      ...(errors.formErrors?.length
        ? ["", "Form-level errors:", ...errors.formErrors.map((e) => `  ❌ ${e}`)]
        : []),
      "",
      "Fix these environment variables before starting the application.",
      "See .env.example for the required variables.",
    ];

    console.error(errorMessages.join("\n"));
    process.exit(1);
  }

  validatedEnv = result.data;
  return validatedEnv;
}

// Convenience accessor
export function env(): Env {
  if (!validatedEnv) {
    throw new Error(
      "Environment not validated. Call validateEnv() at application startup."
    );
  }
  return validatedEnv;
}
```

## Application Startup Integration

```typescript
// packages/config/src/index.ts
export { validateEnv, env } from "./env-validator";
export type { Env } from "./env-schema";
```

### Next.js API Route Validation

```typescript
// apps/api/src/app/api/route.ts
// or apps/web/src/app/layout.tsx — validate at module scope

import { validateEnv } from "@voice-agent/config";

// Validate immediately when the module loads
const env = validateEnv();

// In Next.js API routes:
export async function GET() {
  // env is already validated and cached
  return Response.json({
    app: env.APP_NAME,
    features: {
      analytics: env.FEATURE_VOICE_ANALYTICS,
      handoff: env.FEATURE_HUMAN_HANDOFF,
    },
  });
}
```

### Standalone Server Validation

```typescript
// apps/api/src/index.ts (if using standalone server)
import { validateEnv } from "@voice-agent/config";

function main() {
  // Validate environment before doing anything else
  const env = validateEnv();

  // Now safe to use env variables
  const app = createApp({
    database: { url: env.DATABASE_URL },
    redis: { url: env.REDIS_URL },
    kafka: { brokers: env.KAFKA_BROKERS },
  });

  app.listen(4000, () => {
    console.log(`API server running on port 4000 (${env.NODE_ENV})`);
  });
}

main();
```

## Type Generation from Schema

One of Zod's most powerful features — the inferred type is always in sync with the schema:

```typescript
import { z } from "zod";

export const envSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url(),
  OPENAI_API_KEY: z.string().min(1),
});

// Generated type — automatically updates when schema changes
export type Env = z.infer<typeof envSchema>;

// Usage — full type safety
function connectDatabase(env: Env) {
  // env.DATABASE_URL is string
  // env.NODE_ENV is "development" | "production" | "test"
  // env.OPENAI_API_KEY is string (non-empty)
}
```

## Testing Validation

```typescript
// packages/config/src/env-schema.test.ts
import { describe, it, expect } from "vitest";
import { envSchema } from "./env-schema";

describe("envSchema", () => {
  const validEnv = {
    NODE_ENV: "development",
    APP_URL: "http://localhost:3000",
    API_URL: "http://localhost:4000",
    DATABASE_URL: "postgresql://localhost:5432/test",
    REDIS_URL: "redis://localhost:6379",
    KAFKA_BROKERS: "localhost:9092",
    MINIO_ENDPOINT: "localhost",
    MINIO_PORT: "9000",
    MINIO_ACCESS_KEY: "minioadmin",
    MINIO_SECRET_KEY: "minioadmin123",
    ELEVENLABS_API_KEY: "test-key",
    DEEPGRAM_API_KEY: "test-key",
    CARTESIA_API_KEY: "test-key",
    OPENAI_API_KEY: "test-key",
    ANTHROPIC_API_KEY: "test-key",
    JWT_SECRET: "a".repeat(32),
    AUTH_REDIRECT_URL: "http://localhost:3000/auth/callback",
  };

  it("validates a correct environment", () => {
    const result = envSchema.safeParse(validEnv);
    expect(result.success).toBe(true);
  });

  it("fails when DATABASE_URL is missing", () => {
    const { DATABASE_URL, ...withoutDb } = validEnv;
    const result = envSchema.safeParse(withoutDb);
    expect(result.success).toBe(false);
  });

  it("fails when JWT_SECRET is too short", () => {
    const result = envSchema.safeParse({
      ...validEnv,
      JWT_SECRET: "short",
    });
    expect(result.success).toBe(false);
  });

  it("applies defaults for optional fields", () => {
    const result = envSchema.safeParse(validEnv);
    expect(result.success).toBe(true);
    if (result.success) {
      expect(result.data.LOG_LEVEL).toBe("info");
      expect(result.data.FEATURE_VOICE_ANALYTICS).toBe(true);
      expect(result.data.FEATURE_CAMPAIGNS).toBe(false);
    }
  });
});
```

## Error Formatting for Different Environments

```typescript
// packages/config/src/format-errors.ts
import type { ZodError } from "zod";

export function formatEnvErrors(error: ZodError): string[] {
  const issues = error.issues;
  const messages: string[] = [];

  for (const issue of issues) {
    const path = issue.path.join(".");
    switch (issue.code) {
      case "invalid_type":
        messages.push(
          `${path}: expected ${issue.expected}, received ${issue.received}`
        );
        break;
      case "too_small":
        messages.push(
          `${path}: minimum length is ${issue.minimum}`
        );
        break;
      case "invalid_enum_value":
        messages.push(
          `${path}: must be one of ${issue.options.join(", ")}`
        );
        break;
      default:
        messages.push(`${path}: ${issue.message}`);
    }
  }

  return messages;
}
```

## Design Decisions

### Why Zod over plain TypeScript types?

TypeScript types are compile-time only. Environment variables are inherently runtime values — they can be undefined, null, or the wrong type at runtime. Zod provides runtime validation with:
- **Type coercion**: `z.string().url()` validates the URL format
- **Default values**: `z.string().default("development")`
- **Transformations**: `z.string().transform(v => v === "true")` for boolean env vars
- **Detailed error messages**: Which fields failed and why

### Why validate at startup (eager) vs. on first use (lazy)?

Eager validation (at startup) catches configuration errors immediately with a clear message. Lazy validation would cause errors in production hours after deployment when the first request uses the invalid variable.

## Integration Points

- **packages/config**: Centralized env validation shared by all apps
- **apps/web**: Validates environment during build and at server startup
- **apps/api**: Validates environment at server startup
- **CI/CD**: Env validation runs as part of the build step

## Production Considerations

1. **Secrets in error messages**: Never log actual environment variable values in error messages. Show only the variable name and validation error
2. **Validation caching**: The singleton pattern ensures validation runs once. In serverless environments (Vercel Edge, Lambda), validation must be fast since it runs on every cold start
3. **CI validation**: Add a CI step that validates the environment schema matches the actual environment: `node -e "require('@voice-agent/config').validateEnv()"`
4. **Schema versioning**: When adding required env vars, update the schema and communicate the change to all developers. CI should fail if the schema rejects the current environment
5. **Documentation generation**: The Zod schema can generate markdown documentation automatically: `zod-to-json-schema` or custom script that prints all expected variables with descriptions
