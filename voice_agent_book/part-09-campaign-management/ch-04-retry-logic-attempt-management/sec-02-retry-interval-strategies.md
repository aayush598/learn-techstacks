# Section 02: Retry Interval Strategies

## Overview

Retry interval strategies define how long to wait between attempted calls to the same contact. The interval strategy significantly impacts both contact experience and campaign efficiency — too-frequent retries annoy contacts and risk compliance violations, while too-infrequent retries miss connection opportunities and reduce campaign velocity. The system supports multiple interval strategies that can be configured per campaign or per outcome type.

Common strategies include fixed intervals (e.g., every 2 hours), incremental intervals (e.g., 1 hour, then 2 hours, then 4 hours), exponential backoff (e.g., 1h, 2h, 4h, 8h, 16h), and time-of-day aligned intervals (e.g., next available calling window). Each strategy has different implications for contact experience, compliance, and operational efficiency. The choice depends on campaign type, urgency, and regulatory requirements.

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
class RetryIntervalCalculator {
  constructor(config, scheduleEngine) {
    this.config = config;
    this.schedule = scheduleEngine;
  }

  async calculateNextRetry(contact, campaign, lastAttempt, currentTime = new Date()) {
    const strategy = this.config.getStrategy(campaign.id, lastAttempt.outcome);

    let nextTime;

    switch (strategy.type) {
      case 'fixed':
        nextTime = this.fixedInterval(lastAttempt.timestamp, strategy.intervalMs);
        break;
      case 'incremental':
        nextTime = this.incrementalInterval(lastAttempt, strategy.intervals);
        break;
      case 'exponential':
        nextTime = this.exponentialBackoff(lastAttempt, strategy);
        break;
      case 'time_of_day':
        nextTime = await this.timeOfDayAligned(contact, campaign, lastAttempt, currentTime);
        break;
      case 'outcome_based':
        nextTime = this.outcomeBasedInterval(lastAttempt, strategy.outcomes);
        break;
      default:
        nextTime = this.fixedInterval(lastAttempt.timestamp, 3600000); // 1 hour default
    }

    // Apply max interval cap
    const maxInterval = strategy.maxIntervalMs || 7 * 86400000; // 7 days
    const cappedTime = new Date(Math.min(
      nextTime.getTime(),
      lastAttempt.timestamp.getTime() + maxInterval
    ));

    // Ensure retry is within calling windows
    return this.alignToCallingWindow(contact, campaign, cappedTime);
  }

  fixedInterval(lastTimestamp, intervalMs) {
    return new Date(lastTimestamp.getTime() + intervalMs);
  }

  incrementalInterval(lastAttempt, intervals) {
    // intervals = [60000, 120000, 300000, 600000, ...]
    const attemptIndex = lastAttempt.attemptNumber - 1;
    const interval = intervals[Math.min(attemptIndex, intervals.length - 1)];
    return new Date(lastAttempt.timestamp.getTime() + interval);
  }

  exponentialBackoff(lastAttempt, config) {
    const baseMs = config.baseIntervalMs || 60000; // 1 minute
    const multiplier = config.multiplier || 2;
    const attemptIndex = lastAttempt.attemptNumber - 1;
    
    const interval = baseMs * Math.pow(multiplier, attemptIndex);
    return new Date(lastAttempt.timestamp.getTime() + interval);
  }

  async timeOfDayAligned(contact, campaign, lastAttempt, currentTime) {
    // Align to next calling window rather than strict interval
    const window = await this.schedule.getNextCallingWindow(
      contact, campaign, currentTime
    );
    return window || new Date(currentTime.getTime() + 86400000); // Next day fallback
  }

  outcomeBasedInterval(lastAttempt, outcomeConfig) {
    const interval = outcomeConfig[lastAttempt.outcome]?.intervalMs || 3600000;
    return new Date(lastAttempt.timestamp.getTime() + interval);
  }

  async alignToCallingWindow(contact, campaign, time) {
    // Check if the calculated time is within calling windows
    const canDial = await this.schedule.canDialAt(contact, campaign, time);
    if (canDial) return time;

    // If not, align to next window
    const nextWindow = await this.schedule.getNextCallingWindow(
      contact, campaign, time
    );
    return nextWindow || time;
  }
}
```

## Integration Points

- **Attempt Tracker:** Provides attempt history with timestamps for interval calculation
- **Schedule Engine (Ch 03):** Time-of-day alignment and calling window checking
- **Retry Queue:** Calculated intervals determine when retry jobs are scheduled in BullMQ
- **Campaign Config UI:** Interval strategy configuration per campaign
- **Analytics (Ch 09):** Interval effectiveness tracking — which intervals yield best connection rates

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Interval calculation must handle the case where the next scheduled time is in the past (e.g., a retry job was delayed). Skip and move to the next interval.
- Exponential backoff grows quickly — 2^10 = 1024 minutes (~17 hours) by attempt 10. Ensure the max interval cap prevents unbounded growth.
- Time-of-day aligned retries work best when combined with calling window enforcement — ensure they don't conflict.
- Short intervals (under 5 minutes) risk appearing aggressive — consider a minimum interval configuration.
- Track interval effectiveness per campaign — which intervals produce the highest answer rates on subsequent attempts.
- Provide a retry timeline visualization showing when future retries are scheduled for a contact.
- Interval configuration changes mid-campaign should apply to new retry calculations, not immediately to already-scheduled retries.
- When multiple retry queues exist (different campaigns touching the same contact), coordinate intervals to prevent overlap.
- Test interval behavior around DST transitions — ensure that a "retry in 4 hours" that crosses a DST boundary calculates correctly.
- Consider "smart intervals" that learn from historical data — optimal intervals may vary by time of day and day of week.
