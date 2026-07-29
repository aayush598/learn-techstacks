# Choosing the Right Database for Your SaaS

## The Database Decision

Your database choice is one of the most consequential decisions you'll make. Switching databases later is painful, expensive, and risky. But the wrong choice can also mean unnecessary complexity or costs.

This guide covers every major database option with specific guidance for solo SaaS founders — when each shines, when each fails, and how to make the right choice for your specific product.

## The Solo Founder's Database Framework

### The Three Questions

Before evaluating databases, answer these three questions:

```
1. What does my data look like?
   - Highly structured with relationships (users, projects, invoices)
   - Semi-structured with varying schemas (product catalog, CMS)
   - Unstructured blobs (documents, images, videos)
   - Graph-like (social networks, recommendations)

2. How will I access my data?
   - Complex joins and aggregations (reporting, analytics)
   - Simple key-value lookups (sessions, settings)
   - Full-text search (content, documents)
   - Real-time subscriptions (chat, notifications)

3. What's my scale trajectory?
   - < 100k records (most SaaS MVPs)
   - 100k-10M records (growth stage)
   - 10M-1B records (scale stage)
   - Multi-region, global (enterprise stage)
```

### The Default Recommendation

For 90% of solo founders building SaaS products, the answer is:

**PostgreSQL. Always start with PostgreSQL.**

Here's why:
- It handles 95% of use cases excellently
- It has the best ecosystem of any database
- It scales from $0 hobby project to billion-dollar company
- You can add JSON, full-text search, vectors, and more as extensions
- It has the most mature tooling, hosting options, and community support

The rest of this guide covers when to choose alternatives to PostgreSQL.

## Database Comparison

### Relational Databases

```markdown
| Feature              | PostgreSQL | MySQL | SQLite | SQL Server |
|----------------------|------------|-------|--------|------------|
| ACID compliance      | Excellent  | Good  | Excellent | Excellent |
| JSON support         | Excellent  | Good  | Limited | Good     |
| Full-text search     | Built-in   | Built-in| Limited | Excellent |
| Concurrency          | Excellent  | Good  | Limited | Excellent |
| Extensions           | Excellent  | Limited| Limited | Limited   |
| Hosted options       | Excellent  | Excellent| Limited | Good     |
| Replication          | Excellent  | Good  | Limited | Excellent |
| GIS support          | PostGIS    | Limited| Limited| Good      |
| Vector support       | pgvector   | No    | No      | No        |
| Free tier            | Yes        | Yes   | Yes     | Limited   |
| Learning curve       | Medium     | Low   | Low     | Medium    |
| Performance (reads)  | Excellent  | Excellent| Good | Excellent |
| Performance (writes) | Excellent  | Excellent| Limited | Excellent |
```

### NoSQL Databases

```markdown
| Feature              | MongoDB | Redis | DynamoDB | Firestore |
|----------------------|---------|-------|----------|-----------|
| Data model           | Document| Key-Value| Document| Document  |
| ACID compliance      | Limited | No    | Limited  | Limited   |
| Schema flexibility   | Excellent| N/A  | Flexible| Flexible  |
| Query flexibility    | Good    | Limited| Limited| Limited   |
| Joins                | Poor    | No    | Poor     | Poor      |
| Scalability          | Excellent| Excellent| Excellent| Excellent |
| Read performance     | Good    | Excellent| Excellent| Good     |
| Write performance    | Good    | Excellent| Excellent| Good     |
| Hosting cost         | Medium  | Low   | Pay-per-use| Pay-per-use|
| Lock-in risk         | Low (OSS)| Low (OSS)| High (AWS)| High (GCP)|
```

### Specialized Databases

```markdown
| Database     | Best For                      | When to Use                    |
|--------------|-------------------------------|--------------------------------|
| Elasticsearch| Full-text search, analytics   | When Postgres full-text isn't enough |
| Pinecone     | Vector similarity search      | AI/ML vector embeddings        |
| Redis        | Caching, real-time, sessions  | When you need sub-millisecond reads |
| Neo4j        | Graph relationships           | Social networks, recommenders  |
| InfluxDB     | Time-series data              | IoT, metrics, monitoring       |
| ClickHouse   | Analytics, OLAP               | Heavy reporting, data warehouse|
| DuckDB       | Embedded analytics            | Local analysis, data science   |
```

## PostgreSQL: The Default Choice

### Why PostgreSQL is the Right Default

```markdown
1. Reliability
   - 30+ years of maturity
   - ACID compliant (no data corruption)
   - MVCC for concurrent access
   - Point-in-time recovery
   - Table-level partitioning

2. Feature Set
   - Full-text search (tsvector)
   - JSON/JSONB (NoSQL within SQL)
   - Array, hstore, UUID, CIDR types
   - Window functions, CTEs, recursive queries
   - GiST, GIN, BRIN indexes
   - Foreign Data Wrappers (FDW)
   - Logical replication
   - Row-level security

3. Extensibility
   - pgvector (vector embeddings)
   - PostGIS (geographic data)
   - TimescaleDB (time-series)
   - Citus (horizontal scaling)
   - pg_partman (partition management)
   - wal2json (CDC)

4. Ecosystem
   - Prisma, Drizzle, TypeORM, Sequelize
   - Supabase, Neon, RDS, Cloud SQL
   - pgAdmin, DBeaver, TablePlus
   - pg_stat_statements (query performance)
   - EXPLAIN ANALYZE (query planning)

5. Community
   - Largest open-source database community
   - Extensive documentation
   - Thousands of blog posts, tutorials
   - Active mailing lists and forums
```

### When PostgreSQL is NOT the Right Choice

```markdown
1. When you need sub-millisecond reads for simple lookups
   → Use Redis (caching layer in front of Postgres)

2. When your data is truly schema-less
   → Consider MongoDB (but try JSONB columns in Postgres first)

3. When you need massive write throughput (100k+ writes/second)
   → Consider DynamoDB or Cassandra with eventual consistency

4. When you're doing complex graph traversals
   → Consider Neo4j (but recursive CTEs in Postgres handle many cases)

5. When you need petabyte-scale analytics
   → Consider ClickHouse or Snowflake (data warehouse)

6. When you need full-text search with advanced relevance
   → Consider Elasticsearch (but try Postgres full-text first)

7. When you're building a mobile app with offline sync
   → Consider SQLite (embedded on device) + Postgres (server)

8. When you need vector search at massive scale
   → Consider Pinecone (but try pgvector first)
```

### PostgreSQL Setup Patterns

```sql
-- Basic SaaS schema pattern
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Users table (core)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(50) DEFAULT 'user',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_users_metadata ON users USING GIN (metadata);

-- Multi-tenant pattern
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Row-Level Security for multi-tenancy
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON projects
  USING (tenant_id = current_setting('app.current_tenant_id')::UUID);
```

## MySQL: When to Choose It

### MySQL Strengths

```markdown
1. Performance
   - Faster reads than PostgreSQL for simple queries
   - Excellent for read-heavy workloads
   - Better replication performance
   - More efficient on less powerful hardware

2. Ecosystem
   - WordPress (60% of web uses MySQL)
   - Laravel (PHP's primary database)
   - PlanetScale (serverless MySQL with branching)
   - Aurora (AWS's enhanced MySQL)

3. Simplicity
   - Easier to learn than PostgreSQL
   - Simpler configuration
   - More hosting options at lower prices
   - Larger pool of developers

4. Replication
   - Mature, well-tested replication
   - Easy to set up read replicas
   - Group replication for high availability
```

### When to Choose MySQL Over PostgreSQL

```markdown
1. You're using PlanetScale or Aurora
   - PlanetScale's branching workflow is unique and powerful
   - Aurora MySQL is cheaper than Aurora PostgreSQL

2. Your stack is PHP/Laravel
   - Laravel's ecosystem is MySQL-first
   - Most Laravel hosting is optimized for MySQL

3. You need a specific MySQL feature
   - Spatial indexes (PostGIS is better for complex GIS)
   - Group commit (improves write performance)

4. Your team knows MySQL and not PostgreSQL
   - The best database is the one your team knows
   - Knowledge gap is real and costly

5. You're on a tight budget for the smallest VPS
   - MySQL uses less memory than PostgreSQL
   - Can run on 512MB RAM VPS more comfortably
```

## MongoDB: When to Choose It

### MongoDB Strengths

```markdown
1. Schema Flexibility
   - No migrations for adding fields
   - Different documents can have different shapes
   - Great for rapidly evolving schemas
   - Ideal for product catalogs, CMS, event data

2. Developer Experience
   - JSON-like documents match JavaScript objects
   - No joins (embed instead of reference)
   - Fast prototyping (no schema design upfront)
   - Excellent driver support

3. Horizontal Scaling
   - Built-in sharding (distribute data across servers)
   - Easier to scale than PostgreSQL
   - Good for global distribution
```

### When to Choose MongoDB Over PostgreSQL

```markdown
1. Your data is naturally document-shaped
   - Product catalog with varying attributes per product
   - Content management with flexible schemas
   - Event logging with varying event structures

2. You don't need complex joins
   - MongoDB works best with denormalized, embedded data
   - If you need relational-style joins, use PostgreSQL

3. You need to scale writes horizontally
   - MongoDB shards more naturally than PostgreSQL
   - Citus (Postgres sharding) adds complexity

4. You're prototyping rapidly
   - MongoDB's schema-less nature speeds up early development
   - But: lack of schema enforcement causes production issues

5. Your data has a natural aggregation pipeline
   - MongoDB's aggregation pipeline is excellent
   - Better than PostgreSQL for complex data transformations
```

### MongoDB Anti-Patterns (When NOT to Use It)

```
1. You need transactions across multiple documents
   - MongoDB 4.0+ has multi-document transactions
   - But they're slower than PostgreSQL transactions

2. Your data is highly relational
   - User → Projects → Tasks → Comments
   - MongoDB requires manual joins (manual references)
   - PostgreSQL handles this naturally

3. You need strong consistency guarantees
   - MongoDB's default is eventual consistency
   - Can be configured for strong consistency (at performance cost)

4. You have complex reporting requirements
   - MongoDB struggles with complex ad-hoc queries
   - PostgreSQL with window functions is much better

5. You need full-text search with relevance
   - MongoDB has basic text search
   - PostgreSQL has better full-text capabilities
```

## SQLite: When to Choose It

### SQLite Strengths

```markdown
1. Zero Configuration
   - No server to install or manage
   - Database is a single file
   - No connections, no ports, no users
   - Included in every programming language

2. Performance
   - Faster than PostgreSQL/MySQL for simple queries
   - No network latency (embedded in process)
   - Excellent for read-heavy workloads (< 100k records)

3. Reliability
   - Insanely reliable (most tested database in the world)
   - ACID compliant
   - It's on every smartphone, browser, and embedded device

4. Cost
   - Absolutely free
   - No hosting costs
   - No management overhead
```

### When to Choose SQLite

```markdown
1. For an MVP with low traffic
   - Single-server, low concurrency
   - < 10 concurrent writes per second
   - < 10GB total data

2. For embedded/desktop applications
   - Local-first SaaS apps
   - Desktop software that syncs to cloud
   - Mobile apps

3. For testing and development
   - Use SQLite in test suites (fast, no external deps)
   - Switch to PostgreSQL in production

4. For analytics processing
   - SQLite is great for local data analysis
   - Combine with DuckDB for heavy analytics

5. For single-tenant deployments
   - Each customer gets their own SQLite file
   - Simple backup (copy the file)
   - No multi-tenancy complexity
```

### SQLite Limitations

```markdown
1. Concurrency
   - One writer at a time (table-level locking)
   - WAL mode helps but still limited
   - Not suitable for > 100 concurrent users

2. Replication
   - No built-in replication
   - No read replicas
   - No automatic failover

3. Features
   - Limited full-text search
   - No stored procedures
   - No user management
   - Limited SQL features compared to PostgreSQL

4. Scale
   - Performance degrades above 10GB
   - Not suitable for multi-server deployments
   - No horizontal scaling
```

### SQLite → PostgreSQL Migration Strategy

```typescript
// Step 1: Use an abstraction layer
interface Database {
  query(sql: string, params?: any[]): Promise<any[]>;
  transaction<T>(fn: (query: Function) => Promise<T>): Promise<T>;
}

// Step 2: Implement for both databases
class SQLiteDatabase implements Database {
  private db: Database;
  constructor(path: string) {
    this.db = new Database(path);
  }
  async query(sql: string, params?: any[]) {
    return this.db.prepare(sql).all(...(params || []));
  }
}

class PostgresDatabase implements Database {
  private pool: Pool;
  constructor(connectionString: string) {
    this.pool = new Pool({ connectionString });
  }
  async query(sql: string, params?: any[]) {
    const result = await this.pool.query(sql, params);
    return result.rows;
  }
}

// Step 3: Switch via environment variable
const db: Database = process.env.DATABASE_TYPE === 'postgres'
  ? new PostgresDatabase(process.env.DATABASE_URL!)
  : new SQLiteDatabase('./data/mvp.db');
```

## Multi-Model with PostgreSQL

### Using PostgreSQL for Everything

PostgreSQL can replace multiple databases with extensions:

```sql
-- Instead of MongoDB: Use JSONB
CREATE TABLE products (
  id UUID PRIMARY KEY,
  name VARCHAR(255),
  attributes JSONB, -- Flexible schema
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_products_attributes ON products USING GIN (attributes);

-- Instead of Elasticsearch: Use Full-Text Search
ALTER TABLE documents ADD COLUMN search_vector tsvector;
CREATE INDEX idx_documents_search ON documents USING GIN (search_vector);

CREATE OR REPLACE FUNCTION documents_search_trigger() RETURNS trigger AS $$
BEGIN
  NEW.search_vector := to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.content, ''));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER documents_search_update
  BEFORE INSERT OR UPDATE ON documents
  FOR EACH ROW EXECUTE FUNCTION documents_search_trigger();

-- Query with relevance ranking
SELECT id, title, ts_rank(search_vector, query) AS rank
FROM documents, plainto_tsquery('english', 'search terms') query
WHERE search_vector @@ query
ORDER BY rank DESC;

-- Instead of Redis (simple caching): Use in-memory table
CREATE TABLE cache (
  key VARCHAR(255) PRIMARY KEY,
  value JSONB NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL
);
CREATE INDEX idx_cache_expires ON cache(expires_at);

-- Clean expired entries
DELETE FROM cache WHERE expires_at < NOW();

-- Instead of Pinecone (basic vectors): Use pgvector
CREATE EXTENSION vector;
CREATE TABLE embeddings (
  id UUID PRIMARY KEY,
  content TEXT,
  embedding vector(1536)
);
CREATE INDEX idx_embeddings ON embeddings USING hnsw (embedding vector_cosine_ops);

-- Similarity search
SELECT content, 1 - (embedding <=> '[0.1, 0.2, ...]'::vector) AS similarity
FROM embeddings
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 10;
```

### The PostgreSQL-Only Stack

For most solo founders, PostgreSQL + extensions replaces:

```markdown
Traditional Stack:
  - PostgreSQL (relational data)
  - Redis (caching, sessions)
  - Elasticsearch (search)
  - MongoDB (flexible schemas)
  - RabbitMQ (queues)

PostgreSQL-Only Stack:
  - PostgreSQL + extensions
  - pgvector (AI embeddings)
  - pg_partman (partitioning)
  - SKIP LOCKED + queue table (job queue)
  - NOTIFY/LISTEN (real-time events)
  - BRIN indexes (time-series)
```

## Cache Layer Decisions

### When to Add Redis

```
Do you need Redis?
Ask these questions:

1. Are you serving the same data to multiple users?
   YES → Caching helps
   NO → Skip caching

2. Is the data expensive to compute or query?
   YES → Cache it
   NO → Just query the database

3. Is your database response time > 100ms for common queries?
   YES → Consider caching
   NO → Database is fast enough

4. Are you getting > 100 requests/second for the same data?
   YES → Redis would help
   NO → Database handles this fine

If you answered YES to 3+, add Redis.
Otherwise, skip it.
```

### In-Memory Caching (Cheaper Alternative)

```typescript
// Simple in-memory cache for single-server MVP
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

  set(key: string, value: any, ttlMs: number = 60000) {
    this.store.set(key, {
      value,
      expiresAt: Date.now() + ttlMs,
    });
  }

  invalidate(pattern: string) {
    for (const key of this.store.keys()) {
      if (key.includes(pattern)) {
        this.store.delete(key);
      }
    }
  }
}
```

## Database Decision Flowchart

```
Start: What does your app need?
  |
  ├── Relational data? (users, orders, invoices, projects)
  |   └── YES → PostgreSQL (default)
  |       └── Constraints?
  |           ├── Very low budget VPS (< 1GB RAM) → MySQL or SQLite
  |           ├── Laravel/PHP ecosystem → MySQL
  |           ├── Serverless + branching workflows → PlanetScale (MySQL)
  |           └── None of the above → PostgreSQL
  |
  ├── Document/flexible data? (products, CMS, events)
  |   ├── Need complex queries and joins?
  |   |   ├── YES → PostgreSQL (JSONB columns)
  |   |   └── NO → MongoDB
  |   └── Scale needs?
  |       ├── Single server → PostgreSQL (JSONB)
  |       └── Multi-server sharding → MongoDB
  |
  ├── Key-value / sessions / caching?
  |   ├── Sub-millisecond required?
  |   |   ├── YES → Redis
  |   |   └── NO → PostgreSQL (simple table)
  |   └── Persistence needed?
  |       ├── YES → Redis with persistence or PostgreSQL
  |       └── NO → Redis (ephemeral)
  |
  ├── Search?
  |   ├── Simple full-text search → PostgreSQL (tsvector)
  |   ├── Advanced search with faceting → Elasticsearch
  |   └── Vector similarity → PostgreSQL (pgvector) or Pinecone
  |
  ├── Time-series / metrics?
  |   ├── < 1M data points/month → PostgreSQL (BRIN index)
  |   ├── 1M-100M data points/month → TimescaleDB (PostgreSQL extension)
  |   └── > 100M data points/month → ClickHouse or InfluxDB
  |
  └── Graph / relationships?
      ├── Simple relationships → PostgreSQL (recursive CTEs)
      └── Complex graph traversals → Neo4j
```

## Database Hosting Comparison

```markdown
| Service       | Tech       | Free Tier        | Paid Start  | Best For                |
|---------------|------------|------------------|-------------|-------------------------|
| Supabase      | PostgreSQL | 500MB            | $25/mo      | All-in-one backend      |
| Neon          | PostgreSQL | 0.5GB            | $19/mo      | Serverless, branching   |
| Railway       | PostgreSQL | $5 credit        | $5/mo       | Simple, integrated      |
| Render        | PostgreSQL | 256MB RAM        | $7/mo       | Simple managed          |
| Aiven         | PostgreSQL | None             | $19/mo      | Enterprise features     |
| AWS RDS       | PostgreSQL | Free tier (1yr)  | $15/mo      | Most reliable           |
| Cloud SQL     | PostgreSQL | $300 credit      | $25/mo      | Google Cloud            |
| DigitalOcean  | PostgreSQL | None             | $12/mo      | Simple managed          |
| PlanetScale   | MySQL      | 1GB storage      | $29/mo      | Branching workflows     |
| MongoDB Atlas | MongoDB    | 512MB            | $57/mo      | MongoDB hosting         |
| Upstash       | Redis      | 10MB             | $0.45/GB    | Serverless Redis        |
| Redis Cloud   | Redis      | 30MB             | $15/mo      | Managed Redis           |
| Pinecone      | Vector     | Free tier        | $70/mo      | Vector database         |
```

## Multi-Database Architecture for Solo Founders

If you genuinely need multiple databases, here's the minimum viable architecture:

```markdown
Phase 1: PostgreSQL Only (0-10k users)
  - All data in PostgreSQL
  - Extensions for full-text search, JSON, vectors
  - Simple in-memory caching

Phase 2: PostgreSQL + Redis (10k-100k users)
  - Primary data in PostgreSQL
  - Redis for caching, sessions, rate limiting
  - Consider pgvector for AI features

Phase 3: PostgreSQL + Redis + Elasticsearch (100k-1M users)  
  - Primary data in PostgreSQL
  - Redis for caching
  - Elasticsearch for advanced search
  - Maybe pgvector or dedicated vector DB for AI

Phase 4: Multiple Databases (1M+ users)
  - PostgreSQL for relational data
  - Redis for caching and real-time
  - Elasticsearch for search
  - Dedicated vector DB for AI
  - Data warehouse (ClickHouse/BigQuery) for analytics
  - Message queue (RabbitMQ/Kafka) for async processing
```

### The Database Unified Pattern

When using multiple databases, maintain a unified access layer:

```typescript
// lib/database/index.ts
import { Pool } from 'pg';
import { Redis } from '@upstash/redis';
import { ElasticsearchClient } from './elasticsearch';

interface UnifiedDB {
  // Primary data
  primary: Pool;

  // Cache
  cache: Redis;

  // Search (when needed)
  search?: ElasticsearchClient;

  // Vector store (when needed)
  vectors?: VectorStore;
}

// Usage in service layer
class ProjectService {
  constructor(private db: UnifiedDB) {}

  async getProjects(userId: string) {
    // Try cache first
    const cached = await this.db.cache.get(`projects:${userId}`);
    if (cached) return cached;

    // Query primary database
    const projects = await this.db.primary.query(
      'SELECT * FROM projects WHERE user_id = $1',
      [userId]
    );

    // Cache for next time
    await this.db.cache.set(`projects:${userId}`, projects, 300);

    return projects;
  }

  async searchProjects(userId: string, query: string) {
    if (this.db.search) {
      return this.db.search.search('projects', query, { filter: { userId } });
    }
    // Fallback to PostgreSQL full-text search
    return this.db.primary.query(
      `SELECT * FROM projects
       WHERE user_id = $1
         AND to_tsvector('english', name || ' ' || description) @@ plainto_tsquery('english', $2)`,
      [userId, query]
    );
  }
}
```

## Database Migration Between Types

If you need to migrate between database types, here's the general approach:

```markdown
Phase 1: Extract data from source
  - Full dump of all data
  - Transform to target format (relationalize JSON, etc.)
  - Validate data integrity

Phase 2: Import to target
  - Create target schema
  - Import data in batches
  - Verify row counts match

Phase 3: Dual-write (optional but recommended)
  - Write to both databases
  - Verify consistency
  - Run comparison queries

Phase 4: Cutover
  - Point application at new database
  - Monitor carefully
  - Keep old database for rollback

Phase 5: Cleanup
  - Decommission old database
  - Update backups, monitoring
  - Document the migration
```

## Summary: Database Decision Guide

### The 90% Solution

```markdown
SaaS Type               | Recommended Database
------------------------|---------------------
General CRUD SaaS       | PostgreSQL
Content CMS             | PostgreSQL (+ JSONB)
E-commerce              | PostgreSQL
Analytics/Reporting     | PostgreSQL (+ materialized views)
AI-Powered SaaS         | PostgreSQL (+ pgvector)
Real-Time Dashboard     | PostgreSQL (+ LISTEN/NOTIFY)
Developer Tools         | PostgreSQL
Marketplace             | PostgreSQL
API Service             | PostgreSQL
Social Network          | PostgreSQL (+ Redis for feed)

Default answer: PostgreSQL
```

### The Solo Founder's Database Advice

1. **Start with PostgreSQL.** It covers 95% of use cases and lets you add capabilities later with extensions.
2. **Don't use MongoDB as your primary database for a SaaS.** The lack of schema enforcement causes production issues. Use JSONB columns in PostgreSQL for flexible schemas.
3. **Don't add Redis until you need it.** Simple in-memory caching is sufficient for MVP. Add Redis when you have multiple servers or need persistence.
4. **Don't use Elasticsearch until PostgreSQL full-text search limits you.** PostgreSQL's built-in full-text search handles most cases.
5. **SQLite is fine for MVP if you're using an ORM that abstracts the database.** Just plan to migrate to PostgreSQL before launch.
6. **Use managed database hosting.** Don't self-manage a database server. Use Supabase, Neon, or RDS. Your time is better spent on product.
7. **The database matters less than schema design.** A well-designed PostgreSQL schema beats a poorly-designed MongoDB schema every time.
8. **You can always add more databases later.** Start with one, add others when you have concrete problems that require them.
