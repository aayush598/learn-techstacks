# Partner Portal

## Overview

Partner Portal provides the configuration management framework for the 05 Partner Directory Certification chapter. This section covers the design decisions around configuration storage, retrieval, validation, and runtime management.

## Configuration Architecture

The configuration system follows a layered approach with clear precedence:

```
  Higher Priority
       │
       ▼
  ┌──────────────────────┐
  │  Runtime Overrides   │  (Feature flags, emergency settings)
  ├──────────────────────┤
  │  Environment Vars    │  (Secrets, per-deployment config)
  ├──────────────────────┤
  │  Database Config     │  (Dynamic, user-configurable)
  ├──────────────────────┤
  │  Config Files        │  (YAML/JSON in repository)
  ├──────────────────────┤
  │  Default Values      │  (Code-level defaults)
  └──────────────────────┘
  Lower Priority
       │
       ▼
```

## Implementation

```typescript
// Configuration management system
interface ConfigSource {
  name: string;
  priority: number;
  get<T>(key: string): Promise<T | undefined>;
  set<T>(key: string, value: T): Promise<void>;
  watch<T>(key: string, callback: (value: T) => void): () => void;
}

class ConfigManager {
  private sources: ConfigSource[] = [];
  private cache = new Map<string, unknown>();
  private logger: Logger;

  constructor() {
    this.logger = pino({ name: 'config' });
  }

  registerSource(source: ConfigSource): void {
    this.sources.push(source);
    this.sources.sort((a, b) => b.priority - a.priority);
  }

  async get<T>(key: string, defaultValue?: T): Promise<T> {
    // Check cache first
    if (this.cache.has(key)) {
      return this.cache.get(key) as T;
    }

    // Iterate sources in priority order
    for (const source of this.sources) {
      try {
        const value = await source.get<T>(key);
        if (value !== undefined) {
          this.cache.set(key, value);
          return value;
        }
      } catch (err) {
        this.logger.warn({ source: source.name, key, err }, 'Config source failed');
      }
    }

    if (defaultValue !== undefined) {
      return defaultValue;
    }

    throw new ConfigNotFoundError(key);
  }

  async set<T>(key: string, value: T): Promise<void> {
    // Write to database source (highest writable priority)
    const writableSource = this.sources.find(s => s instanceof DatabaseConfigSource);
    if (!writableSource) {
      throw new ConfigError('No writable configuration source available');
    }
    await writableSource.set(key, value);
    this.cache.set(key, value);
  }

  watch<T>(key: string, callback: (value: T) => void): () => void {
    const unsubscribers: Array<() => void> = [];
    for (const source of this.sources) {
      if (source.watch) {
        const unsub = source.watch(key, (value: T) => {
          this.cache.set(key, value);
          callback(value);
        });
        unsubscribers.push(unsub);
      }
    }
    return () => unsubscribers.forEach(fn => fn());
  }

  invalidateCache(key?: string): void {
    if (key) {
      this.cache.delete(key);
    } else {
      this.cache.clear();
    }
  }
}
```

## Configuration Sources

| Source | Priority | Use Case | Update Method |
|--------|----------|----------|---------------|
| Defaults | 0 | Code-level fallbacks | Code deploy |
| Config File | 10 | Static environment config | Git commit |
| Environment | 20 | Secrets, deployment config | Infra deploy |
| Database | 30 | Dynamic user config | API call |
| Feature Flag | 40 | Runtime toggles | Dashboard |
| Runtime Override | 50 | Emergency settings | API call |

## Open Source Tools

- **dotenv**: Environment variable loading
- **convict**: Schema-based configuration
- **node-config**: Hierarchical config with env overrides
- **LaunchDarkly SDK**: Feature flag management
- **Zod**: Configuration schema validation

## Production Considerations

### Configuration Validation

All configuration values are validated at startup:

```typescript
const configSchema = z.object({
  port: z.number().int().min(1024).max(65535).default(3000),
  database: z.object({
    host: z.string(),
    port: z.number().int().default(5432),
    database: z.string(),
    ssl: z.boolean().default(true),
  }),
  redis: z.object({
    host: z.string(),
    port: z.number().int().default(6379),
    password: z.string().optional(),
  }),
  logLevel: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
  rateLimiting: z.object({
    enabled: z.boolean().default(true),
    maxRequests: z.number().int().positive().default(100),
    windowMs: z.number().int().positive().default(60000),
  }).default({}),
});
```

### Secret Management

Secrets are never stored in configuration files or the database. They are injected via environment variables from a secure vault (HashiCorp Vault or AWS Secrets Manager) at deployment time.

### Configuration Auditing

All configuration changes are logged with:
- Timestamp
- Actor (user or system)
- Previous value (masked for secrets)
- New value (masked for secrets)
- Source of change

## Summary

The configuration management framework for Partner Portal provides a flexible, secure, and observable foundation that supports the voice agent platform's deployment across multiple environments while maintaining security and operational excellence.
