# Section 04: Reconnection Strategy

## Overview

WebSocket connections can drop due to network issues, server restarts, or client mobility. The reconnection strategy uses exponential backoff with jitter, last-known-event replay for state reconciliation, and a connection state machine that guides the client through reconnection phases. The goal is seamless recovery without data loss or duplicate processing.

## Architecture

```
Reconnection State Machine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[CONNECTED] ──→ Disconnect
                    │
                    ▼
               [WAITING] ←── Backoff Delay (1s, 2s, 4s, 8s...)
                    │
                    ▼
               [RECONNECTING] ──→ Attempt WebSocket upgrade
                    │                    │
                    │              [Success] ──→ State reconciliation
                    │                    │
                    │              [Failed] ──→ Increment retry count
                    │                    │
                    │              [Max retries] ──→ Give up
                    │                    │
                    ▼                    ▼
               [RECONNECTED]         [CLOSED]

Backoff Schedule:
  Attempt 1: 1 second + random jitter (0-500ms)
  Attempt 2: 2 seconds + jitter
  Attempt 3: 4 seconds + jitter
  Attempt 4: 8 seconds + jitter
  Attempt 5: 16 seconds + jitter
  Max: 30 seconds + jitter (cap)
  Total max retry duration: 5 minutes
```

## Design Decisions

- **Exponential Backoff with Jitter**: Prevents thundering herd when many clients reconnect simultaneously after server restart
- **Event Replay on Reconnect**: Client sends last received event ID; server replays events from that point forward
- **State Reconciliation**: After replay, client receives full state snapshot (current call statuses, agent states) to sync with reality
- **Total Retry Budget**: 5 minutes of retry before giving up; client displays error and offers manual reconnect

## Implementation Approach

```typescript
// Reconnection strategy configuration
interface ReconnectionConfig {
  initialDelay: number;      // milliseconds
  maxDelay: number;          // milliseconds
  maxRetries: number;
  totalTimeout: number;      // milliseconds
  jitterMax: number;         // milliseconds
}

const DEFAULT_RECONNECTION_CONFIG: ReconnectionConfig = {
  initialDelay: 1000,
  maxDelay: 30000,
  maxRetries: 20,
  totalTimeout: 300_000, // 5 minutes
  jitterMax: 500,
};

// Client-side reconnection manager
class ReconnectionManager {
  private retryCount = 0;
  private startTime: number = 0;
  private config: ReconnectionConfig;
  private lastEventId: string | null = null;

  constructor(config: Partial<ReconnectionConfig> = {}) {
    this.config = { ...DEFAULT_RECONNECTION_CONFIG, ...config };
  }

  getDelay(): number {
    const exponential = this.config.initialDelay * Math.pow(2, this.retryCount);
    const capped = Math.min(exponential, this.config.maxDelay);
    const jitter = Math.random() * this.config.jitterMax;
    return Math.floor(capped + jitter);
  }

  async retry(connectFn: () => Promise<void>): Promise<void> {
    this.startTime = Date.now();

    while (this.retryCount < this.config.maxRetries) {
      const elapsed = Date.now() - this.startTime;
      if (elapsed > this.config.totalTimeout) {
        throw new Error('Reconnection timeout exceeded');
      }

      const delay = this.getDelay();
      await this.sleep(delay);

      try {
        await connectFn();
        this.retryCount = 0; // Reset on success
        return;
      } catch (error) {
        this.retryCount++;
        console.warn(`Reconnection attempt ${this.retryCount} failed:`, error);
      }
    }

    throw new Error(`Max retries (${this.config.maxRetries}) exceeded`);
  }

  setLastEventId(eventId: string): void {
    this.lastEventId = eventId;
  }

  getReconnectionPayload(): { lastEventId: string | null } {
    return { lastEventId: this.lastEventId };
  }

  reset(): void {
    this.retryCount = 0;
    this.lastEventId = null;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Server-side event replay
class EventReplayService {
  constructor(private eventStore: EventStore) {}

  async getEventsSince(
    tenantId: string,
    lastEventId: string | null,
    limit = 1000,
  ): Promise<EventEnvelope[]> {
    if (!lastEventId) {
      // Send recent events as initial state
      return this.eventStore.getRecentEvents(tenantId, limit);
    }

    return this.eventStore.getEventsAfter(tenantId, lastEventId, limit);
  }

  async getStateSnapshot(tenantId: string): Promise<StateSnapshot> {
    const [agents, calls, campaigns] = await Promise.all([
      this.agentService.listActive(tenantId),
      this.callService.listActive(tenantId),
      this.campaignService.listActive(tenantId),
    ]);

    return {
      agents: agents.map(a => ({ id: a.id, status: a.status })),
      calls: calls.map(c => ({ id: c.id, status: c.status, duration: c.duration })),
      campaigns: campaigns.map(c => ({ id: c.id, status: c.status, progress: c.progress })),
      timestamp: new Date().toISOString(),
    };
  }
}

// Reconnect message flow
interface ReconnectMessage {
  type: 'reconnect';
  lastEventId: string | null;
}

interface ReplayMessage {
  type: 'replay';
  events: EventEnvelope[];
  hasMore: boolean;
}

interface StateSyncMessage {
  type: 'state_sync';
  snapshot: StateSnapshot;
}
```

## Integration Points

- **SDK**: Reconnection logic built into SDK client — transparent to application code
- **Event Store**: Events persisted for replay; TTL of 7 days for replay availability
- **Idempotency**: Replayed events carry original event IDs; client deduplicates on event ID

## Production Considerations

- **Replay Window**: Only last 5 minutes of events are available for replay; older events require full state sync
- **State Snapshot Size**: Large state snapshots are paginated; snapshot includes only active resources
- **Concurrent Reconnection Storm**: Use jitter to spread reconnection attempts; rate-limit state snapshot requests
- **Connection Draining**: During deployment, send drain message to clients for graceful reconnection

## Open-Source Tools

- **Socket.IO**: Built-in reconnection with backoff and event replay
- **Redis**: Storing last event IDs for replay across reconnections
