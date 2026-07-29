# Database Migration Strategy for SaaS

## The Migration Challenge

Database migrations are one of the highest-risk operations in software development. A bad migration can corrupt data, cause downtime, or require hours of manual recovery. For solo founders without a team to catch mistakes, a careful migration strategy is essential.

This guide covers migration workflows for solo founders, zero-downtime migration patterns, rollback planning, and tools and practices for safe schema evolution.

## Migration Philosophy

### The Solo Founder's Migration Principles

```markdown
1. Migrations should be reversible
   - Every migration should have a down migration
   - Test both up and down before running on production

2. Migrations should be small and frequent
   - Deploy multiple small migrations rather than one large one
   - Small migrations are easier to review, test, and roll back

3. Migrations should be tested
   - Run migrations against a copy of production data
   - Verify the migration produces expected results

4. Migrations should be automated
   - CI/CD should run migrations automatically
   - Manual migrations are error-prone

5. Zero-downtime should be the default
   - Design migrations so existing queries continue to work
   - Use techniques like expand-contract for breaking changes
```

## Migration Tooling

### Tool Selection

```markdown
| Tool            | Language   | Type         | Best For                    |
|-----------------|------------|--------------|-----------------------------|
| Prisma Migrate  | TypeScript | Declarative  | Full-stack TS/Next.js       |
| Drizzle Kit     | TypeScript | Declarative  | TypeScript SQL projects     |
| Flyway          | Java/SQL   | Versioned    | JVM languages               |
| Alembic         | Python     | Declarative  | Python/SQLAlchemy projects  |
| ActiveRecord    | Ruby       | Declarative  | Rails projects              |
| Django ORM      | Python     | Declarative  | Django projects             |
| goose           | Go         | Versioned    | Go projects                 |
| dbmate          | Any        | Versioned    | Language-agnostic           |
| pgroll          | PostgreSQL | Declarative  | Zero-downtime Postgres      |
| Bytebase        | Any        | Visual       | Team workflow               |
```

### Migration File Format (Language-Agnostic)

```sql
-- migrations/001_create_users.sql
-- Up Migration
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Down Migration
DROP TABLE IF EXISTS users;

-- migrations/002_add_profiles.sql
-- Up
CREATE TABLE profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  display_name VARCHAR(255),
  avatar_url TEXT,
  bio TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Down
DROP TABLE IF EXISTS profiles;

-- migrations/003_add_projects_table.sql
-- Up
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_projects_user ON projects(user_id);

-- Down
DROP TABLE IF EXISTS projects;
```

### Migration Runner Script

```typescript
// lib/database/migrate.ts
// Simple migration runner for solo founders

import { Pool } from 'pg';
import * as fs from 'fs';
import * as path from 'path';

class MigrationRunner {
  private pool: Pool;

  constructor(connectionString: string) {
    this.pool = new Pool({ connectionString });
  }

  async run(): Promise<void> {
    // Ensure migrations table exists
    await this.pool.query(`
      CREATE TABLE IF NOT EXISTS _migrations (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        applied_at TIMESTAMPTZ DEFAULT NOW()
      )
    `);

    // Get list of applied migrations
    const applied = await this.pool.query(
      'SELECT name FROM _migrations ORDER BY name'
    );
    const appliedSet = new Set(applied.rows.map(r => r.name));

    // Get migration files
    const migrationsDir = path.join(process.cwd(), 'migrations');
    const files = fs.readdirSync(migrationsDir)
      .filter(f => f.endsWith('.sql'))
      .sort(); // Ensure order

    for (const file of files) {
      if (appliedSet.has(file)) {
        console.log(`Skipping already applied: ${file}`);
        continue;
      }

      console.log(`Applying migration: ${file}`);
      const sql = fs.readFileSync(
        path.join(migrationsDir, file),
        'utf-8'
      );

      // Parse up and down migrations
      const [up] = this.parseMigration(sql);

      // Run in transaction
      const client = await this.pool.connect();
      try {
        await client.query('BEGIN');
        await client.query(up);
        await client.query(
          'INSERT INTO _migrations (name) VALUES ($1)',
          [file]
        );
        await client.query('COMMIT');
        console.log(`Applied: ${file}`);
      } catch (error) {
        await client.query('ROLLBACK');
        console.error(`Failed to apply ${file}:`, error);
        throw error;
      } finally {
        client.release();
      }
    }

    console.log('All migrations applied successfully');
  }

  async rollback(name?: string): Promise<void> {
    // If no name specified, rollback the last migration
    if (!name) {
      const last = await this.pool.query(
        'SELECT name FROM _migrations ORDER BY name DESC LIMIT 1'
      );
      if (last.rows.length === 0) {
        console.log('No migrations to rollback');
        return;
      }
      name = last.rows[0].name;
    }

    const migrationsDir = path.join(process.cwd(), 'migrations');
    const sql = fs.readFileSync(
      path.join(migrationsDir, name),
      'utf-8'
    );

    const [, down] = this.parseMigration(sql);

    if (!down) {
      throw new Error(`No down migration found for ${name}`);
    }

    console.log(`Rolling back: ${name}`);
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      await client.query(down);
      await client.query('DELETE FROM _migrations WHERE name = $1', [name]);
      await client.query('COMMIT');
      console.log(`Rolled back: ${name}`);
    } catch (error) {
      await client.query('ROLLBACK');
      console.error(`Failed to rollback ${name}:`, error);
      throw error;
    } finally {
      client.release();
    }
  }

  private parseMigration(sql: string): [string, string] {
    const parts = sql.split(/^-- Down$/m);
    const up = parts[0].replace(/^-- Up\n?/, '').trim();
    const down = parts[1]?.trim() || '';
    return [up, down];
  }
}

// Run via CLI
if (require.main === module) {
  const runner = new MigrationRunner(process.env.DATABASE_URL!);
  const command = process.argv[2];

  if (command === 'up') {
    runner.run().catch(console.error);
  } else if (command === 'down') {
    runner.rollback(process.argv[3]).catch(console.error);
  } else {
    console.log('Usage: ts-node migrate.ts up|down [name]');
  }
}
```

## Migration Patterns

### Pattern 1: Simple Add Table

```sql
-- SAFE: Adding a new table never breaks existing queries
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  body TEXT,
  is_read BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id, is_read);
```

### Pattern 2: Add Nullable Column

```sql
-- SAFE: Adding nullable column is backward-compatible
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users ADD COLUMN timezone VARCHAR(50) DEFAULT 'UTC';
```

### Pattern 3: Add Non-Nullable Column

```sql
-- UNSAFE: Adding non-nullable column to existing table
-- This will fail if there are existing rows

-- SAFE approach:
ALTER TABLE users ADD COLUMN timezone VARCHAR(50); -- Nullable first
UPDATE users SET timezone = 'UTC' WHERE timezone IS NULL; -- Fill data
ALTER TABLE users ALTER COLUMN timezone SET NOT NULL; -- Add constraint
```

### Pattern 4: Rename Column

```sql
-- UNSAFE: Renaming column breaks existing queries referencing old name

-- SAFE approach (Expand-Contract):
-- Step 1: Add new column
ALTER TABLE users ADD COLUMN display_name VARCHAR(255);
UPDATE users SET display_name = full_name;

-- Step 2: Update application to use display_name instead of full_name
-- Deploy application update

-- Step 3: Remove old column (after confirming no references)
ALTER TABLE users DROP COLUMN full_name;
```

### Pattern 5: Change Column Type

```sql
-- UNSAFE: Changing column type can fail or lose data

-- SAFE approach:
-- Step 1: Add new column with new type
ALTER TABLE users ADD COLUMN status_new VARCHAR(50);
UPDATE users SET status_new = status::VARCHAR(50);

-- Step 2: Drop old column
ALTER TABLE users DROP COLUMN status;

-- Step 3: Rename new column
ALTER TABLE users RENAME COLUMN status_new TO status;
```

### Pattern 6: Add Index

```sql
-- SAFE: Adding index is non-blocking (CONCURRENTLY in PostgreSQL)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email
  ON users(email);

-- Note: CREATE INDEX CONCURRENTLY cannot run in a transaction.
-- Run outside transaction or use a migration tool that supports it.
```

### Pattern 7: Remove Index

```sql
-- SAFE: Removing index never breaks queries
DROP INDEX IF EXISTS idx_users_old_index;
```

### Pattern 8: Add Foreign Key

```sql
-- UNSAFE: Adding foreign key to a table with existing data
-- Will fail if existing rows violate the constraint

-- SAFE approach:
-- Step 1: Add column
ALTER TABLE tasks ADD COLUMN assignee_id UUID;

-- Step 2: Validate existing data
-- (Fix any rows with invalid assignee_id values)

-- Step 3: Add constraint (validates existing data)
ALTER TABLE tasks ADD CONSTRAINT fk_tasks_assignee
  FOREIGN KEY (assignee_id) REFERENCES users(id);

-- Step 4: Add NOT NULL if appropriate
ALTER TABLE tasks ALTER COLUMN assignee_id SET NOT NULL;
```

## Zero-Downtime Migration Patterns

### The Expand-Contract Pattern

For any migration that changes column names, types, or constraints:

```
Phase 1: Expand
  ┌──────────────────────────────────────────────┐
  │ Add new column/table alongside existing one  │
  │ Write to both old and new                    │
  │ Application continues reading from old       │
  └──────────────────────────────────────────────┘

Phase 2: Migrate Data
  ┌──────────────────────────────────────────────┐
  │ Backfill data from old to new                │
  │ Verify consistency                           │
  └──────────────────────────────────────────────┘

Phase 3: Switch
  ┌──────────────────────────────────────────────┐
  │ Deploy application update to read from new   │
  │ Continue writing to both for rollback        │
  └──────────────────────────────────────────────┘

Phase 4: Contract
  ┌──────────────────────────────────────────────┐
  │ Remove old column/table                      │
  │ Stop writing to old                          │
  └──────────────────────────────────────────────┘
```

### Zero-Downtime Migration: Rename Column Example

```typescript
// Phase 1: Add new column
// migration_004_rename_full_name_to_display_name_p1.sql
ALTER TABLE users ADD COLUMN display_name VARCHAR(255);
CREATE INDEX CONCURRENTLY idx_users_display_name ON users(display_name);

// Phase 2: Backfill data (run as background job)
async function backfillDisplayNames() {
  const batchSize = 1000;
  let offset = 0;

  while (true) {
    const result = await pool.query(
      `UPDATE users
       SET display_name = full_name
       WHERE display_name IS NULL
         AND full_name IS NOT NULL
       LIMIT $1
       RETURNING id`,
      [batchSize]
    );

    if (result.rows.length === 0) break;
    offset += result.rows.length;
    console.log(`Backfilled ${offset} users`);
  }
}

// Phase 3: Update application to write to both
class UserService {
  async updateUser(id: string, data: UpdateUserInput) {
    // Write to BOTH old and new columns
    await pool.query(
      `UPDATE users
       SET full_name = COALESCE($1, full_name),
           display_name = COALESCE($1, display_name),
           updated_at = NOW()
       WHERE id = $2`,
      [data.name, id]
    );
  }

  async getUser(id: string) {
    // Read from NEW column
    const result = await pool.query(
      `SELECT id, email, display_name as name, created_at
       FROM users WHERE id = $1`,
      [id]
    );
    return result.rows[0];
  }
}

// Phase 4: Remove old column
// migration_005_remove_full_name.sql
-- Confirm no application code references full_name
ALTER TABLE users DROP COLUMN full_name;
```

### Lock-Free Index Creation

```sql
-- BAD: Blocks writes during index creation
CREATE INDEX idx_users_email ON users(email);

-- GOOD: Non-blocking index creation (PostgreSQL)
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- Note: CONCURRENTLY index creation:
-- - Takes longer than regular CREATE INDEX
-- - Cannot run inside a transaction
-- - Uses more CPU and I/O during creation
-- - Will NOT block reads or writes
```

### Batch Processing for Large Migrations

```typescript
// lib/database/batch-migration.ts

async function batchUpdate(
  table: string,
  setClause: string,
  whereClause: string,
  params: any[],
  batchSize = 1000
): Promise<number> {
  let totalUpdated = 0;

  while (true) {
    const result = await pool.query(
      `UPDATE ${table}
       SET ${setClause}
       WHERE ${whereClause}
         AND ctid IN (
           SELECT ctid FROM ${table}
           WHERE ${whereClause}
           LIMIT $${params.length + 1}
           FOR UPDATE SKIP LOCKED
         )
       RETURNING id`,
      [...params, batchSize]
    );

    if (result.rows.length === 0) break;
    totalUpdated += result.rows.length;
    console.log(`Updated ${totalUpdated} rows in ${table}`);

    // Small pause to reduce load
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  return totalUpdated;
}

// Usage: Add NOT NULL column in batches
async function addNotNullColumn() {
  // Step 1: Add nullable column
  await pool.query('ALTER TABLE users ADD COLUMN timezone VARCHAR(50)');

  // Step 2: Batch fill in data
  const updated = await batchUpdate(
    'users',
    'timezone = $1',
    'timezone IS NULL',
    ['UTC']
  );

  console.log(`Set timezone for ${updated} users`);

  // Step 3: Add NOT NULL constraint
  await pool.query('ALTER TABLE users ALTER COLUMN timezone SET NOT NULL');
}
```

## Schema Change Safety Checklist

### Pre-Migration Checklist

```markdown
[ ] Migration is reversible (has down migration)
[ ] Migration has been tested on a staging database with production-like data
[ ] For tables with > 10k rows, batch processing is planned
[ ] For columns being renamed, expand-contract pattern is used
[ ] For new NOT NULL columns, default values are backfilled first
[ ] For new indexes, CONCURRENTLY is used
[ ] For foreign keys, existing data has been validated
[ ] Application code has been updated to handle both old and new schema
[ ] Rollback plan is documented
[ ] Maintenance window has been communicated (if needed)
```

### Post-Migration Checklist

```markdown
[ ] All queries are running correctly
[ ] No error rate increase in application
[ ] Database performance is normal (no slow queries)
[ ] Data integrity has been verified (row counts match expectations)
[ ] Old columns/tables are cleaned up
[ ] Migration is marked as successful in tracking system
[ ] Backup has been taken after migration
```

## Rollback Strategies

### Immediate Rollback (Migration Just Applied)

```bash
# If a migration causes issues immediately:
# Step 1: Run down migration
migrate down 004_add_projects_table

# Step 2: Redeploy previous application version
git revert HEAD
git push production

# Step 3: Verify everything is working
```

### Delayed Rollback (Migration Applied Days Ago)

```sql
-- If an issue is discovered days after migration:
-- Don't rollback the schema change directly
-- Instead, create a new migration to fix the issue

-- migration_006_fix_projects_table.sql
-- Up: Fix whatever the issue is
-- Down: Reverse the fix

-- Better approach:
-- 1. Create new migration to fix the issue
-- 2. Deploy as normal
-- 3. Only rollback schema changes in emergencies
```

### Irreversible Migration Protection

```sql
-- Some operations cannot be rolled back easily.
-- Protect against them with validation.

-- migration_destructive_operations_check.sql
DO $$
BEGIN
  -- Check if migration would drop a table with data
  IF EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_name = 'users'
  ) THEN
    RAISE EXCEPTION 'Table users exists - this migration would drop it. Manual confirmation required.';
  END IF;
END $$;
```

## Migration Workflow for Solo Founders

### Development Workflow

```bash
# 1. Create a new migration
touch migrations/004_add_projects_table.sql

# 2. Write the migration (up + down)
# edit migrations/004_add_projects_table.sql

# 3. Apply migration locally
DATABASE_URL=postgresql://localhost:5432/mydb_dev npm run migrate:up

# 4. Verify everything works
npm run test

# 5. If something is wrong, rollback
DATABASE_URL=postgresql://localhost:5432/mydb_dev npm run migrate:down
```

### CI/CD Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: test
          POSTGRES_PASSWORD: postgres
        ports: ['5432:5432']

    steps:
      - uses: actions/checkout@v4

      - name: Setup
        run: npm ci

      - name: Run migrations against test DB
        run: npm run migrate:up
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

      - name: Run tests
        run: npm test
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy to production
        run: |
          # Deploy application first (so old code handles new schema)
          ./deploy.sh

          # Then run migrations
          npm run migrate:up
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Production Migration Safety

```bash
# One-time production migration script
#!/bin/bash
set -euo pipefail

echo "Starting production migration..."
echo "Time: $(date)"
echo "Database: $DATABASE_URL"

# Step 1: Backup
echo "Creating backup..."
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Step 2: Run pre-migration checks
echo "Running pre-migration checks..."
node scripts/pre-migration-check.js

# Step 3: Run migration
echo "Running migration..."
npm run migrate:up

# Step 4: Run post-migration checks
echo "Running post-migration checks..."
node scripts/post-migration-check.js

# Step 5: Verify application
echo "Checking application health..."
curl -f http://localhost:3000/api/health

echo "Migration completed successfully at $(date)"
```

## Migration Anti-Patterns

### Anti-Pattern 1: Migrating in the Same Transaction as Application Code

```typescript
// BAD: Migration and application code change in same deploy
-- This deploy also renames the column
ALTER TABLE users RENAME COLUMN name TO display_name;

// Application code is deployed at the same time
// If application code references old column name, it breaks

// GOOD: Separate the migration from application deploy
// Deploy 1: Add new column, write to both
// Deploy 2: Switch application to read from new column
// Deploy 3: Remove old column
```

### Anti-Pattern 2: Long-Running Migrations Without Batching

```sql
-- BAD: Single UPDATE on a table with millions of rows
-- This locks the table for minutes or hours
UPDATE users SET display_name = full_name WHERE display_name IS NULL;

-- GOOD: Batch the update
-- Use the batchUpdate function shown above
-- Or use pg_batch extension
```

### Anti-Pattern 3: Skipping Down Migrations

```sql
-- BAD: Migration without down
CREATE TABLE projects (...);
-- No "-- Down" section

-- GOOD: Always include down migration
-- Up
CREATE TABLE projects (...);
-- Down
DROP TABLE IF EXISTS projects;
```

### Anti-Pattern 4: Manual Schema Changes

```sql
-- BAD: Direct changes to production database
ALTER TABLE users ADD COLUMN phone VARCHAR(20); -- Directly in prod

-- Now migration tool doesn't know about this change
-- Next migration might conflict or fail

-- GOOD: Always make schema changes through migrations
-- Create a migration file, commit it, apply through CI/CD
```

### Anti-Pattern 5: Auto-Running Migrations on Application Start

```typescript
// BAD: Auto-running migrations on startup
// Multiple app instances might run migrations simultaneously
// Migration failure crashes the application
app.listen(3000, async () => {
  await migrationRunner.up(); // DON'T DO THIS
});

// GOOD: Run migrations separately from app startup
// Run as a separate pre-deploy step or init container
```

## Postgres-Specific Migration Tips

### Lock-Aware Migrations

```sql
-- Check current locks before running migration
SELECT
  relation::regclass AS table_name,
  mode,
  granted
FROM pg_locks
WHERE NOT granted;

-- Check if migration would cause long waits
-- If there are active long-running transactions, wait
```

### Migration Timing

```sql
-- Run long migrations during low-traffic periods
-- For PostgreSQL, some operations are instant:
INSTANT:  CREATE TABLE, CREATE INDEX (non-concurrent), DROP TABLE
          Add NULLABLE column, Add DEFAULT value

NEEDS SCAN: CREATE INDEX CONCURRENTLY
            ALTER COLUMN SET NOT NULL
            ADD FOREIGN KEY
            ALTER COLUMN TYPE (with USING)

HEAVY:  CREATE INDEX without CONCURRENTLY on large table
        ALTER COLUMN TYPE on large table
        Full-table UPDATE
```

### Migration Testing with Production Data

```bash
# Test migrations against a copy of production data
# Step 1: Copy production data to staging
pg_dump $PRODUCTION_DATABASE_URL | psql $STAGING_DATABASE_URL

# Step 2: Run migration
npm run migrate:up
env DATABASE_URL=$STAGING_DATABASE_URL

# Step 3: Verify
npm run test:integration
env DATABASE_URL=$STAGING_DATABASE_URL

# Step 4: If it works, run against production
# If it fails, fix and repeat
```

## Summary

Database migrations are critical infrastructure for your SaaS. The key principles:

1. **Every migration must be reversible** — Always include down migrations
2. **Migrations are separate from code deploys** — Deploy code first, then migrate
3. **Test migrations against production-like data** — Never trust a migration only tested on empty DB
4. **Use expand-contract for breaking changes** — Add new, migrate data, switch, remove old
5. **Batch large migrations** — Use `FOR UPDATE SKIP LOCKED` with small batches
6. **Use CONCURRENTLY for indexes** — Don't block writes during index creation
7. **Automate migration running** — CI/CD should run migrations, not humans
8. **Monitor after migrations** — Watch for slow queries, error rate increases
9. **Backup before every migration** — You'll thank yourself if something goes wrong
10. **Migrations should be boring** — If your migration is exciting, you're doing it wrong

A good migration strategy lets you evolve your schema confidently, without fear of downtime or data loss. Invest in good tooling and processes early — it pays for itself the first time something goes wrong.
