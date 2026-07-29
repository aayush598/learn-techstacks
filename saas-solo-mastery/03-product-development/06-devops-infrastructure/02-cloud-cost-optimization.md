# Cloud Cost Optimization for Solo SaaS Founders

## The Cost Reality

As a solo founder, every dollar counts. Your cloud bill directly impacts your runway and your ability to keep the business running. The goal is to stay under $50/month in infrastructure costs during the early stages, while maintaining reliability and room to grow.

This guide covers every aspect of cloud cost optimization for solo founders, with specific strategies for each service category, hosting options, and cost monitoring.

## The $50/Month SaaS Budget

### What $50/Month Buys You

```markdown
MVP Stage ($0-20/mo):
  Hosting:      $0 (Vercel free tier)
  Database:     $0 (Supabase free tier, 500MB)
  Auth:         $0 (Clerk free tier, 10k users)
  Email:        $0 (Resend, 100 emails/day)
  Monitoring:   $0 (Sentry free tier)
  DNS:          $0 (Cloudflare)
  CDN:          $0 (Cloudflare)
  Total:        $0/month

Growth Stage ($20-50/mo):
  Hosting:      $5-20/mo (Railway basic)
  Database:     $0-15/mo (Supabase Pro or Neon)
  Auth:         $0-25/mo (Clerk or Supabase Auth)
  Email:        $0-10/mo (Resend growth tier)
  Monitoring:   $0-26/mo (Sentry team tier)
  DNS:          $0 (Cloudflare)
  CDN:          $0 (Cloudflare)
  Total:        $5-96/mo (stay under $50 by choosing wisely)

Scale Stage ($50-200/mo):
  When you have revenue to support it.
  At this point, cost optimization becomes less critical.
```

## Hosting Cost Optimization

### Platform Comparison by Cost

```markdown
| Platform     | Starting Cost | What You Get              | Best For              |
|--------------|--------------|---------------------------|-----------------------|
| Vercel       | $0           | 100GB bandwidth, functions | Next.js, frontend     |
| Railway      | $5/mo        | $5 credit, shared CPU     | Full-stack, simple    |
| Fly.io       | $0           | 3 shared VMs, 3GB storage | Docker apps           |
| Render       | $7/mo        | 512MB RAM, shared CPU     | Background services   |
| Hetzner VPS  | $4/mo        | 2 vCPU, 2GB RAM, 20GB SSD | Self-managed, cheap   |
| DigitalOcean | $6/mo        | 1 vCPU, 1GB RAM, 25GB SSD | VPS, full control     |
| Oracle Cloud | $0           | 4 vCPU, 24GB RAM (always free)| Best free VPS      |
| AWS Lightsail| $3.50/mo     | 512MB RAM, 1 vCPU         | AWS ecosystem         |
| Netlify      | $0           | 100GB bandwidth, functions | Static sites, JS apps |
| Cloudflare   | $0           | 100k requests/day Workers | Edge computing        |
```

### Hosting Cost Optimization Strategies

```markdown
Strategy 1: Start on Free Tiers
  - Vercel free tier supports most Next.js SaaS MVPs
  - Only upgrade when you hit limits (not before)
  - Limits: 100GB bandwidth, 60k function invocations on Vercel free

Strategy 2: Use a $4-6/mo VPS
  - Hetzner CX22: €3.79/mo (2 vCPU, 4GB RAM)
  - Single VPS can run: Postgres, Redis, Node.js app, nginx reverse proxy
  - Manage with docker-compose (simple, no k8s needed)

Strategy 3: Combine Free Tiers
  - Frontend on Vercel (free)
  - Backend on Railway ($5/mo)
  - Database on Supabase (free)
  - This splits the load and keeps things free where possible

Strategy 4: Use Spot/Preemptible Instances
  - AWS Spot, GCP Preemptible, Azure Spot
  - 60-90% discount on compute
  - Use for: background workers, batch processing, CI/CD runners
  - NOT for: web servers, databases (can be terminated anytime)

Strategy 5: Right-Size Your Instance
  - Most SaaS apps (0-10k users) run fine on a $6/mo VPS
  - Start small, monitor usage, scale up only when needed
  - CPU/RAM usage under 50%? Downsize.
```

## Database Cost Optimization

### Database Hosting Costs

```markdown
| Service      | Free Tier        | Paid Start      | Cost Optimization         |
|--------------|------------------|-----------------|---------------------------|
| Supabase     | 500MB, 2GB RAM   | $25/mo (8GB)    | Free tier is generous     |
| Neon         | 0.5GB, compute   | $19/mo (3GB)    | Pay-per-compute, cheap    |
| Railway      | $5 credit        | $5/mo           | Cheap, simple             |
| Render       | 256MB RAM        | $7/mo (1GB)     | Affordable managed DB     |
| AWS RDS      | Free tier (1yr)  | $15/mo (1GB)    | Free for first year       |
| DigitalOcean | None             | $12/mo (1GB)    | Simple, no free tier      |
| PlanetScale  | 1GB storage      | $29/mo (10GB)   | Expensive for solo        |
| TiDB         | Free tier        | $20/mo          | Serverless, MySQL-compat  |
| Aiven        | None             | $19/mo (Postgres)| Good for managed          |
| Hetzner      | None             | $0 (self-host)  | Cheapest: run on same VPS |
```

### Database Cost Optimization Strategies

```markdown
Strategy 1: Start with Supabase Free Tier
  - 500MB database, free for up to 50k rows
  - Includes auth, storage, and real-time
  - Upgrade to Pro ($25/mo) only when you exceed limits

Strategy 2: Self-Host on Your VPS
  - Run PostgreSQL on the same server as your app
  - Zero additional cost (use Hetzner $4/mo VPS)
  - Setup: docker run postgres:16 (5 minutes)
  - Backup: pg_dump to S3-compatible storage (automated)

Strategy 3: Connection Pooling
  - Use PgBouncer or built-in pooling (Supabase, Neon)
  - Reduces number of database connections
  - Prevents "too many connections" errors without upgrading

Strategy 4: Query Optimization
  - Add indexes for frequently queried columns
  - Use EXPLAIN ANALYZE to find slow queries
  - Avoid N+1 queries (use eager loading)
  - Cache expensive queries with in-memory cache
  - A well-optimized query can save you from needing a bigger DB

Strategy 5: Data Retention and Archiving
  - Delete or archive old data
  - Partition large tables by date
  - Move historical data to cheaper storage
  - Example: Keep 90 days of logs, archive older ones to S3
```

### Self-Hosted PostgreSQL Cost Example

```yaml
# docker-compose.yml - Single server, zero additional DB cost
version: '3.8'
services:
  app:
    build: .
    ports: ['3000:3000']
    depends_on: [db]
    environment:
      DATABASE_URL: postgresql://app:password@db:5432/app

  db:
    image: postgres:16-alpine  # Smaller image
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: password
    # No exposed port - only accessible internally
    # Save $5/mo by not using managed DB
    deploy:
      resources:
        limits:
          memory: 512M  # Limit memory usage

volumes:
  pgdata:
```

## Third-Party Service Cost Optimization

### Free Tier Maximization

```markdown
Service         | Free Tier Limit                | Upgrade When
----------------|--------------------------------|------------------------------
Auth (Clerk)    | 10,000 users                   | 10k+ monthly active users
Database (Supabase)| 500MB, 2GB RAM, 50k rows    | Exceed any limit
Email (Resend)  | 100 emails/day                 | 3k+ emails/month
Errors (Sentry) | 5,000 events/month             | 5k+ errors/month
Logs (Axiom)    | 5TB/month, 30-day retention    | Exceed 5TB/month
Uptime (Better) | 1 monitor, 5 minute intervals  | Need more monitors
CDN (Cloudflare)| Unlimited bandwidth            | Need advanced rules
Analytics (PostHog)| 1M events/month            | 1M+ events/month
Hosting (Vercel)| 100GB bandwidth, 60k functions | Exceed limits
File Storage (R2)| 10GB, 1M write/month         | Exceed storage
Search (Meilisearch)| 10k docs, 4GB storage     | Exceed document count
```

### Service Cost Optimization Table

```markdown
Service             | Premium Option         | Budget Alternative        | Savings
--------------------|------------------------|---------------------------|---------
Error Monitoring    | Datadog ($15/mo+)      | Sentry (free)             | $15+/mo
Logging             | Datadog Logs ($15/mo+) | Axiom (free 5TB)          | $15+/mo
Analytics           | Mixpanel ($28/mo)      | PostHog self-host (free)  | $28/mo
Email               | SendGrid ($20/mo)      | Resend (100/day free)     | $20/mo
Monitoring          | Datadog ($15/mo+)      | Better Uptime (free)      | $15+/mo
CDN                 | Fastly ($50/mo)        | Cloudflare (free)         | $50/mo
Database            | RDS ($15/mo)           | Supabase/Neon (free)      | $15/mo
Search              | Algolia ($50/mo)       | Meilisearch self-host     | $49/mo
Forms               | Typeform ($25/mo)      | Tally (free)              | $25/mo
Support             | Intercom ($39/mo)      | Crisp (free)              | $39/mo
Feature Flags       | LaunchDarkly ($80/mo)  | PostHog (free tier)       | $80/mo
Total Potential Savings:                          |                          | $340+/mo
```

## Cost Monitoring

### Simple Cost Dashboard

```typescript
// lib/monitoring/costs.ts

interface ServiceCost {
  name: string;
  plan: string;
  monthlyCost: number;
  usagePercent: number; // % of free tier used
  estimatedBill: number;
  nextTierCost: number;
}

class CostMonitor {
  private services: ServiceCost[] = [];

  addService(service: ServiceCost) {
    this.services.push(service);
  }

  getTotalCost(): number {
    return this.services.reduce((sum, s) => sum + s.estimatedBill, 0);
  }

  getServicesNearingLimit(): ServiceCost[] {
    return this.services.filter(s => s.usagePercent > 80);
  }

  getCostBreakdown(): string {
    let report = '=== Monthly Cloud Costs ===\n';
    let total = 0;

    for (const service of this.services) {
      report += `${service.name} (${service.plan}): $${service.estimatedBill}/mo`;
      if (service.usagePercent > 80) {
        report += ` ⚠️ Nearing limit (${service.usagePercent}%)`;
      }
      report += '\n';
      total += service.estimatedBill;
    }

    report += `\nTotal: $${total}/mo`;
    return report;
  }

  async sendWeeklyReport() {
    const report = this.getCostBreakdown();
    if (this.getTotalCost() > 50) {
      await sendEmail({
        to: process.env.ADMIN_EMAIL!,
        subject: '⚠️ Cloud costs exceeded $50/mo',
        body: report,
      });
    } else {
      await sendEmail({
        to: process.env.ADMIN_EMAIL!,
        subject: 'Monthly Cost Report',
        body: report,
      });
    }
  }
}

export const costMonitor = new CostMonitor();
```

### Cloud Provider Cost Alerts

```bash
# AWS Budget Alert
aws budgets create-budget \
  --account-id $ACCOUNT_ID \
  --budget '{
    "BudgetName": "monthly-budget",
    "BudgetLimit": { "Amount": 50, "Unit": "USD" },
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST",
    "CostFilters": {},
    "CostTypes": {
      "IncludeTax": true,
      "IncludeSubscription": true,
      "UseBlended": false,
      "IncludeRefund": false,
      "IncludeCredit": false,
      "IncludeUpfront": true,
      "IncludeRecurring": true,
      "IncludeOtherSubscription": true,
      "IncludeSupport": true,
      "IncludeDiscount": true,
      "UseAmortized": false
    },
    "NotificationWithSubscribers": [{
      "Notification": {
        "ComparisonOperator": "GREATER_THAN",
        "Threshold": 80,
        "ThresholdType": "PERCENTAGE",
        "NotificationType": "ACTUAL"
      },
      "Subscribers": [{
        "SubscriptionType": "EMAIL",
        "Address": "you@example.com"
      }]
    }]
  }'

# GCP Budget Alert
gcp_budget() {
  gcloud billing budgets create \
    --billing-account=$BILLING_ACCOUNT \
    --display-name="monthly-budget" \
    --budget-amount=50usd \
    --threshold-rule=percent=0.5 \
    --threshold-rule=percent=0.8 \
    --threshold-rule=percent=1.0 \
    --notifications-rule-pubsub-topic=budget-alerts \
    --notifications-rule-schema=basic
}
```

## Specific Cost Optimization Patterns

### Pattern 1: Serverless Functions Warmth

```markdown
Serverless cold starts waste money (and time).

Optimizations:
1. Keep functions warm with pings (if free tier allows)
   - Set up a cron job to call functions every 5 minutes
   - BUT: this uses function invocations, may cost more

2. Use provisioned concurrency (if your platform supports it)
   - Keeps N instances warm
   - Costs money for idle time
   - Worth it for latency-critical endpoints

3. Bundle functions optimally
   - Too many small functions = more cold starts
   - Fewer larger functions = fewer cold starts
   - Balance based on your usage pattern

4. Use edge functions when possible
   - Cloudflare Workers, Vercel Edge
   - Near-zero cold start times
   - Often cheaper than serverless functions
```

### Pattern 2: Database Connection Management

```javascript
// BAD: Opening a new connection for every request
app.get('/api/users', async (req, res) => {
  const pool = new Pool({ connectionString: DATABASE_URL });
  const result = await pool.query('SELECT * FROM users');
  await pool.end();
  res.json(result.rows);
});
// This wastes connections and is slow

// GOOD: Connection pooling
const pool = new Pool({
  connectionString: DATABASE_URL,
  max: 10,            // Max connections
  idleTimeoutMillis: 30000,  // Close idle connections
  connectionTimeoutMillis: 2000,  // Fail fast
});

app.get('/api/users', async (req, res) => {
  const client = await pool.connect();
  try {
    const result = await client.query('SELECT * FROM users');
    res.json(result.rows);
  } finally {
    client.release();
  }
});

// Connection pooling saves money by:
// - Requiring fewer database resources (smaller instance)
// - Preventing connection exhaustion errors
// - Reducing database CPU usage
```

### Pattern 3: Asset Compression and Optimization

```bash
# Optimize images before uploading
# BAD: Uploading raw images from users
# Users upload 5MB photos that cost storage + bandwidth

# GOOD: Compress and resize on upload
# Use sharp (Node.js) or similar

#!/bin/bash
# scripts/optimize-images.sh
# Run on CI or as webhook

for img in uploads/*.{jpg,png}; do
  # Resize to max 1200px width
  convert $img -resize 1200x1200\> -quality 80 -strip $img
done

# Benefits:
# - 80% reduction in image size (5MB → 300KB)
# - 80% reduction in storage costs
# - 80% reduction in CDN bandwidth
# - Faster page loads for users
```

### Pattern 4: Cache Everything Cachable

```typescript
// lib/cache/response-cache.ts
// Cache API responses to reduce compute and database load

class ResponseCache {
  private cache: Map<string, { data: any; expiresAt: number }>;
  private defaultTTL: number;

  constructor(defaultTTLMs = 60000) { // 1 minute default
    this.cache = new Map();
    this.defaultTTL = defaultTTLMs;
  }

  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttlMs?: number
  ): Promise<T> {
    const cached = this.cache.get(key);
    if (cached && Date.now() < cached.expiresAt) {
      return cached.data;
    }

    const data = await fetcher();
    this.cache.set(key, {
      data,
      expiresAt: Date.now() + (ttlMs || this.defaultTTL),
    });

    return data;
  }

  invalidate(pattern: string) {
    for (const key of this.cache.keys()) {
      if (key.includes(pattern)) {
        this.cache.delete(key);
      }
    }
  }
}

// Usage
const cache = new ResponseCache();

app.get('/api/stats', async (req, res) => {
  const stats = await cache.getOrSet(
    'dashboard-stats',
    () => computeExpensiveStats(req.user.tenantId),
    5 * 60 * 1000  // Cache for 5 minutes
  );
  res.json(stats);
});
```

### Pattern 5: Database Query Optimization

```sql
-- BAD: Slow queries that waste database CPU
SELECT * FROM projects
  JOIN tasks ON projects.id = tasks.project_id
  JOIN users ON projects.owner_id = users.id
  WHERE projects.tenant_id = 'abc'
  ORDER BY projects.created_at;

-- GOOD: Add indexes for common query patterns
CREATE INDEX idx_projects_tenant_created
  ON projects(tenant_id, created_at DESC);
CREATE INDEX idx_tasks_project
  ON tasks(project_id);
CREATE INDEX idx_users_tenant_id
  ON users(tenant_id);

-- GOOD: Only select columns you need
SELECT p.id, p.name, p.created_at,
       COUNT(t.id) as task_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
WHERE p.tenant_id = 'abc'
GROUP BY p.id
ORDER BY p.created_at DESC;

-- GOOD: Use pagination to limit result sets
SELECT p.id, p.name
FROM projects p
WHERE p.tenant_id = 'abc'
  AND p.id > $1  -- Cursor-based pagination
ORDER BY p.id
LIMIT 20;
```

### Pattern 6: Right-Sizing Background Jobs

```javascript
// BAD: Polling every 5 seconds (wasteful)
setInterval(async () => {
  const jobs = await db.query('SELECT * FROM job_queue WHERE status = 'pending'');
  for (const job of jobs.rows) {
    await processJob(job);
  }
}, 5000);

// GOOD: Use LISTEN/NOTIFY (PostgreSQL) or push-based queues
// Only process when there's work to do

// Worker setup:
const pool = new Pool({ connectionString: DATABASE_URL });

// Listen for notifications
pool.on('notification', async (msg) => {
  if (msg.channel === 'new_job') {
    const jobs = await pool.query(
      `SELECT * FROM job_queue
       WHERE status = 'pending'
       ORDER BY created_at
       FOR UPDATE SKIP LOCKED
       LIMIT 1`
    );
    if (jobs.rows.length > 0) {
      await processJob(jobs.rows[0]);
    }
  }
});

await pool.query('LISTEN new_job');

// Job creator sends notification
await pool.query('SELECT pg_notify('new_job', '')');
```

## Monthly Cost Budget Template

```markdown
## Monthly Cloud Budget

### Fixed Costs
Hosting:          $0-20/mo (Vercel free / Railway $5 / VPS $4)
Database:         $0-15/mo (Supabase free / Neon / self-host)
Domain:           $1/mo (annual billing, average)
Total Fixed:      $1-36/mo

### Variable Costs (Pay as You Grow)
Auth:             $0-25/mo (Clerk free up to 10k users)
Email:            $0-20/mo (Resend / SendGrid)
Monitoring:       $0-26/mo (Sentry free / team)
Logging:          $0-17/mo (Axiom free / Logtail)
Total Variable:   $0-88/mo

### Growth Budget ($50-100/mo Stage - Funded by Revenue)
Hosting:          $20-50/mo (Bigger VPS / Multiple services)
Database:         $15-25/mo (Managed Postgres)
Backup Storage:   $5-10/mo (S3 / R2)
CDN:              $0-20/mo (Cloudflare Pro)
Total Growth:     $40-105/mo

### Budget Rules
1. Stay under $50/mo until you have $500/mo MRR
2. Stay under $100/mo until you have $2000/mo MRR
3. Only spend 10-20% of revenue on infrastructure
4. Review costs every month
5. Downgrade services you're not fully utilizing
```

## Cost Optimization Checklist

```markdown
### Weekly (5 minutes)
[ ] Review any cost alerts from providers
[ ] Check usage % on free tier limits
[ ] Verify no unauthorized resources running

### Monthly (15 minutes)
[ ] Review total cloud spend
[ ] Check for unused resources (stopped servers, old snapshots)
[ ] Review bandwidth usage (unexpected spikes?)
[ ] Check database size (need to archive old data?)
[ ] Review API call volumes (any unexpected increases?)

### Quarterly (30 minutes)
[ ] Review all service tiers (still on the right plan?)
[ ] Check for new free tier offerings
[ ] Evaluate alternative providers
[ ] Review database query performance
[ ] Audit storage usage (clean up old files/data)

### Triggers to Upgrade
When ANY of these happen:
[ ] Hitting free tier limits regularly
[ ] Performance degradation due to resource limits
[ ] Losing customers due to reliability issues
[ ] Infrastructure cost > 20% of revenue
[ ] Spending more time on cost optimization than product
```

## The "Staying Under $50" Cheat Sheet

```markdown
Category        | Best Free Option           | Best $5-15 Option        | Best $15-50 Option
----------------|----------------------------|--------------------------|---------------------
Hosting         | Vercel (100GB free)        | Railway ($5/mo)          | Hetzner VPS ($4/mo)
Database        | Supabase (500MB free)      | Neon ($19 start)          | Railway DB ($5/mo)
Auth            | Clerk (10k users free)     | Supabase Auth ($25)       | Stay on free
Email           | Resend (100/day free)      | Resend ($20 growth)       | SES + Resend ($0)
Errors          | Sentry (5k events free)    | Sentry ($26 team)         | Sentry ($26)
Logs            | Axiom (5TB free)           | Axiom ($17)               | Axiom ($17)
Monitoring      | Better Uptime (1 mon free) | Better Uptime ($20)       | Checkly ($30)
DNS             | Cloudflare (free)          | Cloudflare (free)         | Cloudflare ($20)
CDN             | Cloudflare (free)          | Cloudflare (free)         | Cloudflare ($20)
Analytics       | PostHog (1m events free)   | Plausible ($9)            | PostHog ($30)
File Storage    | R2 (10GB free)             | R2 (pay as you go)        | R2 (pay as you go)
Forms           | Tally (free)               | Tally ($29)               | Fillout ($20)
Support         | Crisp (free)               | Crisp ($25)               | Intercom ($39)
Search          | Meilisearch self-host      | Typesense self-host       | Algolia ($50+)
Feature Flags   | PostHog (free)             | ConfigCat (free 10 flags) | LaunchDarkly ($80)
Jobs/Queues     | Inngest (free tier)        | Inngest ($20)             | Redis + Bull ($0)

Total:          | $0/mo                      | $0-15/mo                 | $0-50/mo
```

## The Cold Hard Truth

Most solo founders spend too much on infrastructure too early. Here's the reality check:

```markdown
Before 100 paying customers:
  - Database: Free tier (Supabase, Neon, or self-hosted)
  - Hosting: Free tier or $5/mo VPS
  - Monitoring: Free tier (Sentry + uptime)
  - Everything else: Free tiers
  - TOTAL: $0-20/mo

Before 1,000 paying customers:
  - Database: $15-25/mo (managed Postgres)
  - Hosting: $20/mo (bigger VPS or PaaS)
  - Monitoring: $26/mo (Sentry team)
  - Auth: $0-25/mo (Clerk or similar)
  - Email: $0-20/mo
  - TOTAL: $50-100/mo

You don't need:
  - Kubernetes (until you have a team managing it)
  - Load balancers (until you have multiple servers)
  - CDN (until you have global traffic)
  - APM tools (until you have performance problems)
  - Data warehouses (until you have data to analyze)

Spend your money on:
  1. Product development (your time)
  2. Customer acquisition (ads, content, outreach)
  3. Customer support (your time, or tools to help)

Not on:
  1. Premature infrastructure scaling
  2. Enterprise tooling for a startup
  3. "Just in case" capacity planning
```

## Summary

The goal of cloud cost optimization for solo founders is not to minimize costs at all costs — it's to match infrastructure spend to business stage. Here are the key principles:

1. **Start at $0/mo** — Use free tiers for everything in MVP stage
2. **Upgrade only when you hit limits** — Not before, not "just in case"
3. **Right-size everything** — Monitor usage, downsize when underutilized
4. **Cache aggressively** — Reduces both latency and cost
5. **Optimize databases first** — Slow queries cost more than bigger servers
6. **Avoid vendor lock-in** — Choose services that are easy to switch from
7. **Review monthly** — Costs creep up if you don't watch them
8. **Spend revenue, not runway** — Infrastructure costs should come from customer payments
9. **The $50/mo SaaS is achievable** — Most solo founders can run their entire stack for $0-50/mo
10. **Cost optimization is not penny-pinching** — It's resource allocation. Spend where it matters.
