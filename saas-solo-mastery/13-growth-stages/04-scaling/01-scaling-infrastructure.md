# Scaling Infrastructure for Growth: Database Optimization, Caching, CDN, Load Balancing

## Why Infrastructure Matters for Solo Founders

Infrastructure is often an afterthought for solo founders. You're focused on building features, acquiring users, and keeping the lights on. But when growth hits — and it will, suddenly — your infrastructure WILL fail if you haven't prepared.

The cost of infrastructure failure:
- **Downtime during viral moment:** You get 50K visitors from a tweet, your site goes down, and you lose them forever
- **Slow performance during launch:** PH users bounce if pages take > 3 seconds
- **Database overload:** One popular feature causes query explosion, everything slows down
- **Data loss:** No backups, corrupted data, hours of recovery

This guide covers what a solo founder needs to know to build infrastructure that scales — without over-engineering before you need it.

## The Solo Founder's Infrastructure Philosophy

### The "Just Enough" Principle

As a solo founder, you have limited time. Don't build infrastructure for 1M users when you have 100. But DO build infrastructure for 10K when you have 100. The key is building systems that can scale incrementally.

```
Right-Sizing Infrastructure:

100 users → Single server, basic CDN, daily backups
1,000 users → Multi-server, caching layer, read replicas
10,000 users → Auto-scaling, Redis cluster, CDN, load balancers
100,000 users → Microservices, sharding, multi-region
```

### The Cost of Not Scaling

| Problem | Impact | Recovery Time | Solo Founder Cost |
|---------|--------|---------------|-------------------|
| Site down during PH launch | Lose 80% of launch traffic | 1-4 hours (if you catch it) | Weeks of marketing effort gone |
| Slow page loads | 40% bounce rate increase | Fix as you notice it | Every visitor is a potential customer |
| Database crash | Complete outage | 2-24 hours (restore from backup) | Trust destroyed, revenue lost |
| Data corruption | Unrecoverable data loss | Days to weeks | Legal, reputation, customer loss |

## Phase 1: Foundation Stack (100-1,000 Users)

### The Solo Founder's Starter Stack

For most solo founders starting out, this stack handles 100-1,000 users without issue:

```
Frontend: Vercel (Next.js/React) or Netlify (static site)
Backend: Single server on Railway, Render, Fly.io, or DigitalOcean
Database: Managed PostgreSQL (Supabase, Railway, Neon) or managed MySQL
Caching: In-memory on the application server
File Storage: S3 or R2 (Cloudflare)
Email: SendGrid, Resend, or SES
Monitoring: Sentry (errors) + PostHog (analytics)
CDN: Cloudflare (free tier)
```

**Why this works:**
- Managed services handle backups, scaling, and maintenance
- You don't need to be a DevOps expert
- Cost is low ($50-200/month total)
- Can scale to 1,000+ users without changes

### Critical Configuration for Starter Stack

**1. Database Connection Pooling**

Without pooling, every request opens a new database connection. With 100 concurrent users, this kills your database.

```javascript
// Use PgBouncer or built-in pooling
// Example with Prisma + Supabase:

import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  // Connection pooling configuration
  // Limit connections to avoid overwhelming the database
  connectionLimit: 10,
  // Timeout for queries
  queryTimeout: 5000,
})

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

**2. Database Indexing**

Indexing is the single highest-impact optimization for a solo founder. A missing index can make a query take 5 seconds instead of 5ms.

```sql
-- ALWAYS index on:
-- 1. Foreign keys (user_id, team_id, etc.)
-- 2. Columns used in WHERE clauses
-- 3. Columns used in ORDER BY
-- 4. Columns used in JOIN conditions
-- 5. Columns used in GROUP BY

-- Check for missing indexes:
SELECT 
  relname,
  seq_scan - idx_scan AS too_much_seq,
  seq_scan,
  idx_scan
FROM pg_stat_user_tables
WHERE seq_scan - idx_scan > 1000
ORDER BY seq_scan - idx_scan DESC;

-- Common indexes for a typical SaaS:
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_teams_owner ON teams(owner_id);
CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_usage_logs_user_date ON usage_logs(user_id, created_at);
```

**3. N+1 Query Prevention**

The N+1 problem is the most common performance killer in SaaS apps.

```javascript
// BAD: N+1 queries
const users = await db.user.findMany()
for (const user of users) {
  const posts = await db.post.findMany({ where: { userId: user.id } })
  // This runs N queries for N users
}

// GOOD: Single query with include
const users = await db.user.findMany({
  include: { posts: true }
})

// Or batch loading (DataLoader pattern)
const userPosts = await db.post.findMany({
  where: { userId: { in: users.map(u => u.id) } }
})
```

**4. Static Page Caching**

For pages that don't change per user (marketing pages, docs, blog):

```javascript
// Next.js static generation
export async function getStaticProps() {
  const data = await fetchExpensiveData()
  return {
    props: { data },
    revalidate: 60 // Regenerate every 60 seconds
  }
}

// Or use ISR (Incremental Static Regeneration)
// This gives you static performance with dynamic updates
```

**5. Asset Optimization**

```javascript
// next.config.js
module.exports = {
  images: {
    formats: ['image/webp', 'image/avif'],
  },
  // Enable gzip/brotli compression
  compress: true,
  // Automatic code splitting
  // Tree shaking for production builds
}
```

## Phase 2: Caching Strategy (1,000-10,000 Users)

### The Caching Hierarchy

As traffic grows, caching becomes essential. Implement caching at multiple levels:

```
Level 1: Browser Cache (fastest, zero cost)
  - Cache static assets (JS, CSS, images) in the browser
  - Set far-future Cache-Control headers

Level 2: CDN Cache (fast, low cost)
  - Cache full pages or assets at edge locations
  - Cloudflare, Fastly, or Vercel Edge

Level 3: Application Cache (fast, moderate cost)
  - Cache rendered HTML or API responses
  - Vercel Data Cache, Rails fragment caching

Level 4: Database Cache (medium, moderate cost)
  - Cache frequently accessed query results
  - Redis, Memcached, or in-memory cache
```

### Implementing Redis Caching

Redis is the most common caching solution for growing SaaS products.

```javascript
// Cache-aside pattern (most common):

async function getUserData(userId: string) {
  const cacheKey = `user:${userId}:data`
  
  // 1. Try cache first
  const cached = await redis.get(cacheKey)
  if (cached) return JSON.parse(cached)
  
  // 2. Cache miss — query database
  const user = await db.user.findUnique({
    where: { id: userId },
    include: { subscriptions: true, teams: true }
  })
  
  // 3. Store in cache with TTL
  await redis.setex(cacheKey, 300, JSON.stringify(user)) // 5 min TTL
  
  return user
}
```

**What to Cache (by priority):**

| Data | Cache Duration | Reason |
|------|---------------|--------|
| User session | 1 hour | Very stable, expensive to query |
| Product catalog/features | 1 day | Rarely changes |
| Pricing page data | 1 day | Rarely changes |
| User preferences | 1 hour | Relatively stable |
| Dashboard metrics | 5 minutes | Acceptable staleness |
| Search results | 1-5 minutes | Low precision requirement |
| User list (admin) | 1 minute | Balance fresh vs. performance |

**What NOT to Cache:**
- User-specific financial data (invoices, billing)
- Real-time status or availability
- Any data that must be immediately consistent

### Cache Invalidation

Cache invalidation is one of the hardest problems in computer science. Simple strategies:

```javascript
// Strategy 1: Time-based expiration (easiest)
await redis.setex(key, TTL, value)
// Product automatically expires

// Strategy 2: Cache-aside with manual invalidation
async function invalidateUserCache(userId: string) {
  await redis.del(`user:${userId}:data`)
  await redis.del(`user:${userId}:dashboard`)
}

// Strategy 3: Versioned keys
const CACHE_VERSION = 2
const key = `v${CACHE_VERSION}:user:${userId}`

// Bumping the version invalidates ALL caches of that type
// Useful when you deploy a change that affects many cached values
```

### Database Query Caching

```javascript
// Cache expensive queries with parameterized keys

async function getDashboardStats(teamId: string, period: string) {
  const cacheKey = `dashboard:${teamId}:${period}`
  
  const cached = await redis.get(cacheKey)
  if (cached) return JSON.parse(cached)
  
  // Expensive query
  const stats = await db.$queryRaw`
    SELECT 
      COUNT(*) as total,
      SUM(amount) as revenue,
      DATE_TRUNC('day', created_at) as date
    FROM transactions
    WHERE team_id = ${teamId}
      AND created_at > NOW() - INTERVAL '1 ${period}'
    GROUP BY DATE_TRUNC('day', created_at)
  `
  
  await redis.setex(cacheKey, 300, JSON.stringify(stats))
  return stats
}
```

## Phase 3: Database Scaling (5,000+ Users)

### The Solo Founder's Database Scaling Path

```
Stage 1: Single instance (starter)
  - Managed PostgreSQL/MySQL on cloud
  - Up to 1,000 concurrent users
  - Cost: $10-50/month

Stage 2: Read replicas (growth)
  - One primary for writes, 1-2 replicas for reads
  - Up to 5,000+ concurrent users
  - Cost: $50-200/month

Stage 3: Connection pooling (heavy growth)
  - PgBouncer or built-in pooler
  - Handles thousands of concurrent connections
  - Cost: Included with managed DB or $10-20/month

Stage 4: Vertical scaling (peak growth)
  - More RAM, faster CPU on database instance
  - Can handle 10K+ users temporarily
  - Cost: $200-500/month

Stage 5: Horizontal sharding (enterprise)
  - Distribute data across multiple databases
  - Complex, rare for solo founders
  - Only when you have millions of users
```

### Read Replicas Setup

```javascript
// Prisma read replica configuration
// Works with Prisma 4.10+

import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL // Primary (write)
    }
  }
})

// Read replica for read operations
const prismaRead = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_READ_URL // Replica (read)
    }
  }
})

// Use prisma for writes, prismaRead for reads
// For reads that need immediate consistency, use primary
```

### Query Optimization for Scale

```sql
-- 1. Use EXPLAIN ANALYZE to find slow queries
EXPLAIN ANALYZE
SELECT * FROM orders 
WHERE user_id = 'abc' 
  AND created_at > NOW() - INTERVAL '30 days';

-- 2. Add partial indexes for common query patterns
CREATE INDEX idx_active_subscriptions 
ON subscriptions(user_id) 
WHERE status = 'active';

-- 3. Use materialized views for expensive aggregations
CREATE MATERIALIZED VIEW monthly_revenue AS
SELECT 
  DATE_TRUNC('month', created_at) as month,
  SUM(amount) as revenue
FROM invoices
WHERE status = 'paid'
GROUP BY DATE_TRUNC('month', created_at);

-- Refresh periodically
REFRESH MATERIALIZED VIEW monthly_revenue;

-- 4. Archive old data
-- Move data older than 12 months to a separate table
-- Or use PostgreSQL partitioning
CREATE TABLE orders_2024 PARTITION OF orders
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

### Connection Pool Configuration

```javascript
// With node-postgres
const { Pool } = require('pg')

const pool = new Pool({
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20, // Maximum connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})

// For serverless (Vercel, Lambda)
// Use Prisma Data Proxy or pgBouncer connection pooling
// Serverless creates many connections — pooling is essential
```

## Phase 4: CDN and Load Balancing (10,000+ Users)

### CDN Strategy

A CDN (Content Delivery Network) caches your content at edge locations worldwide. This is the single highest-ROI infrastructure investment.

**Cloudflare Setup (Free tier is excellent):**

```
1. Add your domain to Cloudflare
2. Update nameservers (takes 5-10 minutes)
3. Enable these features:
   - Auto Minify (HTML, CSS, JS)
   - Brotli compression
   - Rocket Loader (async JS loading)
   - Polish (image optimization)
   - Argo Smart Routing (paid, but worth it)
4. Set caching rules:
   - Static assets: Cache for 1 year
   - HTML pages: Cache for 1 hour (or use bypass)
   - API routes: Bypass cache (dynamic content)
```

**Cache Rules for Cloudflare:**

```
Page Rules (Cloudflare):

1. yourdomain.com/wp-content/* → Cache Everything → Edge Cache TTL: 1 year
2. yourdomain.com/static/* → Cache Everything → Edge Cache TTL: 1 year
3. yourdomain.com/api/* → Cache Level: Bypass
4. yourdomain.com/* → Cache Level: Standard → Edge Cache TTL: 1 hour
```

**For Next.js/Vercel deployments:**

Vercel's Edge Network is already a global CDN. Optimize it:

```javascript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=0, must-revalidate',
          },
        ],
      },
      {
        source: '/_next/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      {
        source: '/static/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
    ]
  },
}
```

### Load Balancing

When a single server isn't enough:

**Option 1: Platform-Level (Easiest)**
- Vercel, Railway, Fly.io, Render handle load balancing automatically
- Just enable multiple instances
- Cost: Included in higher-tier plans

**Option 2: Application-Level (Medium)**
```yaml
# docker-compose.yml with multiple app instances
version: '3'
services:
  app:
    build: .
    replicas: 3  # Run 3 instances
    environment:
      - DATABASE_URL=postgres://...
  nginx:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

**Option 3: Cloud Load Balancer (Advanced)**
- AWS ALB, Google Cloud LB, DigitalOcean LB
- Distributes traffic across multiple servers
- Health checks, auto-scaling, SSL termination
- Cost: $15-30/month + server costs

### Auto-Scaling Configuration

```yaml
# Example: Render auto-scaling config
services:
  - type: web
    name: my-app
    env: node
    scaling:
      minInstances: 1
      maxInstances: 5
      targetMemoryPercent: 70
      targetCPUPercent: 70
```

**Auto-scaling triggers:**
- CPU > 70% for 5 minutes → Add instance
- Memory > 70% for 5 minutes → Add instance
- Response time > 500ms for 5 minutes → Add instance
- Request queue depth > 100 → Add instance

## Phase 5: Monitoring and Alerting

### What to Monitor

As a solo founder, you can't monitor everything. Focus on:

```
1. Uptime (is the site accessible?)
   Tool: Better Uptime, Checkly, or UptimeRobot (free)
   Alert: SMS/call if down for 1+ minute

2. Error rate (are users hitting errors?)
   Tool: Sentry (free tier)
   Alert: Email for 1%+ error rate
   
3. Response time (is the site fast?)
   Tool: PostHog or custom monitoring
   Alert: If P95 > 2 seconds
   
4. Database connections (is DB overloaded?)
   Tool: Cloud dashboard or custom monitoring
   Alert: If > 80% of max connections
   
5. Disk space (is storage full?)
   Tool: Cloud dashboard
   Alert: If > 80% full
```

### The Solo Founder's Monitoring Stack

```yaml
Monitoring Stack ($0-50/month):

1. Better Uptime (free): Uptime monitoring, checks every 5 min
2. Sentry (free): Error tracking, performance monitoring
3. PostHog (free): Product analytics, session recording
4. Grafana + Prometheus ($0): Custom metrics dashboard
5. PagerDuty/OnCall (free tier): Alert routing

Or use a single provider:
- Checkly (synthetic monitoring, $15/mo)
- Datadog (full stack, expensive but powerful)
- New Relic (full stack, free tier limited)
```

### Setting Up Alerts That Matter

As a solo founder, you can't respond to every alert. Be selective:

```javascript
// Alert only when:
// 1. Site is down for 2+ minutes → Ping you (SMS/call)
// 2. Error rate > 5% for 5 minutes → Email + SMS
// 3. Database connections > 80% → Email
// 4. P95 response time > 3 seconds → Email
// 5. Disk space > 85% → Email
// 6. Payment failures > 10 in 1 hour → Email + SMS

// NOT alert-worthy:
// - Single 500 error (unless from payment processing)
// - Occasional slow request
// - Normal traffic spikes
// - Individual user errors
```

## Phase 6: Backup and Disaster Recovery

### Backup Strategy

A solo founder without backups is one server crash away from losing their business.

```
Backup Tiers:

Critical (must never lose):
  - User data
  - Subscription/billing data
  - Configuration

Important (would be very painful):
  - Usage data
  - Content/user-generated data
  - Analytics data

Recoverable from code:
  - Application code (in Git)
  - Infrastructure config (infrastructure as code)
  - Documentation
```

### Backup Schedule

```yaml
Daily:
  - Full database backup → S3/R2
  - User-generated content → S3/R2

Weekly:
  - Full database backup → different region
  - Application logs → S3/R2 (for debugging)

Monthly:
  - Full database backup → cold storage (Glacier/Deep Archive)
  - Configuration backups → encrypted storage
```

### Disaster Recovery Plan

Document and test this:

```
Scenario 1: Database corrupted
1. Stop application (prevent further corruption)
2. Restore database from latest clean backup
3. Run integrity checks
4. Restart application
5. Notify users of data loss (if any)
ETA: 1-4 hours

Scenario 2: Server failure
1. Spin up new instance from saved image/terraform
2. Point DNS to new instance
3. Verify all services running
4. Scale if needed
ETA: 10-30 minutes (if automated)

Scenario 3: Cloud provider outage
1. Activate backup in secondary region
2. Update DNS to secondary region
3. Verify data integrity
4. Monitor primary region recovery
ETA: 30 minutes to 4 hours

Scenario 4: Security breach
1. Isolate compromised systems
2. Rotate all credentials/API keys
3. Restore from pre-breach backup
4. Investigate breach source
5. Notify affected users
ETA: 2-24 hours
```

### Automated Backup Script

```bash
#!/bin/bash
# Automated backup script for solo founder

# Configuration
DB_URL="${DATABASE_URL}"
BACKUP_DIR="/backups/$(date +%Y-%m-%d)"
S3_BUCKET="s3://myapp-backups"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
echo "Backing up database..."
pg_dump "$DB_URL" > "$BACKUP_DIR/database.sql"
gzip "$BACKUP_DIR/database.sql"

# Backup user uploads
echo "Backing up user uploads..."
aws s3 sync s3://myapp-uploads "$BACKUP_DIR/uploads/"

# Upload to backup storage
echo "Uploading to S3..."
aws s3 sync "$BACKUP_DIR" "$S3_BUCKET/$(date +%Y-%m-%d)"

# Rotate old backups (keep 30 days)
find /backups -type d -mtime +30 -exec rm -rf {} \;

# Clean up old S3 backups
aws s3 ls "$S3_BUCKET/" | while read -r line; do
  date=$(echo "$line" | awk '{print $1}')
  if [[ $(date -d "$date" +%s) -lt $(date -d "30 days ago" +%s) ]]; then
    aws s3 rm "s3://myapp-backups/$date/" --recursive
  fi
done

echo "Backup complete: $(date)"
```

## Infrastructure Scaling Decision Tree

```
Is your site slow or crashing? 
├── Yes → 
│   Is the database CPU high? →
│   ├── Yes → Add read replica or optimize queries
│   ├── No → Is app server CPU high? →
│   │   ├── Yes → Scale app horizontally (add instances)
│   │   ├── No → Is CDN cache hit rate low? →
│   │   │   ├── Yes → Improve caching strategy
│   │   │   ├── No → Check for memory leaks or blocking operations
│   │   │   └── No → Is database connection pool exhausted? →
│   │   │       ├── Yes → Increase pool size or add PgBouncer
│   │   │       └── No → Check network/cloud provider issues
│   └── No → Check disk I/O, network, or external API latency
└── No → 
    Are you expecting growth soon? →
    ├── Yes → Pre-optimize (add caching, read replicas, CDN)
    └── No → Monitor, don't change what works
```

## Infrastructure Cost Optimization

As a solo founder, cost matters. Don't over-provision.

| Service | Starter ($50/mo) | Growth ($200/mo) | Scale ($500/mo) |
|---------|------------------|-------------------|-----------------|
| Hosting | Vercel Hobby ($0) | Vercel Pro ($20) | Railway Pro ($50) |
| Database | Supabase Free ($0) | Neon Scale ($19) | RDS ($100+) |
| CDN | Cloudflare Free ($0) | Cloudflare Pro ($20) | Cloudflare Biz ($200) |
| Cache | In-app memory | Redis (Upstash $0) | Redis Cluster ($30) |
| Monitoring | Sentry Free + Better Uptime ($0) | Sentry Team ($26) | Datadog ($80+) |
| Email | Resend Free ($0) | SendGrid ($20) | SES + dedicated IP ($50+) |
| Object Storage | R2 Free (10GB) | R2 ($0.01/GB) | R2 ($1+/GB) |
| Total | $0-50 | $85-125 | $400+ |

## The Solo Founder's Infrastructure Checklist

### Monthly
- [ ] Check database slow query log (EXPLAIN ANALYZE)
- [ ] Review error rates in Sentry
- [ ] Check disk space on all servers
- [ ] Verify backups ran successfully
- [ ] Review cloud provider costs
- [ ] Check for security updates (libraries, OS)

### Quarterly
- [ ] Load test your application (Artillery or k6)
- [ ] Review database indexes for missing ones
- [ ] Review CDN cache hit rate
- [ ] Audit API response times (P50, P95, P99)
- [ ] Test disaster recovery (restore from backup)
- [ ] Review and prune old data

### Before Major Events (Launch, PR, Viral Campaign)
- [ ] Scale up infrastructure (double capacity temporarily)
- [ ] Enable higher logging/alerting sensitivity
- [ ] Pre-warm CDN cache
- [ ] Review error monitoring dashboards
- [ ] Have rollback plan ready
- [ ] Have someone on-call (even a friend to monitor)

## Key Metrics Dashboard

Create a simple dashboard you check daily:

```
INFRASTRUCTURE DASHBOARD

Uptime (30 days): ___%
P50 response time: ___ms (target: < 200ms)
P95 response time: ___ms (target: < 1000ms)
Error rate: ___% (target: < 1%)
Database CPU: ___% (target: < 50%)
Database connections: ___ / ___ (target: < 70%)
CDN cache hit rate: ___% (target: > 70%)
App server CPU: ___% (target: < 50%)
App server memory: ___% (target: < 70%)
Disk space: ___% (target: < 70%)
Cost this month: $___ (budget: $___)
```

## Tools Reference

| Category | Tool | Free Tier | Notes |
|----------|------|-----------|-------|
| Hosting | Vercel | Yes | Next.js optimized |
| Hosting | Railway | $5/mo | Simple, full-stack |
| Hosting | Render | Free tier | Good for APIs |
| Hosting | Fly.io | Free tier | Edge compute |
| Database | Supabase | Free | PostgreSQL + real-time |
| Database | Neon | Free | Serverless PostgreSQL |
| Database | PlanetScale | Free | MySQL-compatible |
| Cache | Upstash Redis | Free | Serverless Redis |
| Cache | Cloudflare KV | Free (limited) | Edge cache |
| CDN | Cloudflare | Free | Essential for any site |
| CDN | Bunny.net | $1/mo | Alternative, fast |
| Monitoring | Sentry | Free | Error tracking |
| Monitoring | PostHog | Free | Product + performance |
| Monitoring | Better Uptime | Free | Uptime monitoring |
| Monitoring | Grafana | Free | Custom dashboards |
| Backup | R2 | Free (10GB) | Object storage |
| Backup | Backblaze B2 | Free (10GB) | S3-compatible |
| Email | Resend | Free (100/day) | Transactional email |
| Security | Cloudflare WAF | Free | DDoS + firewall |

## Final Thoughts

- **Infrastructure is not optional.** It's as important as your product features. A slow or broken product loses customers.
- **Start simple, but have a growth path.** Don't over-engineer for 1M users, but know what you'll do when user 10,001 signs up.
- **Managed services are your friend.** As a solo founder, every hour you spend on DevOps is an hour not building product. Pay for managed services.
- **Backups are non-negotiable.** A solo founder without backups is gambling with their business.
- **Monitor before you need to.** Set up alerts before something breaks. Reactive debugging is stressful and slow.
- **Cost ≠ reliability.** Cloudflare's free tier is excellent. You don't need enterprise tools to be reliable.
- **Know when to upgrade.** When your response time degrades or errors increase, don't wait — scale up. The cost of downtime exceeds the cost of the upgrade.

Your infrastructure should be boring. If people are talking about your infrastructure (except to say "it's fast"), something went wrong. Build it right, automate what you can, and get back to building your product.
