# Section 03: Wait Time and Service Level Metrics

## Overview

Wait time and service level metrics measure the customer experience before a call is answered. These metrics are critical for contact center operations — long wait times directly correlate with customer dissatisfaction and abandonment. The system tracks time-to-answer (the duration from when a call enters the queue to when an agent answers), queue depth (number of calls waiting), longest wait time (the oldest unhandled call), and service level (percentage of calls answered within a target threshold, e.g., 80% of calls answered within 20 seconds).

Service level is computed using the industry-standard methodology (percentage of calls answered within N seconds out of total calls offered, excluding abandoned calls that waited less than N seconds, the "TSF" method). The metrics are segmented by queue, campaign, time of day, and day of week to identify patterns in customer wait experience. Real-time widgets show the current service level against the target with color-coded status (green = meeting target, yellow = within 10% of target, red = below target).

## Architecture

```
               Wait Time and Service Level Pipeline

   Queue Events → Stream Processor → Service Level Calculator
                                            |
                                Redis (current queue state)
                                ClickHouse (historical SLAs)
                                            |
                                 Metrics API / WebSocket
                                            |
                              Service Level Gauge Widget
                              Queue Depth Chart
                              Wait Time Distribution
```

## Design Decisions

- **Service level with "abandoned within threshold" exclusion over simple answered/offered ratio:** The standard formula for service level — percentage of calls answered within N seconds out of all calls offered, excluding calls abandoned before N seconds — provides a fairer measure of the contact center's responsiveness. Calls that abandon very quickly (within the threshold) are assumed to be due to caller impatience rather than center performance. Trade-off: this formula can be gamed by increasing the abandonment exclusion threshold; the system logs the raw answered/offered ratio alongside the adjusted service level for transparency.

- **Real-time queue depth snapshot from Redis over ClickHouse query:** The current queue depth and longest wait time need to be available in under 50 ms for real-time dashboard widgets. Redis stores the current queue state as a sorted set (score = queue entry timestamp), enabling O(log N) queries for count and range. ClickHouse is used for historical queue depth trends. Trade-off: Redis state is ephemeral — on restart, queue state is restored from the stream processor's checkpointed state in Kafka.

- **Time-based segmentation for service level targets over a single target:** Different contact center queues (sales vs support vs billing) and different hours (business hours vs after-hours) have different service level expectations. The system supports configurable service level targets per queue+time segment, evaluated hourly. A weekday daytime queue may have an 80/20 target, while an after-hours queue may have a 60/30 target. Trade-off: segmented targets increase configuration complexity but provide more accurate operational visibility.

## Implementation Approach

```typescript
interface QueueState {
  queueId: string;
  tenantId: string;
  depth: number;
  longestWaitSeconds: number;
  callsInQueue: Array<{
    callSid: string;
    enteredAt: number;
    waitTime: number;
    priority: number;
  }>;
}

interface ServiceLevelResult {
  queueId: string;
  tenantId: string;
  periodStart: number;
  periodEnd: number;
  offered: number;
  answered: number;
  abandoned: number;
  answeredWithinTarget: number;
  abandonedWithinTarget: number;
  serviceLevel: number;          // percentage
  targetPercent: number;
  targetSeconds: number;
  averageSpeedOfAnswer: number;  // ASA
  longestWaitTime: number;
}

class ServiceLevelCalculator {
  private redis: Redis;
  private clickhouse: ClickHouseClient;

  async getQueueState(queueId: string): Promise<QueueState> {
    const queueKey = `queue:${queueId}`;

    // Redis sorted set: score = timestamp entered, member = callSid
    const now = Date.now() / 1000;
    const waitingCalls = await this.redis.zrangebyscore(
      queueKey,
      '-inf',
      now,
      'WITHSCORES'
    );

    const callsInQueue = [];
    for (let i = 0; i < waitingCalls.length; i += 2) {
      const callSid = waitingCalls[i];
      const enteredAt = parseFloat(waitingCalls[i + 1]) * 1000;
      callsInQueue.push({
        callSid,
        enteredAt,
        waitTime: Date.now() - enteredAt,
        priority: 0, // from separate sorted set
      });
    }

    return {
      queueId,
      tenantId: queueId.split(':')[0],
      depth: callsInQueue.length,
      longestWaitSeconds: callsInQueue.length > 0
        ? Math.max(...callsInQueue.map(c => c.waitTime)) / 1000
        : 0,
      callsInQueue,
    };
  }

  async computeServiceLevel(
    queueId: string,
    start: number,
    end: number,
    targetSeconds: number = 20,
    targetPercent: number = 80
  ): Promise<ServiceLevelResult> {
    const result = await this.clickhouse.query(`
      SELECT
        countIf(status = 'answered') as answered,
        countIf(status = 'abandoned') as abandoned,
        countIf(status = 'answered' AND waitTimeSeconds <= ${targetSeconds}) as answeredWithinTarget,
        countIf(status = 'abandoned' AND waitTimeSeconds < ${targetSeconds}) as abandonedBeforeTarget,
        avgIf(waitTimeSeconds, status = 'answered') as avgSpeedOfAnswer,
        max(waitTimeSeconds) as maxWaitTime
      FROM call_queue_events
      WHERE queueId = '${queueId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
    `);

    const row = result[0];
    const totalOffered = row.answered + row.abandoned;

    // Service level formula (TSF method)
    const effectiveAnswered = row.answeredWithinTarget + row.abandonedBeforeTarget;
    const serviceLevel = totalOffered > 0
      ? (effectiveAnswered / totalOffered) * 100
      : 100;

    return {
      queueId,
      tenantId: queueId.split(':')[0],
      periodStart: start,
      periodEnd: end,
      offered: totalOffered,
      answered: row.answered,
      abandoned: row.abandoned,
      answeredWithinTarget: row.answeredWithinTarget,
      abandonedWithinTarget: row.abandonedBeforeTarget,
      serviceLevel,
      targetPercent,
      targetSeconds,
      averageSpeedOfAnswer: row.avgSpeedOfAnswer ?? 0,
      longestWaitTime: row.maxWaitTime ?? 0,
    };
  }

  // Real-time service level (last 30 minutes, refreshed every 30 seconds)
  async getRealtimeServiceLevel(queueId: string, targetSeconds: number): Promise<number> {
    const now = Date.now();
    const thirtyMinutesAgo = now - 30 * 60 * 1000;
    const sl = await this.computeServiceLevel(queueId, thirtyMinutesAgo, now, targetSeconds);
    return sl.serviceLevel;
  }
}

// Service level gauge widget
const ServiceLevelGauge: React.FC<{
  current: number;
  target: number;
  queueId: string;
}> = ({ current, target, queueId }) => {
  const status = current >= target ? 'met'
    : current >= target * 0.9 ? 'warning'
    : 'critical';

  return (
    <div className={`service-level-gauge ${status}`}>
      <CircularGauge value={current} max={100} />
      <div className="sl-meta">
        <span className="sl-value">{current.toFixed(1)}%</span>
        <span className="sl-target">Target: {target}%</span>
      </div>
      <QueueDepthWidget queueId={queueId} />
      <LongestWaitWidget queueId={queueId} />
    </div>
  );
};

const QueueDepthWidget: React.FC<{ queueId: string }> = ({ queueId }) => {
  const [depth, setDepth] = useState(0);
  useEffect(() => {
    const ws = subscribeToQueueDepth(queueId);
    ws.on('depth', setDepth);
    return () => ws.disconnect();
  }, [queueId]);

  return <div className="queue-depth">{depth} waiting</div>;
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Redis (RSAL) | Server | Real-time queue state (sorted sets) |
| ClickHouse (Apache 2.0) | Server | Historical SLA computation |
| Apache Kafka (Apache 2.0) | Server | Queue event ingestion |
| Recharts (MIT) | Client | Wait time distribution charts |

## Production Considerations

**Scaling:** Redis queue state is maintained per queue ID. For tenants with 100+ queues, use Redis Cluster to distribute queue state across shards. The sorted set approach handles up to 1M entries per queue without performance degradation. ClickHouse SLA queries cover configurable time windows — limit queries to max 31 days to prevent excessive scanning. Pre-aggregate hourly service level snapshots into a materialized view for faster historical trend queries.

**Security:** Queue state and service level data are tenant-scoped. Queue IDs are prefixed with tenant ID to prevent cross-tenant access. Service level targets are configurable per queue — only supervisors with the `queues:configure` permission can modify targets. Real-time queue depth should not expose caller identity — the Redis sorted set stores only call SIDs (opaque identifiers), not PII.

**Monitoring:** Track service level per queue over time, queue depth trends, and abandonment rate. Alert if service level drops below target for more than 5 consecutive minutes, if queue depth exceeds 3x the normal peak, or if any single call's wait time exceeds 10 minutes (potential system issue). Monitor Redis memory usage for queue sorted sets — each entry is ~100 bytes, so 10,000 queued calls takes ~1 MB.
