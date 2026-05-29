# Section 04: Kafka Local Setup

## Overview

Apache Kafka serves as the event backbone for the voice agent platform, handling call lifecycle events, transcription streaming, and inter-service communication. Using KRaft mode eliminates the Zookeeper dependency, simplifying the local setup while maintaining production-like behavior.

## KRaft Mode Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              Kafka KRaft Mode Architecture                    │
│                                                              │
│  Traditional Kafka (with Zookeeper):                        │
│  ┌──────────┐          ┌──────────────────────────────┐     │
│  │ Zookeeper │◄────────│  Kafka Broker                 │     │
│  │ :2181     │          │  :9092                       │     │
│  └──────────┘          └──────────────────────────────┘     │
│                                                              │
│  KRaft Mode (our setup):                                    │
│  ┌──────────────────────────────────────────────┐           │
│  │  Kafka Broker + Controller                    │           │
│  │  :9092 (client) :9093 (controller)            │           │
│  │                                               │           │
│  │  Self-managed metadata via Raft consensus     │           │
│  └──────────────────────────────────────────────┘           │
│                                                              │
│  Benefits:                                                   │
│  - One less service to manage                               │
│  - Simpler configuration                                     │
│  - Faster controller failover                               │
│  - No external dependency                                   │
└─────────────────────────────────────────────────────────────┘
```

## Container Configuration

```yaml
# docker/docker-compose.yml (Kafka service)
services:
  kafka:
    image: confluentinc/cp-kafka:7.6.0
    container_name: voice-agent-kafka
    restart: unless-stopped
    ports:
      - "9092:9092"
    environment:
      # KRaft mode configuration
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9093

      # Listener configuration
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,CONTROLLER:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: PLAINTEXT
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER

      # Topic defaults
      KAFKA_NUM_PARTITIONS: 3
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0

      # Log configuration
      KAFKA_LOG_DIRS: /var/lib/kafka/data
      KAFKA_LOG_RETENTION_HOURS: 168
      KAFKA_LOG_RETENTION_BYTES: 1073741824
      KAFKA_LOG_SEGMENT_BYTES: 1073741824
      KAFKA_LOG_RETENTION_CHECK_INTERVAL_MS: 300000

      # Performance
      KAFKA_NUM_NETWORK_THREADS: 3
      KAFKA_NUM_IO_THREADS: 8
      KAFKA_SOCKET_SEND_BUFFER_BYTES: 102400
      KAFKA_SOCKET_RECEIVE_BUFFER_BYTES: 102400
      KAFKA_SOCKET_REQUEST_MAX_BYTES: 104857600

      # Cluster ID (required for KRaft)
      CLUSTER_ID: "voice-agent-dev-cluster"
    volumes:
      - kafka-data:/var/lib/kafka/data
    healthcheck:
      test: ["CMD", "kafka-topics", "--bootstrap-server", "localhost:9092", "--list"]
      interval: 15s
      timeout: 10s
      retries: 10
      start_period: 30s
    networks:
      - voice-agent-dev
```

## Topic Initialization

```yaml
# docker/docker-compose.yml (Kafka init service)
services:
  kafka-init:
    image: confluentinc/cp-kafka:7.6.0
    container_name: voice-agent-kafka-init
    restart: "no"
    depends_on:
      kafka:
        condition: service_healthy
    entrypoint: ["/bin/bash", "-c"]
    command: |
      echo "Creating topics..." && \
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists \
        --topic call-events \
        --partitions 3 \
        --replication-factor 1 \
        --config cleanup.policy=delete \
        --config retention.ms=604800000 && \
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists \
        --topic transcription-results \
        --partitions 2 \
        --replication-factor 1 \
        --config cleanup.policy=delete \
        --config retention.ms=2592000000 && \
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists \
        --topic agent-events \
        --partitions 1 \
        --replication-factor 1 \
        --config cleanup.policy=compact && \
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists \
        --topic analytics-events \
        --partitions 3 \
        --replication-factor 1 \
        --config cleanup.policy=delete \
        --config retention.ms=86400000 && \
      echo "Listing topics:" && \
      kafka-topics --bootstrap-server kafka:9092 --list && \
      echo "Topics created successfully"
    networks:
      - voice-agent-dev
```

## Topic Definitions

```typescript
// packages/voice/src/events/topics.ts
export interface TopicDefinition {
  name: string;
  partitions: number;
  replicationFactor: number;
  config: Record<string, string>;
}

export const TOPICS: Record<string, TopicDefinition> = {
  CALL_EVENTS: {
    name: "call-events",
    partitions: 3,
    replicationFactor: 1,
    config: {
      "cleanup.policy": "delete",
      "retention.ms": "604800000", // 7 days
      "compression.type": "snappy",
    },
  },
  TRANSCRIPTION_RESULTS: {
    name: "transcription-results",
    partitions: 2,
    replicationFactor: 1,
    config: {
      "cleanup.policy": "delete",
      "retention.ms": "2592000000", // 30 days
      "compression.type": "snappy",
    },
  },
  AGENT_EVENTS: {
    name: "agent-events",
    partitions: 1,
    replicationFactor: 1,
    config: {
      "cleanup.policy": "compact", // Keep latest value per key
      "compression.type": "producer",
    },
  },
  ANALYTICS_EVENTS: {
    name: "analytics-events",
    partitions: 3,
    replicationFactor: 1,
    config: {
      "cleanup.policy": "delete",
      "retention.ms": "86400000", // 1 day
      "compression.type": "snappy",
    },
  },
};
```

## Producer/Consumer Implementation

```typescript
// packages/voice/src/events/kafka-client.ts
import { Kafka, type Producer, type Consumer } from "kafkajs";

const globalForKafka = globalThis as unknown as {
  kafka: Kafka | undefined;
  producer: Producer | undefined;
  consumer: Consumer | undefined;
};

function createKafkaClient(): Kafka {
  const brokers = (process.env.KAFKA_BROKERS ?? "localhost:9092").split(",");

  return new Kafka({
    clientId: process.env.KAFKA_CLIENT_ID ?? "voice-agent",
    brokers,
    retry: {
      initialRetryTime: 100,
      retries: 8,
      maxRetryTime: 30000,
    },
    connectionTimeout: 3000,
  });
}

export function getKafka(): Kafka {
  if (!globalForKafka.kafka) {
    globalForKafka.kafka = createKafkaClient();
  }
  return globalForKafka.kafka;
}

export async function getProducer(): Promise<Producer> {
  if (!globalForKafka.producer) {
    const producer = getKafka().producer({
      allowAutoTopicCreation: true,
      transactionTimeout: 30000,
    });
    await producer.connect();
    globalForKafka.producer = producer;
  }
  return globalForKafka.producer;
}

export async function getConsumer(
  groupId: string,
): Promise<Consumer> {
  const consumer = getKafka().consumer({
    groupId: groupId,
    sessionTimeout: 30000,
    rebalanceTimeout: 60000,
    heartbeatInterval: 3000,
    maxBytesPerPartition: 1048576,
  });
  await consumer.connect();
  return consumer;
}
```

### Publishing Events

```typescript
// packages/voice/src/events/publisher.ts
import { getProducer } from "./kafka-client";
import { TOPICS } from "./topics";

export class EventPublisher {
  async publishCallEvent(event: CallEvent): Promise<void> {
    const producer = await getProducer();
    await producer.send({
      topic: TOPICS.CALL_EVENTS.name,
      messages: [
        {
          key: event.callId,
          value: JSON.stringify(event),
          headers: {
            "event-type": event.type,
            "source": "voice-agent",
            "timestamp": Date.now().toString(),
          },
        },
      ],
    });
  }

  async publishTranscription(
    callId: string,
    segment: TranscriptionSegment,
  ): Promise<void> {
    const producer = await getProducer();
    await producer.send({
      topic: TOPICS.TRANSCRIPTION_RESULTS.name,
      messages: [
        {
          key: callId,
          value: JSON.stringify(segment),
          partition: this.getPartition(callId, 2),
        },
      ],
    });
  }

  private getPartition(key: string, numPartitions: number): number {
    let hash = 0;
    for (let i = 0; i < key.length; i++) {
      hash = ((hash << 5) - hash + key.charCodeAt(i)) | 0;
    }
    return Math.abs(hash) % numPartitions;
  }
}
```

### Consuming Events

```typescript
// packages/voice/src/events/consumer.ts
import { getConsumer } from "./kafka-client";
import { TOPICS } from "./topics";

export class CallEventConsumer {
  private consumer;

  constructor(groupId: string) {
    this.consumer = null!;
  }

  async start(handler: (event: CallEvent) => Promise<void>): Promise<void> {
    this.consumer = await getConsumer("call-processor");
    await this.consumer.subscribe({
      topic: TOPICS.CALL_EVENTS.name,
      fromBeginning: false,
    });

    await this.consumer.run({
      autoCommit: true,
      autoCommitInterval: 5000,
      autoCommitThreshold: 100,
      eachMessage: async ({ topic, partition, message }) => {
        try {
          const event = JSON.parse(message.value!.toString()) as CallEvent;
          await handler(event);
        } catch (error) {
          console.error(`Failed to process message from ${topic}:`, error);
          // Dead letter queue would go here
        }
      },
    });
  }

  async stop(): Promise<void> {
    await this.consumer.disconnect();
  }
}
```

## Design Decisions

### KRaft (no Zookeeper) vs. Traditional

**Decision**: Use KRaft mode.

**Rationale**: Zookeeper adds operational complexity, consumes resources, and is one more service that can fail. KRaft mode has been production-ready since Kafka 3.5 (Confluent 7.6). For a development setup, it reduces the Compose file from 3 services to 2.

### Partition count

- **call-events**: 3 partitions (scales to 3 consumers)
- **transcription-results**: 2 partitions (less throughput)
- **agent-events**: 1 partition (ordered processing required)
- **analytics-events**: 3 partitions (higher throughput)

Partition count should be a multiple of the expected consumer count. More partitions = more parallelism but more overhead.

### Compression

Snappy compression for high-throughput topics reduces network bandwidth by ~40-60% with minimal CPU overhead. The `agent-events` topic uses producer compression for lower latency.

## Integration Points

- **kafkajs**: Node.js client library
- **Event Publisher**: Used by call processing pipeline
- **Event Consumer**: Used by transcription service, analytics service
- **Monitoring**: Kafka exposes JMX metrics for monitoring

## Production Considerations

1. **Replication factor**: Development uses RF=1 (single broker). Production requires RF=3 with at least 3 brokers
2. **Data retention**: Configure retention based on consumer lag tolerance. 7 days for call events (consumers process within minutes), 30 days for transcripts (used for training)
3. **Consumer groups**: Each consumer service needs a unique group ID. The offset is stored in Kafka, so restarts resume from the last committed offset
4. **Dead letter queue**: Failed messages should be published to a dead letter topic for manual inspection. Implement in the consumer's error handler
5. **Monitoring**: Use Kafka's built-in metrics or export to Prometheus via JMX exporter. Track consumer lag, request rates, and disk usage
