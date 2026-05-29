# Section 03: Redis Configuration

## Overview

Redis serves multiple roles in the voice agent platform: caching layer, session store, rate limiter, pub/sub message bus, and real-time state management for active calls. Using Redis Stack enables RedisJSON, RediSearch, and RedisTimeSeries modules for advanced capabilities.

## Redis Stack Features

```text
┌─────────────────────────────────────────────────────────────┐
│              Redis Usage in Voice Agent Platform              │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Cache Layer                                           │   │
│  │  - Agent configuration (JSON)                        │   │
│  │  - LLM response cache (reduced latency)              │   │
│  │  - Provider API key lookups                          │   │
│  │  - Organization settings                             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Session Store                                        │   │
│  │  - Active call sessions (callId → state)             │   │
│  │  - WebSocket connections (userId → socketId)         │   │
│  │  - Authentication tokens (JWT blacklist)             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Rate Limiting                                        │   │
│  │  - API rate limits per organization                  │   │
│  │  - Call rate limits (max concurrent calls)           │   │
│  │  - Provider API rate limits                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Pub/Sub Messaging                                    │   │
│  │  - Real-time call events (via channels)              │   │
│  │  - Agent command publishing                          │   │
│  │  - Transcription streaming                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Time Series                                          │   │
│  │  - Call metrics (duration, latency, cost)            │   │
│  │  - Real-time dashboard data                           │   │
│  │  - Voice quality metrics (MOS scores)                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Container Configuration

```yaml
# docker/docker-compose.yml (Redis service)
services:
  redis:
    image: redis/redis-stack-server:7.2.0
    container_name: voice-agent-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
      - ./redis/redis.conf:/redis.conf
    command: ["redis-server", "/redis.conf"]
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - voice-agent-dev
```

## Redis Configuration

```conf
# docker/redis/redis.conf
# Redis configuration for development

# Memory management
maxmemory 512mb
maxmemory-policy allkeys-lru
maxmemory-samples 10

# Persistence
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /data

# Append-only file for crash recovery
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Network
bind 0.0.0.0
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300

# Security
requirepass ""  # No password in development

# Performance
hz 10
dynamic-hz yes
lfu-log-factor 10
lfu-decay-time 1

# Advanced
activerehashing yes
client-output-buffer-limit normal 0 0 0
client-output-buffer-limit replica 256mb 64mb 60
client-output-buffer-limit pubsub 32mb 8mb 60
```

## Redis Connection

```typescript
// packages/voice/src/cache/redis-client.ts
import Redis from "ioredis";

const globalForRedis = globalThis as unknown as {
  redis: Redis | undefined;
};

function createRedisClient(): Redis {
  const url = process.env.REDIS_URL ?? "redis://localhost:6379";

  const client = new Redis(url, {
    maxRetriesPerRequest: 3,
    retryStrategy(times) {
      if (times > 10) return null; // Give up
      return Math.min(times * 100, 3000); // Exponential backoff
    },
    enableReadyCheck: true,
    lazyConnect: false,
    // Key prefix for multi-tenant isolation
    keyPrefix: process.env.REDIS_PREFIX ?? "va:",
  });

  client.on("error", (err) => {
    console.error("Redis connection error:", err);
  });

  client.on("connect", () => {
    console.log("Connected to Redis");
  });

  return client;
}

export const redis = globalForRedis.redis ?? createRedisClient();

if (process.env.NODE_ENV !== "production") {
  globalForRedis.redis = redis;
}
```

## Key Naming Convention

```typescript
// packages/voice/src/cache/redis-keys.ts
export const KEYS = {
  // Session: TTL = call duration + buffer
  session: (callId: string) => ({
    key: `session:${callId}`,
    ttl: 14400, // 4 hours
  }),

  // Agent config: TTL = 5 minutes, invalidate on update
  agentConfig: (agentId: string) => ({
    key: `config:agent:${agentId}`,
    ttl: 300,
  }),

  // LLM cache: TTL = 1 hour
  llmCache: (promptHash: string) => ({
    key: `cache:llm:${promptHash}`,
    ttl: 3600,
  }),

  // Rate limit: sliding window
  rateLimit: (orgId: string, endpoint: string) => ({
    key: `ratelimit:${orgId}:${endpoint}`,
    ttl: 60,
  }),

  // Call rate limit
  callRateLimit: (orgId: string) => ({
    key: `ratelimit:calls:${orgId}`,
    ttl: 1, // 1 second window
  }),

  // Lock: auto-release after 30 seconds
  callLock: (callId: string) => ({
    key: `lock:call:${callId}`,
    ttl: 30,
  }),

  // Pub/Sub channels
  PUBSUB: {
    CALL_EVENTS: "pubsub:call-events",
    AGENT_COMMANDS: "pubsub:agent-commands",
    TRANSCRIPTION: "pubsub:transcription",
  },
} as const;
```

## Usage Patterns

### Caching Agent Configuration

```typescript
// packages/voice/src/cache/agent-cache.ts
import { redis } from "./redis-client";
import { KEYS } from "./redis-keys";

export class AgentConfigCache {
  async getAgentConfig(agentId: string): Promise<AgentConfig | null> {
    const { key, ttl } = KEYS.agentConfig(agentId);

    // Try cache first
    const cached = await redis.get(key);
    if (cached) {
      return JSON.parse(cached);
    }

    // Fetch from database
    const config = await fetchAgentFromDB(agentId);
    if (!config) return null;

    // Cache for next time
    await redis.setex(key, ttl, JSON.stringify(config));
    return config;
  }

  async invalidateAgentConfig(agentId: string): Promise<void> {
    await redis.del(KEYS.agentConfig(agentId).key);
  }
}
```

### Rate Limiting

```typescript
// packages/voice/src/middleware/rate-limit.ts
import { redis } from "../cache/redis-client";
import { KEYS } from "../cache/redis-keys";

export class RateLimiter {
  async checkRateLimit(
    orgId: string,
    endpoint: string,
    maxRequests: number,
    windowMs: number = 60,
  ): Promise<{ allowed: boolean; remaining: number; resetAt: number }> {
    const { key } = KEYS.rateLimit(orgId, endpoint);
    const now = Date.now();
    const window = Math.floor(now / (windowMs * 1000));

    // Use a sorted set for sliding window
    const windowKey = `${key}:${window}`;
    const count = await redis.incr(windowKey);

    if (count === 1) {
      await redis.expire(windowKey, windowMs + 1);
    }

    return {
      allowed: count <= maxRequests,
      remaining: Math.max(0, maxRequests - count),
      resetAt: (window + 1) * windowMs * 1000,
    };
  }
}
```

### Pub/Sub for Real-Time Events

```typescript
// packages/voice/src/cache/pubsub.ts
import { redis } from "./redis-client";
import { KEYS } from "./redis-keys";

export class CallEventBus {
  private subscriber: Redis;

  constructor() {
    this.subscriber = redis.duplicate();
  }

  async publish(event: CallEvent): Promise<void> {
    const channel = KEYS.PUBSUB.CALL_EVENTS;
    await redis.publish(channel, JSON.stringify(event));
  }

  async subscribe(handler: (event: CallEvent) => void): Promise<void> {
    const channel = KEYS.PUBSUB.CALL_EVENTS;
    await this.subscriber.subscribe(channel);
    this.subscriber.on("message", (_ch, message) => {
      try {
        const event = JSON.parse(message) as CallEvent;
        handler(event);
      } catch (err) {
        console.error("Failed to parse pub/sub message:", err);
      }
    });
  }

  async unsubscribe(): Promise<void> {
    await this.subscriber.unsubscribe();
    this.subscriber.disconnect();
  }
}
```

## Design Decisions

### Redis Stack vs. Regular Redis

**Decision**: Use Redis Stack for development.

**Rationale**: Redis Stack bundles RedisJSON, RediSearch, and RedisTimeSeries modules that are useful for storing agent configuration as JSON documents, searching across organization data, and tracking time-series metrics. In production, use Redis Enterprise or a cloud provider that supports these modules.

### Key prefix for multi-tenancy

The `keyPrefix: "va:"` configuration option automatically prefixes all keys with `va:`, providing namespace isolation. In a multi-tenant setup, the prefix could include the organization ID: `org_123:`.

## Integration Points

- **ioredis**: Node.js client library
- **RedisJSON**: Store and query JSON documents (agent config)
- **RedisTimeSeries**: Track call metrics and voice quality
- **Pub/Sub**: Real-time event distribution
- **Redlock**: Distributed locking for concurrent call processing

## Production Considerations

1. **Persistence trade-off**: RDB snapshots are fast but can lose data. AOF is more durable but slower. In production, use both with `appendfsync everysec`
2. **Memory limits**: Set `maxmemory` and an eviction policy. `allkeys-lru` is appropriate for a cache. For session data, use `allkeys-lfu`
3. **Sentinel/Cluster**: For high availability, use Redis Sentinel (for replication) or Redis Cluster (for sharding). Both require application-level connection handling
4. **SSL/TLS**: In production, enable TLS for Redis connections. Redis Stack supports TLS natively
5. **Connection pooling**: ioredis creates a single connection by default. For high-throughput scenarios, use a connection pool with `ioredis` cluster support
