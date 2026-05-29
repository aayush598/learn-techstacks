# Section 05: Real-Time Data Pipeline

## Pipeline Architecture

The real-time data pipeline moves events from Kafka through a **stream processor** to materialized views, then pushes updates to connected clients via WebSocket. This enables sub-second dashboard updates for call status, metrics, and agent state.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REAL-TIME DATA PIPELINE                          │
│                                                                     │
│  ┌──────────┐    ┌────────────────────────────────────────────┐    │
│  │  Service  │───→│              KAFKA EVENT BUS              │    │
│  │  (Event   │    │                                            │    │
│  │  Producer)│    │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │    │
│  └──────────┘    │  │  Call    │  │  Agent   │  │  Metric  │ │    │
│                  │  │  Events  │  │  Events  │  │  Events  │ │    │
│                  │  └────┬─────┘  └────┬─────┘  └────┬─────┘ │    │
│                  └───────┼──────────────┼──────────────┼──────┘    │
│                          │              │              │           │
│                          ▼              ▼              ▼           │
│                  ┌────────────────────────────────────────────┐    │
│                  │            STREAM PROCESSOR                │    │
│                  │           (Kafka Streams / Flink)          │    │
│                  │                                            │    │
│                  │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │    │
│                  │  │  Filter  │  │  Enrich  │  │  Aggregate│ │    │
│                  │  └──────────┘  └──────────┘  └──────────┘ │    │
│                  │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │    │
│                  │  │  Join    │  │  Window  │  │   Route  │ │    │
│                  │  └──────────┘  └──────────┘  └──────────┘ │    │
│                  └────────────────────────────────────────────┘    │
│                          │              │              │           │
│          ┌────────────────┼──────────────┼──────────────┼───┐     │
│          ▼                ▼              ▼              ▼   │     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │     │
│  │ Materialized  │  │  ClickHouse  │  │  Redis Cache     │  │     │
│  │  View (PG)   │  │  (Analytics) │  │  (Hot Data)      │  │     │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │     │
│          │              │              │                    │     │
│          └──────────────┼──────────────┼────────────────────┘     │
│                         │              │                          │
│                         ▼              ▼                          │
│                  ┌────────────────────────────────────────────┐    │
│                  │          WEBSOCKET SERVER                  │    │
│                  │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │    │
│                  │  │ Channel  │  │  Room    │  │  Client  │ │    │
│                  │  │ Manager  │  │  Manager │  │  Auth    │ │    │
│                  │  └──────────┘  └──────────┘  └──────────┘ │    │
│                  └────────────────────────────────────────────┘    │
│                          │                                         │
│                          ▼                                         │
│                  ┌──────────────┐                                  │
│                  │   Browser    │                                  │
│                  │  Dashboard   │                                  │
│                  └──────────────┘                                  │
└─────────────────────────────────────────────────────────────────────┘
```

## Stream Processor (Kafka Streams)

```typescript
// Kafka Streams topology for real-time metrics
import { Kafka, EachMessagePayload } from 'kafkajs';

class MetricsStreamProcessor {
  private windowDuration = 60_000; // 1-minute windows
  private slidingStep = 10_000;    // 10-second sliding steps

  async process(payload: EachMessagePayload): Promise<void> {
    const event = JSON.parse(payload.message.value!.toString());
    const { tenantId, type, timestamp } = event;

    // Sliding window aggregation
    const windowKey = `${tenantId}:${this.getWindowKey(timestamp)}`;

    switch (type) {
      case 'call.initiated':
        await this.redis.hincrby(`metrics:${windowKey}`, 'calls_initiated', 1);
        break;
      case 'call.completed':
        await this.redis.hincrby(`metrics:${windowKey}`, 'calls_completed', 1);
        await this.redis.hincrby(`metrics:${windowKey}`, 'total_duration', event.data.duration);
        await this.redis.hincrbyfloat(`metrics:${windowKey}`, 'total_cost', event.data.cost);
        break;
      case 'call.failed':
        await this.redis.hincrby(`metrics:${windowKey}`, 'calls_failed', 1);
        break;
    }

    // Publish updated metrics to WebSocket
    await this.publishMetrics(tenantId, windowKey);
  }

  private getWindowKey(timestamp: string): string {
    const ms = new Date(timestamp).getTime();
    const windowStart = Math.floor(ms / this.slidingStep) * this.slidingStep;
    return String(windowStart);
  }

  private async publishMetrics(tenantId: string, windowKey: string): Promise<void> {
    const metrics = await this.redis.hgetall(`metrics:${windowKey}`);
    const activeCalls = await this.redis.scard(`active_calls:${tenantId}`);

    const payload = {
      type: 'metrics:update',
      data: {
        window: windowKey,
        ...metrics,
        activeCalls,
        timestamp: new Date().toISOString(),
      },
    };

    await this.wsServer.publish(`tenant:${tenantId}`, payload);
  }
}
```

## Materialized View Builder

```typescript
// Materialized view updated in real-time via Kafka consumer
class CallStatusViewBuilder {
  constructor(
    private db: PrismaClient,
    private redis: RedisClient
  ) {}

  async onCallInitiated(event: CallEvent<'initiated'>): Promise<void> {
    // Write to PostgreSQL read model
    await this.db.activeCall.create({
      data: {
        callId: event.data.callId,
        tenantId: event.data.tenantId,
        agentId: event.data.agentId,
        callerNumber: event.data.callerNumber,
        status: 'ringing',
        startedAt: new Date(event.timestamp),
      },
    });

    // Update Redis set of active calls
    await this.redis.sadd(
      `active_calls:${event.data.tenantId}`,
      event.data.callId
    );
  }

  async onCallCompleted(event: CallEvent<'completed'>): Promise<void> {
    // Move from active to history
    await this.db.activeCall.delete({
      where: { callId: event.data.callId },
    });

    await this.db.callHistory.create({
      data: {
        callId: event.data.callId,
        tenantId: event.data.tenantId,
        agentId: event.data.agentId,
        duration: event.data.duration,
        cost: event.data.cost,
        completedAt: new Date(event.timestamp),
      },
    });

    // Remove from active set
    await this.redis.srem(
      `active_calls:${event.data.tenantId}`,
      event.data.callId
    );
  }
}
```

## WebSocket Push

```typescript
// WebSocket server subscription management
class RealtimeSubscriptionManager {
  private subscriptions = new Map<string, Set<string>>(); // channel → clientIds

  subscribe(clientId: string, channel: string): void {
    if (!this.subscriptions.has(channel)) {
      this.subscriptions.set(channel, new Set());
    }
    this.subscriptions.get(channel)!.add(clientId);
  }

  unsubscribe(clientId: string, channel: string): void {
    this.subscriptions.get(channel)?.delete(clientId);
  }

  async publish<T>(channel: string, data: T): Promise<void> {
    const subscribers = this.subscriptions.get(channel);
    if (!subscribers || subscribers.size === 0) return;

    const message = JSON.stringify({
      channel,
      event: 'message',
      data,
      timestamp: new Date().toISOString(),
    });

    // Publish to Redis for cross-process broadcasting
    await this.redis.publish(`ws:${channel}`, message);

    // Local delivery for in-process clients
    for (const clientId of subscribers) {
      const ws = this.connections.get(clientId);
      if (ws?.readyState === WebSocket.OPEN) {
        ws.send(message);
      }
    }
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Stream processor | Kafka Streams (Node.js) | Same language as services, Kafka-native |
| Windowing | Sliding windows (10s step, 60s width) | Sub-minute granularity, smooth transitions |
| Materialized view | PostgreSQL + Redis | PG for persistence, Redis for hot data |
| Update frequency | Per-event push (no polling) | Lowest latency, efficient for moderate scale |
| Backpressure | Kafka consumer lag monitoring | Slow consumers don't lose events |

## Integration Points

- **Ch 04 (Real-Time Communication)** — WebSocket server delivers pipeline output
- **Ch 09 (Event-Driven Data Flow)** — Events are pipeline input
- **Ch 09 (CQRS)** — Materialized views are the read side
- **Ch 06 (Frontend)** — Chart components subscribe to pipeline output

## Production Considerations

- **Latency Target**: Event → Dashboard update: < 500ms (p99)
- **Throughput**: Pipeline handles 10K events/second on 3 consumer nodes
- **Failure Recovery**: Kafka offsets committed after successful materialized view update; at-least-once delivery
- **Data Skew**: Hot partitions mitigated by salting tenant ID with sub-tenant key
- **Monitoring**: Pipeline latency tracked at each stage (Kafka → Processor → View → WebSocket)
