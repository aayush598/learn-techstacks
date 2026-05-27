# Section 04: Slot Availability Management

## Overview

Slot availability management aggregates and normalizes availability information from multiple calendar sources (Google Calendar, Outlook Calendar, Calendly, custom business hours) into a unified schedule view. The service provides a consistent interface for answering "When is this person available?" across different scheduling platforms, handling the complexities of working hours, buffer times, minimum notice periods, blocked time slots, and multi-user scheduling (finding time when multiple participants are all available).

The availability service operates in two modes: calendar-backed (real-time queries against connected calendars, used for high-accuracy scheduling) and rule-backed (availability computed from working hours, buffer, and notice configurations, used when calendar integration is not available or for initial scheduling before calendar sync). The service supports configurable slot durations, gap detection (minimum time between meetings), preferred time zones, and blackout periods (holidays, personal time, out-of-office).

## Architecture

```
                    Slot Availability Management

   +------------------+     +------------------+     +------------------+
   | Google Calendar  |     | Outlook Calendar |     | Calendly         |
   | Adapter          |     | Adapter          |     | Adapter          |
   +------------------+     +------------------+     +------------------+
           |                       |                       |
           v                       v                       v
   +----------------------------------------------------------+
   |              Unified Availability Service                 |
   |                                                          |
   |  +------------------+  +------------------+              |
   |  | Query Planner    |  | Slot Calculator  |              |
   |  | • Source routing |  | • Duration       |              |
   |  | • Sub-query      |  | • Buffer time    |              |
   |  |   optimization   |  | • Notice period  |              |
   |  +------------------+  +------------------+              |
   |  +------------------+  +------------------+              |
   |  | Intersection     |  | Enrichment       |              |
   |  | Engine           |  | • User prefs     |              |
   |  | • Multi-user     |  | • Timezone       |              |
   |  | • Priority       |  | • Blackout dates |              |
   |  +------------------+  +------------------+              |
   +----------------------------------------------------------+
```

## Design Decisions

- **Query decomposition with parallel execution:** An availability query for "next Tuesday, 30-minute slots, for John and Jane" is decomposed into sub-queries for each user/calendar source. Sub-queries execute in parallel, and results are intersected to find common availability. For users with multiple calendar sources (e.g., Google Calendar + Calendly), both sources are queried and the union of busy times is used. Trade-off: parallel queries multiply API call volume but reduce total response time.

- **Graceful degradation with fallback availability models:** If a calendar API is unreachable (offline, rate limited, auth expired), the service falls back to the user's configured availability model (working hours, default slot duration, notice period). The response includes a data freshness indicator: "live" (from calendar), "cached" (< 5 minutes old), or "model" (rule-based). Trade-off: fallback availability may not reflect last-minute schedule changes.

- **Slot ranking and filtering beyond simple availability:** Available slots are ranked by preference score based on user configuration: preferred times (morning vs. afternoon), proximity to existing events (back-to-back vs. gap), and user-specific preferences (no meetings before 10 AM). The top-ranked slots are returned to the voice agent for presentation. Trade-off: ranking adds complexity but improves the quality of schedule suggestions.

## Implementation Approach

```
interface AvailabilityQuery {
  participants: { userId: string; sources: ('google' | 'outlook' | 'calendly' | 'model')[] }[];
  dateRange: { start: string; end: string };
  durationMinutes: number;
  preferences?: {
    timeZone?: string;
    workingHours?: { start: string; end: string; days: number[] };
    bufferMinutes?: number;
    minNoticeMinutes?: number;
    preferredTimes?: { start: string; end: string }[];
    blackoutDates?: string[];
    maxResults?: number;
  };
}

interface TimeSlot {
  start: string;
  end: string;
  source: 'live' | 'cached' | 'model';
  participants: string[];  // Which participants are available
  preferenceScore?: number;
}

class UnifiedAvailabilityService {
  async getAvailableSlots(query: AvailabilityQuery): Promise<TimeSlot[]> {
    const busyPeriods = await Promise.all(
      query.participants.map(p => this.getParticipantBusyPeriods(p, query.dateRange))
    );

    const mergedBusy = this.mergeBusyPeriods(busyPeriods);
    const available = this.computeSlots(
      new Date(query.dateRange.start),
      new Date(query.dateRange.end),
      query.durationMinutes,
      mergedBusy,
      query.preferences
    );

    return this.rankAndFilter(available, query.preferences);
  }

  private async getParticipantBusyPeriods(
    participant: AvailabilityQuery['participants'][0],
    dateRange: { start: string; end: string }
  ): Promise<BusyPeriod[]> {
    const allBusy: BusyPeriod[] = [];

    for (const source of participant.sources) {
      try {
        const busy = await this.querySource(source, participant.userId, dateRange);
        allBusy.push(...busy);
      } catch (error) {
        // Fall back to model-based availability
        const modelBusy = await this.getModelBusyPeriods(participant.userId, dateRange);
        allBusy.push(...modelBusy);
      }
    }
    return allBusy;
  }

  private computeSlots(
    start: Date, end: Date, durationMin: number,
    busyPeriods: BusyPeriod[], prefs?: AvailabilityQuery['preferences']
  ): TimeSlot[] {
    const slots: TimeSlot[] = [];
    const intervalMs = 30 * 60 * 1000;  // 30-min increments
    const durationMs = durationMin * 60 * 1000;
    const noticeMs = (prefs?.minNoticeMinutes || 0) * 60 * 1000;
    const bufferMs = (prefs?.bufferMinutes || 0) * 60 * 1000;
    const now = Date.now();
    let cursor = new Date(Math.max(start.getTime(), now + noticeMs));

    while (cursor.getTime() + durationMs <= end.getTime()) {
      const slotEnd = new Date(cursor.getTime() + durationMs + bufferMs);
      const slotWithBuffer = new Date(cursor.getTime() - bufferMs);

      const isBusy = busyPeriods.some(bp =>
        slotWithBuffer < new Date(bp.end) && slotEnd > new Date(bp.start)
      );

      if (!isBusy && this.isWithinWorkingHours(cursor, prefs)) {
        slots.push({
          start: cursor.toISOString(),
          end: new Date(cursor.getTime() + durationMs).toISOString(),
          source: 'live',
          participants: [],
          preferenceScore: this.calculatePreferenceScore(cursor, prefs)
        });
      }
      cursor = new Date(cursor.getTime() + intervalMs);
    }
    return slots;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Redis** (BSD) | Cache | Availability query caching |
| **BullMQ** (MIT) | Queue | Parallel query processing |
| **date-fns** (MIT) | Dates | Date/time manipulation |

## Production Considerations

**Scaling:** Availability queries trigger multiple API calls in parallel. Cache results per user per date range with 30-second TTL. For multi-user scheduling, the complexity grows with the number of participants — limit to 10 participants per query. Use Redis for distributed caching across instances.

**Security:** Availability data reveals when users are busy or free. Restrict access to authorized users within the same organization. Do not expose detailed calendar event information through availability queries — just busy/free status.

**Monitoring:** Track availability query latency (target p95 < 3 seconds), cache hit rate, fallback model usage rate (indicates calendar API issues), slot ranking distribution, and multi-user query complexity. Alert on query latency exceeding 10 seconds, high fallback rates > 20%, and calendar source errors.
