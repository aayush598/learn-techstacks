# Section 06: Timezone-Aware Dialing Engine

## Overview

The timezone-aware dialing engine is the runtime component that determines whether a specific contact can be called right now, considering their timezone, campaign schedule, calling windows, and blackout dates. Unlike simpler systems that check timezone once at campaign creation, the dialing engine evaluates timezone constraints in real-time before every dial attempt, accounting for time-sensitive changes like DST transitions and contacts traveling between timezones.

The engine sits between the campaign scheduler and the telephony layer, acting as a gatekeeper that only passes contacts through when all time-related conditions are satisfied. It also computes "next available time" for contacts that cannot be called now, enabling the retry engine to schedule the next attempt at the most appropriate time.

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
class TimezoneAwareDialingEngine {
  constructor(
    timezoneResolver,
    scheduleEngine,
    windowEnforcer,
    blackoutCalendar,
    gracePeriodMs = 30000
  ) {
    this.tz = timezoneResolver;
    this.schedule = scheduleEngine;
    this.window = windowEnforcer;
    this.blackout = blackoutCalendar;
    this.gracePeriod = gracePeriodMs;
  }

  async evaluateDial(contact, campaign, currentTime = new Date()) {
    const tzInfo = await this.tz.resolve(contact);

    // Parallel checks
    const [scheduleResult, windowResult, blackoutResult] = await Promise.all([
      this.schedule.isInSchedule(campaign, tzInfo.timezone),
      this.window.getCallingWindow(contact, campaign, currentTime),
      this.blackout.isBlackedOut(contact, campaign, currentTime)
    ]);

    const canDial = scheduleResult && windowResult.canDial && !blackoutResult.isBlackout;

    if (canDial) {
      return {
        eligible: true,
        decision: 'dial',
        timezone: tzInfo.timezone
      };
    }

    // Calculate next available time
    const nextAvailable = await this.findNextAvailableWindow(
      contact, campaign, currentTime, tzInfo.timezone
    );

    return {
      eligible: false,
      decision: 'blocked',
      timezone: tzInfo.timezone,
      nextAvailable,
      blockingRules: this.identifyBlockingRules(
        scheduleResult, windowResult, blackoutResult
      )
    };
  }

  async findNextAvailableWindow(contact, campaign, fromTime, timezone) {
    const maxLookAhead = 14; // Days
    let checkTime = new Date(fromTime);

    for (let day = 0; day < maxLookAhead; day++) {
      // Check each hour in the day
      for (let hour = 0; hour < 24; hour++) {
        checkTime.setHours(hour, 0, 0, 0);
        
        const [scheduled, windowOk, blackedOut] = await Promise.all([
          this.schedule.isInSchedule(campaign, timezone),
          this.window.canDialNow(contact, campaign),
          this.blackout.isBlackedOut(contact, campaign, checkTime)
        ]);

        if (scheduled && windowOk && !blackedOut.isBlackout) {
          return checkTime;
        }
      }
      checkTime.setDate(checkTime.getDate() + 1);
    }

    return null;
  }

  handleInProgressCall(callStartTime, currentTime) {
    // Allow calls that started during a valid window to complete
    // even if the window has since closed (within grace period)
    const callDuration = currentTime.getTime() - callStartTime.getTime();
    return callDuration <= this.gracePeriod;
  }
}
```

## Integration Points

- **Campaign Dialer (Ch 01):** Calls evaluateDial for each contact before placing a call
- **Retry Engine (Ch 04):** Uses nextAvailable for optimal retry scheduling
- **Timezone Resolver (sec-02):** Provides per-contact timezone resolution
- **Schedule Engine (sec-01):** Campaign schedule evaluation
- **Calling Window Enforcer (sec-03):** Contact-level window enforcement
- **Blackout Calendar (sec-05):** Holiday and blackout date checking
- **Compliance Engine (Ch 07):** Compliance hour enforcement integration

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Evaluation latency target: <50ms for the entire window check chain
- Cache timezone resolution for 24 hours (timezone rarely changes for a contact)
- Cache window evaluation for 5 minutes (windows change infrequently)
- At high scale (1000+ calls/minute), consider a pre-check batch that evaluates contacts in bulk before sending to the dialer
- The grace period for in-progress calls should be configurable per campaign
- Monitor "blocked dial" rate — a high blocked rate indicates schedule/campaign misconfiguration
- Next-available-window computation can be expensive — limit look-ahead to 14 days
- Consider pre-computing next available windows for retry queue contacts during off-peak hours
- Log all blocked dial decisions with the blocking rule for compliance and debugging
- Timezone-aware dialing is a key differentiator for compliance — document its behavior for regulatory audits
