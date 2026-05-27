# Section 04: DST Transition Handling

## Overview

Daylight Saving Time (DST) transitions create significant operational challenges for campaign scheduling. Twice a year, clocks shift forward or backward by one hour, creating edge cases that can cause campaigns to call outside permitted windows, miss scheduled slots entirely, or double-schedule contacts. The system must handle both spring-forward (clock moves ahead, losing one hour) and fall-back (clock moves back, repeating one hour) transitions correctly.

DST handling is remarkably complex due to non-standard observance rules. Not all regions observe DST (Arizona, Hawaii, Saskatchewan, most of Europe vs. most of Asia). The transition dates vary by year and jurisdiction (US second Sunday of March, first Sunday of November; EU last Sunday of March, last Sunday of October). Some regions have abolished DST recently (Turkey, Russia), creating a moving target for timezone databases.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```
class DSTHandler {
  constructor(timezoneDb) {
    this.tz = timezoneDb; // IANA timezone database interface
  }

  isInGap(time, timezone) {
    // Check if a given local time falls in a spring-forward gap
    const utcOffsetBefore = this.tz.utcOffset(time, timezone, { earlier: true });
    const utcOffsetAfter = this.tz.utcOffset(time, timezone, { later: true });
    
    // If the offset changes across this time, it's a gap
    return utcOffsetBefore !== utcOffsetAfter;
  }

  resolveScheduledTime(localTime, timezone) {
    // If the time falls in a DST gap, advance to the next valid time
    if (this.isInGap(localTime, timezone)) {
      // Get the start of the gap
      const gapStart = this.findDSTTransition(timezone, 'spring', localTime.getFullYear());
      // Advance to end of gap (spring forward)
      return new Date(gapStart.getTime() + 3600000); // +1 hour
    }
    return localTime;
  }

  findDSTTransition(timezone, type, year) {
    // Find the exact DST transition date for a given year and timezone
    const transitions = this.tz.getTransitions(timezone);
    return transitions.find(t => 
      t.type === type && t.year === year
    ).date;
  }

  normalizeScheduledJob(job, contactTimezone) {
    const localTime = new Date(job.scheduledAt);
    const resolvedTime = this.resolveScheduledTime(localTime, contactTimezone);

    if (resolvedTime.getTime() !== localTime.getTime()) {
      // Log that the schedule was adjusted for DST
      return {
        ...job,
        scheduledAt: resolvedTime.toISOString(),
        adjustedForDST: true,
        originalTime: localTime.toISOString()
      };
    }

    return job;
  }

  async checkDupForFallback(job, contactTimezone) {
    // During fall-back, check if the job was already scheduled
    // in the first occurrence of the repeated hour
    if (!this.isFallBackPeriod(job.scheduledAt, contactTimezone)) {
      return false;
    }

    // Convert to UTC
    const utcTime = this.tz.toUTC(job.scheduledAt, contactTimezone);
    
    // Check if there's already a job for this contact in the same UTC window
    const dup = await this.jobQueue.findDuplicate(
      job.contactId,
      utcTime
    );

    return !!dup;
  }

  isFallBackPeriod(time, timezone) {
    const year = time.getFullYear();
    const fallBackDate = this.findDSTTransition(timezone, 'fall', year);
    // Fall-back period is the 24 hours starting at the transition
    const periodStart = fallBackDate;
    const periodEnd = new Date(fallBackDate.getTime() + 86400000);
    
    return time >= periodStart && time < periodEnd;
  }
}
```

## Integration Points

- **Scheduling Engine (sec-01):** DST handling wraps schedule generation to adjust for transitions
- **Timezone Resolver (sec-02):** Provides timezone information for DST calculations
- **Job Queue (BullMQ):** DST-adjusted job scheduling and deduplication
- **Campaign Analytics (Ch 09):** Tracks DST-related schedule adjustments for reporting
- **Retry Engine (Ch 04):** DST-aware retry time calculation
- **UI:** Displays DST-adjusted times with clear indication of transitions

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Never use JavaScript `Date` objects with local timezone for scheduling — always use UTC internally
- The IANA timezone database must be kept updated — new DST rules are adopted by governments unpredictably
- DST transition dates change — code that hard-codes "second Sunday of March" will break if governments change the rules
- Test campaign behavior around DST transitions thoroughly — schedule a campaign that runs through a transition and verify correct behavior
- Spring-forward gap: if a campaign is scheduled for the skipped hour, skip that hour's calls entirely
- Fall-back duplication: ensure contacts are called only once during the repeated hour
- Notify campaign operators about DST transitions that affect their active campaigns
- Contacts in non-DST observing timezones (Arizona, Hawaii, most of Asia) should not be affected by DST handling
- Server timezone configuration should always be UTC to avoid DST issues in the application layer
- Log DST adjustment events for auditability — "Scheduled time 2:30 AM adjusted to 3:00 AM due to DST transition"
