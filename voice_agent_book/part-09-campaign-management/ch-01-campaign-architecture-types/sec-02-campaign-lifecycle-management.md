# Section 02: Campaign Lifecycle Management

## Overview

Every campaign progresses through a defined lifecycle of states: draft, active, paused, completed, and archived. Managing these states correctly is critical for operational control, compliance, and data integrity. The lifecycle state machine enforces valid transitions, triggers side effects (like starting or stopping dialing), and prevents invalid operations such as editing an active campaign's contact list or deleting a campaign with in-progress calls.

The lifecycle system must handle both manual transitions (operator pauses a campaign) and automatic transitions (campaign completes when all contacts are exhausted). It must also support scheduled activation and deactivation, allowing campaigns to start and stop automatically based on time windows. Each state transition generates an audit event that records the actor, timestamp, and reason for the change.

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
class CampaignLifecycle {
  constructor(campaign) {
    this.state = campaign.state;
    this.validTransitions = {
      draft: ['active'],
      active: ['paused', 'completed'],
      paused: ['active', 'completed'],
      completed: ['archived'],
      archived: []
    };
  }

  async transition(newState, actor, reason) {
    if (!this.validTransitions[this.state].includes(newState)) {
      throw new InvalidTransitionError(this.state, newState);
    }
    
    const previousState = this.state;
    this.state = newState;
    
    await this.executeSideEffects(previousState, newState);
    await this.auditLog(previousState, newState, actor, reason);
    
    return this.state;
  }

  async executeSideEffects(from, to) {
    if (to === 'active') {
      await this.callScheduler.start();
      await this.dialer.resume();
    } else if (to === 'paused') {
      await this.dialer.pause(); // Finish in-progress, block new
    } else if (to === 'completed') {
      await this.callScheduler.stop();
      await this.generateCampaignSummary();
    }
  }
}
```

## Integration Points

- **Call Scheduler:** Lifecycle transitions start/stop the scheduling engine
- **Dialer Engine:** Active/paused states control dialing initiation
- **Contact List Manager:** Draft state allows list editing; active state locks lists
- **Analytics Pipeline:** State transitions trigger metric recording and snapshot creation
- **Notification System:** State changes trigger alerts to campaign operators
- **Compliance Engine:** Campaign state affects DNC checking requirements

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Use database transactions for state transitions to prevent race conditions in concurrent environments
- Implement a dead-letter queue for failed transitions — if a transition side effect fails, the campaign should not be stuck in an inconsistent state
- Cache the active campaign state in Redis for sub-millisecond checks before each dial attempt
- Archive completed campaigns in batches during off-peak hours to reduce database load
- Store full transition history in a separate audit table to keep the campaign table lean
- Implement a grace period on pause — allow in-progress calls up to 30 seconds to complete
- Monitor stuck campaigns — campaigns that remain active without dialing for 24+ hours should auto-pause with an alert
