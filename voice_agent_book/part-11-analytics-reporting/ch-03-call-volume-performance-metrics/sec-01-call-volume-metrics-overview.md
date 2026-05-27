# Section 01: Call Volume Metrics Overview

## Overview

Call volume metrics provide the foundational quantitative data for understanding contact center workload patterns. These metrics track the number of calls offered, answered, abandoned, and overflowed over configurable time windows (5 minutes, hourly, daily, weekly, monthly). They are the primary input for capacity planning, staffing optimization, and trend analysis. The metrics are computed from the stream processor's aggregation layer, which consumes call lifecycle events (call.ringing, call.answered, call.ended) and writes pre-aggregated counts to Redis Time Series and ClickHouse.

The system distinguishes between inbound calls (offered by customers), outbound calls (initiated by agents or campaigns), and internal transfers. Each call type has different volume characteristics and business implications. Volume metrics are displayed on the dashboard as sparkline widgets, bar charts comparing current period to previous period, and cumulative daily counts with projected end-of-day estimates based on historical patterns.

## Architecture

```
            Call Volume Metrics Pipeline

   Kafka Events → Stream Processor → Aggregator
                                          |
                              Redis Time Series (5s)
                              ClickHouse (hourly/daily)
                                          |
                               Metrics API / WebSocket
                                          |
                              Volume Widgets & Charts
                                          |
                    Current vs Previous Comparison
                    Projected End-of-Day Estimate
```

## Design Decisions

- **Dual storage with Redis for real-time and ClickHouse for historical analysis:** Real-time volume queries (last 5 minutes) read from Redis Time Series for low-latency access. Historical queries (daily, weekly, monthly trends) read from ClickHouse, which stores pre-aggregated rollups. This dual approach provides sub-10 ms real-time reads while keeping historical query costs low. Trade-off: the two stores must be kept in sync; the batch aggregation job runs every hour to reconcile ClickHouse with the raw event data from Kafka.

- **Distinct handling of inbound, outbound, and transferred calls over a unified "calls" metric:** Treating all call types identically hides important operational signals. The stream processor tags each call event with a `direction` field (`inbound`, `outbound`, `internal`) and volume aggregations are computed per direction. Dashboards show both total volume and per-direction breakdowns. Trade-off: per-direction aggregation triples the number of time series keys, but the additional storage cost is negligible (each key is just a counter).

- **Projected end-of-day estimates using historical patterns over simple linear extrapolation:** A simple extrapolation ("current volume / elapsed fraction of day") is unreliable because call volume follows daily seasonality (peak hours, lunch dips, end-of-day surges). Instead, the projection compares current volume against the same time window from the last 30 days (weighted average, with more weight on recent days and same day of week). Trade-off: the projection model requires 30 days of history to warm up and must be recalculated whenever the historical data is updated.

## Implementation Approach

```typescript
interface CallVolumeAggregation {
  tenantId: string;
  timestamp: number;
  windowSeconds: number;
  direction: 'inbound' | 'outbound' | 'internal' | 'total';
  offered: number;
  answered: number;
  abandoned: number;
  overflowed: number;
  transferred: number;
  avgConcurrent: number;
  peakConcurrent: number;
}

class CallVolumeAggregator {
  private redisTs: RedisTimeSeries;
  private clickhouse: ClickHouseClient;

  async aggregate(windowSeconds: number = 300): Promise<void> {
    const now = Date.now();
    const windowStart = now - windowSeconds * 1000;

    // Query call events from Kafka stream processor output
    const events = await this.queryCallEvents(windowStart, now);

    const byDirection = new Map<string, CallVolumeAggregation>();

    for (const event of events) {
      const key = `${event.direction}`;
      if (!byDirection.has(key)) {
        byDirection.set(key, {
          tenantId: event.tenantId,
          timestamp: now,
          windowSeconds,
          direction: event.direction,
          offered: 0, answered: 0, abandoned: 0,
          overflowed: 0, transferred: 0,
          avgConcurrent: 0, peakConcurrent: 0,
        });
      }
      const agg = byDirection.get(key)!;
      agg.offered++;
      if (event.status === 'answered') agg.answered++;
      if (event.status === 'abandoned') agg.abandoned++;
      if (event.overflowed) agg.overflowed++;
      if (event.transferred) agg.transferred++;
    }

    // Write per-direction to Redis Time Series
    for (const [direction, agg] of byDirection) {
      await this.redisTs.add(
        `ts:${agg.tenantId}:volume:${direction}`,
        agg.offered,
        now,
        { labels: { tenantId: agg.tenantId, direction, metric: 'offered' } }
      );
    }

    // Write total aggregate
    const total = Array.from(byDirection.values()).reduce(
      (acc, agg) => ({
        ...acc,
        offered: acc.offered + agg.offered,
        answered: acc.answered + agg.answered,
        abandoned: acc.abandoned + agg.abandoned,
        overflowed: acc.overflowed + agg.overflowed,
        transferred: acc.transferred + agg.transferred,
      }),
      { offered: 0, answered: 0, abandoned: 0, overflowed: 0, transferred: 0 }
    );

    await this.redisTs.add(
      `ts:${events[0]?.tenantId}:volume:total`,
      total.offered,
      now,
      { labels: { metric: 'offered' } }
    );
  }

  async getProjectedEndOfDay(
    tenantId: string,
    date: string
  ): Promise<{ projected: number; confidence: number }> {
    // Get historical patterns for the same day of week
    const historicalVolumes = await this.clickhouse.query(`
      SELECT toStartOfHour(timestamp) as hour, avg(offered) as avgOffered
      FROM daily_volume_rollups
      WHERE tenantId = '${tenantId}'
        AND dayOfWeek(timestamp) = dayOfWeek('${date}')
        AND timestamp >= '${date}' - INTERVAL 30 DAY
        AND timestamp < '${date}'
      GROUP BY hour
      ORDER BY hour
    `);

    // Get current volume so far today
    const currentVolume = await this.clickhouse.query(`
      SELECT sum(offered) as offeredSoFar
      FROM call_events
      WHERE tenantId = '${tenantId}'
        AND toDate(timestamp) = '${date}'
    `);

    // Extrapolate remaining hours using historical pattern
    const currentHour = new Date().getHours();
    const remainingHours = 24 - currentHour;
    const projectedRemaining = historicalVolumes
      .filter((h: any) => h.hour > currentHour)
      .reduce((sum: number, h: any) => sum + h.avgOffered, 0);

    return {
      projected: currentVolume[0].offeredSoFar + projectedRemaining,
      confidence: Math.min(0.95, remainingHours > 12 ? 0.7 : 0.9),
    };
  }
}

// Dashboard volume comparison widget
interface VolumeComparisonProps {
  currentPeriod: { label: string; offered: number; answered: number };
  previousPeriod: { label: string; offered: number; answered: number };
}

const VolumeComparisonWidget: React.FC<VolumeComparisonProps> = ({ currentPeriod, previousPeriod }) => {
  const deltaOffered = currentPeriod.offered - previousPeriod.offered;
  const pctOffered = previousPeriod.offered > 0
    ? (deltaOffered / previousPeriod.offered) * 100 : 0;
  const answerRate = currentPeriod.offered > 0
    ? (currentPeriod.answered / currentPeriod.offered) * 100 : 0;

  return (
    <div className="volume-comparison">
      <div className="metric-group">
        <MetricLabel label="Offered" value={currentPeriod.offered} />
        <DeltaBadge value={pctOffered} direction={pctOffered >= 0 ? 'up' : 'down'} />
      </div>
      <div className="metric-group">
        <MetricLabel label="Answered" value={currentPeriod.answered} />
        <MetricLabel label="Answer Rate" value={`${answerRate.toFixed(1)}%`} />
      </div>
      <div className="metric-group">
        <MetricLabel label="Previous" value={`${previousPeriod.label}: ${previousPeriod.offered}`} />
      </div>
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| RedisTimeSeries (RSAL) | Server | Real-time volume counters |
| ClickHouse (Apache 2.0) | Server | Historical volume rollups |
| Apache Kafka (Apache 2.0) | Server | Call event ingestion |
| Apache Flink (Apache 2.0) | Server | Stream aggregation |

## Production Considerations

**Scaling:** Volume aggregation windows are computed at multiple granularities simultaneously (5-minute, 15-minute, hourly, daily). The stream processor uses tumbling windows with concurrent sliding windows — each call event is counted in exactly one 5-minute window, one 15-minute window, one hourly bucket, etc. Use Redis pipeline commands to batch all time-series writes for a single aggregation cycle. For tenants with 10,000+ calls/hour, pre-aggregate in Kafka Streams before writing to Redis.

**Security:** Volume metrics are tenant-scoped — the aggregation key includes the tenant ID, and queries filter by tenant ID. Projected end-of-day estimates use only historical data from the same tenant. Rate-limit volume metric API calls to 10 requests per second per user to prevent abuse. Cache projection results for 5 minutes since they change slowly.

**Monitoring:** Track aggregation latency (event timestamp to Redis write), Redis TimeSeries memory usage, and ClickHouse query performance for volume rollups. Alert if aggregation latency exceeds 30 seconds — this indicates stream processor backpressure. Monitor the accuracy of end-of-day projections by comparing projected vs actual volume at the end of each day; if average error exceeds 15%, review the projection model parameters.
