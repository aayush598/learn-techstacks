# Section 03: Tenant Context Middleware Pattern

## Overview

Tenant context middleware bridges the stateless HTTP request world and the stateful database session, ensuring that every database operation is scoped to the correct tenant. This middleware extracts the tenant identity from the incoming request (JWT claims, API key lookup, or subdomain), validates it, and propagates it to the database layer and application code. In Node.js, this is typically implemented using AsyncLocalStorage (ALS), which provides thread-safe, request-scoped storage without passing parameters through every function call.

The middleware must solve several challenges: extracting tenant ID from various sources (authentication token, API key, custom domain), validating that the tenant is active and not suspended, setting the database session context for RLS, handling unauthenticated requests (login page, public endpoints), and managing errors when tenant context is missing or invalid. The middleware also provides an opportunity for pre-request validation—checking whether the tenant has exceeded resource quotas or is in a maintenance window.

For a voice agent platform, tenant context middleware is also responsible for loading tenant-specific configuration: feature flags, rate limits, white-labeling settings, and AI model preferences. This configuration is cached and refreshed periodically to minimize database load while keeping settings current.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
import { AsyncLocalStorage } from 'async_hooks';
import { Request, Response, NextFunction } from 'express';

interface TenantContext {
  tenantId: string;
  userId: string;
  userRole: string;
  tenantConfig: TenantConfig;
  featureFlags: Record<string, boolean>;
  ipAddress: string;
  requestId: string;
}

// Singleton storage
const als = new AsyncLocalStorage<TenantContext>();

export class TenantContextMiddleware {
  private tenantCache: RedisCache;
  private apiKeyService: ApiKeyService;
  private domainService: DomainMappingService;

  constructor(
    private pool: Pool,
    config: MiddlewareConfig
  ) {
    this.tenantCache = new RedisCache(config.redisUrl);
    this.apiKeyService = new ApiKeyService(pool);
    this.domainService = new DomainMappingService(pool);
  }

  middleware() {
    return async (req: Request, res: Response, next: NextFunction) => {
      const requestId = crypto.randomUUID();

      try {
        // Step 1: Extract tenant identity from request
        const tenantId = await this.resolveTenantId(req);
        
        if (!tenantId) {
          // Allow unauthenticated access to public routes
          if (this.isPublicRoute(req.path)) {
            return next();
          }
          return res.status(401).json({ error: 'Authentication required' });
        }

        // Step 2: Validate tenant
        const tenant = await this.validateTenant(tenantId);
        if (!tenant) {
          return res.status(403).json({ error: 'Tenant not found' });
        }
        if (tenant.status === 'suspended') {
          return res.status(403).json({ 
            error: 'Account suspended', 
            code: 'ACCOUNT_SUSPENDED',
            supportEmail: 'support@voiceagent.com'
          });
        }

        // Step 3: Load tenant configuration
        const [tenantConfig, featureFlags] = await Promise.all([
          this.loadTenantConfig(tenantId),
          this.loadFeatureFlags(tenantId),
        ]);

        // Step 4: Create tenant context
        const context: TenantContext = {
          tenantId,
          userId: req.user?.id || 'system',
          userRole: req.user?.role || 'anonymous',
          tenantConfig,
          featureFlags,
          ipAddress: req.ip,
          requestId,
        };

        // Step 5: Run request within ALS context
        als.run(context, async () => {
          // Set database context for RLS
          const client = await this.pool.connect();
          try {
            await client.query('BEGIN');
            await client.query(
              `SELECT set_config('app.tenant_id', $1, true)`, 
              [tenantId]
            );
            await client.query(
              `SELECT set_config('app.user_role', $1, true)`, 
              [context.userRole]
            );
            await client.query(
              `SELECT set_config('app.request_id', $1, true)`, 
              [requestId]
            );

            // Attach client to request for route handlers
            req.dbClient = client;
            
            await next();

            await client.query('COMMIT');
          } catch (error) {
            await client.query('ROLLBACK');
            throw error;
          } finally {
            client.release();
          }
        });
      } catch (error) {
        next(error);
      }
    };
  }

  private async resolveTenantId(req: Request): Promise<string | null> {
    // Strategy 1: JWT token
    const authHeader = req.headers.authorization;
    if (authHeader?.startsWith('Bearer ')) {
      const token = authHeader.slice(7);
      const decoded = verifyToken(token);
      return decoded.tenant_id;
    }

    // Strategy 2: API key
    const apiKey = req.headers['x-api-key'] as string;
    if (apiKey) {
      return this.apiKeyService.resolveTenant(apiKey);
    }

    // Strategy 3: Custom domain / subdomain
    const host = req.headers.host;
    if (host) {
      return this.domainService.resolveTenant(host);
    }

    // Strategy 4: Cookie session
    const sessionToken = req.cookies?.session_token;
    if (sessionToken) {
      const session = await this.sessionStore.get(sessionToken);
      return session?.tenant_id;
    }

    return null;
  }

  private async loadTenantConfig(tenantId: string): Promise<TenantConfig> {
    const cacheKey = `tenant:config:${tenantId}`;
    const cached = await this.tenantCache.get(cacheKey);
    if (cached) return JSON.parse(cached);

    const config = await this.pool.query(
      `SELECT settings, branding, quotas FROM tenant_config WHERE tenant_id = $1`,
      [tenantId]
    );
    
    await this.tenantCache.setex(cacheKey, 300, JSON.stringify(config.rows[0]));
    return config.rows[0];
  }

  private async loadFeatureFlags(tenantId: string): Promise<Record<string, boolean>> {
    const cacheKey = `tenant:flags:${tenantId}`;
    const cached = await this.tenantCache.get(cacheKey);
    if (cached) return JSON.parse(cached);

    const flags = await this.pool.query(
      `SELECT f.name, tf.enabled 
       FROM tenant_feature_flags tf
       JOIN feature_flags f ON tf.flag_id = f.id
       WHERE tf.tenant_id = $1`,
      [tenantId]
    );

    const flagMap: Record<string, boolean> = {};
    for (const row of flags.rows) {
      flagMap[row.name] = row.enabled;
    }
    
    await this.tenantCache.setex(cacheKey, 300, JSON.stringify(flagMap));
    return flagMap;
  }

  private isPublicRoute(path: string): boolean {
    const publicPrefixes = ['/auth/', '/webhook/', '/health', '/api/v1/public/'];
    return publicPrefixes.some(prefix => path.startsWith(prefix));
  }
}

// Helper to access tenant context anywhere in the application
export function getTenantContext(): TenantContext {
  const context = als.getStore();
  if (!context) {
    throw new Error('Tenant context not available. Ensure middleware is applied.');
  }
  return context;
}

export function getTenantId(): string {
  return getTenantContext().tenantId;
}
```

## Integration Points

- **API Routes:** Every API route handler accesses tenant context via `getTenantContext()`
- **Database Layer:** `pg` client connections have `app.tenant_id` set for RLS
- **Background Jobs:** Job worker threads initialize their own tenant context from job payload
- **WebSocket Connections:** Initial WS handshake establishes tenant context for the connection
- **Logging:** All log entries include tenant_id from context for operational visibility

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **ALS Performance:** AsyncLocalStorage has minimal overhead (~1μs per operation). It's the recommended approach for context propagation in modern Node.js.
- **Cache Invalidation:** Tenant configuration changes must invalidate the Redis cache. Use a Redis pub/sub channel or cache version counter.
- **Transaction Safety:** Always use `SET LOCAL` within `BEGIN...COMMIT` blocks. Never use `SET SESSION` which would leak tenant context between requests reusing the same database connection.
- **Middleware Ordering:** Tenant context middleware must run after authentication but before route handlers. Ensure proper ordering in your Express/Fastify middleware chain.
- **Error Handling:** Wrap the entire middleware in try/catch. If tenant context setup fails, respond with a 500 error rather than leaving the database in an inconsistent state.
- **Background Jobs:** For async job processing (Bull/BullMQ), initialize tenant context from the job data before executing. This ensures background tasks respect tenant isolation.
- **Testing:** In test environments, initialize tenant context explicitly: `als.run({ tenantId: 'test_tenant', ... }, testFn)`. Create test helpers that wrap test cases with tenant context.
- **Monitoring:** Track tenant resolution latency, cache hit rates, and configuration load times. Alert on slow tenant resolution (<100ms).
