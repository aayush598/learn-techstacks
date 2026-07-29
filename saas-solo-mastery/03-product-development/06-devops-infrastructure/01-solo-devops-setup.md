# Solo DevOps Setup

## The Solo Founder's DevOps Reality

DevOps for a solo founder means one thing: maximum reliability with minimum time investment. You don't have a dedicated DevOps engineer, a 24/7 on-call rotation, or budget for expensive monitoring tools. Your DevOps strategy must be built on automation, simplicity, and leverage.

This guide covers the complete DevOps setup for a solo founder: CI/CD, hosting, monitoring, logging, alerting, and incident response — all designed to be set up in a weekend and managed in under 2 hours per week.

## The DevOps Stack

### Minimum Viable DevOps

For a solo founder, your DevOps stack should be:

```markdown
1. Version Control: GitHub (free)
2. CI/CD: GitHub Actions (free, 2000 min/mo)
3. Hosting: Platform-as-a-Service ($5-20/mo)
4. Database: Managed PostgreSQL ($0-15/mo)
5. Monitoring: Sentry + Uptime monitor (both free)
6. Logging: Axiom or Logtail (free tier)
7. Backups: Automated DB backups ($0)
8. DNS: Cloudflare (free)
9. CDN: Cloudflare (free)
10. Secrets: GitHub Secrets + .env ($0)
```

This stack costs $0-35/mo and covers 95% of solo founder needs.

### What You DON'T Need

```markdown
DON'T set up (at MVP stage):
  - Kubernetes (run on a platform or VPS)
  - Terraform (manual setup is fine with 1 server)
  - Prometheus/Grafana (Sentry + platform metrics suffice)
  - ELK Stack (use managed log service)
  - Separate staging environment (deploy from branch)
  - Load testing tools (you have 0 users)
  - APM (application performance monitoring)
  - Service mesh
  - Container orchestration
```

## CI/CD Pipeline

### GitHub Actions Template

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  PNPM_VERSION: '9'

jobs:
  lint:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: ${{ env.PNPM_VERSION }}
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm lint
      - run: pnpm typecheck

  test:
    name: Test
    needs: lint
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: ${{ env.PNPM_VERSION }}
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm db:migrate
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
      - run: pnpm test
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
          REDIS_URL: redis://localhost:6379
          NODE_ENV: test

  deploy:
    name: Deploy
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with:
          version: ${{ env.PNPM_VERSION }}
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      - run: pnpm install
      - run: pnpm build

      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway up --service ${{ vars.RAILWAY_SERVICE }}
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

### Deployment Script

```bash
#!/bin/bash
# scripts/deploy.sh
# Simple deployment script for VPS-based hosting

set -euo pipefail

echo "Deploying to production..."

# 1. Build application
npm run build

# 2. Copy files to server
rsync -avz --delete \
  --exclude 'node_modules' \
  --exclude '.git' \
  --exclude '*.test.ts' \
  --exclude '.env' \
  ./build/ \
  deploy@server:/app/

# 3. Install production dependencies
ssh deploy@server "cd /app && npm ci --production"

# 4. Run database migrations
ssh deploy@server "cd /app && npm run db:migrate"

# 5. Restart application
ssh deploy@server "pm2 restart app"

echo "Deployment complete!"
```

## Hosting Setup

### Option 1: Platform-as-a-Service (Simplest)

```markdown
Platforms ranked by solo founder friendliness:

1. Railway ($5/mo)
   - Connect GitHub repo → auto-deploy
   - Managed PostgreSQL + Redis
   - Built-in monitoring
   - Custom domains, SSL
   - Best DX for solo founders

2. Fly.io (free tier)
   - Global regions
   - Docker-based deployments
   - Managed PostgreSQL (with scaling)
   - Generous free tier

3. Render ($7/mo)
   - Auto-deploy from GitHub
   - Managed PostgreSQL, Redis
   - Static sites + background workers
   - Simple and reliable

4. DigitalOcean App Platform ($12/mo)
   - Auto-deploy from GitHub
   - Managed databases
   - Built-in monitoring
   - More control than PaaS
```

### Option 2: VPS (More Control, Lower Cost)

```bash
#!/bin/bash
# scripts/setup-server.sh
# Bootstrap a new VPS server

set -euo pipefail

SERVER_IP=$1

echo "Setting up server: $SERVER_IP"

# SSH into server and run setup
ssh root@$SERVER_IP bash -s << 'EOF'
  # Update system
  apt-get update && apt-get upgrade -y

  # Install Node.js
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get install -y nodejs git nginx postgresql redis

  # Install PM2
  npm install -g pm2

  # Create deploy user
  useradd -m -s /bin/bash deploy
  usermod -aG sudo deploy

  # Set up SSH key
  mkdir -p /home/deploy/.ssh
  cp /root/.ssh/authorized_keys /home/deploy/.ssh/
  chown -R deploy:deploy /home/deploy/.ssh

  # Configure nginx as reverse proxy
  cat > /etc/nginx/sites-available/app << 'NGINX'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
NGINX

  ln -sf /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
  rm -f /etc/nginx/sites-enabled/default
  nginx -t && systemctl restart nginx

  # Configure firewall
  ufw allow 22
  ufw allow 80
  ufw allow 443
  ufw --force enable

  # Configure PostgreSQL
  sudo -u postgres psql -c "CREATE USER app WITH PASSWORD 'change-me';"
  sudo -u postgres psql -c "CREATE DATABASE app OWNER app;"

  echo "Server setup complete!"
EOF
```

### Docker Compose for Local Development

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/app
      REDIS_URL: redis://redis:6379
      NODE_ENV: development
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

## Monitoring Setup

### Sentry Error Tracking

```typescript
// lib/monitoring/sentry.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
  profilesSampleRate: 0.1,

  // Ignore 400-level errors (client errors, not bugs)
  beforeSend(event) {
    if (event.exception) {
      const values = event.exception.values;
      if (values) {
        for (const value of values) {
          // Don't report 404 errors
          if (value.value?.includes('Not found')) {
            return null;
          }
        }
      }
    }
    return event;
  },
});

// Performance monitoring wrapper
export function monitorPerformance(name: string) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;

    descriptor.value = async function (...args: any[]) {
      const transaction = Sentry.startTransaction({
        name: `${name}.${propertyKey}`,
        op: 'function',
      });

      try {
        const result = await originalMethod.apply(this, args);
        transaction.setStatus('ok');
        return result;
      } catch (error) {
        transaction.setStatus('internal_error');
        throw error;
      } finally {
        transaction.finish();
      }
    };

    return descriptor;
  };
}
```

### Uptime Monitoring

```typescript
// app/api/health/route.ts
// Health check endpoint for monitoring services

export async function GET() {
  const checks = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    checks: {} as Record<string, { status: string; latency: number }>,
  };

  // Check database
  try {
    const dbStart = Date.now();
    await pool.query('SELECT 1');
    checks.checks.database = {
      status: 'ok',
      latency: Date.now() - dbStart,
    };
  } catch (error) {
    checks.checks.database = { status: 'error', latency: 0 };
    checks.status = 'degraded';
  }

  // Check Redis (if used)
  if (redis) {
    try {
      const redisStart = Date.now();
      await redis.ping();
      checks.checks.redis = {
        status: 'ok',
        latency: Date.now() - redisStart,
      };
    } catch (error) {
      checks.checks.redis = { status: 'error', latency: 0 };
      if (checks.status === 'healthy') checks.status = 'degraded';
    }
  }

  // Check external services (Stripe, OpenAI, etc.)
  for (const [name, checkFn] of Object.entries(externalChecks)) {
    try {
      const start = Date.now();
      await checkFn();
      checks.checks[name] = { status: 'ok', latency: Date.now() - start };
    } catch (error) {
      checks.checks[name] = { status: 'error', latency: 0 };
      if (checks.status === 'healthy') checks.status = 'degraded';
    }
  }

  const statusCode = checks.status === 'healthy' ? 200 : 503;
  return Response.json(checks, { status: statusCode });
}

// Configure Better Uptime to hit this endpoint every 1 minute
// Configure threshold: 3 failures in a row = alert
```

### Simple Server Monitoring Script

```bash
#!/bin/bash
# scripts/monitor-server.sh
# Run via cron every 5 minutes

THRESHOLD_DISK=90   # Alert when disk usage > 90%
THRESHOLD_MEM=90    # Alert when memory usage > 90%
THRESHOLD_CPU=90    # Alert when CPU usage > 90%
WEBHOOK_URL=$1      # Slack/Discord webhook for alerts

# Check disk usage
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt "$THRESHOLD_DISK" ]; then
  curl -H "Content-Type: application/json" \
    -d "{\"text\": \"⚠️ Disk usage critical: ${DISK_USAGE}%\"}" \
    $WEBHOOK_URL
fi

# Check memory usage
MEM_USAGE=$(free | awk '/Mem/ {printf "%.0f", $3/$2 * 100}')
if [ "$MEM_USAGE" -gt "$THRESHOLD_MEM" ]; then
  curl -H "Content-Type: application/json" \
    -d "{\"text\": \"⚠️ Memory usage critical: ${MEM_USAGE}%\"}" \
    $WEBHOOK_URL
fi

# Check if application is running
if ! curl -f -s http://localhost:3000/api/health > /dev/null 2>&1; then
  curl -H "Content-Type: application/json" \
    -d "{\"text\": \"🚨 Application is not responding!\"}" \
    $WEBHOOK_URL
fi

# Check nginx
if ! systemctl is-active --quiet nginx; then
  curl -H "Content-Type: application/json" \
    -d "{\"text\": \"🚨 Nginx is not running!\"}" \
    $WEBHOOK_URL
fi
```

## Logging Setup

### Structured Logging

```typescript
// lib/logging/index.ts
// Structured JSON logging for production

const LOG_LEVELS = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
} as const;

type LogLevel = keyof typeof LOG_LEVELS;

interface LogEntry {
  level: LogLevel;
  message: string;
  service: string;
  environment: string;
  timestamp: string;
  correlationId?: string;
  userId?: string;
  requestId?: string;
  duration?: number;
  error?: {
    name: string;
    message: string;
    stack?: string;
  };
  [key: string]: any;
}

class Logger {
  private service: string;
  private environment: string;
  private minLevel: number;

  constructor(service: string) {
    this.service = service;
    this.environment = process.env.NODE_ENV || 'development';
    this.minLevel = this.environment === 'production'
      ? LOG_LEVELS.info
      : LOG_LEVELS.debug;
  }

  private log(level: LogLevel, message: string, meta?: Record<string, any>) {
    if (LOG_LEVELS[level] < this.minLevel) return;

    const entry: LogEntry = {
      level,
      message,
      service: this.service,
      environment: this.environment,
      timestamp: new Date().toISOString(),
      ...meta,
    };

    // In development, pretty-print
    if (this.environment === 'development') {
      const prefix = `[${level.toUpperCase()}]`;
      const color = level === 'error' ? '\x1b[31m' :
                    level === 'warn' ? '\x1b[33m' :
                    level === 'info' ? '\x1b[36m' : '\x1b[90m';
      const reset = '\x1b[0m';
      console.log(`${color}${prefix}${reset} ${message}`, meta || '');
      return;
    }

    // In production, output JSON (for log aggregation tools)
    if (level === 'error') {
      console.error(JSON.stringify(entry));
    } else {
      console.log(JSON.stringify(entry));
    }
  }

  debug(message: string, meta?: Record<string, any>) {
    this.log('debug', message, meta);
  }

  info(message: string, meta?: Record<string, any>) {
    this.log('info', message, meta);
  }

  warn(message: string, meta?: Record<string, any>) {
    this.log('warn', message, meta);
  }

  error(message: string, error?: Error, meta?: Record<string, any>) {
    this.log('error', message, {
      ...meta,
      error: error ? {
        name: error.name,
        message: error.message,
        stack: error.stack,
      } : undefined,
    });
  }
}

export const logger = new Logger('my-saas');
```

### Log Aggregation with Axiom

```typescript
// lib/logging/axiom.ts
import { createLogger } from '@axiomhq/axiom';

const axiom = createLogger({
  token: process.env.AXIOM_TOKEN!,
  dataset: process.env.AXIOM_DATASET!,
});

export class AxiomLogger {
  log(entry: LogEntry) {
    axiom.log(entry);
  }

  async query(query: string, options?: { start?: Date; end?: Date }) {
    return axiom.query(query, {
      startTime: options?.start || new Date(Date.now() - 24 * 60 * 60 * 1000),
      endTime: options?.end || new Date(),
    });
  }
}
```

## Backup Strategy

### Automated Database Backups

```bash
#!/bin/bash
# scripts/backup-db.sh
# Run daily via cron

set -euo pipefail

BACKUP_DIR="/backups/database"
RETENTION_DAYS=30
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATABASE_URL=${DATABASE_URL:-"postgresql://localhost:5432/app"}

mkdir -p $BACKUP_DIR

echo "Starting database backup at $(date)"

# Dump database
pg_dump $DATABASE_URL \
  --format=custom \
  --compress=9 \
  --file="${BACKUP_DIR}/backup_${TIMESTAMP}.dump"

# Create plain SQL dump as well
pg_dump $DATABASE_URL \
  --format=plain \
  --no-owner \
  --compress=9 \
  --file="${BACKUP_DIR}/backup_${TIMESTAMP}.sql.gz"

# Upload to S3-compatible storage (Cloudflare R2, AWS S3, etc.)
if [ -n "${S3_BACKUP_BUCKET:-}" ]; then
  aws s3 cp "${BACKUP_DIR}/backup_${TIMESTAMP}.dump" \
    "s3://${S3_BACKUP_BUCKET}/database/"
fi

# Clean old backups
find $BACKUP_DIR -name "backup_*.dump" -mtime +$RETENTION_DAYS -delete
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "Backup completed at $(date)"
```

### Automated Backup Cron

```bash
# /etc/cron.d/database-backups
# Run backup daily at 2 AM
0 2 * * * root /opt/app/scripts/backup-db.sh >> /var/log/backup.log 2>&1

# Run backup verification weekly (Sun 3 AM)
0 3 * * 0 root /opt/app/scripts/verify-backup.sh >> /var/log/backup-verify.log 2>&1
```

### Restore Script

```bash
#!/bin/bash
# scripts/restore-db.sh
# Usage: ./restore-db.sh <backup-file>

set -euo pipefail

BACKUP_FILE=$1
DATABASE_URL=${DATABASE_URL:-"postgresql://localhost:5432/app"}

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Backup file not found: $BACKUP_FILE"
  exit 1
fi

echo "WARNING: This will overwrite the current database!"
read -p "Are you sure? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  exit 1
fi

echo "Restoring from $BACKUP_FILE..."

case "$BACKUP_FILE" in
  *.dump)
    pg_restore --clean --if-exists --dbname=$DATABASE_URL $BACKUP_FILE
    ;;
  *.sql.gz)
    gunzip -c $BACKUP_FILE | psql $DATABASE_URL
    ;;
  *)
    echo "Unknown backup format. Use .dump or .sql.gz"
    exit 1
    ;;
esac

echo "Restore complete!"
```

## Secrets Management

### GitHub Secrets

```yaml
# .github/workflows/deploy.yml
# Store these in GitHub Secrets (Settings → Secrets and variables → Actions)

# Required secrets:
# - DOCKER_USERNAME
# - DOCKER_PASSWORD
# - RAILWAY_TOKEN (or equivalent)
# - DATABASE_URL
# - REDIS_URL
# - STRIPE_SECRET_KEY
# - SENTRY_DSN
# - AXIOM_TOKEN

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: ./deploy.sh
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          STRIPE_SECRET_KEY: ${{ secrets.STRIPE_SECRET_KEY }}
```

### Environment File Management

```bash
#!/bin/bash
# scripts/pull-env.sh
# Pull environment variables from cloud provider

# Option 1: Railway
railway env pull --environment production

# Option 2: Doppler (third-party secrets manager)
doppler secrets download --project mysaas --config prd --format env > .env.production

# Option 3: Vercel
vercel env pull --environment production

# Option 4: Manual decryption
# Store encrypted .env in git
gpg --decrypt .env.production.gpg > .env.production
```

## Incident Response

### Solo Founder On-Call

```markdown
On-call schedule for solo founders:
  You're always on call. Accept this reality.

Alerting setup:
  1. Critical alerts: Phone call (Twilio or similar)
  2. High alerts: SMS or push notification
  3. Medium alerts: Email (batch hourly)
  4. Low alerts: No notification (check in morning)

Alert fatigue prevention:
  - Only alert on things you can actually fix at 3 AM
  - Don't alert on things that can wait until morning
  - Batch non-critical alerts
  - Set minimum intervals between alerts
```

### Incident Response Runbook

```markdown
## Incident Response Process

1. DETECT
   - Alert received (Better Uptime, Sentry, or user report)
   - Acknowledge alert within 5 minutes

2. ASSESS
   - Is the app completely down?
   - Are errors partial?
   - Is it a database issue? Deploy issue? External service?

3. RESPOND
   - Check health endpoint: /api/health
   - Check recent deploys: git log --oneline -5
   - Check logs: axiom query or tail logs on server
   - Check database: is it connected? Slow queries?
   - Check external services: Stripe, OpenAI status pages

4. MITIGATE
   - For bad deploy: Rollback to previous version
   - For database issues: Check backups, restore if needed
   - For external service: Switch to fallback or wait
   - For security incident: Isolate affected systems

5. COMMUNICATE
   - Update status page (Better Uptime/Instatus)
   - If paying customers affected, send email
   - Document what happened and what was done

6. RESOLVE
   - Confirm fix is working
   - Monitor for 30 minutes
   - Close incident

7. LEARN
   - What caused the incident?
   - What can prevent it in the future?
   - Implement prevention as a code change
```

### Quick Incident Commands

```bash
# Emergency rollback
# If using Railway:
railway rollback

# If using VPS:
cd /app && git checkout HEAD~1 && pm2 restart app

# Database emergency restart
systemctl restart postgresql

# Check recent errors in logs
journalctl -u app --since "10 minutes ago" --no-pager

# Kill and restart hanging process
pm2 delete app && pm2 start app

# Emergency database connection check
psql $DATABASE_URL -c "SELECT count(*) FROM pg_stat_activity;"

# Check disk space
df -h

# Check memory
free -h

# List recent deploys
git log --oneline --decorate -10
```

## DevOps Health Score

### Weekly DevOps Checklist

```markdown
Every Monday morning (15 minutes):

[ ] Check Sentry: Any new errors in the last 24h?
[ ] Check uptime monitor: 100% uptime last week?
[ ] Check database storage: < 80% full?
[ ] Check backup: Last backup successful?
[ ] Check server disk: < 80% full?
[ ] Check application logs: Any anomalies?
[ ] Review deploy frequency: Any failed deploys?
[ ] Check dependent services: Stripe, OpenAI status
[ ] Update dependencies: Critical security updates?
[ ] Review costs: Any unexpected charges?
```

### Monthly DevOps Review

```markdown
First of each month (30 minutes):

[ ] Review incident log: Any incidents last month?
[ ] Run security updates: apt update && apt upgrade
[ ] Review database performance: Slow queries?
[ ] Review monitoring coverage: Missing any checks?
[ ] Review backup retention: Need to adjust?
[ ] Review cloud costs: Within budget?
[ ] Update runbook: Any new procedures needed?
[ ] Test backup restoration: Verify backups work
[ ] Review API rate limits: Hitting any?
[ ] Plan capacity: Need to scale soon?
```

## DevOps Anti-Patterns for Solo Founders

### Anti-Pattern 1: Over-Automation

```bash
# BAD: Spending days automating something you do twice
terraform apply  # For a single VPS
ansible-playbook # For 1 server
k8s manifest     # For 1 container

# GOOD: Manual setup with documented steps
# Spend 15 minutes setting up vs. hours automating
```

### Anti-Pattern 2: Self-Hosting Everything

```markdown
BAD: Self-hosting (time sink for solo founders):
  - Self-hosted GitLab instead of GitHub
  - Self-hosted Sentry instead of SaaS
  - Self-hosted Docker registry
  - Self-hosted monitoring (Prometheus + Grafana)

GOOD: SaaS services (minutes to set up):
  - GitHub for version control
  - Sentry SaaS for error tracking
  - Docker Hub or GitHub Container Registry
  - Better Uptime or similar for monitoring
```

### Anti-Pattern 3: No Monitoring Because "It's Just Me"

```markdown
BAD: "I'm the only one using it, I'll know if it breaks"
  - You won't know at 3 AM
  - You won't know if users can't sign up
  - You won't know if Stripe calls are failing
  - You won't know if the database is filling up

GOOD: Set up basic monitoring (1 hour):
  - Sentry for errors (free, 30 min setup)
  - Better Uptime for availability (free, 15 min setup)
  - Platform metrics (built into Railway/Heroku/etc.)
```

## Solo Founder's DevOps Timeline

```markdown
Week 1 (MVP Launch):
  [ ] GitHub repo with CI (lint + test)
  [ ] Deploy to Railway or similar (5 min)
  [ ] Set up custom domain + SSL (Cloudflare, 10 min)
  [ ] Configure Sentry error tracking (30 min)
  [ ] Set up database backups (15 min)

Month 1:
  [ ] Add uptime monitoring (15 min)
  [ ] Set up structured logging (30 min)
  [ ] Configure performance monitoring (30 min)
  [ ] Set up alerting (email + push) (30 min)

Quarter 1:
  [ ] Create incident response runbook (1 hour)
  [ ] Set up status page (30 min)
  [ ] Review and optimize costs (1 hour)
  [ ] Add database query monitoring (1 hour)

Quarter 2:
  [ ] Performance audit (2 hours)
  [ ] Security review (2 hours)
  [ ] Load testing (if needed) (2 hours)
  [ ] Disaster recovery drill (1 hour)

Quarter 3+:
  [ ] Auto-scaling setup
  [ ] Multi-region deployment
  [ ] Full observability stack
  [ ] Dedicated DevOps time per week
```

## Summary

A solo founder's DevOps setup should be functional in a weekend and maintainable in under 2 hours per week. Key principles:

1. **Use managed services** — Don't self-host what you can buy for $5-20/mo
2. **Automate deploys** — CI/CD from day one (GitHub Actions + platform deploy)
3. **Monitor from day one** — Sentry + uptime monitor takes 45 minutes to set up
4. **Backup automatically** — Daily DB backups to S3/R2, test restoration monthly
5. **Log properly** — Structured JSON logs from the start
6. **Document runbooks** — You won't remember what to do at 3 AM
7. **Keep it simple** — Avoid Kubernetes, Terraform, and complex tooling
8. **Review weekly** — 15 minutes every Monday prevents firefighting
9. **Budget for DevOps time** — 2 hours/week is enough for most solo founders
10. **Incidents will happen** — Have a plan, keep calm, fix, learn, improve
