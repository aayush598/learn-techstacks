# Section 09: Data Archival & Cleanup

## Data Lifecycle Management

Data in the AI Voice Agent platform follows a defined lifecycle from creation through archival to deletion. Different data types have different retention requirements based on regulatory compliance, business needs, and storage costs.

```
Data Type          | Hot (PG) | Warm (ClickHouse) | Cold (MinIO) | Deleted
-------------------|----------|-------------------|--------------|---------
Active Calls       | 30 days  | —                 | —            | —
Completed Calls    | 90 days  | 12 months         | 84 months    | 7 yrs
Conversation Ev.   | 30 days  | —                 | 12 months    | 2 yrs
Usage Records      | 90 days  | 24 months         | —            | 7 yrs
Audit Logs         | 12 months| —                 | 84 months    | 10 yrs
Agent Configs      | Forever  | —                 | —            | Manual
Recordings         | 30 days  | —                 | 84 months    | 7 yrs
API Keys           | Forever  | —                 | —            | Manual
User Sessions      | 24 hours | —                 | —            | 24 hrs
Metrics            | —        | 12 months         | —            | —
```

## Data Flow Through Tiers

```
HOT (PostgreSQL) ──> WARM (ClickHouse) ──> COLD (MinIO JSON) ──> DELETE
   • Online           • Aggregations        • Archive            • Purge
   • Indexed          • Queries             • Backup
   • Fast access      • Cheap storage       • Cheap storage
   • Expensive

Timeline:
Day 0     Day 30          Day 90          Day 365          Day 2555
(PG Hot)  (Archive to     (Move to        (Archive to      (Purge if past
           MinIO, remove   ClickHouse,     MinIO JSON,      retention)
           from PG active) remove from PG) remove from CH)
```

## Partitioning Strategy

```sql
-- Calls table partitioned by month
CREATE TABLE calls (
  id UUID DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL,
  agent_id UUID NOT NULL,
  status VARCHAR(20) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Create monthly partitions via pg_partman
CREATE EXTENSION IF NOT EXISTS pg_partman;

SELECT partman.create_parent(
  p_parent_table := 'public.calls',
  p_control := 'created_at',
  p_type := 'native',
  p_interval := '1 month',
  p_premake := 3
);

-- Detach old partition for archival
ALTER TABLE calls DETACH PARTITION calls_2024_01;

-- Attach historical data partition
CREATE TABLE calls_2024_01_archive (
  LIKE calls INCLUDING ALL
) WITH (autovacuum_enabled = false);

ALTER TABLE calls ATTACH PARTITION calls_2024_01_archive
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## Archival Implementation

```typescript
// lib/data/archival.ts
import { prisma } from '@/lib/db'
import { minio } from '@/lib/minio'
import { kafka } from '@/lib/kafka'
import { redis } from '@/lib/redis'

interface ArchivalConfig {
  table: string
  retentionDays: number
  archiveTo: 'minio' | 'clickhouse' | 'delete'
  batchSize: number
}

const ARCHIVAL_POLICIES: ArchivalConfig[] = [
  { table: 'conversation_events', retentionDays: 30, archiveTo: 'minio', batchSize: 10000 },
  { table: 'transcript_chunks', retentionDays: 30, archiveTo: 'minio', batchSize: 10000 },
  { table: 'usage_records', retentionDays: 90, archiveTo: 'clickhouse', batchSize: 50000 },
  { table: 'audit_logs', retentionDays: 365, archiveTo: 'minio', batchSize: 25000 },
  { table: 'sessions', retentionDays: 1, archiveTo: 'delete', batchSize: 100000 },
]

export async function runArchival(): Promise<ArchivalResult> {
  const results: ArchivalResult = { archived: 0, deleted: 0, errors: 0 }

  for (const policy of ARCHIVAL_POLICIES) {
    const cutoffDate = new Date()
    cutoffDate.setDate(cutoffDate.getDate() - policy.retentionDays)

    let processed = 0
    let hasMore = true

    while (hasMore) {
      // Fetch batch of records to archive
      const records = await prisma.$queryRawUnsafe<Record<string, unknown>[]>(
        `SELECT * FROM ${policy.table}
         WHERE created_at < $1
         ORDER BY created_at ASC
         LIMIT $2`,
        cutoffDate,
        policy.batchSize
      )

      if (records.length === 0) {
        hasMore = false
        break
      }

      try {
        if (policy.archiveTo === 'minio') {
          // Archive to MinIO as JSON lines
          const tenantGroups = groupBy(records, 'tenant_id')
          for (const [tenantId, tenantRecords] of Object.entries(tenantGroups)) {
            const dateStr = cutoffDate.toISOString().split('T')[0]
            const key = `archives/${policy.table}/${tenantId}/${dateStr}-${Date.now()}.json`
            const content = tenantRecords.map(r => JSON.stringify(r)).join('\n')

            await minio.putObject(
              'data-archive',
              key,
              content,
              { 'Content-Type': 'application/json' }
            )
          }
        }

        // Delete archived records
        const ids = records.map(r => r.id)
        await prisma.$executeRawUnsafe(
          `DELETE FROM ${policy.table} WHERE id = ANY($1::uuid[])`,
          ids
        )

        processed += records.length
        results.archived += records.length

        // Throttle to avoid DB overload
        await sleep(100)

      } catch (error) {
        results.errors++
        console.error(`Archival error for ${policy.table}:`, error)
      }
    }

    logger.info({
      table: policy.table,
      archived: processed,
      destination: policy.archiveTo
    }, 'Archival batch completed')
  }

  return results
}
```

## TTL-Based Cleanup with pg_cron

```sql
-- Schedule archival via pg_cron
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Daily cleanup of expired sessions
SELECT cron.schedule(
  'cleanup-sessions',
  '0 3 * * *',  -- 3 AM daily
  $$DELETE FROM sessions WHERE expires_at < NOW() - INTERVAL '1 hour'$$
);

-- Weekly archival of old conversation events
SELECT cron.schedule(
  'archive-events',
  '0 4 * * 0',  -- 4 AM every Sunday
  $$SELECT run_archival_procedure()$$
);

-- Monthly partition maintenance
SELECT cron.schedule(
  'maintain-partitions',
  '0 5 1 * *',  -- 5 AM on the 1st of every month
  $$CALL partman.run_maintenance()$$
);

-- Nightly VACUUM ANALYZE on active tables
SELECT cron.schedule(
  'vacuum-analyze',
  '0 2 * * *',
  $$VACUUM ANALYZE calls; VACUUM ANALYZE agents; VACUUM ANALYZE campaigns$$
);
```

## Soft Delete Pattern

```typescript
// lib/data/soft-delete.ts
// Instead of DELETE, mark records as deleted

export async function softDeleteAgent(agentId: string, userId: string) {
  await prisma.agent.update({
    where: { id: agentId },
    data: {
      status: 'deleted',
      deletedAt: new Date(),
      deletedBy: userId
    }
  })

  // Exclude from normal queries via Prisma middleware
}

// Prisma middleware to filter soft-deleted records
prisma.$use(async (params, next) => {
  // Only apply to models with soft delete
  const softDeleteModels = ['agent', 'campaign', 'contact', 'prompt', 'voice']

  if (softDeleteModels.includes(params.model ?? '') &&
      params.action === 'findMany') {
    params.args = {
      ...params.args,
      where: {
        ...params.args.where,
        status: { not: 'deleted' }
      }
    }
  }

  return next(params)
})
```

## Data Retention Compliance

```typescript
// lib/compliance/retention.ts
import { prisma } from '@/lib/db'
import { minio } from '@/lib/minio'

interface RetentionPolicy {
  dataType: string
  retentionMonths: number
  regulatory: string[]  // GDPR, HIPAA, TCPA, etc.
  action: 'anonymize' | 'delete' | 'export'
}

export async function applyRetentionPolicy(tenantId: string, policy: RetentionPolicy) {
  const cutoffDate = new Date()
  cutoffDate.setMonth(cutoffDate.getMonth() - policy.retentionMonths)

  switch (policy.action) {
    case 'delete':
      // Hard delete after retention period
      if (policy.dataType === 'call_recordings') {
        const recordings = await prisma.callRecording.findMany({
          where: {
            call: { tenantId, createdAt: { lt: cutoffDate } }
          }
        })

        for (const rec of recordings) {
          // Delete from MinIO first
          await minio.removeObject(rec.storageBucket, rec.storagePath)
          if (rec.stereoUrl) await deleteFromURL(rec.stereoUrl)
          if (rec.agentUrl) await deleteFromURL(rec.agentUrl)
          if (rec.callerUrl) await deleteFromURL(rec.callerUrl)
        }

        // Then delete records
        await prisma.callRecording.deleteMany({
          where: {
            call: { tenantId, createdAt: { lt: cutoffDate } }
          }
        })

        // Anonymize call records (keep metadata, remove PII)
        await prisma.call.updateMany({
          where: { tenantId, createdAt: { lt: cutoffDate } },
          data: {
            callerNumber: '[REDACTED]',
            calledNumber: '[REDACTED]',
            recordingUrl: null,
            transcriptUrl: null
          }
        })
      }
      break

    case 'anonymize':
      // For GDPR right-to-erasure
      await prisma.user.update({
        where: { id: tenantId },
        data: {
          name: '[REDACTED]',
          email: `deleted-${Date.now()}@redacted.com`,
          passwordHash: null,
          avatarUrl: null
        }
      })
      break
  }
}
```

## Cleanup Monitoring

```typescript
// Prometheus metrics for archival
const archivalDuration = new prometheus.Histogram({
  name: 'data_archival_duration_seconds',
  help: 'Time taken for data archival by table',
  labelNames: ['table', 'status'],
  buckets: [10, 30, 60, 120, 300, 600]
})

const archivalRecordsCount = new prometheus.Counter({
  name: 'data_archival_records_total',
  help: 'Total records archived by table',
  labelNames: ['table', 'destination']
})

const archivalErrors = new prometheus.Counter({
  name: 'data_archival_errors_total',
  help: 'Total archival errors by table',
  labelNames: ['table']
})
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Partitioning | Monthly by created_at | Manageable size, aligns with retention periods |
| Archival Format | JSON Lines (MinIO) | Simple, compressible, queryable with tools |
| Soft Delete | Status column + middleware | Retains data for recovery within 30-day window |
| Hard Delete | Batch deletion after retention | Regulatory compliance, storage cost |
| Orchestration | pg_cron for DB, BullMQ for app | Respective strengths for scheduled tasks |

## Integration Points

- **Part 03 (Database Architecture)** — Partitioning and cleanup are schema-level concerns
- **Part 11 (Analytics)** — ClickHouse archives fed from cleanup pipeline
- **Part 12 (Recording)** — Recording retention governed by archival policies
- **Part 15 (Security/Compliance)** — GDPR right-to-erasure implemented via anonymization

## Production Considerations

- **Archival Window**: Run during low-traffic periods (3-5 AM local time)
- **Batch Size**: 10,000 records per batch; adjust based on row width and I/O
- **Error Handling**: Failed batches are retried with exponential backoff (3 retries)
- **Monitoring**: Track archival lag (how far behind real-time the archive is)
- **Storage Projection**: Project data growth to budget storage costs (MinIO is cheap but not free)
- **Testing**: Restore a partition from cold storage quarterly to verify archival integrity
