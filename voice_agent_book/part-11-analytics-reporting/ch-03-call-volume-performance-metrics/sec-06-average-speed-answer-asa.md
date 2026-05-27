# Section 06: Average Speed of Answer

## Overview

Average Speed of Answer (ASA) is the average time a caller waits in queue before being connected to an agent. It is one of the most commonly tracked contact center metrics and a key component of service level agreements (SLAs). The system computes ASA for answered calls only (excluding abandoned calls) and provides both the arithmetic mean and percentile breakdowns (p50, p75, p90, p95, p99) to give a complete picture of the wait experience.

ASA is tracked across multiple dimensions: per queue (each queue may have different SLA targets), per campaign (outbound vs inbound campaigns have different expectations), per time segment (peak hours vs off-peak), and per agent group (skill-based routing may affect ASA differently). Real-time ASA is computed on a rolling 30-minute window, updated every 30 seconds, and displayed alongside the trend. Historical ASA is available for any date range with comparison to previous periods.

## Architecture

```
              ASA Computation Pipeline

   Answer Events → Stream Processor → ASA Calculator
                                         |
                              Redis (rolling 30m ASA)
                              ClickHouse (historical ASA)
                                         |
                              Metrics API / WebSocket
                                         |
                    ASA Gauge Widget
                    ASA Trend Comparison
                    ASA by Queue/Campaign
                    ASA Percentile Breakdown
```

## Design Decisions

- **ASA computed from queue events (entered queue → answered) over call lifecycle events:** The canonical ASA metric measures the wait in queue, not the total time from call initiation (which includes IVR navigation). The system uses the `queue.entered` and `call.answered` events to compute queue wait time precisely. This ensures consistency across different IVR configurations. Trade-off: this requires the IVR system to emit `queue.entered` events with accurate timestamps, adding an integration requirement.

- **Percentile ASA alongside mean ASA over mean-only display:** The mean ASA is heavily influenced by outliers — a single call that waited 30 minutes while all others waited 30 seconds would push the mean from 30 seconds to 90 seconds. Percentiles (p50 = typical experience, p95 = near-worst case) provide a more actionable view. The system displays both mean and p95 ASA, with delta indicators showing how the tail experience compares to the typical. Trade-off: displaying multiple metrics increases visual complexity; the dashboard allows users to choose their preferred metric.

- **ASA comparison to previous period with significance testing over simple delta:** A 5-second increase in ASA from last week could be noise or a real degradation. The system applies a two-sample t-test comparing the current period's ASA distribution to the previous period's, flagging changes that are statistically significant (p < 0.05). Non-significant changes are shown with a muted visual treatment. Trade-off: statistical testing adds computational overhead and is not supported by all visualization libraries — we compute the p-value server-side and pass it as a data field.

## Implementation Approach

```typescript
interface AsaResult {
  queueId: string;
  periodStart: number;
  periodEnd: number;
  answeredCalls: number;
  meanAsaSeconds: number;
  p50AsaSeconds: number;
  p75AsaSeconds: number;
  p90AsaSeconds: number;
  p95AsaSeconds: number;
  p99AsaSeconds: number;
  maxAsaSeconds: number;
  previousPeriod?: {
    meanAsaSeconds: number;
    p95AsaSeconds: number;
    deltaMeanSeconds: number;
    deltaP95Seconds: number;
    significant: boolean;
    pValue: number;
  };
}

class AsaCalculator {
  private redis: Redis;
  private clickhouse: ClickHouseClient;

  // Real-time ASA for rolling window
  async getRealtimeAsa(queueId: string, windowMinutes: number = 30): Promise<AsaResult> {
    const now = Date.now();
    const windowStart = now - windowMinutes * 60 * 1000;

    return this.computeAsa(queueId, windowStart, now);
  }

  async computeAsa(queueId: string, start: number, end: number): Promise<AsaResult> {
    const result = await this.clickhouse.query(`
      SELECT
        count() as answeredCalls,
        avg(queueWaitTimeSeconds) as meanAsa,
        quantile(0.5)(queueWaitTimeSeconds) as p50,
        quantile(0.75)(queueWaitTimeSeconds) as p75,
        quantile(0.9)(queueWaitTimeSeconds) as p90,
        quantile(0.95)(queueWaitTimeSeconds) as p95,
        quantile(0.99)(queueWaitTimeSeconds) as p99,
        max(queueWaitTimeSeconds) as maxAsa
      FROM call_queue_events
      WHERE queueId = '${queueId}'
        AND status = 'answered'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
    `);

    const row = result[0];

    // Get previous period for comparison
    const periodDuration = end - start;
    const previousStart = start - periodDuration;
    const previousAsa = await this.computePreviousAsa(queueId, previousStart, start);

    return {
      queueId,
      periodStart: start,
      periodEnd: end,
      answeredCalls: row.answeredCalls,
      meanAsaSeconds: row.meanAsa ?? 0,
      p50AsaSeconds: row.p50 ?? 0,
      p75AsaSeconds: row.p75 ?? 0,
      p90AsaSeconds: row.p90 ?? 0,
      p95AsaSeconds: row.p95 ?? 0,
      p99AsaSeconds: row.p99 ?? 0,
      maxAsaSeconds: row.maxAsa ?? 0,
      previousPeriod: previousAsa ? {
        meanAsaSeconds: previousAsa.mean,
        p95AsaSeconds: previousAsa.p95,
        deltaMeanSeconds: (row.meanAsa ?? 0) - previousAsa.mean,
        deltaP95Seconds: (row.p95 ?? 0) - previousAsa.p95,
        significant: previousAsa.pValue < 0.05,
        pValue: previousAsa.pValue,
      } : undefined,
    };
  }

  private async computePreviousAsa(
    queueId: string,
    start: number,
    end: number
  ): Promise<{ mean: number; p95: number; pValue: number } | null> {
    const current = await this.clickhouse.query(`
      SELECT avg(queueWaitTimeSeconds) as mean, quantile(0.95)(queueWaitTimeSeconds) as p95
      FROM call_queue_events
      WHERE queueId = '${queueId}'
        AND status = 'answered'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
    `);

    if (current.length === 0 || current[0].mean == null) return null;

    // Compute p-value using Welch's t-test approximation via ClickHouse
    const stats = await this.clickhouse.query(`
      SELECT
        t.testStatistic as tStat,
        t.pValue as pValue
      FROM (
        SELECT
          (avg1 - avg2) / sqrt(var1/n1 + var2/n2) as testStatistic,
          /* Approximate p-value using Student's t distribution */
          2 * (1 - cdfStudentsT(testStatistic, 
            (pow(var1/n1 + var2/n2, 2)) / 
            (pow(var1/n1, 2)/(n1-1) + pow(var2/n2, 2)/(n2-1))
          )) as pValue
        FROM (
          SELECT
            avgIf(queueWaitTimeSeconds, timestamp >= ${start} AND timestamp <= ${end}) as avg1,
            varSampIf(queueWaitTimeSeconds, timestamp >= ${start} AND timestamp <= ${end}) as var1,
            countIf(timestamp >= ${start} AND timestamp <= ${end}) as n1,
            avgIf(queueWaitTimeSeconds, timestamp >= ${start} - ${end - start} AND timestamp < ${start}) as avg2,
            varSampIf(queueWaitTimeSeconds, timestamp >= ${start} - ${end - start} AND timestamp < ${start}) as var2,
            countIf(timestamp >= ${start} - ${end - start} AND timestamp < ${start}) as n2
          FROM call_queue_events
          WHERE queueId = '${queueId}'
            AND status = 'answered'
            AND timestamp >= ${start - (end - start)}
            AND timestamp <= ${end}
        )
      ) as t
    `);

    return {
      mean: current[0].mean,
      p95: current[0].p95,
      pValue: stats[0]?.pValue ?? 1.0,
    };
  }

  // Real-time ASA via Redis sorted set
  async pushWaitTime(queueId: string, callSid: string, waitTimeSeconds: number): Promise<void> {
    const key = `asa:${queueId}`;
    await this.redis.zadd(key, Date.now(), `${callSid}:${waitTimeSeconds}`);
    await this.redis.expire(key, 3600); // 1 hour TTL
  }

  async getRollingAsa(queueId: string, windowMinutes: number = 30): Promise<number> {
    const cutoff = Date.now() - windowMinutes * 60 * 1000;
    const entries = await this.redis.zrangebyscore(
      `asa:${queueId}`,
      cutoff,
      '+inf',
      'WITHSCORES'
    );

    let total = 0;
    let count = 0;
    for (let i = 0; i < entries.length; i += 2) {
      const waitTime = parseInt(entries[i].split(':')[1]);
      total += waitTime;
      count++;
    }
    return count > 0 ? total / count : 0;
  }
}

// ASA widget component
const AsaWidget: React.FC<{
  queueId: string;
  slaTargetSeconds: number;
}> = ({ queueId, slaTargetSeconds }) => {
  const [asa, setAsa] = useState<AsaResult | null>(null);

  useEffect(() => {
    const fetchAsa = async () => {
      const result = await fetchRealtimeAsa(queueId);
      setAsa(result);
    };
    fetchAsa();
    const interval = setInterval(fetchAsa, 30000);
    return () => clearInterval(interval);
  }, [queueId]);

  if (!asa) return <Loading />;

  const meetingSla = asa.meanAsaSeconds <= slaTargetSeconds;

  return (
    <div className={`asa-widget ${meetingSla ? 'on-target' : 'below-target'}`}>
      <div className="asa-main">
        <span className="asa-value">{formatDuration(asa.meanAsaSeconds)}</span>
        <span className="asa-label">Avg Speed of Answer</span>
      </div>
      <div className="asa-percentiles">
        <PercentileBar
          p50={asa.p50AsaSeconds}
          p75={asa.p75AsaSeconds}
          p95={asa.p95AsaSeconds}
          target={slaTargetSeconds}
        />
      </div>
      {asa.previousPeriod && (
        <ComparisonIndicator
          delta={asa.previousPeriod.deltaMeanSeconds}
          significant={asa.previousPeriod.significant}
        />
      )}
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | ASA computation and statistical testing |
| Redis (RSAL) | Server | Rolling ASA buffer |
| Apache Kafka (Apache 2.0) | Server | Queue event ingestion |
| Recharts (MIT) | Client | ASA trend and percentile visualization |

## Production Considerations

**Scaling:** Rolling ASA in Redis uses a sorted set per queue with 1-hour TTL. Each call adds one entry (~50 bytes), so 10,000 answered calls = ~500 KB per queue. For 200 queues this is ~100 MB — acceptable on a Redis instance with 8 GB RAM. Historical ASA queries use ClickHouse with indexes on (queueId, timestamp). Pre-aggregate hourly ASA into a materialized view for fast dashboard loading.

**Security:** ASA data is queue-scoped. Queue IDs include the tenant ID prefix to enforce tenant isolation. The ASA metric itself is generally not sensitive, but per-agent ASA breakdown (ASA for calls answered by a specific agent) is considered agent performance data and requires the `agent-performance:view` permission.

**Monitoring:** Track ASA per queue over time. Alert if ASA exceeds the SLA target for more than 10 consecutive minutes, if p95 ASA exceeds 3x the mean (indicating a severe tail issue), or if ASA increases by more than 20% compared to the same period last week (statistically significant). Monitor the ASA calculation latency — it should complete in under 100 ms for real-time queries.
