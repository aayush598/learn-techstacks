# Retention & Archival

## Overview

Log retention policies define how long activity data is kept in hot storage and when it transitions to warm/cold tiers. This balances query performance with storage costs and compliance requirements.

## Retention Model

```typescript
interface RetentionPolicy {
  tenantId: string;
  hotStorageDays: number;      // Elasticsearch: fast query
  warmStorageDays: number;     // S3/Glacier: cheaper, slower query
  coldStorageDays: number;     // Glacier Deep Archive: long-term
  maxTotalDays: number;        // Hard retention limit
  complianceMinDays: number;   // Minimum retention for compliance
}

const DEFAULT_RETENTION: RetentionPolicy = {
  hotStorageDays: 90,
  warmStorageDays: 365,
  coldStorageDays: 1095,       // 3 years
  maxTotalDays: 1825,          // 5 years
  complianceMinDays: 365,      // SOC 2 minimum
};
```

## Archival Service

```typescript
class LogArchivalService {
  async archiveHotToWarm(): Promise<ArchivalResult> {
    const cutoff = new Date(Date.now() - DEFAULT_RETENTION.hotStorageDays * 86400000);

    // Query logs older than hot storage period
    const oldLogs = await this.es.search({
      index: 'activity_logs',
      body: {
        query: { range: { timestamp: { lt: cutoff } } },
        size: 10000,
      },
    });

    // Store in S3 as compressed JSON
    const key = `warm/activity_logs/${cutoff.toISOString().slice(0, 7)}.json.gz`;
    const compressed = gzipSync(JSON.stringify(oldLogs.hits));
    await this.s3.putObject({ Bucket: WARM_BUCKET, Key: key, Body: compressed });

    // Delete from hot storage
    await this.es.deleteByQuery({
      index: 'activity_logs',
      body: { query: { range: { timestamp: { lt: cutoff } } } },
    });

    return { archived: oldLogs.hits.length, to: 'warm', key };
  }

  async queryArchivedLogs(query: LogSearchQuery): Promise<ActivityEvent[]> {
    const results: ActivityEvent[] = [];

    // Search hot storage first
    const hotResults = await this.searchService.search({
      ...query,
      dateRange: {
        start: new Date(Math.max(query.dateRange.start.getTime(), Date.now() - DEFAULT_RETENTION.hotStorageDays * 86400000)),
        end: query.dateRange.end,
      },
    });
    results.push(...hotResults.hits);

    // If query range extends beyond hot storage, search warm storage
    if (query.dateRange.start.getTime() < Date.now() - DEFAULT_RETENTION.hotStorageDays * 86400000) {
      const warmResults = await this.queryWarmStorage(query);
      results.push(...warmResults);
    }

    return results;
  }

  private async queryWarmStorage(query: LogSearchQuery): Promise<ActivityEvent[]> {
    // List relevant S3 files by month
    const months = this.getMonthsInRange(query.dateRange.start, query.dateRange.end);
    const results: ActivityEvent[] = [];

    for (const month of months) {
      const key = `warm/activity_logs/${month}.json.gz`;
      try {
        const obj = await this.s3.getObject({ Bucket: WARM_BUCKET, Key: key });
        const decompressed = gunzipSync(obj.Body as Buffer);
        const logs: ActivityEvent[] = JSON.parse(decompressed.toString());

        // Apply filters in-memory
        const filtered = logs.filter(log =>
          log.timestamp >= query.dateRange.start &&
          log.timestamp <= query.dateRange.end &&
          (!query.filters.actions?.length || query.filters.actions.includes(log.action))
        );
        results.push(...filtered);
      } catch { /* File doesn't exist */ }
    }

    return results;
  }
}
```

## Deletion Scheduling

```typescript
class LogDeletionService {
  async deleteExpiredLogs(): Promise<number> {
    const cutoff = new Date(Date.now() - DEFAULT_RETENTION.maxTotalDays * 86400000);
    let deleted = 0;

    // Delete from cold storage
    const months = this.getMonthsBefore(cutoff);
    for (const month of months) {
      const key = `cold/activity_logs/${month}.json.gz`;
      try {
        await this.s3.deleteObject({ Bucket: COLD_BUCKET, Key: key });
        deleted++;
      } catch { /* File doesn't exist */ }
    }

    return deleted;
  }
}
```

## Open-Source Tools

- **AWS S3 Glacier** / **S3-compatible** — Cold storage
- **AWS S3 Lifecycle Policies** — Automated tier transitions
- **Elasticsearch ILM** (Index Lifecycle Management) — Hot/warm/cold phases

## Production Considerations

- Hot: Elasticsearch (90 days, SSD-backed)
- Warm: S3 Standard (1 year, compressed JSON)
- Cold: S3 Glacier Deep Archive (3-5 years)
- Compliance minimum retention: 1 year (configurable per framework)
- Provide archived log access with 24-hour retrieval delay for cold storage
- Test archival/restore process quarterly
- Monitor storage costs per tier, project monthly growth
- Encrypt all archived logs at rest (AES-256)
- Include tenant ID in archive key for tenant-level deletion
