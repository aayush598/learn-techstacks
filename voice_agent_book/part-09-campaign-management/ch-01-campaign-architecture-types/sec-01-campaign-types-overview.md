# Section 01: Campaign Types Overview

## Overview

Outbound campaign management systems support multiple dialing modes, each optimized for different business requirements and operational constraints. The four primary campaign types — predictive, preview, progressive, and broadcast — differ fundamentally in how they manage the relationship between dialing rate, agent availability, and contact connection. Choosing the right campaign type directly impacts connect rates, agent utilization, compliance risk, and overall campaign ROI.

Predictive dialing uses algorithms to dial multiple contacts simultaneously, predicting when an agent will become available and connecting only answered calls to waiting agents. Preview dialing presents contact information to agents before dialing, allowing them to review context and decide whether to initiate the call. Progressive dialing automatically dials the next contact as soon as an agent becomes available, maintaining a one-to-one agent-to-call ratio. Broadcast dialing delivers pre-recorded messages to large contact lists without live agent involvement.

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
class CampaignDialer {
  constructor(type, config) {
    this.type = type; // predictive | preview | progressive | broadcast
    this.config = config;
    this.queue = new CallQueue();
    this.agentPool = new AgentPool();
  }

  async dialNext() {
    switch (this.type) {
      case 'predictive':
        const ratio = this.calculateDialRatio();
        const contacts = this.queue.popBatch(ratio);
        return Promise.all(contacts.map(c => this.placeCall(c)));
      case 'preview':
        const agent = this.agentPool.getReadyAgent();
        if (!agent) return;
        const contact = this.queue.peekNext();
        return this.sendPreview(agent, contact);
      case 'progressive':
        const readyAgent = this.agentPool.getReadyAgent();
        if (!readyAgent) return;
        const nextContact = this.queue.popNext();
        return this.placeCall(nextContact, readyAgent);
      case 'broadcast':
        return this.queue.drainBatch(this.config.batchSize);
    }
  }
}
```

## Integration Points

- **Agent Runtime (Part 06):** Provides agent presence and availability status for all dialing modes
- **Telephony Layer (Part 07):** SIP trunking and call control for actual call placement
- **Campaign Scheduler:** Triggers dialing based on campaign schedule and timezone rules
- **Compliance Engine (Ch 07):** DNC check and compliance validation before each dial attempt
- **Analytics Pipeline (Ch 09):** Collects dialing metrics per campaign type for performance analysis

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Predictive dialing requires carrier relationship management to avoid being flagged as spam
- Monitor abandonment rates in real-time for predictive campaigns to maintain regulatory compliance
- Preview dialing queues must include timeout mechanisms to prevent stale contact data
- Progressive dialing latency is critical — sub-100ms agent-to-call connection is the target
- Broadcast campaigns should stagger message delivery to avoid carrier throttling
- Campaign type switching (e.g., predictive → progressive) should be possible without campaign restart
