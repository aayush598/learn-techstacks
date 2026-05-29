# Section 03: Message Broker (Apache Kafka)

## Kafka Architecture

Apache Kafka serves as the **event backbone** for all asynchronous communication between microservices. It provides durable, ordered, replayable event streams that enable loose coupling and reliable processing.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      APACHE KAFKA ARCHITECTURE                        │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    KAFKA CLUSTER                                │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │    │
│  │  │ Broker 1 │  │ Broker 2 │  │ Broker 3 │                      │    │
│  │  │ (Leader) │  │(Follower)│  │(Follower)│                      │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘                      │    │
│  └───────┼──────────────┼──────────────┼───────────────────────────┘    │
│          │              │              │                                │
│  ┌───────┴──────────────┴──────────────┴───────────────────────────┐    │
│  │                        TOPICS & PARTITIONS                      │    │
│  │                                                                  │    │
│  │  call.events (12 partitions)                                    │    │
│  │  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐  │    │
│  │  │ P0 │ P1 │ P2 │ P3 │ P4 │ P5 │ P6 │ P7 │ P8 │ P9 │ P10│ P11│  │    │
│  │  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘  │    │
│  │                                                                  │    │
│  │  agent.events (6 partitions)                                    │    │
│  │  ┌────┬────┬────┬────┬────┬────┐                                │    │
│  │  │ P0 │ P1 │ P2 │ P3 │ P4 │ P5 │                                │    │
│  │  └────┴────┴────┴────┴────┴────┘                                │    │
│  │                                                                  │    │
│  │  billing.events (6 partitions)                                  │    │
│  │  ┌────┬────┬────┬────┬────┬────┐                                │    │
│  │  │ P0 │ P1 │ P2 │ P3 │ P4 │ P5 │                                │    │
│  │  └────┴────┴────┴────┴────┴────┘                                │    │
│  │                                                                  │    │
│  │  voice.pipeline (12 partitions)                                 │    │
│  │  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐  │    │
│  │  │ P0 │ P1 │ P2 │ P3 │ P4 │ P5 │ P6 │ P7 │ P8 │ P9 │ P10│ P11│  │    │
│  │  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘  │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    CONSUMER GROUPS                              │    │
│  │                                                                  │    │
│  │  call.events:                                                    │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │    │
│  │  │ billing-service │  │  ai-service     │  │ voice-service   │  │    │
│  │  │ (6 consumers)   │  │ (3 consumers)   │  │ (3 consumers)   │  │    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘  │    │
│  │                                                                  │    │
│  │  Each consumer group gets every message (broadcast within group) │    │
│  │  Within a group, partitions are distributed across consumers     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Topic Design

```typescript
// Topic configuration
interface TopicConfig {
  name: string
  partitions: number
  replicationFactor: number
  retentionMs: number
  cleanupPolicy: 'delete' | 'compact' | 'compact,delete'
  compressionType: 'gzip' | 'snappy' | 'lz4' | 'zstd' | 'none'
  maxMessageBytes: number
  minInSyncReplicas: number
}

export const TOPICS: Record<string, TopicConfig> = {
  'call.events': {
    name: 'call.events',
    partitions: 12,
    replicationFactor: 3,
    retentionMs: 604800000,     // 7 days
    cleanupPolicy: 'delete',
    compressionType: 'zstd',
    maxMessageBytes: 1048576,   // 1MB
    minInSyncReplicas: 2
  },
  'agent.events': {
    name: 'agent.events',
    partitions: 6,
    replicationFactor: 3,
    retentionMs: 2592000000,    // 30 days
    cleanupPolicy: 'compact',   // Keep latest state per key
    compressionType: 'zstd',
    maxMessageBytes: 524288,    // 512KB
    minInSyncReplicas: 2
  },
  'voice.pipeline': {
    name: 'voice.pipeline',
    partitions: 12,
    replicationFactor: 3,
    retentionMs: 86400000,      // 1 day (high volume, low value over time)
    cleanupPolicy: 'delete',
    compressionType: 'lz4',     // Faster compression for real-time
    maxMessageBytes: 1048576,
    minInSyncReplicas: 2
  },
  'billing.events': {
    name: 'billing.events',
    partitions: 6,
    replicationFactor: 3,
    retentionMs: 7776000000,    // 90 days (audit requirement)
    cleanupPolicy: 'delete',
    compressionType: 'zstd',
    maxMessageBytes: 524288,
    minInSyncReplicas: 2
  },
  'dlq': {
    name: 'dlq',
    partitions: 3,
    replicationFactor: 3,
    retentionMs: 2592000000,    // 30 days
    cleanupPolicy: 'delete',
    compressionType: 'zstd',
    maxMessageBytes: 2097152,   // 2MB (may include error context)
    minInSyncReplicas: 2
  },
  'audit.events': {
    name: 'audit.events',
    partitions: 6,
    replicationFactor: 3,
    retentionMs: 31536000000,   // 365 days (audit trail)
    cleanupPolicy: 'compact,delete',
    compressionType: 'zstd',
    maxMessageBytes: 524288,
    minInSyncReplicas: 2
  }
}
```

## Avro Schema Registry

```typescript
// Event schemas using Avro for schema evolution and compatibility

// call-events.avsc
{
  "namespace": "com.voiceplatform.event",
  "type": "record",
  "name": "CallEvent",
  "fields": [
    { "name": "eventId", "type": "string" },
    { "name": "callId", "type": "string" },
    { "name": "type", "type": {
      "type": "enum",
      "name": "CallEventType",
      "symbols": ["INITIATED", "RINGING", "ANSWERED", "UPDATED", "ENDED", "TRANSFERRED", "ERROR"]
    }},
    { "name": "tenantId", "type": "string" },
    { "name": "agentId", "type": ["null", "string"], "default": null },
    { "name": "timestamp", "type": { "type": "long", "logicalType": "timestamp-millis" } },
    { "name": "data", "type": ["null", { "type": "map", "values": "string" }], "default": null },
    { "name": "version", "type": "int", "default": 1 }
  ]
}

// Schema registry client
import { SchemaRegistry } from '@kafkajs/schema-registry'

const registry = new SchemaRegistry({
  host: process.env.SCHEMA_REGISTRY_URL!,
  auth: {
    username: processenv.SCHEMA_REGISTRY_USERNAME!,
    password: process.env.SCHEMA_REGISTRY_PASSWORD!
  }
})

export async function registerSchemas(): Promise<void> {
  await registry.register({
    type: 'AVRO',
    schema: CALL_EVENT_SCHEMA
  })
}

// Produce with Avro encoding
export async function produceCallEvent(event: CallEvent): Promise<void> {
  await producer.send({
    topic: 'call.events',
    messages: [{
      key: event.callId,
      // Encode with schema ID for compact wire format
      value: await registry.encode(event.callId, event)
    }]
  })
}
```

## Producer Patterns

```typescript
// Reliable producer with idempotency and retry
import { Kafka, Producer, Partitioners } from 'kafkajs'

export function createReliableProducer(): Producer {
  const kafka = new Kafka({
    clientId: 'call-service',
    brokers: process.env.KAFKA_BROKERS!.split(','),
    ssl: true,
    sasl: {
      mechanism: 'scram-sha-512',
      username: process.env.KAFKA_USERNAME!,
      password: process.env.KAFKA_PASSWORD!
    }
  })

  return kafka.producer({
    createPartitioner: Partitioners.DefaultPartitioner,
    // Idempotent producer
    idempotent: true,
    maxInFlightRequests: 5,
    // Transaction support
    transactionalId: `call-service-${process.env.HOSTNAME}`,
    retry: {
      initialRetryTime: 100,
      retries: 10,
      maxRetryTime: 30000,
      factor: 2
    }
  })
}

// Transactional producer (for exactly-once semantics)
export async function processCallCompletion(callId: string): Promise<void> {
  const producer = createReliableProducer()
  await producer.connect()

  // Start transaction
  await producer.sendBatch({
    topicMessages: [
      {
        topic: 'call.events',
        messages: [{ key: callId, value: JSON.stringify({ type: 'ENDED', callId }) }]
      },
      {
        topic: 'billing.events',
        messages: [{ key: callId, value: JSON.stringify({ type: 'CALL_COMPLETED', callId }) }]
      }
    ]
  })
}
```

## Consumer Patterns

```typescript
// Reliable consumer with checkpointing and error handling
import { Kafka, Consumer, EachMessagePayload } from 'kafkajs'

export class EventConsumer {
  private consumer: Consumer
  private handler: (event: any) => Promise<void>
  private dlqProducer: Producer

  constructor(options: {
    groupId: string
    topics: string[]
    handler: (event: any) => Promise<void>
    fromBeginning?: boolean
  }) {
    const kafka = new Kafka({
      clientId: options.groupId,
      brokers: process.env.KAFKA_BROKERS!.split(','),
      ssl: true,
      sasl: { mechanism: 'scram-sha-512', username: '...', password: '...' }
    })

    this.consumer = kafka.consumer({
      groupId: options.groupId,
      sessionTimeout: 30000,
      heartbeatInterval: 3000,
      maxBytesPerPartition: 1048576,  // 1MB per partition
      minBytes: 1,
      maxWaitTimeInMs: 100,
      retry: { retries: 5 }
    })

    this.handler = options.handler
    this.dlqProducer = kafka.producer({ allowAutoTopicCreation: false })
  }

  async start(): Promise<void> {
    await this.consumer.connect()
    await this.dlqProducer.connect()

    await this.consumer.subscribe({
      topics: this.topics,
      fromBeginning: false
    })

    await this.consumer.run({
      autoCommit: false,
      eachMessage: async (payload: EachMessagePayload) => {
        await this.processMessage(payload)
      }
    })
  }

  private async processMessage({ topic, partition, message }: EachMessagePayload) {
    const startTime = Date.now()

    try {
      // Parse event
      const event = JSON.parse(message.value!.toString())

      // Check idempotency
      const idempotencyKey = message.headers!['idempotency-key']?.toString()
      if (idempotencyKey) {
        const alreadyProcessed = await this.checkIdempotency(idempotencyKey)
        if (alreadyProcessed) {
          await this.consumer.commitOffsets([{ topic, partition, offset: message.offset }])
          return
        }
      }

      // Process
      await this.handler(event)

      // Record metrics
      this.recordLatency(topic, Date.now() - startTime)

      // Commit offset
      await this.consumer.commitOffsets([{ topic, partition, offset: message.offset }])

      // Mark idempotency
      if (idempotencyKey) {
        await this.markIdempotency(idempotencyKey)
      }

    } catch (error) {
      await this.handleError(topic, partition, message, error)
    }
  }

  private async handleError(topic: string, partition: number, message: any, error: unknown) {
    // Send to DLQ
    await this.dlqProducer.send({
      topic: 'dlq',
      messages: [{
        key: message.key?.toString(),
        value: JSON.stringify({
          originalTopic: topic,
          originalPartition: partition,
          originalOffset: message.offset,
          originalMessage: message.value?.toString(),
          error: (error as Error).message,
          errorStack: (error as Error).stack,
          timestamp: new Date().toISOString()
        })
      }]
    })

    // Still commit offset (skip bad message)
    await this.consumer.commitOffsets([{ topic, partition, offset: message.offset }])

    logger.error({
      topic, partition, offset: message.offset,
      error: (error as Error).message
    }, 'Message processing failed, sent to DLQ')
  }

  private async checkIdempotency(key: string): Promise<boolean> {
    return redis.exists(`idempotency:${key}`)
  }

  private async markIdempotency(key: string): Promise<void> {
    await redis.set(`idempotency:${key}`, '1', { ex: 86400 })
  }

  private recordLatency(topic: string, latencyMs: number): void {
    messageLatency.observe({ topic }, latencyMs)
  }

  async disconnect(): Promise<void> {
    await this.consumer.disconnect()
    await this.dlqProducer.disconnect()
  }
}
```

## Stream Processing

```typescript
// Kafka Streams-style processing using ksqldb or custom processor
// Example: Real-time sentiment aggregation

// ksqlDB query
/*
CREATE STREAM call_events (
  eventId VARCHAR,
  callId VARCHAR,
  type VARCHAR,
  tenantId VARCHAR,
  data MAP<VARCHAR, VARCHAR>
) WITH (kafka_topic='call.events', value_format='avro');

-- Aggregated sentiment by tenant
CREATE TABLE tenant_sentiment AS
  SELECT
    tenantId,
    COUNT(*) AS total_calls,
    AVG(CAST(data['sentiment_score'] AS DOUBLE)) AS avg_sentiment,
    SUM(CASE WHEN data['status'] = 'completed' THEN 1 ELSE 0 END) AS completed_calls,
    SUM(CASE WHEN data['status'] = 'failed' THEN 1 ELSE 0 END) AS failed_calls,
    WINDOW TUMBLING (SIZE 1 HOUR)
  FROM call_events
  WHERE type = 'ENDED'
  GROUP BY tenantId;
*/

// Alternative: Node.js stream processor using kafkajs
export class StreamProcessor {
  async processCallVolume(windowMs: number = 60000) {
    const consumer = new EventConsumer({
      groupId: 'stream-processor',
      topics: ['call.events'],
      handler: async (event) => {
        // Update sliding window counters
        const windowKey = `stream:calls:${Math.floor(Date.now() / windowMs)}`
        await redis.incr(windowKey)
        await redis.expire(windowKey, Math.ceil(windowMs / 1000) * 2)
      }
    })

    await consumer.start()
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Message Format | Avro + Schema Registry | Schema evolution, compatibility enforcement, compact binary |
| Partition Strategy | Key-based (call_id, tenant_id) | Ordering guarantee per key |
| Replication | 3 brokers, min ISR = 2 | Fault tolerance with consistency |
| Retention | Per-topic based on value | 7 days for events, 90 days for billing, 1 year for audit |
| Compression | zstd (default), lz4 (real-time) | zstd: best ratio; lz4: fastest |
| Error Handling | DLQ with retry 3x | Reliable processing, no data loss |

## Integration Points

- **Part 05 (Microservices)** — Kafka is the communication backbone
- **Part 09 (Data Flow)** — Event-driven architecture built on Kafka
- **Part 11 (Analytics)** — Stream data into ClickHouse via Kafka
- **Part 20 (Notifications)** — Events trigger webhook/email delivery

## Production Considerations

- **Cluster Size**: 3 brokers minimum (development); 6+ for production (2 per AZ)
- **Storage**: Each broker: 1TB+ NVMe; monitor disk usage; set retention based on volume
- **Monitoring**: Track consumer lag (critical), request rate, disk usage, network I/O
- **Consumer Lag Alert**: Alert if lag > 10K messages for more than 5 minutes
- **Rebalance**: Minimize rebalances (stable group membership); use cooperative rebalancing
- **Security**: TLS encryption, SASL/SCRAM authentication, ACL-based authorization
- **Backup**: MirrorMaker 2 for cross-cluster replication (DR)
