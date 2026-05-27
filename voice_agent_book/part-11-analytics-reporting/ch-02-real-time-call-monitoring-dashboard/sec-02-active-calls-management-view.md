# Section 02: Active Calls Management View

## Overview

The active calls management view provides supervisors with control over currently connected calls. Beyond passive monitoring, this view enables real-time interventions: barge into a call (three-way), whisper coaching tips to the agent without the customer hearing, monitor silently, or transfer the call to another agent or queue. The view displays each active call with detailed metadata — agent name, customer info, elapsed time, current IVR state, transcription snippets, and real-time sentiment.

The management view is role-gated: agents see only their own active calls; supervisors see all calls in their campaigns; administrators see all calls across the tenant. Actions are logged to an audit trail for compliance. The view must maintain sub-second responsiveness even when displaying hundreds of active calls with real-time transcription updates, achieved through incremental DOM updates and memoized components.

## Architecture

```
               Active Calls Management

   WebSocket ↔ Feed Service → Call State Store (Redis)
                                    |
                          Active Calls Manager
                                    |
                          Supervisor Actions:
                          Barge | Whisper | Monitor | Transfer
                                    |
                          Twilio Client SDK / SIP.js
```

## Design Decisions

- **Centralized call state in Redis over per-instance memory:** The call management service maintains the authoritative state of every active call in Redis (keyed by `call:{callSid}` with TTL matching max call duration). Gateway instances read from and write to this shared state. This enables any supervisor to take over management from any dashboard instance. Trade-off: Redis becomes a single point of failure — mitigated by Redis Sentinel/Cluster. Reads add 1-2 ms latency but writes remain fast.

- **Action commands via Kafka over direct SIP signaling:** When a supervisor clicks "Barge," the dashboard publishes a command event to a Kafka topic (`commands.call.{callSid}`). The voice platform's streaming media server consumes this topic and executes the Twilio/SIP action (e.g., `<Conference>` modification). This decouples the dashboard from the media server and provides an audit log of all commands. Trade-off: Kafka adds ~50 ms latency compared to direct SIP, but provides durability, retry, and ordering guarantees.

- **Transcription snippet streaming over full transcription:** Instead of sending the entire transcription on each update, the server sends only incremental word/sentence deltas. The client appends these to its local buffer. This reduces WebSocket payload size by 90% compared to sending the full transcript every 500ms. Trade-off: the client must manage a growing buffer and handle reconnection gaps by requesting a full transcript sync.

## Implementation Approach

```typescript
interface ActiveCallState {
  callSid: string;
  status: 'ringing' | 'in-progress' | 'hold' | 'completed';
  agentId: string;
  agentName: string;
  customerName: string;
  customerPhone: string;
  startTime: number;
  duration: number;
  sentimentScore: number;
  transcription: TranscriptionSnippet[];
  ivrState: string;
  queueWaitTime?: number;
  recordingUrl?: string;
  muted: boolean;
  onHold: boolean;
}

interface TranscriptionSnippet {
  text: string;
  speaker: 'agent' | 'customer';
  timestamp: number;
  confidence: number;
  isFinal: boolean;
}

enum SupervisorAction {
  BARGE = 'barge',
  WHISPER = 'whisper',
  MONITOR = 'monitor',
  TRANSFER = 'transfer',
  MUTE = 'mute',
  UNMUTE = 'unmute',
  HOLD = 'hold',
  RESUME = 'resume',
}

class ActiveCallManager {
  private redis: Redis;
  private kafkaProducer: KafkaProducer;
  private liveFeed: LiveCallFeedService;

  async getActiveCalls(tenantId: string, supervisorId: string): Promise<ActiveCallState[]> {
    // Fetch all active calls for this tenant's campaigns
    const supervisor = await this.getSupervisor(supervisorId);
    const campaignIds = supervisor.campaigns;
    const pattern = `call:*:${tenantId}:*`;
    const keys = await this.redis.keys(pattern);
    const calls: ActiveCallState[] = [];

    for (const key of keys) {
      const call = await this.redis.hgetall(key);
      if (campaignIds.includes(call.campaignId)) {
        calls.push(parseCallState(call));
      }
    }

    return calls.sort((a, b) => b.startTime - a.startTime);
  }

  async executeAction(
    callSid: string,
    action: SupervisorAction,
    params: Record<string, string>,
    performedBy: string
  ): Promise<void> {
    // Publish command to Kafka
    await this.kafkaProducer.send({
      topic: `commands.call.${callSid}`,
      key: callSid,
      value: JSON.stringify({
        callSid,
        action,
        params,
        performedBy,
        timestamp: Date.now(),
      }),
    });

    // Audit log
    await this.redis.xadd(
      `audit:${callSid}`,
      '*',
      'action', action,
      'performedBy', performedBy,
      'params', JSON.stringify(params),
      'timestamp', Date.now().toString()
    );
  }
}

// React component for active call card
const ActiveCallCard: React.FC<{
  call: ActiveCallState;
  onAction: (callSid: string, action: SupervisorAction, params?: Record<string, string>) => void;
}> = ({ call, onAction }) => {
  const [transcript, setTranscript] = useState<TranscriptionSnippet[]>([]);

  // Subscribe to transcription updates
  useEffect(() => {
    const unsubscribe = subscribeToTranscription(call.callSid, (snippet) => {
      setTranscript(prev => [...prev, snippet]);
    });
    return unsubscribe;
  }, [call.callSid]);

  return (
    <div className="active-call-card" data-status={call.status}>
      <CallHeader
        agentName={call.agentName}
        customerName={call.customerName}
        duration={call.duration}
        sentiment={call.sentimentScore}
      />
      <TranscriptionPreview snippets={transcript.slice(-5)} />
      <ActionToolbar>
        <ActionButton
          icon={BargeIcon}
          label="Barge"
          onClick={() => onAction(call.callSid, SupervisorAction.BARGE)}
          disabled={call.status !== 'in-progress'}
        />
        <ActionButton
          icon={WhisperIcon}
          label="Whisper"
          onClick={() => onAction(call.callSid, SupervisorAction.WHISPER)}
        />
        <ActionButton
          icon={MonitorIcon}
          label="Monitor"
          onClick={() => onAction(call.callSid, SupervisorAction.MONITOR)}
        />
        <TransferButton
          callSid={call.callSid}
          onTransfer={(target) =>
            onAction(call.callSid, SupervisorAction.TRANSFER, { target })
          }
        />
      </ActionToolbar>
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Redis (RSAL) | Server | Call state store with TTL |
| Apache Kafka (Apache 2.0) | Server | Command event bus |
| Twilio Client SDK | Client | Media stream actions (SIP.js for non-Twilio) |
| React.memo / useMemo | Client | Render optimization |

## Production Considerations

**Scaling:** The Redis call state keys have a TTL equal to the maximum expected call duration (4 hours by default). For tenants exceeding 2000 concurrent calls, partition Redis across multiple shards by tenant ID. The Kafka command topics use compacted retention so the latest state for each call SID is always available on consumer restart. Supervisor action buttons should debounce to prevent double-sends (500 ms debounce on click).

**Security:** Supervisor actions require the `calls:manage` permission, with specific sub-permissions for barge, whisper, and monitor. All actions are logged to an immutable audit trail (Redis stream append-only). For regulated industries (finance, healthcare), the system must not allow barge/whisper on calls with active payment collection or sensitive data disclosure. The audit log must be retained for at least 7 years for PCI/HIPAA compliance.

**Monitoring:** Track actions per second by type (barge, whisper, monitor, transfer), action success vs failure rate, and action latency (click to media server acknowledgement). Alert on action failure rate exceeding 5% — this may indicate a media server connectivity issue. Monitor WebSocket reconnection frequency per supervisor session. Track the number of active calls per agent to detect agent overload situations.
