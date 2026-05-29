# Section 02: Service Communication Patterns

## Communication Protocol Map

Microservices communicate through four primary protocols, each suited to different interaction patterns. The choice depends on latency requirements, consistency needs, and coupling tolerance.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SERVICE COMMUNICATION PATTERNS                      │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  PROTOCOL │ USE CASE            │ LATENCY │ COUPLING │ RELIABIL│    │
│  │───────────┼─────────────────────┼─────────┼──────────┼─────────┤    │
│  │  REST     │ CRUD operations     │ <100ms  │ Tight    │ At-most │    │
│  │  gRPC     │ High-throughput IPC  │ <10ms   │ Tight    │ At-most │    │
│  │  Kafka    │ Async events        │ <100ms  │ Loose    │ At-least│    │
│  │  WS       │ Real-time data      │ <50ms   │ None     │ Best-eff│    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      INTERACTION PATTERNS                       │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  Synchronous (Request-Response)                          │   │    │
│  │  │                                                          │   │    │
│  │  │  Service A ──request──▶ Service B                        │   │    │
│  │  │  Service A ◀──response── Service B                       │   │    │
│  │  │                                                          │   │    │
│  │  │  Used for: queries, commands that need immediate result  │   │    │
│  │  │  Protocols: REST (HTTP/2), gRPC (HTTP/2)                │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  Asynchronous (Event-Driven)                            │   │    │
│  │  │                                                          │   │    │
│  │  │  Service A ──publish(event)──▶ Kafka ──consume──▶ Serv. B│    │    │
│  │  │  Service A ──publish(event)──▶ Kafka ──consume──▶ Serv. C│    │    │
│  │  │                                                          │   │    │
│  │  │  Used for: state changes, notifications, workflows      │   │    │
│  │  │  Protocols: Kafka (Avro/Protobuf)                       │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  Streaming (Real-Time)                                  │   │    │
│  │  │                                                          │   │    │
│  │  │  Service A ◀══════ stream ═══════▶ Service B            │   │    │
│  │  │                                                          │   │    │
│  │  │  Used for: audio, transcript, real-time events          │   │    │
│  │  │  Protocols: WebSocket, gRPC streaming, Kafka streams    │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## REST Communication

```typescript
// Agent Service REST API — example endpoints
// Synchronous CRUD operations

// Agent Service listens on port 3001
// GET /api/v1/agents — List agents
// POST /api/v1/agents — Create agent
// GET /api/v1/agents/:id — Get agent by ID
// PATCH /api/v1/agents/:id — Update agent
// DELETE /api/v1/agents/:id — Delete agent

// Call Service → Agent Service (REST)
// When Call Service needs agent config synchronously:

export class AgentServiceClient {
  private baseUrl = process.env.AGENT_SERVICE_URL!
  private timeout = 5000

  async getAgentConfig(agentId: string): Promise<AgentConfig> {
    const response = await fetch(`${this.baseUrl}/api/v1/agents/${agentId}/config`, {
      headers: {
        'Authorization': `Bearer ${this.getServiceToken()}`,
        'X-Request-Id': crypto.randomUUID()
      },
      signal: AbortSignal.timeout(this.timeout)
    })

    if (!response.ok) {
      throw new AgentServiceError(response.status, await response.text())
    }

    return response.json()
  }

  private async getServiceToken(): Promise<string> {
    // Service-to-service JWT with short expiry (5 min)
    const token = await this.tokenCache.get('agent-service-token')
    if (token) return token

    const newToken = await generateServiceToken({
      service: 'call-service',
      audience: 'agent-service',
      expiresIn: '5m'
    })

    await this.tokenCache.set('agent-service-token', newToken, { ttl: 240 })
    return newToken
  }
}
```

## gRPC Communication

```typescript
// gRPC for high-throughput internal communication
// Particularly used for the voice pipeline (STT/TTS streaming)

// Proto definition: voice.proto
syntax = "proto3";

service VoiceService {
  // Unary
  rpc SynthesizeSpeech (TTSRequest) returns (TTSResponse);
  rpc TranscribeAudio (STTRequest) returns (STTResponse);

  // Server-side streaming
  rpc StreamingSTT (stream AudioChunk) returns (stream STTResult);

  // Client-side streaming
  rpc StreamingTTS (stream TTSInput) returns (stream AudioChunk);

  // Bidirectional streaming
  rpc VoiceConversation (stream CallAudio) returns (stream AgentAudio);
}

message AudioChunk {
  string session_id = 1;
  bytes audio_data = 2;
  uint32 sample_rate = 3;
  uint64 timestamp = 4;
  bool is_final = 5;
}

message STTResult {
  string session_id = 1;
  string text = 2;
  float confidence = 3;
  repeated WordTiming words = 4;
  bool is_final = 5;
  uint64 end_time = 6;
}

// gRPC client implementation
import * as grpc from '@grpc/grpc-js'
import * as protoLoader from '@grpc/proto-loader'

const packageDefinition = protoLoader.loadSync('proto/voice.proto', {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
})

const voiceProto = grpc.loadPackageDefinition(packageDefinition).voice

export class VoiceServiceGrpcClient {
  private client: any

  constructor() {
    this.client = new voiceProto.VoiceService(
      process.env.VOICE_SERVICE_GRPC_URL!,
      grpc.credentials.createSsl()
    )
  }

  async transcribe(audio: AudioChunk): Promise<STTResult> {
    return new Promise((resolve, reject) => {
      this.client.TranscribeAudio(audio, (error: any, response: STTResult) => {
        if (error) reject(error)
        else resolve(response)
      })
    })
  }

  streamingSTT(): gRPCStream<AudioChunk, STTResult> {
    const call = this.client.StreamingSTT()
    return {
      write: (chunk: AudioChunk) => call.write(chunk),
      end: () => call.end(),
      onData: (callback: (data: STTResult) => void) => call.on('data', callback),
      onEnd: (callback: () => void) => call.on('end', callback),
      onError: (callback: (error: Error) => void) => call.on('error', callback)
    }
  }
}
```

## Kafka Communication

```typescript
// Kafka for async event-driven communication
// Topics organized by domain with event schemas

interface KafkaTopics {
  // Call domain events
  'call.events': {
    key: string        // call_id
    value: CallEvent
    partitions: 12
    retention: '7d'
    cleanup: 'delete'
  }

  // Agent domain events
  'agent.events': {
    key: string        // agent_id
    value: AgentEvent
    partitions: 6
    retention: '30d'
    cleanup: 'compact'  // Keep latest state per key
  }

  // Voice pipeline events
  'voice.pipeline': {
    key: string        // session_id
    value: VoicePipelineEvent
    partitions: 12
    retention: '1d'
    cleanup: 'delete'
  }

  // Billing events
  'billing.events': {
    key: string        // tenant_id
    value: BillingEvent
    partitions: 6
    retention: '90d'
    cleanup: 'delete'
  }

  // Dead letter queue
  'dlq': {
    key: string
    value: DeadLetterRecord
    partitions: 3
    retention: '30d'
    cleanup: 'delete'
  }
}

// Producer example
import { Kafka, Producer } from 'kafkajs'

export class EventProducer {
  private producer: Producer

  constructor() {
    const kafka = new Kafka({
      clientId: 'call-service',
      brokers: process.env.KAFKA_BROKERS!.split(','),
      ssl: true,
      sasl: {
        mechanism: 'scram-sha-512',
        username: process.env.KAFKA_USERNAME!,
        password: process.env.KAFKA_PASSWORD!
      },
      retry: {
        initialRetryTime: 100,
        retries: 8
      }
    })

    this.producer = kafka.producer({
      allowAutoTopicCreation: false,
      transactionTimeout: 30000
    })
  }

  async connect(): Promise<void> {
    await this.producer.connect()
  }

  async publishCallEvent(event: CallEvent): Promise<void> {
    await this.producer.send({
      topic: 'call.events',
      messages: [{
        key: event.callId,
        value: JSON.stringify(event),
        headers: {
          'event-type': event.type,
          'event-version': '1',
          'source-service': 'call-service',
          'timestamp': new Date().toISOString()
        }
      }]
    })
  }

  // Idempotent producer
  async publishWithIdempotency(event: CallEvent): Promise<void> {
    await this.producer.send({
      topic: 'call.events',
      messages: [{
        key: event.callId,
        value: JSON.stringify(event),
        // Idempotency key prevents duplicate processing
        headers: {
          'idempotency-key': `${event.callId}-${event.sequence}`,
          'event-type': event.type
        }
      }]
    })
  }
}

// Consumer example
export class CallEventConsumer {
  private consumer: any
  private handlers: Map<string, (event: CallEvent) => Promise<void>>

  constructor() {
    const kafka = new Kafka({ clientId: 'billing-service', brokers: [...] })
    this.consumer = kafka.consumer({
      groupId: 'billing-call-events',
      sessionTimeout: 30000,
      rebalanceTimeout: 60000,
      heartbeatInterval: 3000
    })
    this.handlers = new Map()
  }

  async subscribe(handler: CallEventHandler): Promise<void> {
    await this.consumer.connect()
    await this.consumer.subscribe({ topic: 'call.events', fromBeginning: false })

    await this.consumer.run({
      autoCommit: false,
      eachBatchAutoResolve: false,
      eachBatch: async ({ batch, resolveOffset, heartbeat, commitOffsetsIfNecessary }) => {
        for (const message of batch.messages) {
          try {
            const event = JSON.parse(message.value!.toString())
            const handler = this.handlers.get(event.type)
            if (handler) {
              await handler(event)
            }
            // Commit offset after successful processing
            resolveOffset(message.offset)
          } catch (error) {
            // Send to DLQ
            await this.sendToDLQ(message, error)
          }

          await heartbeat()
        }

        await commitOffsetsIfNecessary()
      }
    })
  }

  onEvent(type: string, handler: (event: CallEvent) => Promise<void>): void {
    this.handlers.set(type, handler)
  }

  private async sendToDLQ(message: any, error: unknown): Promise<void> {
    const dlqProducer = new EventProducer()
    await dlqProducer.connect()
    await dlqProducer.publish({
      topic: 'dlq',
      messages: [{
        key: message.key?.toString(),
        value: JSON.stringify({
          originalTopic: 'call.events',
          originalMessage: message.value?.toString(),
          error: (error as Error).message,
          timestamp: new Date().toISOString()
        })
      }]
    })
  }
}
```

## Communication Flow Example: Call Completion

```
                    ╔════════════════════════════════╗
                    ║     CALL COMPLETION FLOW      ║
                    ╚════════════════════════════════╝

Call Service                    Kafka                  Voice Service
    │                            │                        │
    │── call.ended ─────────────▶│                        │
    │                            │                        │
    │                            ├── call.ended ────────▶│ (Stop processing)
    │                            │                        │
    │                            ├── call.ended ────┐     │
    │                            │                  │     │
    │                            ▼                  ▼     │
    │                     Billing Service     AI Service   │
    │                            │                  │     │
    │                            │ Record usage     │     │
    │                            │ Generate cost    │     │
    │                            │<─────────────────│─────│── Save summary
    │                            │                  │     │
    │◀───────────────────────────│──────────────────│─────│── Recording done
    │                            │                  │     │
    │                            │                  │     │
    │── call.completed ─────────▶│ (Notify WebSocket)      │
    │                            │                        │
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Sync Protocol | REST for external, gRPC for internal | REST: universal; gRPC: high-performance IPC |
| Async Protocol | Kafka (not RabbitMQ) | Durability, replay, partitioning at scale |
| Data Format | JSON for REST, Protobuf for gRPC/Kafka | JSON: developer-friendly; Protobuf: compact, typed |
| Service Auth | mTLS + short-lived JWT | Defense in depth: transport + application layer |
| Error Handling | Retry with backoff → DLQ | Reliable processing, observability of failures |
| Idempotency | Idempotency keys on Kafka messages | Exactly-once semantics for critical events |

## Integration Points

- **Part 05 (Microservices)** — Communication patterns used across all services
- **Part 09 (Data Flow)** — Event-driven architecture built on Kafka
- **Part 04 (Real-Time)** — WebSocket streams events to frontend
- **Part 15 (Security)** — Service-to-service authentication with mTLS

## Production Considerations

- **gRPC Performance**: ~10x faster than REST for serialization + smaller payloads
- **Kafka Throughput**: Single partition handles ~1MB/s; scale partitions for higher
- **Retry Budget**: Max 3 retries with exponential backoff (100ms, 500ms, 2.5s)
- **Timeout Hierarchy**: REST: 5s, gRPC: 2s, Kafka: no timeout (async)
- **Rate Limiting**: Inter-service API calls rate-limited at 1000 req/s per service
- **Circuit Breaking**: After 5 failures in 30s, circuit opens for 60s (half-open after 30s)
