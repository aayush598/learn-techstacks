# Automated Deployment Pipeline for Solo Founders

## The Deployment Philosophy

Automated deployments are non-negotiable for solo founders. Manual deploys waste time, introduce errors, and create fear around shipping. A proper deployment pipeline lets you ship multiple times per day with confidence, even when you're the only person on the team.

This guide covers deployment automation for solo founders: zero-downtime deploys, blue-green deployment, rollback strategies, and the complete pipeline from commit to production.

## The Deployment Pipeline

### Pipeline Overview

```
[Developer Push] → [CI Checks] → [Build] → [Deploy] → [Verify] → [Done]
     |                 |            |         |          |
  git push         lint + test   build     deploy    health check
  to main                        assets    to prod   + smoke test
```

### Minimal CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

env:
  NODE_VERSION: '20'
  PNPM_VERSION: '9'

jobs:
  quality:
    name: Quality Checks
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: app_test
        ports: ['5432:5432']

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run type checker
        run: npm run typecheck

      - name: Run database migrations
        run: npm run db:migrate
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/app_test

      - name: Run tests
        run: npm test
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/app_test
          NODE_ENV: test

  build:
    name: Build & Deploy
    needs: quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build
        env:
          NODE_ENV: production
          NEXT_PUBLIC_APP_URL: ${{ vars.APP_URL }}
          NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: ${{ vars.CLERK_PUBLISHABLE_KEY }}

      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway up --service ${{ vars.RAILWAY_SERVICE }}
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

      - name: Run database migrations
        run: |
          railway run --service ${{ vars.RAILWAY_SERVICE }} \
            "npm run db:migrate"
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

      - name: Health check
        run: |
          sleep 10
          curl -f ${{ vars.APP_URL }}/api/health || exit 1
```

## Zero-Downtime Deployments

### The Zero-Downtime Challenge

Zero-downtime deployment means users experience no interruption when you deploy new code. This requires:

1. **No dropped connections** — Existing users continue their sessions
2. **No 502 errors** — The application is always serving requests
3. **No data loss** — In-progress operations complete successfully
4. **Instant switch** — New requests go to the new version

### Strategy 1: Platform-Managed (Simplest)

```markdown
Platforms with built-in zero-downtime deploys:

1. Railway
   - Multiple instances, rolling update
   - Each instance is replaced one at a time
   - No configuration needed

2. Fly.io
   - Blue-green by default
   - New VM starts, accepts connections, old VM drains
   - Configurable via fly.toml

3. Vercel
   - Instant deployment with no downtime
   - Previous version serves until new version is ready
   - Automatic for all deployments

4. Render
   - Rolling deploy with health checks
   - New instances start before old ones are terminated
   - Configured in service settings

5. Heroku
   - Preboot feature for zero-downtime
   - New dynos receive traffic before old dynos are removed
   - Requires paid dynos
```

### Strategy 2: Docker Rolling Updates

```yaml
# railway.toml
# Railway handles zero-downtime automatically
[build]
  builder = "nixpacks"
  buildCommand = "npm run build"

[deploy]
  numReplicas = 2  # At least 2 for zero-downtime
  healthcheckPath = "/api/health"
  healthcheckTimeout = 30
  restartPolicyType = "always"

# fly.toml
[experimental]
  auto_rollback = true

[[services]]
  http_checks = []
  [[services.ports]]
    handlers = ["http"]
    port = 8080

  [services.concurrency]
    type = "connections"
    hard_limit = 25
    soft_limit = 20

  [[services.checks]]
    grace_period = "10s"
    interval = "15s"
    method = "get"
    path = "/api/health"
    protocol = "http"
    timeout = "5s"
```

### Strategy 3: VPS Blue-Green Deployment

For self-hosted VPS setups, implement blue-green deployment manually:

```bash
#!/bin/bash
# scripts/deploy-blue-green.sh
# Blue-green deployment for VPS

set -euo pipefail

APP_NAME="my-saas"
BLUE_PORT=3001
GREEN_PORT=3002
NGINX_CONFIG="/etc/nginx/sites-available/app"

# Determine current active color
if curl -s -f http://localhost:$BLUE_PORT/api/health > /dev/null 2>&1; then
  ACTIVE_COLOR="blue"
  IDLE_COLOR="green"
  IDLE_PORT=$GREEN_PORT
  ACTIVE_PORT=$BLUE_PORT
else
  ACTIVE_COLOR="green"
  IDLE_COLOR="blue"
  IDLE_PORT=$BLUE_PORT
  ACTIVE_PORT=$GREEN_PORT
fi

echo "Active: $ACTIVE_COLOR (port $ACTIVE_PORT)"
echo "Deploying to $IDLE_COLOR (port $IDLE_PORT)"

# 1. Build application
npm run build

# 2. Start new version on idle port
cp -r . /app/$IDLE_COLOR/
cd /app/$IDLE_COLOR
npm ci --production

# 3. Run migrations
NODE_ENV=production DATABASE_URL=$DATABASE_URL \
  npm run db:migrate

# 4. Start application on idle port
PORT=$IDLE_PORT NODE_ENV=production \
  pm2 start dist/index.js \
  --name "${APP_NAME}-${IDLE_COLOR}" \
  --update-env

# 5. Wait for health check
echo "Waiting for health check..."
for i in {1..30}; do
  if curl -s -f http://localhost:$IDLE_PORT/api/health > /dev/null 2>&1; then
    echo "Health check passed!"
    break
  fi
  if [ $i -eq 30 ]; then
    echo "Health check failed! Rolling back..."
    pm2 delete "${APP_NAME}-${IDLE_COLOR}"
    exit 1
  fi
  sleep 2
done

# 6. Switch nginx to new version
cat > $NGINX_CONFIG << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:$IDLE_PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

nginx -t && systemctl reload nginx

# 7. Stop old version
pm2 delete "${APP_NAME}-${ACTIVE_COLOR}"

echo "Deployment complete!"
echo "Now active: $IDLE_COLOR (port $IDLE_PORT)"
```

### Strategy 4: Database Migrations in Zero-Downtime

```typescript
// lib/database/migrate-safely.ts
// Run migrations without downtime

async function migrateSafely() {
  const client = await pool.connect();

  try {
    // Step 1: Run backward-compatible changes
    await client.query('BEGIN');

    // Add new columns (nullable)
    await client.query(`
      ALTER TABLE users
      ADD COLUMN IF NOT EXISTS display_name VARCHAR(255)
    `);

    // Add new indexes (concurrently, outside transaction)
    await client.query('COMMIT');

    // Step 2: Create new indexes (non-blocking)
    await client.query(`
      CREATE INDEX CONCURRENTLY IF NOT EXISTS
      idx_users_display_name ON users(display_name)
    `);

    // Step 3: Backfill data in batches
    await batchUpdate(
      'users',
      'display_name = email',
      'display_name IS NULL',
      [],
      1000
    );

    // Step 4: Make column NOT NULL (after ensuring all data is filled)
    await client.query('BEGIN');
    await client.query(`
      ALTER TABLE users ALTER COLUMN display_name SET NOT NULL
    `);
    await client.query('COMMIT');

    console.log('Migration completed safely!');
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

## Deployment Strategies

### Strategy A: Direct Deploy (MVP Stage)

```markdown
# Simplest approach for early stage

Flow:
  1. Push to main
  2. CI runs tests
  3. If tests pass, deploy to production
  4. Run migrations (if any)
  5. Health check

Downside: Brief downtime during deploy (seconds, not minutes)
Upside: Extremely simple

Best for: MVP stage, 0-100 users
```

### Strategy B: Rolling Deploy (Growth Stage)

```markdown
# Standard approach for most SaaS

Flow:
  1. Push to main
  2. CI runs tests
  3. Build new version
  4. Start new instance alongside old one
  5. Route new traffic to new instance
  6. Stop old instance

Downside: Requires multiple instances (costs more)
Upside: Zero downtime, easy rollback

Best for: 100-10k users, $50-500/mo infra
```

### Strategy C: Blue-Green Deploy (Scale Stage)

```markdown
# Full isolation between versions

Flow:
  1. Push to main
  2. CI runs tests
  3. Build new version on "green" environment
  4. Run migrations
  5. Run smoke tests on green
  6. Switch router from blue to green
  7. Keep blue running for rollback

Downside: Requires double infrastructure (2x cost during deploy)
Upside: Instant switch, easy rollback, pre-production validation

Best for: 10k+ users, critical uptime requirements
```

### Strategy D: Canary Deploy (Advanced)

```markdown
# Gradual traffic shift

Flow:
  1. Deploy new version to 1% of servers
  2. Monitor error rates and latency
  3. If healthy, increase to 10%, 50%, 100%
  4. If errors, rollback the canary

Downside: Complex, requires load balancer with traffic splitting
Upside: Minimizes blast radius of bad deploys

Best for: 100k+ users, large-scale systems
```

## Deployment Configuration

### Environment Configuration

```typescript
// config/deployment.ts
// Environment-aware configuration

interface DeploymentConfig {
  environment: 'development' | 'staging' | 'production';
  domain: string;
  database: {
    url: string;
    maxConnections: number;
    ssl: boolean;
  };
  redis?: {
    url: string;
  };
  features: {
    maintenance: boolean;
    debug: boolean;
    cacheEnabled: boolean;
  };
  logging: {
    level: 'debug' | 'info' | 'warn' | 'error';
    structured: boolean;
  };
  monitoring: {
    sentry: boolean;
    performance: boolean;
  };
}

function getDeploymentConfig(): DeploymentConfig {
  const env = process.env.NODE_ENV || 'development';

  const configs: Record<string, DeploymentConfig> = {
    development: {
      environment: 'development',
      domain: 'localhost:3000',
      database: {
        url: process.env.DATABASE_URL || 'postgresql://localhost:5432/app_dev',
        maxConnections: 5,
        ssl: false,
      },
      features: {
        maintenance: false,
        debug: true,
        cacheEnabled: false,
      },
      logging: {
        level: 'debug',
        structured: false,
      },
      monitoring: {
        sentry: false,
        performance: false,
      },
    },
    staging: {
      environment: 'staging',
      domain: 'staging.mysaas.com',
      database: {
        url: process.env.DATABASE_URL!,
        maxConnections: 10,
        ssl: true,
      },
      redis: {
        url: process.env.REDIS_URL!,
      },
      features: {
        maintenance: false,
        debug: true,
        cacheEnabled: true,
      },
      logging: {
        level: 'info',
        structured: true,
      },
      monitoring: {
        sentry: true,
        performance: true,
      },
    },
    production: {
      environment: 'production',
      domain: 'mysaas.com',
      database: {
        url: process.env.DATABASE_URL!,
        maxConnections: 20,
        ssl: true,
      },
      redis: {
        url: process.env.REDIS_URL!,
      },
      features: {
        maintenance: false,
        debug: false,
        cacheEnabled: true,
      },
      logging: {
        level: 'info',
        structured: true,
      },
      monitoring: {
        sentry: true,
        performance: true,
      },
    },
  };

  return configs[env] || configs.development;
}

export const deployment = getDeploymentConfig();
```

### Feature Flags for Deployment

```typescript
// lib/features/deployment-flags.ts
// Control features per deployment

class DeploymentFlags {
  // Maintenance mode: set via environment variable
  get maintenance() {
    return process.env.MAINTENANCE_MODE === 'true';
  }

  // Feature toggles that vary by environment
  get showBetaFeatures() {
    return process.env.NODE_ENV !== 'production';
  }

  get enableAnalytics() {
    return process.env.DISABLE_ANALYTICS !== 'true';
  }

  get enableBackgroundJobs() {
    return process.env.DISABLE_JOBS !== 'true';
  }

  // Gradual rollout (percentage-based)
  async isFeatureEnabled(
    feature: string,
    userId: string,
    percentage: number
  ): Promise<boolean> {
    // Simple hash-based rollout
    const hash = this.hashCode(`${feature}:${userId}`);
    return (hash % 100) < percentage;
  }

  private hashCode(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash |= 0;
    }
    return Math.abs(hash);
  }
}

export const deploymentFlags = new DeploymentFlags();
```

## Rollback Strategy

### Automated Rollback Triggers

```yaml
# .github/workflows/deploy.yml (with rollback)
jobs:
  deploy:
    steps:
      - name: Deploy to Production
        run: ./deploy.sh

      - name: Health Check
        run: |
          for i in {1..30}; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${{ vars.APP_URL }}/api/health)
            if [ "$STATUS" == "200" ]; then
              echo "Deploy successful!"
              exit 0
            fi
            sleep 2
          done
          echo "Health check failed! Triggering rollback..."
          exit 1

      - name: Rollback on Failure
        if: failure()
        run: |
          echo "Rolling back to previous version..."
          ./scripts/rollback.sh

  rollback:
    name: Rollback
    if: failure()
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.before }} # Previous commit

      - name: Deploy previous version
        run: ./deploy.sh
```

### Rollback Script

```bash
#!/bin/bash
# scripts/rollback.sh
# Automated rollback to previous version

set -euo pipefail

echo "Starting rollback..."

# Railway rollback
if command -v railway &> /dev/null; then
  echo "Rolling back Railway deployment..."
  railway rollback
  echo "Railway rollback complete!"
  exit 0
fi

# VPS blue-green rollback
if [ -f "/app/previous-version" ]; then
  echo "Rolling back from blue-green deployment..."
  PREV_VERSION=$(cat /app/previous-version)
  APP_NAME="my-saas"

  # Switch nginx to previous version
  cat > /etc/nginx/sites-available/app << EOF
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://localhost:$PREV_VERSION;
    }
}
EOF
  nginx -t && systemctl reload nginx
  echo "Rollback complete!"
fi

# Simple VPS rollback (restore backup)
if [ -d "/app/backups/latest" ]; then
  echo "Restoring application from backup..."
  rm -rf /app/current
  cp -r /app/backups/latest /app/current
  cd /app/current
  npm ci --production
  pm2 restart app
  echo "Rollback complete!"
fi
```

### Rollback Decision Framework

```markdown
When to rollback immediately:
  - Application returns 5xx errors
  - Database errors or corruption
  - Security vulnerability discovered
  - Critical feature broken for all users
  - Payment flow is broken

When NOT to rollback:
  - Minor UI issues
  - Non-critical feature broken
  - Cosmetic bugs
  - Performance degradation (fix forward instead)
  - Feature that affects only a few users

Rollback should:
  - Be automated (one command or button)
  - Take < 5 minutes
  - Restore the previous known-good state
  - Preserve database state (schema changes are NOT rolled back automatically)
  - Be tested regularly
```

## Post-Deploy Verification

### Smoke Tests

```typescript
// tests/smoke/deploy.test.ts
// Run after every deployment

import { describe, it, expect } from 'vitest';

const BASE_URL = process.env.APP_URL || 'http://localhost:3000';

describe('Deployment Smoke Tests', () => {
  it('health endpoint returns 200', async () => {
    const response = await fetch(`${BASE_URL}/api/health`);
    expect(response.status).toBe(200);
    const body = await response.json();
    expect(body.status).toBe('healthy');
  });

  it('homepage loads', async () => {
    const response = await fetch(BASE_URL);
    expect(response.status).toBe(200);
    expect(response.headers.get('content-type')).toContain('text/html');
  });

  it('signup page loads', async () => {
    const response = await fetch(`${BASE_URL}/signup`);
    expect(response.status).toBe(200);
  });

  it('API returns proper JSON', async () => {
    const response = await fetch(`${BASE_URL}/api/v1/users`);
    expect(response.headers.get('content-type')).toContain('json');
  });

  it('authentication endpoints work', async () => {
    const response = await fetch(`${BASE_URL}/api/auth/session`);
    // Should at least not crash
    expect(response.status).toBeLessThan(500);
  });

  it('database is accessible', async () => {
    const response = await fetch(`${BASE_URL}/api/health`);
    const body = await response.json();
    expect(body.checks.database.status).toBe('ok');
  });
});
```

### Deploy Notification

```typescript
// scripts/notify-deploy.ts
// Send deploy notification to Slack/Discord

interface DeployInfo {
  version: string;
  commit: string;
  author: string;
  timestamp: string;
  changes: string[];
  environment: string;
}

async function notifyDeploy(deploy: DeployInfo) {
  const webhookUrl = process.env.DEPLOY_WEBHOOK_URL!;

  const message = {
    text: `🚀 Deploy to ${deploy.environment}`,
    blocks: [
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Deploy to ${deploy.environment}*\nVersion: \`${deploy.version}\`\nCommit: \`${deploy.commit}\`\nAuthor: ${deploy.author}`,
        },
      },
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text: `*Changes:*\n${deploy.changes.map(c => `• ${c}`).join('\n')}`,
        },
      },
    ],
  };

  await fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(message),
  });
}
```

## Deployment Runbook

### Deploy Checklist

```markdown
## Pre-Deploy Checklist
[ ] All tests pass locally
[ ] Database migrations are backward-compatible
[ ] New environment variables are documented
[ ] Feature flags are configured for gradual rollout
[ ] Smoke tests are ready
[ ] Rollback plan is prepared
[ ] Deploy window is communicated (if not zero-downtime)

## Deploy Steps
1. [ ] Push code and create PR
2. [ ] Review PR (self-review or ask a friend)
3. [ ] Merge to main
4. [ ] CI/CD pipeline starts automatically
5. [ ] Watch deploy progress in CI dashboard
6. [ ] Verify smoke tests pass
7. [ ] Check health endpoint
8. [ ] Monitor error rates (Sentry) for 5 minutes

## Post-Deploy Checklist
[ ] Smoke tests pass
[ ] No increase in error rate
[ ] No increase in response time
[ ] All features work as expected
[ ] No user complaints in support channels
[ ] Database performance normal

## Rollback Triggers
If ANY of these occur within 30 minutes of deploy:
[ ] Error rate increases by 50%+
[ ] 5xx errors > 1% of requests
[ ] Critical feature is broken
[ ] Payment flow errors
[ ] User data integrity issue

→ Execute rollback immediately, investigate after
```

## Solo Founder's Deploy Timeline

```markdown
### Month 1: Manual Deploy
  Flow: git pull → npm run build → pm2 restart
  Frequency: 1-2 times per week
  Time: 5 minutes per deploy
  Risk: Medium (manual steps can be forgotten)

### Month 2-3: Basic CI/CD
  Flow: GitHub Actions → auto-deploy
  Frequency: Daily
  Time: Automated (2 min pipeline)
  Risk: Low (automated, consistent)

### Month 4-6: Automated + Verified
  Flow: CI → Deploy → Smoke Tests
  Frequency: Multiple times/day
  Time: Automated (5 min pipeline)
  Risk: Very low (verified at every step)

### Month 7+: Zero-Downtime
  Flow: CI → Build → Blue-Green → Smoke Tests → Switch
  Frequency: Any time, any day
  Time: Automated (10 min pipeline)
  Risk: Near-zero (fully automated rollback)
```

## Continuous Deployment Anti-Patterns

### Anti-Pattern 1: Deploying on Friday Afternoon

```markdown
BAD: Deploying at 4 PM on Friday
  - If something breaks, you fix it at 9 PM
  - Or worse: it breaks over the weekend
  - Your users suffer while you're unavailable

GOOD: Deploy on Tuesday-Thursday mornings
  - You have the rest of the day to fix issues
  - Your users' week isn't disrupted
  - You're fresh and focused
```

### Anti-Pattern 2: Skipping the Staging Environment

```markdown
BAD: Deploying directly to production without testing
  - "It works on my machine" → breaks in production
  - Database differences cause unexpected issues
  - Environment variable mismatches

GOOD: Deploy to staging first
  - Staging mirrors production
  - Run full test suite against staging
  - Only then promote to production

MINIMUM: If you skip staging, at least:
  - Run tests in CI with production-like environment
  - Use production database backup for test data
  - Verify environment variables are all set
```

### Anti-Pattern 3: Manual Steps in Deploy

```bash
# BAD: Manual deploy with multiple steps
# Step 1: Build
npm run build
# Step 2: Copy files
scp -r dist/* server:/app/
# Step 3: SSH and restart
ssh server "pm2 restart app"
# Step 4: Run migrations
ssh server "cd /app && npm run db:migrate"
# Step 5: Pray

# GOOD: Automated CI/CD
# git push → everything automated
```

### Anti-Pattern 4: Not Testing the Deploy Process

```markdown
BAD: Never testing rollback
  - When you need it, you'll fumble
  - Scripts might be broken
  - You'll make mistakes under pressure

GOOD: Test rollback monthly
  - Schedule a "game day" exercise
  - Practice the full rollback process
  - Verify backup restoration works
  - Document improvements to the process
```

## Summary

Automated deployments are the backbone of a productive solo founder workflow. Key principles:

1. **Automate from day one** — Manual deploys waste time and introduce errors
2. **Test everything** — CI checks quality, smoke tests verify deployment
3. **Zero-downtime is achievable** — Use platform features or blue-green pattern
4. **Rollback must be automated** — One command or button, tested regularly
5. **Deploy small, deploy often** — Small changes are easier to rollback
6. **Monitor after every deploy** — Watch error rates and response times
7. **Database migrations are the riskiest part** — Always backward-compatible
8. **Don't deploy on Fridays** — Give yourself time to fix issues
9. **Smoke test after every deploy** — Verify the basics still work
10. **Document the process** — Your future self (and possible hires) will thank you

A good deployment pipeline turns shipping from a stressful event into an automated routine. You should deploy without thinking about it — the same way you breathe.
