# Section 02: Call Duration Distribution Analysis

## Overview

Call duration distribution analysis provides statistical insights into how long calls last across different segments (campaign, agent, IVR path, time of day, day of week). Understanding the distribution — not just the average — is critical for staffing optimization, cost estimation (per-minute billing), and identifying outliers that may indicate problems (e.g., agents keeping customers on hold excessively, or calls stuck in IVR loops).

The system computes duration statistics at multiple granularities: per-call (individual call duration logged on call end), per-session (agent shift aggregates), and per-campaign (aggregate distributions). The distribution is visualized as histograms (number of calls in each duration bucket: 0-30s, 30-60s, 1-2m, 2-5m, 5-10m, 10-30m, 30m+), box plots (showing min, p25, p50, p75, p95, p99, max), and violin plots (showing the full distribution shape). The analysis is available in real-time for the current window and historically for any date range.

## Architecture

```
            Call Duration Distribution Pipeline

   Call End Events → Stream Processor → Histogram Builder
                                              |
                                    ClickHouse
                                    (per-call raw durations)
                                              |
                          ┌───────────────────┴──┐
                          |                      |
                    Distribution API        Batch Aggregator
                    (percentile queries)    (hourly histograms)
                          |                      |
                    Duration Widgets       Data Export (CSV)
                    (histogram, box,       (for offline analysis)
                     violin charts)
```

## Design Decisions

- **Percentile-based statistics (p50, p95, p99) over mean and standard deviation:** Call duration distributions are typically right-skewed — most calls are short (2-5 minutes) but a few are very long (30+ minutes). The mean is pulled right by outliers, making it a poor representation of the typical experience. Percentiles provide a more accurate picture: p50 (median) represents the typical call, p95 represents the near-worst case, p99 represents the extreme. Trade-off: percentile computation is more expensive than mean — we use t-digest algorithm for approximate percentiles in the stream processor, and exact percentiles in ClickHouse for historical queries.

- **t-digest for stream percentile computation over exact sorting:** The t-digest algorithm maintains a sparse representation of the distribution, merging nearby centroids as data arrives. It provides ε-accurate quantile estimates (ε = 0.01 for p50, ε = 0.001 for p99) with O(log N) memory. This enables real-time percentile tracking without storing all individual call durations. Trade-off: t-digest is approximate — estimates for extreme percentiles (p99.9) have lower accuracy. For exact billing-grade statistics, we use ClickHouse's `quantileExact` in the batch layer.

- **Histogram buckets with logarithmic spacing over linear spacing:** Linear buckets (0-60s, 60-120s, 120-180s, ...) would require hundreds of buckets to cover the full range from 5 seconds to 2 hours. Logarithmic buckets (0-30s, 30-60s, 60-120s, 2-5m, 5-10m, 10-30m, 30-60m, 60m+) provide better resolution for short calls (where precision matters more) while still covering long tail calls. Trade-off: logarithmic buckets make the histogram harder to read for users who expect equal-width bars.

## Implementation Approach

```typescript
interface DurationRecord {
  callSid: string;
  tenantId: string;
  campaignId: string;
  agentId?: string;
  direction: 'inbound' | 'outbound' | 'internal';
  durationSeconds: number;
  status: string;
  ivrPath?: string;
  timestamp: number;
}

interface DurationDistribution {
  tenantId: string;
  timeRange: { start: number; end: number };
  totalCalls: number;
  percentiles: { p50: number; p75: number; p90: number; p95: number; p99: number; max: number };
  histogram: Array<{ bucket: string; count: number; percentage: number }>;
  average: number;
  standardDeviation: number;
  segments?: Record<string, DurationDistribution>; // per-agent/per-campaign breakdown
}

class DurationAnalyzer {
  private tdigests: Map<string, TDigest> = new Map();
  private clickhouse: ClickHouseClient;

  // Process call end event in stream
  processCallEnd(event: DurationRecord): void {
    const key = `${event.tenantId}:${event.campaignId ?? 'default'}`;

    if (!this.tdigests.has(key)) {
      this.tdigests.set(key, new TDigest({ compression: 100 }));
    }

    this.tdigests.get(key)!.push(event.durationSeconds);
  }

  async getDistribution(
    tenantId: string,
    start: number,
    end: number,
    filters?: { campaignId?: string; agentId?: string; direction?: string }
  ): Promise<DurationDistribution> {
    // Build ClickHouse query with filters
    const conditions = [
      `tenantId = '${tenantId}'`,
      `timestamp >= ${start}`,
      `timestamp <= ${end}`,
    ];
    if (filters?.campaignId) conditions.push(`campaignId = '${filters.campaignId}'`);
    if (filters?.agentId) conditions.push(`agentId = '${filters.agentId}'`);
    if (filters?.direction) conditions.push(`direction = '${filters.direction}'`);

    const result = await this.clickhouse.query(`
      SELECT
        count() as totalCalls,
        avg(durationSeconds) as average,
        stddevSamp(durationSeconds) as standardDeviation,
        quantile(0.5)(durationSeconds) as p50,
        quantile(0.75)(durationSeconds) as p75,
        quantile(0.9)(durationSeconds) as p90,
        quantile(0.95)(durationSeconds) as p95,
        quantile(0.99)(durationSeconds) as p99,
        max(durationSeconds) as maxDuration,
        histogram(10)(durationSeconds) as histData
      FROM call_records
      WHERE ${conditions.join(' AND ')}
    `);

    const row = result[0];

    // Build histogram from ClickHouse histogram result
    const histogram = this.buildHistogram(row.histData, row.totalCalls);

    return {
      tenantId,
      timeRange: { start, end },
      totalCalls: row.totalCalls,
      percentiles: {
        p50: row.p50, p75: row.p75, p90: row.p90,
        p95: row.p95, p99: row.p99, max: row.maxDuration,
      },
      histogram,
      average: row.average,
      standardDeviation: row.standardDeviation,
    };
  }

  private buildHistogram(
    histData: Array<[number, number, number]>,
    totalCalls: number
  ): Array<{ bucket: string; count: number; percentage: number }> {
    return histData.map(([lower, upper, count]) => ({
      bucket: this.formatBucketRange(lower, upper),
      count: Math.round(count),
      percentage: (count / totalCalls) * 100,
    }));
  }

  private formatBucketRange(lower: number, upper: number): string {
    if (lower < 60) return `${Math.round(lower)}-${Math.round(upper)}s`;
    if (lower < 3600) return `${Math.round(lower / 60)}-${Math.round(upper / 60)}m`;
    return `${Math.round(lower / 3600)}-${Math.round(upper / 3600)}h`;
  }
}

// Duration distribution chart component
const DurationDistributionChart: React.FC<{
  distribution: DurationDistribution;
  groupBy?: 'agent' | 'campaign' | 'ivrPath';
}> = ({ distribution, groupBy }) => {
  return (
    <div className="duration-distribution">
      <div className="percentile-summary">
        <PercentileCard label="Median (p50)" value={formatDuration(distribution.percentiles.p50)} />
        <PercentileCard label="p95" value={formatDuration(distribution.percentiles.p95)} />
        <PercentileCard label="p99" value={formatDuration(distribution.percentiles.p99)} />
        <PercentileCard label="Max" value={formatDuration(distribution.percentiles.max)} />
        <PercentileCard label="Average" value={formatDuration(distribution.average)} />
      </div>
      <HistogramChart
        data={distribution.histogram}
        xKey="bucket"
        yKey="count"
        tooltipFormatter={(d: any) => `${d.bucket}: ${d.count} calls (${d.percentage.toFixed(1)}%)`}
      />
      {groupBy && distribution.segments && (
        <SegmentBreakdown
          segments={distribution.segments}
          metricKey="average"
        />
      )}
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| t-digest (Apache 2.0) | Server | Approximate percentile computation |
| ClickHouse (Apache 2.0) | Server | Exact percentile and histogram queries |
| Apache ECharts (Apache 2.0) | Client | Box plot and violin chart rendering |
| D3.js (ISC) | Client | Custom histogram visualization |

## Production Considerations

**Scaling:** The t-digest data structure is maintained per tenant+campaign in memory (~10 KB per digest). For tenants with 500+ campaigns, use a digest pool with LRU eviction, serializing evicted digests to Redis. ClickHouse's `quantile` and `histogram` functions are optimized for columnar storage and handle millions of rows in under 100 ms. For dashboard auto-refresh, cache percentile results for 30 seconds since they change slowly.

**Security:** Duration data is tenant-scoped. Per-agent duration distributions should only be visible to supervisors with the `agent-performance:view` permission. Raw duration records (individual call durations) are PII-adjacent because they can identify specific customer interactions — access to raw records requires `calls:view-details` permission. Aggregate distributions (histograms, percentiles) are safe for broader access.

**Monitoring:** Track duration distribution query performance (p95 < 200 ms). Alert if the stream processor's t-digest memory exceeds 500 MB — this indicates too many segments requiring digest serialization offload. Monitor the percentage of calls with duration > 30 minutes — a sudden increase may indicate an IVR loop bug. Track the median handle time trend per campaign to detect gradual degradation requiring investigation.
