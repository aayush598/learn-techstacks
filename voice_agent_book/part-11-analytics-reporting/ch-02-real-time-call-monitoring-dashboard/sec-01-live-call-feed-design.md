# Section 01: Live Call Feed Design

## Overview

The live call feed is the central real-time component of the call monitoring dashboard, displaying incoming, active, and recently completed calls as they happen. It provides operations teams with an at-a-glance view of the contact center's current state, enabling rapid response to emerging issues. The feed consumes events from the analytics pipeline's stream processing layer via WebSocket connections, rendering each call as a rich card with caller information, current status, duration, sentiment indicators, and action buttons (barge, whisper, transfer, monitor).

The design prioritizes sub-second update latency — a call event published to Kafka must appear in the feed within 500 ms. The feed supports filtering by campaign, agent, status, and sentiment threshold, as well as search by caller ID or customer name. It implements virtual scrolling to handle high throughput scenarios (1000+ concurrent calls) without DOM overhead. The feed uses Redis Streams as a real-time buffer between the event bus and WebSocket gateway to absorb traffic spikes and provide exactly-once delivery semantics.

## Architecture

```
           Live Call Feed Architecture

   Call Events → Kafka → Stream Processor → Redis Streams
                                                |
                                          WebSocket Gateway
                                                |
                                     Dashboard Client (React)
                                                |
                                     Virtual Scroll List
                                     Filter / Search Bar
                                     Status Badges / Actions
```

## Design Decisions

- **Redis Streams as a real-time buffer over direct Kafka-to-WebSocket:** The stream processor writes enriched call events to Redis Streams with consumer group support. The WebSocket gateway reads from Redis Streams as a consumer, allowing horizontal scaling of gateway instances. If the gateway restarts, it resumes from the last acknowledged message. Trade-off: Redis introduces an additional hop and memory overhead, but it decouples Kafka consumer offset management from the WebSocket layer, enabling independent scaling of ingestion and delivery.

- **Virtual scrolling with fixed-height cards over paginated loading:** When the live feed must render hundreds of concurrent calls, DOM re-renders become a bottleneck. A virtual scroll library (react-window or TanStack Virtual) renders only the visible rows (typically 10-15) plus a small overscan buffer. Trade-off: virtual scrolling requires all rows to have uniform or known heights, and row reordering (sorting by newest event) requires recalculating the visible window.

- **Optimistic UI updates with server reconciliation over waiting for acknowledgment:** When a supervisor performs an action (e.g., mute a call), the UI immediately updates the action button state to "pending" before the server confirms. If the server rejects or fails, the UI reverts within 2 seconds. This keeps the feed feeling responsive even under network latency. Trade-off: optimistic updates can cause brief UI inconsistencies if the server state diverges (e.g., a call ends between the optimistic mute and the actual mute command).

## Implementation Approach

```typescript
interface LiveCallFeedEvent {
  callSid: string;
  tenantId: string;
  campaignId: string;
  agentId: string;
  customerName: string;
  customerPhone: string;
  status: 'ringing' | 'in-progress' | 'completed' | 'failed' | 'queued';
  startTime: number;
  duration: number;
  sentiment: { score: number; label: 'positive' | 'neutral' | 'negative' };
  queuePosition?: number;
  waitTime?: number;
  skills?: string[];
}

interface FeedFilter {
  campaignIds?: string[];
  agentIds?: string[];
  statuses?: string[];
  sentimentMin?: number;
  searchQuery?: string;
}

class LiveCallFeedService {
  private ws: WebSocket;
  private stream: RedisStreamConsumer;
  private feedBuffer: Map<string, LiveCallFeedEvent> = new Map();
  private subscribers: Set<(events: LiveCallFeedEvent[]) => void> = new Set();

  async connect(tenantId: string, filters: FeedFilter): Promise<void> {
    // Establish WebSocket connection with authentication
    this.ws = new WebSocket(`${WS_URL}/feed/${tenantId}`);
    await this.ws.connect();

    // Subscribe to Redis Stream for this tenant
    await this.stream.subscribe({
      stream: `feed:${tenantId}`,
      consumerGroup: 'dashboard',
      onMessage: (event: LiveCallFeedEvent) => {
        this.handleEvent(event);
      },
    });

    // Send filter on connect
    this.ws.send(JSON.stringify({ type: 'subscribe', filters }));
  }

  private handleEvent(event: LiveCallFeedEvent): void {
    const existing = this.feedBuffer.get(event.callSid);

    if (!existing) {
      // New call
      this.feedBuffer.set(event.callSid, event);
    } else {
      // Update existing call
      this.feedBuffer.set(event.callSid, { ...existing, ...event });

      // Remove completed calls after 30 seconds
      if (event.status === 'completed' || event.status === 'failed') {
        setTimeout(() => {
          this.feedBuffer.delete(event.callSid);
          this.notifySubscribers();
        }, 30000);
      }
    }

    this.notifySubscribers();
  }

  private notifySubscribers(): void {
    const events = Array.from(this.feedBuffer.values())
      .sort((a, b) => b.startTime - a.startTime);
    this.subscribers.forEach(cb => cb(events));
  }
}

// Virtual scroll integration
interface FeedRowProps {
  event: LiveCallFeedEvent;
  onAction: (callSid: string, action: string) => void;
}

const FeedRow: React.FC<FeedRowProps> = ({ event, onAction }) => {
  const elapsed = useElapsedTime(event.startTime); // custom hook

  return (
    <div className="feed-row" data-call-sid={event.callSid}>
      <StatusBadge status={event.status} waitTime={event.waitTime} />
      <CallerInfo name={event.customerName} phone={event.customerPhone} />
      <DurationDisplay elapsed={elapsed} />
      <SentimentIndicator score={event.sentiment.score} />
      <ActionButtons
        callSid={event.callSid}
        status={event.status}
        onAction={onAction}
      />
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Redis Streams (RSAL) | Server | Real-time event buffer |
| Socket.IO (MIT) | Server/Client | WebSocket transport gateway |
| react-window (MIT) | Client | Virtual scrolling for large lists |
| TanStack Virtual (MIT) | Client | Alternative virtual scroll library |

## Production Considerations

**Scaling:** Each tenant gets a dedicated Redis Stream (`feed:{tenantId}`) to isolate data. WebSocket gateway instances are stateless and scale horizontally behind a load balancer with sticky sessions. Redis Stream consumer groups ensure each event is delivered to exactly one gateway instance. For very high traffic tenants (5000+ concurrent calls), apply backpressure: if the Redis Stream exceeds 50 MB, throttle non-critical event types (sentiment updates every 5 seconds instead of every second).

**Security:** Every WebSocket connection authenticates via JWT with the tenant ID embedded. The gateway validates that the requesting user has the `monitoring:live-feed` permission. Caller PII (phone numbers, names) is masked for agents and supervisors without the `pii:view` permission. Rate-limit reconnections to 5 per minute per user to prevent abuse.

**Monitoring:** Track WebSocket connection count per tenant, message throughput (events/second), end-to-end latency (Kafka publish to feed render), and feed buffer size. Alert if latency exceeds 1 second, if the reconnection rate exceeds 10% of active connections, or if the Redis Stream memory exceeds 100 MB.
