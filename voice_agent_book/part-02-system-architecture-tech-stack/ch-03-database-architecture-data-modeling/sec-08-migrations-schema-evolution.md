# Section 08: Migrations & Schema Evolution

## Migration Strategy

Database schema evolution follows a **continuous, automated, and reversible** process using Prisma Migrate. Every change is versioned, reviewed, tested in CI, and applied with zero-downtime patterns.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      MIGRATION WORKFLOW                                │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    DEVELOPMENT                                   │    │
│  │                                                                  │    │
│  │  1. Developer modifies schema.prisma                           │    │
│  2. Run prisma migrate dev --name add_agent_status_index         │    │
│  3. Migration SQL file generated in prisma/migrations/            │    │
│  4. Apply to local dev database                                   │    │
│  5. Generate Prisma Client                                        │    │
│  6. Run tests to verify                                           │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                               │                                         │
│                               ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    CI/CD PIPELINE                              │    │
│  │                                                                  │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │    │
│  │  │  Lint        │  │  Migration   │  │  Integration │          │    │
│  │  │  Migration   │  │  Dry Run     │  │  Tests       │          │    │
│  │  │  (prisma     │  │  (apply to   │  │  (run against │         │    │
│  │  │  validate)   │  │  CI DB)      │  │  migrated DB) │         │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘          │    │
│  │                                                                  │    │
│  │  Failures prevent deployment                                    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                               │                                         │
│                               ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                  STAGING (PRE-PROD)                             │    │
│  │                                                                  │    │
│  1. prisma migrate deploy --preview-feature  (applies pending)    │    │
│  2. Run smoke tests against staging database                       │    │
│  3. Performance benchmark queries                                  │    │
│  4. Rollback drill (verify rollback procedure)                     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                               │                                         │
│                               ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    PRODUCTION                                   │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  1. Backup database (pg_dump)                             │   │    │
│  │  │  2. Run prisma migrate deploy                             │   │    │
│  │  │  3. Verify migration applied (prisma migrate status)      │   │    │
│  │  │  4. Run post-migration validation queries                  │   │    │
│  │  │  5. Monitor error rates and query performance              │   │    │
│  │  │  6. Alert if anomalies detected                            │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Migration Naming Convention

```bash
# Migration naming: YYYYMMDD_HHMMSS_short_description
prisma/migrations/
├── 20250101_000001_init/
│   └── migration.sql
├── 20250115_120000_add_agent_status_index/
│   └── migration.sql
├── 20250120_083000_add_campaign_model/
│   └── migration.sql
├── 20250201_000000_add_call_analytics_columns/
│   └── migration.sql
├── 20250210_143000_add_rls_policies/
│   └── migration.sql
├── 20250215_090000_create_call_partitions/
│   └── migration.sql
├── 20250301_000001_add_webhook_delivery_attempts/
│   └── migration.sql
└── migration_lock.toml
```

## Zero-Downtime Migration Patterns

### Expand-Contract Pattern (for column changes)

```sql
-- Phase 1: EXPAND — Add new column alongside old one
-- Migration: add_agent_status_v2
ALTER TABLE agents ADD COLUMN status_v2 VARCHAR(20);

-- Application writes to both columns during transition
-- Application reads from new column

-- Phase 2: MIGRATE — Backfill data
-- Migration: backfill_agent_status
UPDATE agents SET status_v2 = status WHERE status_v2 IS NULL;

-- Phase 3: CONTRACT — Remove old column
-- Migration: drop_agent_status
ALTER TABLE agents DROP COLUMN status;
ALTER TABLE agents RENAME COLUMN status_v2 TO status;
```

### Online Migration with Views

```sql
-- For complex schema changes, use views for backward compatibility

-- Step 1: Create new table
CREATE TABLE agents_new (LIKE agents INCLUDING ALL);

-- Step 2: Create view combining both tables
CREATE VIEW agents_vw AS
  SELECT * FROM agents
  UNION ALL
  SELECT * FROM agents_new;

-- Step 3: Backfill data to new table (batched)
DO $$
DECLARE
  batch_size INT := 1000;
  offset INT := 0;
  rows_affected INT;
BEGIN
  LOOP
    WITH batch AS (
      SELECT * FROM agents
      ORDER BY id
      LIMIT batch_size OFFSET offset
    )
    INSERT INTO agents_new SELECT * FROM batch;
    
    GET DIAGNOSTICS rows_affected = ROW_COUNT;
    EXIT WHEN rows_affected = 0;
    offset := offset + batch_size;
    COMMIT;
  END LOOP;
END $$;

-- Step 4: Swap tables when ready
BEGIN;
  DROP VIEW agents_vw;
  ALTER TABLE agents RENAME TO agents_old;
  ALTER TABLE agents_new RENAME TO agents;
COMMIT;

-- Step 5: Clean up old table
DROP TABLE agents_old;
```

### Adding Non-Nullable Column

```sql
-- Step 1: Add as nullable
ALTER TABLE agents ADD COLUMN timezone VARCHAR(50);

-- Step 2: Backfill default value
UPDATE agents SET timezone = 'UTC' WHERE timezone IS NULL;

-- Step 3: Add NOT NULL constraint
ALTER TABLE agents ALTER COLUMN timezone SET NOT NULL;
```

## Migration Runbook

```bash
# List migration status
pnpm prisma migrate status

# Create development migration
pnpm prisma migrate dev --name add_call_transfer_fields

# Apply to production
pnpm prisma migrate deploy

# Reset local database
pnpm prisma migrate reset

# Generate Prisma client only (if schema already applied)
pnpm prisma generate

# Check if migrations have been applied
pnpm prisma migrate status

# Mark migration as applied (emergency — if manually applied)
pnpm prisma migrate resolve --applied 20250210_143000_add_rls_policies
```

## Migration Validation in CI

```yaml
# .github/workflows/migration-check.yml
name: Database Migration Check
on:
  pull_request:
    paths:
      - 'prisma/schema.prisma'
      - 'prisma/migrations/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        ports:
          - 5432:5432
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
      - uses: actions/setup-node@v4
      
      - name: Install dependencies
        run: pnpm install
        
      - name: Check migration health
        run: pnpm prisma migrate dev --name ci_check
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
          
      - name: Run integration tests
        run: pnpm test:integration
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
          
      - name: Verify no schema drift
        run: pnpm prisma validate
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
```

## Rollback Strategy

```typescript
// app/api/admin/migrations/route.ts
import { execSync } from 'child_process'
import { prisma } from '@/lib/db'

export async function POST(request: Request) {
  const { action, migrationName } = await request.json()
  
  if (action === 'rollback') {
    // 1. Take a backup first
    execSync('pg_dump ...')
    
    // 2. Run the down migration (manually written)
    const downMigration = getDownMigration(migrationName)
    await prisma.$executeRawUnsafe(downMigration)
    
    // 3. Update migration tracking
    await prisma.$executeRawUnsafe(
      `DELETE FROM _prisma_migrations WHERE migration_name = $1`,
      migrationName
    )
    
    return Response.json({ success: true })
  }
  
  return Response.json({ error: 'Invalid action' }, { status: 400 })
}

// Down migrations (reverse of each migration)
function getDownMigration(name: string): string {
  const downMigrations: Record<string, string> = {
    '20250210_143000_add_rls_policies': `
      DROP POLICY tenant_isolation ON users;
      DROP POLICY tenant_isolation ON agents;
      ALTER TABLE users DISABLE ROW LEVEL SECURITY;
    `,
    '20250215_090000_create_call_partitions': `
      DROP TABLE IF EXISTS calls CASCADE;
      CREATE TABLE calls (LIKE calls_template INCLUDING ALL);
    `
  }
  
  return downMigrations[name] ?? '-- No down migration defined'
}
```

## Seed Data Strategy

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  // 1. Seed plan definitions
  await prisma.planDefinition.createMany({
    data: [
      {
        name: 'Free',
        tier: 'free',
        priceCents: 0,
        features: { call_minutes: 100, agents: 1, team_members: 1 },
        limits: { call_minutes: 100, agents: 1, team_members: 1 },
        overageRates: {},
        sortOrder: 0
      },
      {
        name: 'Starter',
        tier: 'starter',
        priceCents: 2900,
        features: { call_minutes: 1000, agents: 3, team_members: 5 },
        limits: { call_minutes: 1000, agents: 3, team_members: 5 },
        overageRates: { call_minute_overage_cents: 1.0 },
        sortOrder: 1
      },
      // ... more plans
    ]
  })

  // 2. Seed default voices
  await prisma.voice.createMany({
    data: [
      { tenantId: 'default', name: 'Default (Female)', provider: 'coqui_tts', voiceId: 'default_female', language: 'en-US', gender: 'female', isDefault: true },
      { tenantId: 'default', name: 'Default (Male)', provider: 'coqui_tts', voiceId: 'default_male', language: 'en-US', gender: 'male', isDefault: false },
    ]
  })

  // 3. Seed default prompts
  await prisma.prompt.createMany({
    data: [
      {
        tenantId: 'default',
        name: 'Default Agent',
        content: `You are a helpful AI voice agent. Keep responses concise and natural for phone conversation.`,
        version: 1
      }
    ]
  })
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect())
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Migration Tool | Prisma Migrate | TypeScript-native, schema validation |
| Migration Format | SQL files (not auto-generated) | Reviewable, reversible, DBA-friendly |
| Deployment | Separate step before app deploy | Schema must be ready for new code |
| Rollback | Down migration scripts | Explicit undo, automated via API |
| Seed Data | TypeScript seed script | Version-controlled, repeatable |

## Integration Points

- **Part 03 (Database Architecture)** — Migrations implement schema changes
- **Part 23 (DevOps/CI-CD)** — Migration runs as CI step before deployment
- **Part 19 (Testing)** — Test databases migrated in CI pipeline

## Production Considerations

- **Migration Time**: Large tables (calls, events) may require hours; use concurrent index creation
- **Locking**: Avoid long-running locks; use `CREATE INDEX CONCURRENTLY` and `ALTER TABLE ... ALTER COLUMN ...` without blocking
- **Rollback Plan**: Every migration must have a tested rollback script
- **Backup**: Always backup before production migration; keep 7 days of backups
- **Monitoring**: Track migration duration, errors, and performance regression after deployment
- **Staging Mirror**: Staging database should have production-like data volume for migration timing estimates
