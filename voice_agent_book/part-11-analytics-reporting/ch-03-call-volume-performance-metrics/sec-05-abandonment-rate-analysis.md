# Section 05: Abandonment Rate Analysis

## Overview

Abandonment rate analysis tracks the percentage of callers who hang up before reaching an agent, segmented by queue, campaign, time of day, and wait time bucket. Abandonment rate is a critical customer experience metric — high abandonment rates indicate that customers are frustrated with wait times or IVR complexity and may take their business elsewhere. The system provides both real-time abandonment rate (last 30 minutes, updated every 30 seconds) and historical trend analysis, with automatic threshold alerts when abandonment exceeds configurable limits.

The analysis distinguishes between early abandonment (within first 5 seconds — assumed to be misdials or IVR fatigue), mid-queue abandonment (5-60 seconds — indicates impatience with wait time), and late abandonment (60+ seconds — indicates serious service failure). Each category has different operational implications and remediation strategies. Abandonment is correlated with other metrics (queue depth, wait time, IVR path) to identify root causes and recommend interventions.

## Architecture

```
              Abandonment Rate Analysis Pipeline

   Call End Events → Stream Processor → Abandonment Calculator
                                             |
                                 ┌───────────┴───────────┐
                                 |                       |
                           Redis (real-time       ClickHouse (historical
                            abandonment %)        abandonment analysis)
                                 |                       |
                           Metrics API / WebSocket
                                 |
                   Abandonment Rate Gauge
                   Wait Time Bucket Breakdown
                   Time-of-Day Heatmap
                   Correlation Analysis
```

## Design Decisions

- **Abandonment categories (early, mid, late) over a single abandonment rate:** A single "abandonment rate" masks important differences. Early abandonments (< 5 seconds) are typically not the contact center's fault; late abandonments (> 60 seconds) indicate a service failure requiring immediate action. The system computes three abandonment rates and tracks them separately, with different alert thresholds for each. Trade-off: categorization requires tracking the time-of-abandonment precisely, which increases event processing complexity.

- **Normalized abandonment rate over raw abandonment percentage:** The raw abandonment rate (abandoned / offered) is misleading if self-service (IVR) handles a significant portion of calls before they reach a queue. The normalized rate excludes calls that abandoned during the IVR greeting or self-service flow, computing abandonment only for calls that entered a queue. Trade-off: determining "call entered queue" requires tracking the IVR-to-queue transition event, adding a dependency on the IVR event stream.

- **Heatmap visualization for time-of-day/day-of-week patterns over simple line charts:** Abandonment patterns often follow predictable time-based cycles (high abandonment during lunch hours, low abandonment mid-morning). A heatmap (hour × day of week, color = abandonment rate) reveals these patterns at a glance, enabling proactive staffing adjustments. Trade-off: heatmaps require more screen space than line charts and may be less familiar to some users; the dashboard provides both views.

## Implementation Approach

```typescript
interface AbandonmentRecord {
  callSid: string;
  tenantId: string;
  queueId: string;
  campaignId: string;
  waitTimeSeconds: number;
  abandonmentTimeSeconds: number;
  category: 'early' | 'mid' | 'late';
  ivrPath: string;
  timestamp: number;
  enteredQueueAt: number;
  abandonedAt: number;
}

interface AbandonmentStats {
  tenantId: string;
  periodStart: number;
  periodEnd: number;
  offered: number;
  abandoned: number;
  earlyAbandoned: number;
  midAbandoned: number;
  lateAbandoned: number;
  rawAbandonmentRate: number;     // abandoned / offered
  normalizedRate: number;         // abandoned / enteredQueue
  avgWaitBeforeAbandon: number;
  p50WaitBeforeAbandon: number;
  p95WaitBeforeAbandon: number;
}

class AbandonmentAnalyzer {
  private clickhouse: ClickHouseClient;

  async getAbandonmentStats(
    tenantId: string,
    start: number,
    end: number,
    filters?: { queueId?: string; campaignId?: string }
  ): Promise<AbandonmentStats> {
    const conditions = [
      `tenantId = '${tenantId}'`,
      `timestamp >= ${start}`,
      `timestamp <= ${end}`,
    ];
    if (filters?.queueId) conditions.push(`queueId = '${filters.queueId}'`);
    if (filters?.campaignId) conditions.push(`campaignId = '${filters.campaignId}'`);

    const result = await this.clickhouse.query(`
      SELECT
        count() as totalOffered,
        countIf(status = 'abandoned') as totalAbandoned,
        countIf(status = 'abandoned' AND waitTimeSeconds < 5) as earlyAbandoned,
        countIf(status = 'abandoned' AND waitTimeSeconds >= 5 AND waitTimeSeconds < 60) as midAbandoned,
        countIf(status = 'abandoned' AND waitTimeSeconds >= 60) as lateAbandoned,
        countIf(enteredQueue = 1) as enteredQueue,
        avgIf(waitTimeSeconds, status = 'abandoned') as avgWaitAbandon,
        quantile(0.5)If(waitTimeSeconds, status = 'abandoned') as p50WaitAbandon,
        quantile(0.95)If(waitTimeSeconds, status = 'abandoned') as p95WaitAbandon
      FROM call_queue_events
      WHERE ${conditions.join(' AND ')}
    `);

    const row = result[0];
    const abandoned = row.totalAbandoned;
    const offered = row.totalOffered;
    const enteredQueue = row.enteredQueue;

    return {
      tenantId,
      periodStart: start,
      periodEnd: end,
      offered,
      abandoned,
      earlyAbandoned: row.earlyAbandoned,
      midAbandoned: row.midAbandoned,
      lateAbandoned: row.lateAbandoned,
      rawAbandonmentRate: offered > 0 ? (abandoned / offered) * 100 : 0,
      normalizedRate: enteredQueue > 0 ? (abandoned / enteredQueue) * 100 : 0,
      avgWaitBeforeAbandon: row.avgWaitAbandon ?? 0,
      p50WaitBeforeAbandon: row.p50WaitAbandon ?? 0,
      p95WaitBeforeAbandon: row.p95WaitAbandon ?? 0,
    };
  }

  async getAbandonmentHeatmap(
    tenantId: string,
    start: number,
    end: number
  ): Promise<Array<{ hour: number; dayOfWeek: number; abandonmentRate: number; totalCalls: number }>> {
    const result = await this.clickhouse.query(`
      SELECT
        toHour(timestamp) as hour,
        toDayOfWeek(timestamp) as dayOfWeek,
        countIf(status = 'abandoned') / count() * 100 as abandonmentRate,
        count() as totalCalls
      FROM call_queue_events
      WHERE tenantId = '${tenantId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
      GROUP BY hour, dayOfWeek
      ORDER BY dayOfWeek, hour
    `);

    return result.map((row: any) => ({
      hour: row.hour,
      dayOfWeek: row.dayOfWeek,
      abandonmentRate: row.abandonmentRate,
      totalCalls: row.totalCalls,
    }));
  }

  async getAbandonmentCorrelation(
    tenantId: string,
    start: number,
    end: number
  ): Promise<{ queueDepth: number; avgWaitBeforeAnswer: number }> {
    // Correlate abandonment with queue depth and wait time
    const result = await this.clickhouse.query(`
      SELECT
        corr(abandoned.queueDepth, abandoned.count) as queueDepthCorrelation,
        corr(abandoned.avgWaitTime, abandoned.count) as waitTimeCorrelation
      FROM (
        SELECT
          toStartOfFiveMinutes(timestamp) as period,
          avg(queueDepth) as queueDepth,
          avg(avgWaitTimeSeconds) as avgWaitTime,
          countIf(status = 'abandoned') as count
        FROM call_queue_events
        WHERE tenantId = '${tenantId}'
          AND timestamp >= ${start}
          AND timestamp <= ${end}
        GROUP BY period
      ) as abandoned
    `);

    return {
      queueDepth: result[0].queueDepthCorrelation ?? 0,
      avgWaitBeforeAnswer: result[0].waitTimeCorrelation ?? 0,
    };
  }
}

// Abandonment rate widget
const AbandonmentWidget: React.FC<{
  tenantId: string;
  queueId?: string;
  threshold: number;
}> = ({ tenantId, queueId, threshold }) => {
  const [stats, setStats] = useState<AbandonmentStats | null>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      fetchAbandonmentStats(tenantId, { queueId }).then(setStats);
    }, 30000);
    return () => clearInterval(interval);
  }, [tenantId, queueId]);

  if (!stats) return <Loading />;

  const isAboveThreshold = stats.normalizedRate > threshold;

  return (
    <div className={`abandonment-widget ${isAboveThreshold ? 'alert' : 'normal'}`}>
      <div className="abandonment-gauge">
        <CircularGauge value={stats.normalizedRate} max={Math.max(threshold * 2, stats.normalizedRate)} />
        <div className="abandonment-rate">{stats.normalizedRate.toFixed(1)}%</div>
      </div>
      <div className="abandonment-breakdown">
        <CategoryBar
          early={stats.earlyAbandoned}
          mid={stats.midAbandoned}
          late={stats.lateAbandoned}
        />
      </div>
      <AbandonmentHeatmap tenantId={tenantId} />
      <AbandonmentCorrelationCard tenantId={tenantId} />
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Abandonment rate computation |
| Redis (RSAL) | Server | Real-time abandonment counter |
| Apache ECharts (Apache 2.0) | Client | Heatmap visualization |
| Apache Kafka (Apache 2.0) | Server | Call end event ingestion |

## Production Considerations

**Scaling:** Abandonment rate queries aggregate over time windows — use ClickHouse materialized views with 5-minute granularity for sub-second queries. Real-time abandonment rate uses Redis counters (abandoned count / offered count), updated via the stream processor every 10 seconds. For multi-queue tenants, compute abandonment rate per queue and display the worst-performing queue prominently.

**Security:** Abandonment rate data is tenant-scoped. Queue-level abandonment rates may be sensitive — a queue with consistently high abandonment may indicate understaffing, which could be used competitively. Access to queue-level abandonment data requires the `analytics:abandonment` permission. Raw abandonment records (individual caller wait times) are not exposed in aggregate views.

**Monitoring:** Track abandonment rate trends per queue and per campaign. Alert if normalized abandonment rate exceeds 10% for more than 10 consecutive minutes, if late abandonment (> 60s) exceeds 5%, or if the average wait-before-abandon drops below 15 seconds (indicating callers are giving up faster than usual). Monitor the correlation between queue depth and abandonment — if the correlation exceeds 0.8, staffing adjustments are likely needed.
