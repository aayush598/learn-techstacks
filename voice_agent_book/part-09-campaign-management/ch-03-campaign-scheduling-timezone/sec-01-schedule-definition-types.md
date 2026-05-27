# Section 01: Schedule Definition Types

## Overview

Campaign scheduling defines when a campaign is allowed to place calls. Schedules range from simple one-time slots (call between 9 AM and 5 PM on a specific date) to complex recurring patterns (call every weekday at 10 AM, excluding holidays, until the campaign completes or a specified end date). The schedule system must support multiple schedule types, combination of schedules for advanced scenarios, and timezone-relative time specifications.

The schedule engine interprets schedule definitions and generates concrete dialing windows — precise time ranges during which the dialer is permitted to operate. These windows are then intersected with contact-level timezone windows and compliance constraints to produce the actual calling schedule. The schedule definition format should be expressive enough to handle most business scenarios without requiring custom code.

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
class ScheduleEngine {
  constructor(holidayCalendar) {
    this.holidayCalendar = holidayCalendar;
    this.parsers = {
      'one_time': new OneTimeParser(),
      'recurring': new RecurringParser(),
      'cron': new CronParser(),
      'combined': new CombinedParser()
    };
  }

  getDialingWindows(scheduleDefinition, timezone, dateRange) {
    const parser = this.parsers[scheduleDefinition.type];
    if (!parser) throw new Error(`Unknown schedule type: ${scheduleDefinition.type}`);

    let windows = parser.parse(scheduleDefinition, dateRange);

    // Apply timezone conversion
    windows = windows.map(w => ({
      start: this.convertToContactTimezone(w.start, timezone),
      end: this.convertToContactTimezone(w.end, timezone)
    }));

    // Remove holiday windows
    windows = this.removeHolidayWindows(windows, timezone);

    return windows;
  }

  async isInSchedule(campaign, contactTimezone) {
    const now = new Date();
    const windows = this.getDialingWindows(
      campaign.schedule,
      contactTimezone,
      { start: now, end: now }
    );

    return windows.some(w => now >= w.start && now <= w.end);
  }
}

class RecurringParser {
  parse(schedule, dateRange) {
    const windows = [];
    let current = new Date(dateRange.start);
    
    while (current <= dateRange.end) {
      const dayName = current.toLocaleDateString('en-US', { weekday: 'long' });
      
      if (schedule.days.includes(dayName)) {
        for (const timeSlot of schedule.timeSlots) {
          const [startH, startM] = timeSlot.start.split(':');
          const [endH, endM] = timeSlot.end.split(':');
          
          const windowStart = new Date(current);
          windowStart.setHours(parseInt(startH), parseInt(startM), 0, 0);
          
          const windowEnd = new Date(current);
          windowEnd.setHours(parseInt(endH), parseInt(endM), 0, 0);
          
          windows.push({ start: windowStart, end: windowEnd });
        }
      }
      
      current.setDate(current.getDate() + 1);
    }

    return windows;
  }
}

class CronParser {
  parse(schedule, dateRange) {
    // Use cron-parser library to expand cron into time windows
    const parser = new CronParser.Lib();
    const interval = parser.parseExpression(schedule.cron);
    
    const windows = [];
    let next = interval.next();
    
    while (next && next.toDate() <= dateRange.end) {
      if (next.toDate() >= dateRange.start) {
        windows.push({
          start: next.toDate(),
          end: new Date(next.toDate().getTime() + schedule.durationMs || 3600000)
        });
      }
      next = interval.next();
    }

    return windows;
  }
}
```

## Integration Points

- **Timezone Service (sec-02):** Resolves contact timezone for schedule evaluation
- **Dialing Engine (Ch 01):** Consults schedule before each dial attempt
- **Compliance Service (Ch 07):** Schedule is intersected with compliance calling windows
- **Campaign Lifecycle (Ch 01, sec-02):** Schedule determines auto-activation/deactivation
- **Holiday Calendar (sec-05):** Excluded dates are applied to schedule evaluation
- **Analytics (Ch 09):** Schedule adherence tracking and optimization

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Schedule evaluation must be fast — sub-10ms — since it's checked before every dial attempt
- Cache schedule evaluation results with a short TTL (30 seconds) since schedules rarely change mid-campaign
- Schedule validation should catch infinite loops in combined schedules (e.g., a schedule that includes itself)
- Holiday exclusion should use a maintained holidays package or API for accuracy
- Timezone-aware schedule display in the UI should show times in the user's local timezone
- Schedule changes to active campaigns should take effect immediately with existing calls completing under old schedule
- Consider a "next window" preview in the UI so operators can see when the campaign will next be allowed to dial
- Schedule definitions should be exportable as iCalendar (ICS) for external calendar integration
- Monitor schedule violations — calls placed outside valid schedule windows are a compliance risk
- Support schedule templates for common patterns (business hours, after-hours, weekends only)
