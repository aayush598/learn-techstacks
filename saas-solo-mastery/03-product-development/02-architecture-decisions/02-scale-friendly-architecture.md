# Scale-Friendly Architecture Without Over-Engineering

## The Over-Engineering Trap

Solo founders face a unique challenge: your architecture needs to support growth, but you can't afford to build for scale you don't have yet. The key is "scale-friendly" architecture — designs that don't constrain future growth but also don't add complexity today.

This guide covers architecture patterns that naturally accommodate growth without the overhead of distributed systems, with concrete code examples and decision frameworks.

## The Scale-Friendly Philosophy

### The Core Principle

> Build for today's scale. Design for tomorrow's growth. Don't implement tomorrow's solution.

This means:
1. Your code should be structured in a way that makes future changes possible
2. But you only build what you need right now
3. You leave "extension points" that are easy to hook into later

### The Four Levels of Scaling

```
Level 1: Single Server (0 - 10k users)
  - One web server, one database
  - $5-50/mo hosting
  - No caching, no replication
  - This works for 95% of SaaS products

Level 2: Vertical Scale (10k - 100k users)
  - Bigger server (more RAM, CPU)
  - Database connection pooling
  - Basic caching (Redis or in-memory)
  - Read replicas if needed

Level 3: Horizontal Scale (100k - 1M users)
  - Multiple web servers behind load balancer
  - Database read replicas
  - CDN for static assets
  - Background job workers
  - Full caching layer

Level 4: Distributed Systems (1M+ users)
  - Microservices (carefully extracted)
  - Database sharding
  - Event-driven architecture
  - Multiple data stores
  - Global distribution
```

For most solo founders, you need to build for Level 1 with the flexibility to reach Level 2 without rewriting. Levels 3 and 4 can wait until you have a team.

## Architectural Patterns That Scale Naturally

### Pattern 1: The Repository Pattern

The repository pattern abstracts data access behind an interface. This single pattern makes scaling dramatically easier.

```typescript
// WITHOUT repository pattern (tightly coupled to implementation)
class UserService {
  async getUser(id: string) {
    // Direct database access — hard to change later
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0];
  }
}
```

```typescript
// WITH repository pattern (abstracted)
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: string): Promise<void>;
}

class PostgresUserRepository implements UserRepository {
  async findById(id: string): Promise<User | null> {
    const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
    return result.rows[0] ? User.fromDatabase(result.rows[0]) : null;
  }

  async save(user: User): Promise<void> {
    await pool.query(
      `INSERT INTO users (id, email, name, created_at)
       VALUES ($1, $2, $3, $4)
       ON CONFLICT (id) DO UPDATE SET
         email = $2, name = $3`,
      [user.id, user.email, user.name, user.createdAt]
    );
  }
}

// Now the service doesn't care HOW data is stored
class UserService {
  constructor(private userRepo: UserRepository) {}

  async getUser(id: string): Promise<User | null> {
    return this.userRepo.findById(id);
  }
}
```

**Why this scales:**
- Switch from Postgres to MySQL: implement `MysqlUserRepository`
- Add caching: implement `CachedUserRepository` that wraps `PostgresUserRepository`
- Split to microservice: implement `HttpUserRepository` that calls a remote service
- Test without database: implement `InMemoryUserRepository`

### Pattern 2: The Service Layer

Separate business logic from transport (HTTP, CLI, queues, etc.).

```typescript
// WITHOUT service layer (logic in controller)
app.post('/api/users', async (req, res) => {
  const { email, name } = req.body;

  // Validation
  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  // Business logic
  const existing = await userRepo.findByEmail(email);
  if (existing) {
    return res.status(409).json({ error: 'Email already exists' });
  }

  const user = User.create(email, name);
  await userRepo.save(user);
  await emailService.sendWelcome(user.email);

  res.status(201).json(user);
});
```

```typescript
// WITH service layer (controller is thin)
// controllers/UserController.ts
app.post('/api/users', async (req, res) => {
  const result = await userService.createUser(req.body.email, req.body.name);

  if (result instanceof Error) {
    return res.status(result.statusCode).json({ error: result.message });
  }

  res.status(201).json(result);
});

// services/UserService.ts
class UserService {
  constructor(
    private userRepo: UserRepository,
    private emailService: EmailService,
  ) {}

  async createUser(email: string, name: string): Promise<User | AppError> {
    if (!email || !email.includes('@')) {
      return new AppError(400, 'Invalid email');
    }

    const existing = await this.userRepo.findByEmail(email);
    if (existing) {
      return new AppError(409, 'Email already exists');
    }

    const user = User.create(email, name);
    await this.userRepo.save(user);
    await this.emailService.sendWelcome(user.email);

    return user;
  }
}
```

**Why this scales:**
- Business logic is testable without HTTP
- Can add additional transports (CLI, queue consumer) later
- Easy to extract into a separate service
- Consistent error handling

### Pattern 3: The Event-Driven Extension

Even in a monolith, emit events for important state changes. This lets you add side effects later without modifying core code.

```typescript
// Domain events — emitted when important things happen
interface DomainEvent {
  type: string;
  data: unknown;
  occurredAt: Date;
}

class UserCreatedEvent implements DomainEvent {
  type = 'user.created';
  constructor(
    public data: { userId: string; email: string; name: string },
    public occurredAt = new Date(),
  ) {}
}

// Simple event bus (in-process for monolith)
class EventBus {
  private handlers = new Map<string, Set<Function>>();

  on(event: string, handler: Function) {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    this.handlers.get(event)!.add(handler);
  }

  async emit(event: DomainEvent) {
    const handlers = this.handlers.get(event.type) || new Set();
    await Promise.all([...handlers].map(h => h(event)));
  }
}

// Core service emits events
class UserService {
  constructor(
    private userRepo: UserRepository,
    private eventBus: EventBus,
  ) {}

  async createUser(email: string, name: string): Promise<User> {
    const user = User.create(email, name);
    await this.userRepo.save(user);

    // Core logic emits events — doesn't know who listens
    await this.eventBus.emit(new UserCreatedEvent({
      userId: user.id,
      email: user.email,
      name: user.name,
    }));

    return user;
  }
}

// Later, you can add listeners without changing UserService:
// listener 1: send welcome email
eventBus.on('user.created', async (event) => {
  await emailService.sendWelcome(event.data.email);
});

// listener 2: add to CRM (added months later, no core code change)
eventBus.on('user.created', async (event) => {
  await crmService.createContact(event.data.email, event.data.name);
});

// listener 3: send to analytics (added even later)
eventBus.on('user.created', async (event) => {
  await analytics.track('user_signed_up', event.data);
});
```

**Why this scales:**
- Add new features without modifying existing code
- Easy to move event handlers to separate processes later
- Natural audit log
- Loose coupling between concerns

### Pattern 4: Background Job Queue (Built-In, Not Separate)

Instead of a separate job queue system, use the database as a simple job queue:

```sql
-- Simple job table — no Redis or SQS needed
CREATE TABLE job_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type VARCHAR(100) NOT NULL,
  payload JSONB NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  error TEXT,
  retry_count INTEGER DEFAULT 0,
  max_retries INTEGER DEFAULT 3
);

CREATE INDEX idx_job_queue_status ON job_queue(status, created_at);
```

```typescript
// Simple job processor (runs in same process or separate)
class JobProcessor {
  async processNext(): Promise<void> {
    // Atomic claim — get a pending job and mark it as running
    const job = await db.query(`
      UPDATE job_queue
      SET status = 'running', started_at = NOW()
      WHERE id = (
        SELECT id FROM job_queue
        WHERE status = 'pending'
          AND (retry_count < max_retries)
        ORDER BY created_at ASC
        LIMIT 1
        FOR UPDATE SKIP LOCKED
      )
      RETURNING *
    `);

    if (!job.rows[0]) return;

    try {
      const handler = this.handlers.get(job.rows[0].type);
      await handler(job.rows[0].payload);

      await db.query(
        `UPDATE job_queue SET status = 'completed', completed_at = NOW()
         WHERE id = $1`,
        [job.rows[0].id]
      );
    } catch (error) {
      await db.query(
        `UPDATE job_queue SET
          status = 'failed',
          error = $1,
          retry_count = retry_count + 1
         WHERE id = $2`,
        [error.message, job.rows[0].id]
      );
    }
  }
}

// Usage — adding a job is just an INSERT
await db.query(
  `INSERT INTO job_queue (type, payload) VALUES ($1, $2)`,
  ['send_email', { to: user.email, template: 'welcome' }]
);
```

**Why this scales:**
- No additional infrastructure (uses existing database)
- Atomic operations, no job loss
- Retry logic built in
- Can move to separate worker process easily
- Can upgrade to Redis/SQS later without application changes

### Pattern 5: Read Models / CQRS Lite

For read-heavy operations, maintain a denormalized read model alongside your normalized write model.

```typescript
// Write model — normalized, transactional
class OrderService {
  async createOrder(items: OrderItem[]): Promise<Order> {
    // Transactional writes to normalized tables
    return await db.transaction(async (tx) => {
      const order = await tx.query(
        `INSERT INTO orders (user_id, total_cents, status)
         VALUES ($1, $2, 'pending') RETURNING *`,
        [userId, total]
      );

      for (const item of items) {
        await tx.query(
          `INSERT INTO order_items (order_id, product_id, quantity, price_cents)
           VALUES ($1, $2, $3, $4)`,
          [order.id, item.productId, item.quantity, item.priceCents]
        );
      }

      return order;
    });
  }
}

// Read model — denormalized for fast reads
class OrderReadService {
  // After order is created, build the read model
  async buildReadModel(orderId: string): Promise<void> {
    const order = await this.getOrderDetails(orderId);

    await db.query(`
      INSERT INTO order_summaries (
        order_id, user_id, user_email, user_name,
        item_count, total_cents, status,
        product_names, created_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
      ON CONFLICT (order_id) DO UPDATE SET
        status = $7
    `, [
      order.id, order.user.id, order.user.email, order.user.name,
      order.items.length, order.totalCents, order.status,
      order.items.map(i => i.productName).join(', '),
      order.createdAt,
    ]);
  }

  // Dashboard query — single table, no joins
  async getDashboard(userId: string) {
    return await db.query(
      `SELECT * FROM order_summaries WHERE user_id = $1 ORDER BY created_at DESC`,
      [userId]
    );
  }
}
```

**Why this scales:**
- Dashboard/reporting queries are fast (single table, no joins)
- Write performance isn't impacted by complex reads
- Read models can be moved to a cache or separate database later
- Easy to add new read models without changing write logic

## Data Patterns That Scale

### Database Connection Pooling

Don't open a new connection for every request. Use connection pooling.

```typescript
// GOOD: Connection pooling
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20, // Max connections in pool
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Single pool, reused across entire application
export async function query(text: string, params?: any[]) {
  const start = Date.now();
  const result = await pool.query(text, params);
  const duration = Date.now() - start;
  console.log('Executed query', { text: text.slice(0, 50), duration, rows: result.rowCount });
  return result;
}
```

### Caching Strategy

Add caching in layers. Start with none, add only when needed.

```markdown
Layer 0: No cache (MVP — works fine)
Layer 1: In-memory cache (single server)
Layer 2: Distributed cache (Redis — multiple servers)
Layer 3: CDN (global distribution)

Add each layer only when you need it.
```

```typescript
// Layer 1: Simple in-memory cache
class InMemoryCache {
  private store = new Map<string, { value: any; expiresAt: number }>();

  get<T>(key: string): T | null {
    const entry = this.store.get(key);
    if (!entry) return null;
    if (Date.now() > entry.expiresAt) {
      this.store.delete(key);
      return null;
    }
    return entry.value as T;
  }

  set(key: string, value: any, ttlMs: number = 60000): void {
    this.store.set(key, {
      value,
      expiresAt: Date.now() + ttlMs,
    });
  }
}

const cache = new InMemoryCache();

// Usage
async function getExpensiveData(id: string) {
  const cached = cache.get(`data:${id}`);
  if (cached) return cached;

  const data = await expensiveQuery(id);
  cache.set(`data:${id}`, data, 60_000); // Cache for 60 seconds
  return data;
}

// When you need Layer 2: Distributed cache
// Replace InMemoryCache with Redis — interface is the same
class RedisCache {
  private client: Redis;

  async get<T>(key: string): Promise<T | null> {
    const value = await this.client.get(key);
    return value ? JSON.parse(value) : null;
  }

  async set(key: string, value: any, ttlMs: number = 60000): Promise<void> {
    await this.client.set(key, JSON.stringify(value), 'PX', ttlMs);
  }
}
```

### Read Replicas

When your database read load exceeds write load (typical for SaaS), add read replicas.

```typescript
// Database configuration with read/write splitting
const config = {
  primary: {
    host: process.env.DB_PRIMARY_HOST,
    // Writes go here
  },
  replicas: [
    { host: process.env.DB_REPLICA_1 },
    { host: process.env.DB_REPLICA_2 },
  ],
};

class Database {
  private primary: Pool;
  private replicas: Pool[];
  private replicaIndex = 0;

  async write(query: string, params?: any[]) {
    return this.primary.query(query, params);
  }

  async read(query: string, params?: any[]) {
    // Round-robin across replicas
    const replica = this.replicas[this.replicaIndex % this.replicas.length];
    this.replicaIndex++;
    return replica.query(query, params);
  }
}
```

### Pagination

Always paginate list endpoints. Even with 100 records today, pagination prevents problems with 100k records tomorrow.

```typescript
// Cursor-based pagination (preferred for scale)
async function getProjects(userId: string, cursor?: string, limit = 20) {
  const query = cursor
    ? `SELECT * FROM projects
       WHERE user_id = $1 AND id > $2
       ORDER BY id ASC
       LIMIT $3`
    : `SELECT * FROM projects
       WHERE user_id = $1
       ORDER BY id ASC
       LIMIT $2`;

  const params = cursor ? [userId, cursor, limit] : [userId, limit];
  const result = await db.query(query, params);

  return {
    data: result.rows,
    nextCursor: result.rows.length === limit
      ? result.rows[result.rows.length - 1].id
      : null,
  };
}

// Offset-based pagination (simpler but slower at scale)
async function getProjectsOffset(userId: string, page = 1, limit = 20) {
  const offset = (page - 1) * limit;
  const result = await db.query(
    `SELECT * FROM projects
     WHERE user_id = $1
     ORDER BY created_at DESC
     LIMIT $2 OFFSET $3`,
    [userId, limit, offset]
  );

  return {
    data: result.rows,
    page,
    hasMore: result.rows.length === limit,
  };
}
```

## Infrastructure Patterns That Scale

### Stateless Application Servers

Keep application servers stateless. All state goes in the database or external stores.

```typescript
// BAD: State on the server
class SessionManager {
  private sessions = new Map<string, SessionData>();

  async getSession(token: string) {
    return this.sessions.get(token);
  }

  async setSession(token: string, data: SessionData) {
    this.sessions.set(token, data);
  }
}
// Problem: If the server restarts, all sessions are lost.
// Problem: Can't add a second server because sessions aren't shared.
```

```typescript
// GOOD: State in database/external store
class SessionManager {
  async getSession(token: string) {
    return db.query('SELECT * FROM sessions WHERE token = $1', [token]);
  }

  async setSession(token: string, data: SessionData) {
    return db.query(
      `INSERT INTO sessions (token, data, expires_at)
       VALUES ($1, $2, $3)
       ON CONFLICT (token) DO UPDATE SET data = $2`,
      [token, data, new Date(Date.now() + 24 * 60 * 60 * 1000)]
    );
  }

  async deleteSession(token: string) {
    return db.query('DELETE FROM sessions WHERE token = $1', [token]);
  }
}
```

### Graceful Shutdown

Your application should handle being killed (for deploys, scaling, etc.).

```typescript
// Graceful shutdown handler
const server = app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});

async function shutdown() {
  console.log('Shutting down gracefully...');

  // 1. Stop accepting new connections
  server.close(() => {
    console.log('HTTP server closed');
  });

  // 2. Drain existing connections (give them 30 seconds)
  // (Implement if you have long-running requests)

  // 3. Close database connections
  await pool.end();
  console.log('Database connections closed');

  // 4. Exit
  process.exit(0);
}

process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
```

### Health Checks

Expose health check endpoints for load balancers and monitoring.

```typescript
// Health check endpoint — shows if the service is healthy
app.get('/health', async (req, res) => {
  const health = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    database: 'unknown',
    memory: process.memoryUsage(),
  };

  try {
    await pool.query('SELECT 1');
    health.database = 'connected';
    res.json(health);
  } catch (error) {
    health.database = 'disconnected';
    health.status = 'unhealthy';
    res.status(503).json(health);
  }
});

// Readiness check — shows if the service is ready for traffic
app.get('/ready', (req, res) => {
  // Add checks: are migrations complete? Is cache warm?
  res.json({ ready: true });
});
```

## Configuration Patterns

### Environment-Based Configuration

```typescript
// config/index.ts
const config = {
  env: process.env.NODE_ENV || 'development',

  port: parseInt(process.env.PORT || '3000', 10),

  database: {
    url: process.env.DATABASE_URL,
    maxConnections: parseInt(process.env.DB_MAX_CONNECTIONS || '20', 10),
  },

  redis: process.env.REDIS_URL,

  stripe: {
    secretKey: process.env.STRIPE_SECRET_KEY,
    webhookSecret: process.env.STRIPE_WEBHOOK_SECRET,
    priceIds: {
      starter: process.env.STRIPE_STARTER_PRICE_ID,
      pro: process.env.STRIPE_PRO_PRICE_ID,
    },
  },

  aws: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    region: process.env.AWS_REGION || 'us-east-1',
    s3Bucket: process.env.S3_BUCKET,
  },

  email: {
    from: process.env.EMAIL_FROM || 'noreply@example.com',
    provider: process.env.EMAIL_PROVIDER || 'resend',
    apiKey: process.env.EMAIL_API_KEY,
  },
} as const;

export default config;
```

### Feature Flags

```typescript
// features/index.ts
import config from '@/config';

// Simple feature flag system
const features = {
  newOnboarding: config.env === 'production' ? false : true,
  advancedAnalytics: false,
  betaSearch: process.env.ENABLE_BETA_SEARCH === 'true',
  v2Api: false,
};

export function isEnabled(feature: keyof typeof features): boolean {
  return features[feature];
}

// Or use a database-backed feature flags (when you have more users)
class FeatureFlagService {
  async isEnabled(flag: string, userId?: string): Promise<boolean> {
    // Check global flag
    const globalFlag = await db.query(
      `SELECT enabled FROM feature_flags WHERE name = $1`,
      [flag]
    );

    if (globalFlag.rows[0]?.enabled) return true;

    // Check user-specific flag (for beta testing)
    if (userId) {
      const userFlag = await db.query(
        `SELECT enabled FROM user_feature_flags
         WHERE user_id = $1 AND flag_name = $2`,
        [userId, flag]
      );
      if (userFlag.rows[0]?.enabled) return true;
    }

    return false;
  }
}
```

## Avoiding Over-Engineering

### The "Do We Need It?" Checklist

Before adding any architectural component, ask:

```markdown
1. Do we have a CURRENT problem that this solves?
   [YES → proceed] [NO → skip]

2. Would adding this now save us significant time later?
   [YES → proceed] [NO → skip]

3. Does adding this NOW reduce complexity, not increase it?
   [YES → proceed] [NO → skip]

4. Would shipping without this be risky?
   [YES → proceed] [NO → skip]

5. Do we have evidence (data, user feedback) that we need this?
   [YES → proceed] [NO → skip]
```

If you answered "NO" to any of these, don't implement it yet.

### Architectural Components to Skip (For Now)

| Component | Skip Until | Why |
|---|---|---|
| Message broker (RabbitMQ, Kafka) | You need to process >10k events/day | Database-as-queue works for small scale |
| Container orchestration (K8s) | You have >5 services | Docker Compose or platform-as-a-service is sufficient |
| API gateway | You have >3 services | Reverse proxy (nginx) handles this |
| Service mesh | You have >10 services | Direct HTTP calls between services is fine |
| Distributed tracing | You have >5 services | Log-based debugging works at small scale |
| Database sharding | You have >100GB data or >10M records | Indexing and read replicas handle this |
| CDN | Your users are in one region | Single-region hosting is fine initially |
| Full-text search (Elasticsearch) | You need advanced search features | PostgreSQL full-text search handles basic needs |
| Real-time updates (WebSockets) | Users accept page refresh | Polling is simpler and works for most cases |

### The Right-Sized Technology Stack

```markdown
**For Solo Founder MVP:**
- Web server: Express/Fastify (Node.js), Rails, Django, or Phoenix
- Database: PostgreSQL (hosted on Supabase, Railway, or self-hosted)
- Caching: In-memory (no Redis)
- Jobs: Database-backed queue
- File storage: Local filesystem or S3 if needed
- Search: PostgreSQL LIKE/ILIKE or pg_search
- Background processing: Same process, simple setTimeout/Timed interval
- Frontend: Server-rendered templates or simple SPA
- Hosting: Single VPS ($10-20/mo) or platform-as-a-service

**For 10k-100k Users (add as needed):**
- Caching: Redis
- Jobs: Redis-backed queue (Bull, Sidekiq)
- Background workers: Separate process(es)
- Search: PostgreSQL full-text search or basic Elasticsearch
- CDN: Cloudflare or AWS CloudFront
- Read replicas: 1-2 database replicas
- Multi-server: Load balancer + 2-3 app servers

**For 100k+ Users (add as needed):**
- Microservices: Extract 1-2 services
- Message broker: Redis streams or RabbitMQ
- Full search: Elasticsearch
- Distributed caching: Redis cluster
- Database sharding: If needed
- Multi-region: If needed
```

## Real-World Architecture Evolution

### Evolution 1: Simple SaaS

```
Month 1:
  [Browser] → [Single Server (Node.js + PostgreSQL)]

Month 6:
  [Browser] → [Single Server (Node.js + PostgreSQL)] → [Redis (caching)]

Month 12:
  [Browser] → [Load Balancer] → [App Server 1] → [PostgreSQL + Read Replica]
                              → [App Server 2] → [Redis]
                                                [Background Worker]

Month 24:
  [Browser] → [CDN] → [Load Balancer] → [App Server 1]  → [PostgreSQL Primary]
                                        [App Server 2]  → [PostgreSQL Replica 1]
                                        [App Server 3]  → [PostgreSQL Replica 2]
                                        [WebSocket Server]  [Redis Cluster]
                                        [Background Workers]  [Elasticsearch]
```

### Evolution 2: AI SaaS

```
Month 1:
  [Browser] → [Single Server] → [PostgreSQL]
                               [OpenAI API]

Month 6:
  [Browser] → [Single Server] → [PostgreSQL]
                               [Redis (rate limiting, caching)]
                               [OpenAI API]
                               [Background Worker for LLM calls]

Month 12:
  [Browser] → [Load Balancer] → [App Server] → [PostgreSQL]
                                [Worker Pool] → [Redis]
                                                [Vector DB (Pinecone)]
                                                [OpenAI API]
                                                [Background Workers]
```

## Architecture Decision Record (ADR) Templates

### ADR: Add Redis

```markdown
# ADR: Add Redis Caching

## Status
Proposed

## Context
- Querying user dashboards takes 500ms+ due to complex joins
- Dashboard is the most-viewed page
- Data changes infrequently (user creates ~5 projects/day)

## Decision
Add Redis for caching dashboard data with 60-second TTL.

## Consequences
+ Dashboard loads in < 50ms
+ Reduced database load
- Additional infrastructure to manage
- Stale data risk (acceptable with 60s TTL)
- $5/mo additional cost

## Implementation
- Use Upstash (serverless Redis) to avoid managing a Redis server
- Cache key: `dashboard:{userId}`
- Cache TTL: 60 seconds
- Invalidate on: project create/update/delete
```

### ADR: Add Background Workers

```markdown
# ADR: Extract Background Workers

## Status
Proposed

## Context
- Email sending blocks HTTP responses (adds 200ms to request)
- PDF generation times out for large documents
- 10% of requests take > 5 seconds due to background work

## Decision
Move email sending, PDF generation, and webhook delivery to background jobs.

## Consequences
+ HTTP responses are < 200ms for all requests
+ Better user experience
+ Failed jobs can be retried
+ Need to manage worker processes

## Implementation
- Use database-backed queue (no new infrastructure)
- Worker runs in a separate Node.js process
- Deployed alongside main app, scaled together
- Jobs: email, pdf_generation, webhook_delivery
```

## Checklist: Scale-Friendly Architecture Review

Before shipping, review your architecture against this checklist:

```markdown
### Code Organization
[ ] Business logic is separated from transport (HTTP, CLI, etc.)
[ ] Data access is behind a repository interface
[ ] Configuration is environment-based
[ ] Feature flags exist for toggling behavior

### Database
[ ] Connection pooling is configured
[ ] All list endpoints use pagination
[ ] Indexes exist on frequently queried columns
[ ] Migrations are reversible
[ ] N+1 query patterns are identified and fixed

### Infrastructure
[ ] Application servers are stateless
[ ] Health check endpoints exist
[ ] Graceful shutdown is implemented
[ ] Logs are structured (JSON) for analysis
[ ] Error tracking is configured (Sentry)
[ ] Database backups are automated

### Performance (as needed)
[ ] Slow queries are identified and optimized
[ ] Caching strategy is defined
[ ] Read replicas are available if needed
[ ] CDN is configured for static assets

### Future-Proofing
[ ] Events are emitted for important state changes
[ ] Repository pattern enables future data source changes
[ ] Service layer enables future API changes
[ ] Configuration is centralized
[ ] Dependencies are explicitly versioned
```

## Summary

Scale-friendly architecture is about making good choices today that don't paint you into a corner tomorrow. It's NOT about building for scale you don't have.

**The key principles:**
1. Separate concerns (service layer, repository pattern)
2. Keep application servers stateless
3. Use events for cross-cutting concerns
4. Caching is the last resort, not the first
5. Database-backed queues work for most solo founder needs
6. Add infrastructure components only when you have a concrete need
7. Health checks, graceful shutdown, and good logging are non-negotiable

**Remember:** A simple architecture that ships today is better than a scalable architecture that ships next month. Build for today, design for tomorrow, implement when necessary.
