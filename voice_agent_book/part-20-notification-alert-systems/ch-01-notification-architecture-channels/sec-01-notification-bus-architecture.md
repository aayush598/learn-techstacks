# Section 01: Notification Bus Architecture

## Overview

The notification bus is an event-driven pub/sub system that decouples notification producers from delivery channels. Events are published to topics, and the bus routes them to subscribed channels based on routing rules. This architecture enables adding new notification channels without modifying producers, supports multi-channel delivery from a single event, and provides reliable delivery guarantees.

## Architecture

```
┌──────────────┐     ┌──────────────────────────────────────┐     ┌──────────────┐
│  Producers    │     │          Notification Bus             │     │  Channels    │
│              │     │                                       │     │              │
│  API Server  │────▶│  ┌──────────┐  ┌──────────┐         │────▶│  Email       │
│  Agent       │     │  │  Topics   │  │  Router  │         │     │  Slack      │
│  Monitoring  │────▶│  │          │  │          │         │────▶│  SMS         │
│  Scheduler   │     │  │alerts    │  │ Rules    │         │     │  Webhook    │
│              │────▶│  │digests   │  │ Filters  │         │────▶│  In-App     │
│              │     │  │system    │  │ Transfrm │         │     │  Push       │
└──────────────┘     └──────────────────────────────────────┘     └──────────────┘
```

## Design Decisions

- **Async Processing**: Producers fire-and-forget; bus handles delivery
- **Topic-Based Routing**: Events published to topics, channels subscribe
- **Persistence**: Messages stored in queue until acknowledged
- **Idempotency**: Duplicate detection prevents duplicate deliveries

## Implementation Approach

```typescript
interface NotificationEvent {
  id: string;
  topic: string;
  type: string;
  payload: Record<string, unknown>;
  metadata: {
    tenantId: string;
    source: string;
    timestamp: string;
    correlationId: string;
  };
}

interface ChannelSubscriber {
  channel: string;
  filter: (event: NotificationEvent) => boolean;
  transform: (event: NotificationEvent) => ChannelPayload;
}

class NotificationBus {
  private subscribers: Map<string, ChannelSubscriber[]> = new Map();

  async publish(event: NotificationEvent): Promise<void> {
    const subscribers = this.subscribers.get(event.topic) || [];
    const matching = subscribers.filter(s => s.filter(event));
    await Promise.all(matching.map(s => this.deliver(s, event)));
  }

  subscribe(topic: string, subscriber: ChannelSubscriber): void {
    const subs = this.subscribers.get(topic) || [];
    subs.push(subscriber);
    this.subscribers.set(topic, subs);
  }

  private async deliver(subscriber: ChannelSubscriber, event: NotificationEvent): Promise<void> {
    const payload = subscriber.transform(event);
    const provider = this.getChannelProvider(subscriber.channel);
    await provider.send(payload);
  }
}
```

## Integration Points

- **Producer Integration**: Services publish events via SDK
- **Channel Integration**: Each channel implements provider interface
- **Monitoring**: Bus metrics tracked (messages published, delivery time, failures)

## Open-Source Tools

- **BullMQ** (MIT): Redis-backed job queue for reliable delivery
- **Apache Kafka** (Apache 2.0): High-throughput event streaming
- **NATS** (Apache 2.0): Lightweight pub/sub messaging
- **RabbitMQ** (MPL 2.0): AMQP message broker

## Production Considerations

- **Queue Depth Monitoring**: Alert when queues grow; indicates consumer issues
- **Dead Letter Queue**: Failed deliveries routed to DLQ for inspection
- **Backpressure**: Rate-limit producers when channels are slow
