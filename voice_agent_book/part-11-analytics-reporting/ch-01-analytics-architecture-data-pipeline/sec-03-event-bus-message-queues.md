# Section 03: Event Bus and Message Queues

## Overview

The event bus and message queue infrastructure forms the central nervous system of the analytics pipeline, connecting event producers (ingestion layer, telephony engine, payment engine) with event consumers (stream processors, batch processors, notification systems, webhook engine). The event bus provides reliable, ordered, and scalable message delivery with configurable delivery semantics (at-least-once, exactly-once for critical events).

Apache Kafka serves as the primary event bus due to its high throughput, durability, replay capability, and ecosystem of stream processing frameworks. Message queues (Bull/BullMQ with Redis) complement Kafka for task-oriented workloads (email notifications, report generation, webhook delivery) where individual message acknowledgement and retry semantics are more important than event streaming. The combination provides both the event streaming capabilities needed for real-time analytics and the reliable task execution needed for operational workflows.

## Architecture

```
                Event Bus & Message Queue Architecture

   Producers → Kafka (Event Bus) → Stream Processors
                 |                      |
                 v                      v
           Event Archive           Real-time DB
                 |
           S3/Parquet
                 
   Workers → BullMQ (Task Queue) → Notification
               |                    |
               v                    v
           Report Gen           Webhook Deliv
```

## Design Decisions

- **Kafka for event streaming over RabbitMQ/Pulsar:** Kafka's log-based architecture provides ordered, replayable, and partitionable event streams that are ideal for analytics. Events can be replayed from any point in time, enabling backfill scenarios and recovery from processing errors. RabbitMQ is better for complex routing use cases (topic exchanges, headers exchanges) but Kafka's simplicity and replayability make it the better choice for analytics pipelines where data completeness is critical. Trade-off: Kafka has higher operational complexity (ZooKeeper/KRaft, controller nodes) but provides stronger guarantees for event streaming at scale.

- **Topic-per-event-type over single monolithic topic:** Each event type has its own Kafka topic (events.call.started, events.call.ended, events.payment.succeeded, etc.). This allows consumer groups to subscribe only to the event types they need, provides independent retention policies per event type, and simplifies schema management (one schema per topic). The topic naming convention includes the source domain and event version for clarity. Trade-off: topic-per-event-type increases the total number of topics (potentially hundreds) but provides cleaner separation of concerns and independent scalability.

- **BullMQ for task queues over Kafka consumers for operational tasks:** While Kafka consumers could handle task execution, BullMQ provides built-in retry with exponential backoff, delayed job scheduling, job rate limiting, job progress tracking, and a job dashboard UI. These features are essential for operational tasks like sending emails (which may fail and need retry), generating PDF reports (which may take minutes), and delivering webhooks (which need per-endpoint rate limiting). Trade-off: task queues require a Redis infrastructure separate from Kafka but provide operational features that Kafka consumers lack.

## Implementation Approach

```
class EventBusService {
  private kafka: Kafka;
  private admin: Admin;

  constructor(private config: EventBusConfig) {
    this.kafka = new Kafka({
      clientId: config.clientId,
      brokers: config.brokers,
      ssl: config.ssl,
      sasl: config.sasl,
    });
    this.admin = this.kafka.admin();
  }

  async ensureTopics(): Promise<void> {
    const topics = EVENT_TOPICS.map(t => ({
      topic: t.name,
      numPartitions: t.partitions,
      replicationFactor: t.replicationFactor,
      configEntries: [
        { name: 'retention.ms', value: String(t.retentionMs) },
        { name: 'compression.type', value: 'snappy' },
        { name: 'cleanup.policy', value: t.compacted ? 'compact,delete' : 'delete' },
      ],
    }));

    await this.admin.createTopics({ topics, waitForLeaders: true });
    logger.info('Kafka topics ensured', { count: topics.length });
  }

  createProducer(): KafkaProducer {
    return this.kafka.producer({
      allowAutoTopicCreation: false,
      transactionTimeout: 30000,
      idempotent: true,
      maxInFlightRequests: 5,
    });
  }

  createConsumer(groupId: string, options?: ConsumerOptions): KafkaConsumer {
    return this.kafka.consumer({
      groupId,
      sessionTimeout: 30000,
      heartbeatInterval: 3000,
      rebalanceTimeout: 60000,
      ...options,
    });
  }

  // Exactly-once semantics for critical event types using Kafka transactions
  async sendExactlyOnce(transactionalProducer: KafkaProducer, messages: MessageBatch): Promise<void> {
    await transactionalProducer.connect();
    await transactionalProducer.sendBatch(messages);
    await transactionalProducer.disconnect();
  }
}

// Standard event topics configuration
const EVENT_TOPICS = [
  { name: 'events.call.started', partitions: 24, replicationFactor: 3, retentionMs: 604800000 },     // 7 days
  { name: 'events.call.ended', partitions: 24, replicationFactor: 3, retentionMs: 604800000 },       // 7 days
  { name: 'events.call.transcription', partitions: 48, replicationFactor: 3, retentionMs: 2592000000 }, // 30 days
  { name: 'events.call.sentiment', partitions: 24, replicationFactor: 3, retentionMs: 2592000000 },
  { name: 'events.payment.succeeded', partitions: 12, replicationFactor: 3, retentionMs: 7776000000 },  // 90 days
  { name: 'events.payment.failed', partitions: 12, replicationFactor: 3, retentionMs: 7776000000 },
  { name: 'events.customer.created', partitions: 8, replicationFactor: 3, retentionMs: 7776000000, compacted: true },
  { name: 'events.customer.updated', partitions: 8, replicationFactor: 3, retentionMs: 7776000000, compacted: true },
  { name: 'events.agent.status', partitions: 8, replicationFactor: 3, retentionMs: 604800000 },
  { name: 'analytics.realtime', partitions: 16, replicationFactor: 2, retentionMs: 3600000 },        // 1 hour
];

// Task queue configuration for operational workloads
class TaskQueueService {
  private queues: Map<string, Queue>;

  constructor(private redis: Redis) {
    this.queues = new Map();
  }

  getQueue(name: string): Queue {
    if (!this.queues.has(name)) {
      this.queues.set(name, new Queue(name, {
        connection: this.redis,
        defaultJobOptions: {
          attempts: 5,
          backoff: { type: 'exponential', delay: 1000 },
          removeOnComplete: { count: 100 },
          removeOnFail: { count: 50 },
        },
      }));
    }
    return this.queues.get(name)!;
  }

  async enqueueNotification(params: {
    type: 'email' | 'sms' | 'slack';
    to: string;
    subject?: string;
    body: string;
    tenantId: string;
  }): Promise<Job> {
    const queue = this.getQueue('notifications');
    return queue.add(params.type, params, {
      priority: params.type === 'sms' ? 1 : 2,
      attempts: 3,
    });
  }

  async enqueueReportGeneration(params: {
    reportId: string;
    format: 'pdf' | 'csv' | 'xlsx';
    filters: Record<string, any>;
    tenantId: string;
  }): Promise<Job> {
    const queue = this.getQueue('report-generation');
    return queue.add(params.reportId, params, {
      timeout: 300000, // 5 minute timeout for PDF generation
      attempts: 2,
    });
  }

  async enqueueWebhookDelivery(params: {
    endpointId: string;
    eventId: string;
    payload: any;
    tenantId: string;
  }): Promise<Job> {
    const queue = this.getQueue(`webhook-delivery-${params.endpointId}`);
    return queue.add(params.eventId, params, {
      attempts: 5,
      backoff: { type: 'exponential', delay: 2000 },
    });
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apache Kafka (Apache 2.0) | Server | Event streaming |
| KafkaJS (MIT) | Node.js | Kafka client |
| BullMQ (MIT) | Node.js | Task queues |
| Redpanda (BSL) | Server | Kafka alternative |

## Production Considerations

**Scaling:** Kafka partitions are the unit of parallelism — more partitions enable higher throughput but increase the number of open file descriptors and rebalance time. Recommended partition count: max(24, peak_throughput_MBps / 10MBps_per_partition). Retention is a storage concern — 30 days of event data at 1000 events/second at 1KB each = 2.5TB. Use tiered storage or S3-backed Kafka for longer retention. Task queues use Redis — ensure Redis is configured with persistence (AOF) for durability.

**Security:** Kafka supports SSL encryption for data in transit and SASL/SCRAM or mTLS for authentication. ACLs control topic access per principal. BullMQ queues should be in a separate Redis namespace with access control. Encrypt sensitive event payload fields before they enter Kafka (field-level encryption). Never log message contents from Kafka topics.

**Monitoring:** Track Kafka broker disk usage, under-replicated partitions, consumer group lag (difference between latest offset and consumer offset — critical metric), messages in per second per topic, and request handler latency. Monitor BullMQ queue depth, job completion rates, job failure rates, and stalled job count. Alert on consumer lag exceeding 5 minutes, under-replicated partitions, broker disk usage exceeding 80%, and BullMQ stalled jobs.
