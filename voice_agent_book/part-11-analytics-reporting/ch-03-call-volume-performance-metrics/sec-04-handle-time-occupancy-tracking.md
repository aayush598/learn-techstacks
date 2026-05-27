# Section 04: Handle Time and Occupancy Tracking

## Overview

Handle time and occupancy tracking measures agent productivity and workload balance. Average Handle Time (AHT) is the sum of talk time plus after-call work (ACW) divided by the number of handled calls. Occupancy is the percentage of an agent's logged-in time spent handling calls (talk + ACW) versus waiting for calls (idle time). These metrics are essential for staffing calculations, agent scheduling, and identifying operational inefficiencies.

The system tracks AHT and occupancy at multiple levels: per agent (individual performance), per team/group (team-level averages), per campaign (campaign-specific performance), and per tenant (overall averages). AHT is further broken down into its components (talk time, hold time, ACW time) to identify where time is spent. The metrics are available in real-time for the current shift and historically for trend analysis. Outlier detection flags agents with AHT significantly above or below the team average for coaching opportunities.

## Architecture

```
              Handle Time and Occupancy Pipeline

   Call Events → Stream Processor → AHT Calculator
                                        |
                            ┌───────────┴───────────┐
                            |                       |
                      Redis (current shift     ClickHouse (historical
                       per-agent AHT)           AHT and occupancy)
                            |                       |
                      Metrics API / WebSocket
                            |
                  AHT Trend Widget
                  Occupancy Gauge
                  Component Breakdown
                  Outlier Detection Alerts
```

## Design Decisions

- **Real-time AHT as a rolling 4-hour window over shift-to-date:** Computing AHT since the agent's shift start can give misleading results early in the shift (a single 20-minute call would show AHT = 20 minutes). Instead, the rolling 4-hour window provides a more stable metric that still reflects recent performance. For end-of-shift reporting, the full shift AHT is computed from ClickHouse. Trade-off: the rolling window lags behind current performance by up to 2 hours; we display both rolling AHT and shift-to-date AHT side by side.

- **Occupancy computed from agent state transitions over (talk + ACW) / logged-in time ratio:** The simple ratio formula is inaccurate because it doesn't account for non-call activities (training, meetings, breaks). The system tracks agent state transitions via the agent desktop WebSocket: available, on-call, ACW, break, training, meeting, offline. Occupancy is computed as (on-call + ACW) / (logged-in minus break/training/meeting). This provides a true measure of work utilization. Trade-off: occupancy depends on accurate agent state reporting; agents must manually set their state for non-call activities.

- **Component breakdown of AHT (talk, hold, ACW) over a single AHT number:** Displaying AHT alone hides important signals. A rising AHT might be due to longer talk time (complex issues), more hold time (agent consulting), or longer ACW (slow CRM system). The system computes each component separately and visualizes them as stacked bars and trend lines. Trade-off: component breakdown requires tracking additional event types (hold start/end, ACW start/end) that increase event volume by ~3x.

## Implementation Approach

```typescript
interface AgentShiftMetrics {
  agentId: string;
  tenantId: string;
  shiftDate: string;
  callsHandled: number;
  talkTimeSeconds: number;
  holdTimeSeconds: number;
  acwTimeSeconds: number;
  idleTimeSeconds: number;
  breakTimeSeconds: number;
  trainingTimeSeconds: number;
  loggedInSeconds: number;
  // Computed
  ahtSeconds: number;
  occupancy: number;
  rollingAht4h: number;
}

interface AhtComponent {
  label: string;
  seconds: number;
  percentage: number;
}

class AhtTracker {
  private redis: Redis;
  private clickhouse: ClickHouseClient;

  // Process agent state transition
  async trackStateTransition(
    agentId: string,
    fromState: string,
    toState: string,
    timestamp: number
  ): Promise<void> {
    const shiftKey = `agent:${agentId}:${this.getCurrentShiftDate()}`;

    // Calculate elapsed time in previous state
    const prevTransition = await this.redis.hget(shiftKey, 'lastStateTransition');
    if (prevTransition) {
      const { state, time } = JSON.parse(prevTransition);
      const elapsed = timestamp - time;

      await this.redis.hincrby(
        shiftKey,
        `${fromState}Time`,
        Math.round(elapsed / 1000)
      );
    }

    await this.redis.hset(
      shiftKey,
      'lastStateTransition',
      JSON.stringify({ state: toState, time: timestamp })
    );
  }

  async getShiftMetrics(agentId: string, shiftDate?: string): Promise<AgentShiftMetrics> {
    const date = shiftDate ?? this.getCurrentShiftDate();
    const shiftKey = `agent:${agentId}:${date}`;

    const data = await this.redis.hgetall(shiftKey);

    const talkTime = parseInt(data.talkTime ?? '0');
    const holdTime = parseInt(data.holdTime ?? '0');
    const acwTime = parseInt(data.acwTime ?? '0');
    const idleTime = parseInt(data.idleTime ?? '0');
    const breakTime = parseInt(data.breakTime ?? '0');
    const trainingTime = parseInt(data.trainingTime ?? '0');
    const callsHandled = parseInt(data.callsHandled ?? '0');

    const billedTime = talkTime + holdTime + acwTime;
    const productiveTime = billedTime + idleTime;
    const loggedInSeconds = billedTime + idleTime + breakTime + trainingTime;
    const availableSeconds = productiveTime; // logged in minus breaks/training

    return {
      agentId,
      tenantId: shiftKey.split(':')[0],
      shiftDate: date,
      callsHandled,
      talkTimeSeconds: talkTime,
      holdTimeSeconds: holdTime,
      acwTimeSeconds: acwTime,
      idleTimeSeconds: idleTime,
      breakTimeSeconds: breakTime,
      trainingTimeSeconds: trainingTime,
      loggedInSeconds,
      ahtSeconds: callsHandled > 0 ? billedTime / callsHandled : 0,
      occupancy: availableSeconds > 0 ? (billedTime / availableSeconds) * 100 : 0,
      rollingAht4h: await this.getRollingAht(agentId, 4 * 3600),
    };
  }

  private async getRollingAht(agentId: string, windowSeconds: number): Promise<number> {
    const now = Date.now();
    const windowStart = now - windowSeconds * 1000;

    const result = await this.clickhouse.query(`
      SELECT
        count() as calls,
        sum(talkTimeSeconds + holdTimeSeconds + acwTimeSeconds) as totalTime
      FROM call_records
      WHERE agentId = '${agentId}'
        AND timestamp >= ${windowStart}
        AND timestamp <= ${now}
    `);

    const row = result[0];
    return row.calls > 0 ? row.totalTime / row.calls : 0;
  }

  async getComponentBreakdown(
    agentId: string,
    start: number,
    end: number
  ): Promise<AhtComponent[]> {
    const result = await this.clickhouse.query(`
      SELECT
        avg(talkTimeSeconds) as talk,
        avg(holdTimeSeconds) as hold,
        avg(acwTimeSeconds) as acw
      FROM call_records
      WHERE agentId = '${agentId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
    `);

    const row = result[0];
    const total = row.talk + row.hold + row.acw;

    return [
      { label: 'Talk Time', seconds: row.talk, percentage: total > 0 ? (row.talk / total) * 100 : 0 },
      { label: 'Hold Time', seconds: row.hold, percentage: total > 0 ? (row.hold / total) * 100 : 0 },
      { label: 'After-Call Work', seconds: row.acw, percentage: total > 0 ? (row.acw / total) * 100 : 0 },
    ];
  }

  private getCurrentShiftDate(): string {
    return new Date().toISOString().split('T')[0];
  }
}

// AHT trend visualization
const AhtTrendWidget: React.FC<{
  agentId: string;
  teamAverage: number;
}> = ({ agentId, teamAverage }) => {
  const [ahtData, setAhtData] = useState<Array<{ date: string; aht: number }>>([]);

  useEffect(() => {
    fetchAhtTrend(agentId, 30).then(setAhtData);
  }, [agentId]);

  return (
    <div className="aht-trend">
      <div className="aht-summary">
        <MetricLabel label="Current AHT" value={formatDuration(ahtData[ahtData.length - 1]?.aht ?? 0)} />
        <MetricLabel label="Team Avg" value={formatDuration(teamAverage)} />
        <DeltaBadge
          value={((ahtData[ahtData.length - 1]?.aht ?? 0) - teamAverage) / teamAverage * 100}
          direction={ahtData[ahtData.length - 1]?.aht > teamAverage ? 'up' : 'down'}
        />
      </div>
      <LineChart data={ahtData} xKey="date" yKey="aht" yLabel="AHT (seconds)" />
      <ComponentBreakdownChart agentId={agentId} />
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Redis (RSAL) | Server | Real-time shift state per agent |
| ClickHouse (Apache 2.0) | Server | Historical AHT and occupancy |
| Apache Kafka (Apache 2.0) | Server | Agent state transition events |
| Recharts (MIT) | Client | AHT trend and component charts |

## Production Considerations

**Scaling:** Agent state tracking uses one Redis hash key per agent per shift with TTL of 7 days. For 1000 agents, this is 1000 keys per shift — Redis handles this easily. ClickHouse queries for rolling AHT use indexes on (agentId, timestamp) for fast range scans. Pre-aggregate hourly AHT and occupancy into a materialized view for dashboards covering 30+ days.

**Security:** Per-agent AHT and occupancy data is sensitive — supervisors can view their team's metrics, agents can view their own, and administrators can view all. The API enforces this hierarchy: an agent querying another agent's metrics gets a 403 unless they share a team and the requesting user has `agent-performance:view-team` permission. Occupancy data should not be used for punitive performance evaluation without considering external factors (complexity of calls, system issues).

**Monitoring:** Track AHT trend per agent and per team. Alert if an individual agent's AHT deviates more than 2 standard deviations from the team average for 3 consecutive days — this may indicate a coaching need or a system issue. Alert if occupancy exceeds 95% for extended periods — this indicates the agent is overloaded and likely to experience burnout. Monitor the ACW-to-talk-time ratio — if ACW exceeds 30% of talk time, investigate workflow inefficiencies.
