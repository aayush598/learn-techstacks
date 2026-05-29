# Section 05: Environment-Specific Configuration

## Overview

Different environments — development, staging, production — require different configurations for feature flags, API endpoints, logging levels, and service connections. This section covers how to manage environment-specific configuration without duplicating code.

## Environment Configuration Matrix

```text
┌─────────────────────────────────────────────────────────────┐
│              Environment Configuration Matrix                 │
│                                                              │
│  Setting            Dev         Staging       Production     │
│  ─────────────────────────────────────────────────────       │
│  Log Level          debug       info          info           │
│  DB Connection       local       staging-     production-    │
│                      Docker      RDS          RDS            │
│  Redis              local       ElastiCache  ElastiCache    │
│  MinIO/S3           local       staging-     production-    │
│                      MinIO       S3           S3             │
│  Kafka              local MSK   staging MSK  production MSK │
│  Voice Provider     mock        sandbox      production     │
│  LLM Provider       mock        production   production     │
│  Feature Voice Ana  true        true         true           │
│  Feature Handoff    false       true         true           │
│  Feature Campaigns  false       true         true           │
│  Sentry             disabled    errors       errors+traces  │
│  JWT Expiry         7d          1h           1h             │
│  Rate Limiting      disabled    enabled      enabled        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Configuration Loading Strategy

```typescript
// packages/config/src/environment.ts
import { z } from "zod";
import { env } from "./env-validator";

export type Environment = "development" | "staging" | "production";

export interface EnvironmentConfig {
  // API endpoints
  api: {
    baseUrl: string;
    websocketUrl: string;
  };

  // External service URLs
  services: {
    database: DatabaseConfig;
    redis: RedisConfig;
    kafka: KafkaConfig;
    storage: StorageConfig;
  };

  // Provider selection
  providers: {
    stt: string;         // deepgram | assemblyai | mock
    tts: string;         // elevenlabs | cartesia | mock
    llm: string;         // openai | anthropic | mock
    vad: string;         // silero | mock
  };

  // Feature flags
  features: {
    voiceAnalytics: boolean;
    humanHandoff: boolean;
    campaigns: boolean;
    realtimeTranscription: boolean;
    callRecording: boolean;
  };

  // Operational settings
  operations: {
    logLevel: "debug" | "info" | "warn" | "error" | "silent";
    rateLimiting: boolean;
    requestLogging: boolean;
    requestTimeout: number;
    maxCallDuration: number;
  };

  // Monitoring
  monitoring: {
    sentryEnabled: boolean;
    sentryTracesSampleRate: number;
    metricsEnabled: boolean;
    tracingEnabled: boolean;
  };

  // Auth
  auth: {
    jwtExpiry: string;
    sessionTimeout: number;
    maxLoginAttempts: number;
    mfaRequired: boolean;
  };
}
```

## Environment-Specific Files

```typescript
// packages/config/src/environments/development.ts
import type { EnvironmentConfig } from "../environment";

export const developmentConfig: EnvironmentConfig = {
  api: {
    baseUrl: "http://localhost:3000",
    websocketUrl: "ws://localhost:4000/ws",
  },
  services: {
    database: {
      host: "localhost",
      port: 5432,
      name: "voice_agent_dev",
      poolMin: 2,
      poolMax: 10,
    },
    redis: {
      host: "localhost",
      port: 6379,
    },
    kafka: {
      brokers: ["localhost:9092"],
    },
    storage: {
      endpoint: "http://localhost:9000",
      region: "us-east-1",
      useSSL: false,
    },
  },
  providers: {
    stt: "mock",
    tts: "mock",
    llm: "mock",
    vad: "silero",
  },
  features: {
    voiceAnalytics: true,
    humanHandoff: false,
    campaigns: false,
    realtimeTranscription: true,
    callRecording: true,
  },
  operations: {
    logLevel: "debug",
    rateLimiting: false,
    requestLogging: true,
    requestTimeout: 30000,
    maxCallDuration: 600,
  },
  monitoring: {
    sentryEnabled: false,
    sentryTracesSampleRate: 0,
    metricsEnabled: false,
    tracingEnabled: false,
  },
  auth: {
    jwtExpiry: "7d",
    sessionTimeout: 604800,
    maxLoginAttempts: 10,
    mfaRequired: false,
  },
};
```

```typescript
// packages/config/src/environments/production.ts
import type { EnvironmentConfig } from "../environment";

export const productionConfig: EnvironmentConfig = {
  api: {
    baseUrl: "https://app.voiceagent.example.com",
    websocketUrl: "wss://api.voiceagent.example.com/ws",
  },
  services: {
    database: {
      host: process.env.DB_HOST!,
      port: parseInt(process.env.DB_PORT ?? "5432"),
      name: "voice_agent_prod",
      poolMin: 5,
      poolMax: 50,
    },
    redis: {
      host: process.env.REDIS_HOST!,
      port: parseInt(process.env.REDIS_PORT ?? "6379"),
      password: process.env.REDIS_PASSWORD,
    },
    kafka: {
      brokers: (process.env.KAFKA_BROKERS ?? "").split(","),
    },
    storage: {
      endpoint: `https://${process.env.S3_ENDPOINT}`,
      region: process.env.S3_REGION ?? "us-east-1",
      useSSL: true,
    },
  },
  providers: {
    stt: "deepgram",
    tts: "elevenlabs",
    llm: "openai",
    vad: "silero",
  },
  features: {
    voiceAnalytics: true,
    humanHandoff: true,
    campaigns: true,
    realtimeTranscription: true,
    callRecording: true,
  },
  operations: {
    logLevel: "info",
    rateLimiting: true,
    requestLogging: true,
    requestTimeout: 10000,
    maxCallDuration: 14400,
  },
  monitoring: {
    sentryEnabled: true,
    sentryTracesSampleRate: 0.1,
    metricsEnabled: true,
    tracingEnabled: true,
  },
  auth: {
    jwtExpiry: "1h",
    sessionTimeout: 3600,
    maxLoginAttempts: 5,
    mfaRequired: true,
  },
};
```

## Feature Flags via Environment

```typescript
// packages/config/src/features.ts
import { env } from "./env-validator";

export interface FeatureFlag {
  key: string;
  description: string;
  defaultValue: boolean;
  environments: ("development" | "staging" | "production")[];
}

export const featureFlags: Record<string, FeatureFlag> = {
  VOICE_ANALYTICS: {
    key: "FEATURE_VOICE_ANALYTICS",
    description: "Enable voice analytics dashboard",
    defaultValue: true,
    environments: ["development", "staging", "production"],
  },
  HUMAN_HANDOFF: {
    key: "FEATURE_HUMAN_HANDOFF",
    description: "Enable human agent handoff",
    defaultValue: true,
    environments: ["staging", "production"],
  },
  CAMPAIGNS: {
    key: "FEATURE_CAMPAIGNS",
    description: "Enable outbound campaign management",
    defaultValue: false,
    environments: ["staging", "production"],
  },
  REALTIME_TRANSCRIPTION: {
    key: "FEATURE_REALTIME_TRANSCRIPTION",
    description: "Enable real-time transcription during calls",
    defaultValue: true,
    environments: ["development", "staging", "production"],
  },
};

export function isFeatureEnabled(featureKey: string): boolean {
  const flag = featureFlags[featureKey];
  if (!flag) return false;

  const envValue = process.env[flag.key];
  if (envValue !== undefined) {
    return envValue === "true";
  }

  return flag.defaultValue;
}
```

## Provider Selection Strategy

```typescript
// packages/config/src/providers.ts
import { env } from "./env-validator";

export type STTProvider = "deepgram" | "assemblyai" | "mock";
export type TTSProvider = "elevenlabs" | "cartesia" | "mock";
export type LLMProvider = "openai" | "anthropic" | "mock";
export type VADProvider = "silero" | "mock";

interface ProviderSelection {
  stt: STTProvider;
  tts: TTSProvider;
  llm: LLMProvider;
  vad: VADProvider;
}

export function getProviders(): ProviderSelection {
  if (env().NODE_ENV === "development") {
    return {
      stt: "mock",
      tts: "mock",
      llm: "mock",
      vad: "silero",
    };
  }

  return {
    stt: "deepgram",
    tts: "elevenlabs",
    llm: env().NODE_ENV === "staging" ? "openai" : "openai",
    vad: "silero",
  };
}
```

## Logging Configuration

```typescript
// packages/config/src/logging.ts
import { env } from "./env-validator";
import type { EnvironmentConfig } from "./environment";

export function getLoggingConfig() {
  const isProduction = env().NODE_ENV === "production";

  return {
    level: env().LOG_LEVEL ?? (isProduction ? "info" : "debug"),
    format: isProduction ? "json" : "pretty",
    output: isProduction ? "stdout" : "console",
    redact: isProduction
      ? ["req.headers.authorization", "req.body.apiKey", "DATABASE_URL"]
      : [],
    // Development-specific
    ...(env().NODE_ENV === "development" && {
      prettyPrint: {
        colorize: true,
        translateTime: "SYS:yyyy-mm-dd HH:MM:ss",
        ignore: "pid,hostname",
      },
    }),
  };
}
```

## Rate Limiting Configuration

```typescript
// packages/config/src/rate-limiting.ts
import { env } from "./env-validator";

interface RateLimitConfig {
  enabled: boolean;
  windowMs: number;
  maxRequests: number;
  standardHeaders: boolean;
  legacyHeaders: boolean;
  skip?: (req: Request) => boolean;
}

export function getRateLimitConfig(): RateLimitConfig {
  const isProduction = env().NODE_ENV === "production";

  return {
    // Disabled in development for easier testing
    enabled: isProduction || env().NODE_ENV === "staging",

    // 1-minute window
    windowMs: 60 * 1000,

    // Requests per window
    maxRequests: isProduction ? 100 : 1000,

    // Return RateLimit-* headers
    standardHeaders: true,
    legacyHeaders: false,

    // Skip health check endpoints
    skip: (req) => req.url?.startsWith("/api/health") ?? false,
  };
}
```

## Design Decisions

### Static config objects vs. database-driven config

**Decision**: Use static TypeScript configuration objects per environment.

**Rationale**: Environment-specific configuration rarely changes at runtime. Static objects are type-safe, testable, and have zero runtime overhead. For runtime-configurable values (feature flags), use feature flag service like LaunchDarkly or a database-backed configuration store.

### Feature flags in env vars vs. dedicated service

**Decision**: Use environment variables for simple on/off flags that change between environments. Use a dedicated feature flag service for per-tenant or runtime toggles.

**Rationale**: Environment variables are simple and require no additional infrastructure. For per-organization feature flags (e.g., enabling beta features for specific customers), a dedicated service provides granular control without requiring redeployment.

## Integration Points

- **Next.js**: `publicRuntimeConfig` and server-side env vars
- **API routes**: Environment config injected via request context
- **Feature checks**: `isFeatureEnabled()` used throughout the codebase
- **Provider selection**: `getProviders()` used by voice processing pipeline
- **Logging**: `getLoggingConfig()` configures the logger at startup

## Production Considerations

1. **Config validation**: Validate environment-specific config at startup with Zod. Catch misconfigured environments before they serve traffic
2. **Config as code**: Keep environment config in version control. Changes go through code review like any other code change
3. **Drift detection**: Periodically compare staging and production configs to detect unintended differences. Use `doppler secrets diff` or custom scripts
4. **Least privilege**: Production API keys should only be accessible to the production environment. Use environment protection rules in CI/CD
5. **Documentation**: Auto-generate environment documentation from the config schema. Developers should be able to see what variables an environment needs
