# Section 05: Schedule Adherence Tracking

## Overview

Schedule adherence tracking measures how well agents follow their assigned schedules. It compares the agent's actual state (available, on-call, break, training, offline) against their scheduled activities at 15-minute intervals throughout the day. Key metrics include: schedule adherence percentage (time spent in the correct activity), punctuality (starting and ending shifts on time), break and lunch compliance (taking breaks at the correct times and durations), and overtime tracking.

The system computes adherence automatically by consuming agent state transition events and cross-referencing them with the schedule data from the workforce management (WFM) system. Adherence data is displayed in real-time as a color-coded timeline (green = on schedule, yellow = slightly off, red = significantly off) and summarized in the agent scorecard as a compliance percentage. Supervisors receive alerts when an agent's adherence drops below 80% for a sustained period.

## Architecture

```
           Schedule Adherence Pipeline

   WFM System → Schedule API → Adherence Engine
                                   |
   Agent State Events (Kafka) →    |
                                   |
                    ┌──────────────┴──┐
                    |                 |
              Adherence Calculator   Alert Engine
              (15-min intervals)     (< 80% threshold)
                    |                 |
              ClickHouse        WebSocket / Slack
              (adherence         (alerts to
               history)           supervisors)
                    |
              Scorecard Integration
              Real-time Timeline Widget
```

## Design Decisions

- **15-minute interval granularity for adherence checks over per-minute:** Checking adherence every minute would be too noisy (agents may be 1-2 minutes late returning from break without indicating a problem) and computationally expensive. A 15-minute interval aligns with standard workforce management practices and provides actionable data without excessive granularity. Trade-off: 15-minute intervals miss micro-adherence issues (e.g., an agent who takes four 5-minute unscheduled breaks in an hour would show 80% adherence instead of 0%).

- **Tolerance windows for schedule transitions over strict moment-in-time checks:** An agent scheduled to start a break at 10:00 AM who actually starts at 10:03 AM is not necessarily non-adherent. The system applies configurable tolerance windows: 5 minutes for shift start/end, 3 minutes for break start/end, 5 minutes for lunch start/end. Adherence is only flagged if the agent exceeds these tolerances. Trade-off: tolerance windows can mask chronic but minor lateness; the system tracks both strict adherence and tolerance-adjusted adherence separately.

- **WFM system integration via API over direct database access:** The adherence engine connects to the workforce management system (e.g., NICE IEX, Verint, Calabrio) via its API rather than reading from its database directly. This maintains separation of concerns and avoids coupling to the WFM system's internal schema. The API returns scheduled activities in 15-minute intervals for each agent per day. Trade-off: the adherence engine depends on the WFM API's availability and response time; a WFM API outage would prevent real-time adherence tracking.

## Implementation Approach

```typescript
interface ScheduleEntry {
  agentId: string;
  tenantId: string;
  date: string;
  startTime: number;           // shift start Unix ms
  endTime: number;             // shift end Unix ms
  activities: Array<{
    startTime: number;         // scheduled activity start
    endTime: number;           // scheduled activity end
    activityType: 'work' | 'break' | 'lunch' | 'training' | 'meeting';
  }>;
}

interface AdherenceRecord {
  agentId: string;
  tenantId: string;
  date: string;
  intervalStart: number;       // 15-min interval start
  scheduledActivity: string;
  actualActivity: string;
  isAdherent: boolean;
  toleranceMinutes: number;
  deviationMinutes: number;
}

interface AgentAdherenceSummary {
  agentId: string;
  tenantId: string;
  date: string;
  overallAdherence: number;       // percentage
  shiftAdherence: number;         // started/ended on time
  breakAdherence: number;         // break timing compliance
  lunchAdherence: number;         // lunch timing compliance
  totalScheduledMinutes: number;
  totalDeviatedMinutes: number;
  adherenceByHour: Array<{ hour: number; adherence: number }>;
}

class ScheduleAdherenceTracker {
  private clickhouse: ClickHouseClient;
  private wfmApi: WfmApiClient;
  private toleranceConfig = {
    shiftStart: 5 * 60 * 1000,     // 5 minutes
    shiftEnd: 5 * 60 * 1000,
    breakStart: 3 * 60 * 1000,     // 3 minutes
    breakEnd: 3 * 60 * 1000,
    lunchStart: 5 * 60 * 1000,     // 5 minutes
    lunchEnd: 5 * 60 * 1000,
  };

  async computeAdherence(
    agentId: string,
    tenantId: string,
    date: string
  ): Promise<AgentAdherenceSummary> {
    // Get schedule from WFM
    const schedule = await this.wfmApi.getSchedule(agentId, date);
    if (!schedule) {
      return { agentId, tenantId, date, overallAdherence: 100, shiftAdherence: 100,
        breakAdherence: 100, lunchAdherence: 100, totalScheduledMinutes: 0,
        totalDeviatedMinutes: 0, adherenceByHour: [] };
    }

    // Get actual agent states from ClickHouse
    const actualStates = await this.getActualStates(agentId, date);
    if (actualStates.length === 0) {
      return { ...schedule, overallAdherence: 0 };
    }

    // Generate 15-minute intervals for the shift
    const intervals = this.generateIntervals(schedule);

    // Check adherence for each interval
    let totalAdherent = 0;
    let totalIntervals = 0;
    const shiftAdherence = this.checkShiftAdherence(schedule, actualStates[0], actualStates[actualStates.length - 1]);
    let breakAdherenceTotal = 0;
    let breakAdherenceCount = 0;
    let lunchAdherenceTotal = 0;
    let lunchAdherenceCount = 0;
    const adherenceByHour = new Map<number, { sum: number; count: number }>();

    for (const interval of intervals) {
      const actualActivity = this.getActivityAt(actualStates, (interval.start + interval.end) / 2);
      const isAdherent = this.isAdherent(
        interval.scheduledActivity,
        actualActivity,
        interval.start,
        interval.end,
        actualStates
      );

      if (isAdherent) totalAdherent++;
      totalIntervals++;

      const hour = new Date(interval.start).getHours();
      if (!adherenceByHour.has(hour)) adherenceByHour.set(hour, { sum: 0, count: 0 });
      const h = adherenceByHour.get(hour)!;
      h.sum += isAdherent ? 1 : 0;
      h.count++;
    }

    // Track break and lunch specific adherence
    for (const activity of schedule.activities) {
      if (activity.activityType === 'break') {
        const actual = this.getActivityAt(actualStates, (activity.startTime + activity.endTime) / 2);
        breakAdherenceTotal += actual === 'break' ? 1 : 0;
        breakAdherenceCount++;
      }
      if (activity.activityType === 'lunch') {
        const actual = this.getActivityAt(actualStates, (activity.startTime + activity.endTime) / 2);
        lunchAdherenceTotal += actual === 'lunch' ? 1 : 0;
        lunchAdherenceCount++;
      }
    }

    return {
      agentId,
      tenantId,
      date,
      overallAdherence: totalIntervals > 0 ? (totalAdherent / totalIntervals) * 100 : 100,
      shiftAdherence,
      breakAdherence: breakAdherenceCount > 0 ? (breakAdherenceTotal / breakAdherenceCount) * 100 : 100,
      lunchAdherence: lunchAdherenceCount > 0 ? (lunchAdherenceTotal / lunchAdherenceCount) * 100 : 100,
      totalScheduledMinutes: totalIntervals * 15,
      totalDeviatedMinutes: (totalIntervals - totalAdherent) * 15,
      adherenceByHour: Array.from(adherenceByHour.entries()).map(([hour, data]) => ({
        hour,
        adherence: (data.sum / data.count) * 100,
      })),
    };
  }

  private async getActualStates(agentId: string, date: string): Promise<any[]> {
    // Query agent state transitions from ClickHouse
    const result = await this.clickhouse.query(`
      SELECT timestamp, state
      FROM agent_state_transitions
      WHERE agentId = '${agentId}'
        AND toDate(timestamp) = '${date}'
      ORDER BY timestamp
    `);
    return result;
  }

  private generateIntervals(schedule: ScheduleEntry): Array<{
    start: number;
    end: number;
    scheduledActivity: string;
  }> {
    const intervals = [];
    let current = schedule.startTime;

    while (current < schedule.endTime) {
      const intervalEnd = current + 15 * 60 * 1000;
      const activity = this.getActivityAt(schedule.activities, (current + intervalEnd) / 2);

      intervals.push({
        start: current,
        end: intervalEnd,
        scheduledActivity: activity,
      });

      current = intervalEnd;
    }

    return intervals;
  }

  private getActivityAt(activities: Array<{ startTime: number; endTime: number; activityType: string }>, timestamp: number): string {
    for (const activity of activities) {
      if (timestamp >= activity.startTime && timestamp < activity.endTime) {
        return activity.activityType;
      }
    }
    return 'work'; // Default if outside scheduled activities
  }

  private isAdherent(
    scheduledActivity: string,
    actualActivity: string,
    intervalStart: number,
    intervalEnd: number,
    actualStates: any[]
  ): boolean {
    if (scheduledActivity === actualActivity) return true;

    // Check tolerance for shift boundaries
    const isShiftStart = intervalStart === actualStates[0]?.timestamp;
    const isShiftEnd = intervalEnd === actualStates[actualStates.length - 1]?.timestamp;

    if (isShiftStart || isShiftEnd) {
      return true; // Tolerance handled separately
    }

    // Check break/lunch tolerance
    if ((scheduledActivity === 'break' || scheduledActivity === 'lunch') && actualActivity === 'work') {
      // Agent is late returning from break
      const deviation = this.calculateDeviation(intervalStart, actualStates, scheduledActivity);
      const tolerance = scheduledActivity === 'lunch'
        ? this.toleranceConfig.lunchEnd
        : this.toleranceConfig.breakEnd;
      return deviation <= tolerance;
    }

    return false;
  }

  private calculateDeviation(intervalStart: number, actualStates: any[], targetActivity: string): number {
    // Find when the agent actually transitioned to the target activity
    for (const state of actualStates) {
      if (state.state === targetActivity) {
        return Math.abs(state.timestamp - intervalStart);
      }
    }
    return Infinity;
  }

  private checkShiftAdherence(schedule: ScheduleEntry, firstState: any, lastState: any): number {
    const startDeviation = Math.abs(firstState?.timestamp - schedule.startTime) ?? 0;
    const endDeviation = Math.abs(lastState?.timestamp - schedule.endTime) ?? 0;

    const startAdherent = startDeviation <= this.toleranceConfig.shiftStart;
    const endAdherent = endDeviation <= this.toleranceConfig.shiftEnd;

    if (startAdherent && endAdherent) return 100;
    if (startAdherent || endAdherent) return 50;
    return 0;
  }
}

// Adherence timeline visualization
const AdherenceTimeline: React.FC<{
  agentId: string;
  date: string;
  summary: AgentAdherenceSummary;
}> = ({ agentId, date, summary }) => {
  const [intervals, setIntervals] = useState<AdherenceRecord[]>([]);

  useEffect(() => {
    fetchAdherenceIntervals(agentId, date).then(setIntervals);
  }, [agentId, date]);

  return (
    <div className="adherence-widget">
      <div className="adherence-summary">
        <CircularGauge value={summary.overallAdherence} max={100} />
        <MetricRow label="Shift Adherence" value={`${summary.shiftAdherence.toFixed(0)}%`} />
        <MetricRow label="Break Adherence" value={`${summary.breakAdherence.toFixed(0)}%`} />
        <MetricRow label="Lunch Adherence" value={`${summary.lunchAdherence.toFixed(0)}%`} />
      </div>
      <TimelineGrid intervals={intervals} />
      {summary.overallAdherence < 80 && (
        <AlertBanner message={`Agent adherence is ${summary.overallAdherence.toFixed(0)}%. Review schedule compliance.`} />
      )}
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Agent state and adherence storage |
| NICE IEX / Verint API | Commercial | WFM schedule data |
| Apache Kafka (Apache 2.0) | Server | Agent state event ingestion |
| Recharts (MIT) | Client | Adherence timeline visualization |

## Production Considerations

**Scaling:** Adherence computation for an agent-shift takes ~50 ms. For daily batch processing of 1000 agents, parallelize across 10 workers (5 seconds per worker batch). Real-time adherence dashboards use pre-computed cache with 5-minute refresh. ClickHouse stores adherence records partitioned by date and ordered by (agentId, intervalStart).

**Security:** Adherence data is tenant-scoped and agent-specific. Agents can view their own adherence. Supervisors can view their team's adherence. Adherence data may be sensitive in unionized environments — access requires the `agent-performance:view` permission. Schedule data from WFM is also sensitive and should be masked in API responses (show only derived adherence, not raw schedule details).

**Monitoring:** Track average adherence per team per day, adherence alert rate, and WFM API availability. Alert if the WFM API fails to respond for more than 5 consecutive minutes. Alert if any team's average adherence drops below 85% for 3 consecutive days. Monitor the adherence computation job for failures — a failed job means agents have no adherence data for that day, which may affect scorecard computation.
