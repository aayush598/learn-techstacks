# Section 08: Latency & Performance Targets

## Performance Budget

The real-time communication layer must meet strict latency targets to provide a natural conversational experience. Users perceive delays >500ms as unnatural, and >1s as broken. Every component in the pipeline is measured against these targets.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    END-TO-END LATENCY BUDGET                          │
│                                                                         │
│  Total Budget: <800ms (from user speech to agent response)            │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  COMPONENT          │ TARGET   │ P95      │ P99     │ ALLOWED  │    │
│  │─────────────────────┼──────────┼──────────┼─────────┼──────────┤    │
│  │ Audio Capture       │ <10ms    │ <20ms    │ <50ms   │ 10ms     │    │
│  │ Network Transport   │ <30ms    │ <80ms    │ <150ms  │ 30ms     │    │
│  │ VAD Detection       │ <20ms    │ <30ms    │ <50ms   │ 20ms     │    │
│  │ STT (Speech-to-Text)│ <300ms   │ <500ms   │ <1s     │ 250ms    │    │
│  │ AI Processing       │ <300ms   │ <500ms   │ <2s     │ 250ms    │    │
│  │ TTS (Text-to-Speech)│ <200ms   │ <300ms   │ <500ms  │ 150ms    │    │
│  │ Audio Output        │ <10ms    │ <20ms    │ <50ms   │ 10ms     │    │
│  │─────────────────────┼──────────┼──────────┼─────────┼──────────┤    │
│  │ TOTAL (Synchronous) │ <870ms   │ <1.45s   │ <2.8s   │ 720ms    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  Visual representation of latency:                                     │
│                                                                         │
│  User speaks: │░░░░░░░░░░░░░░░░░░░░│                                    │
│               │  VAD   │  STT   │  AI    │  TTS    │                   │
│               │ 20ms   │ 250ms  │ 250ms  │ 150ms   │                   │
│               │        │        │        │         │                   │
│  Response:    │░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│                  │
│               │        │        │        │         │                   │
│  Total:       │              ~670ms              │                     │
│                                                                         │
│  Key targets:                                                          │
│  • First audio in:  <300ms  (time from call answer to first greeting) │
│  • First response:  <1s     (time from user speech to AI response)    │
│  • Subsequent:      <500ms  (turn-taking latency)                      │
│  • Barge-in:        <200ms  (interruption detection)                  │
│  • Reconnection:    <3s     (WebSocket reconnect)                     │
└─────────────────────────────────────────────────────────────────────────┘
```

## Measuring Latency

```typescript
// lib/telemetry/latency-tracking.ts
import { trace, context, Span } from '@opentelemetry/api'
import { Histogram, Counter } from 'prom-client'

interface LatencyPoint {
  component: string
  operation: string
  startTime: number
  endTime?: number
  durationMs?: number
  metadata?: Record<string, unknown>
}

export class LatencyTracker {
  private points: Map<string, LatencyPoint> = new Map()
  private callId: string

  // Prometheus metrics
  private componentLatency: Histogram
  private endToEndLatency: Histogram
  private latencyBudgetExceeded: Counter

  constructor(callId: string) {
    this.callId = callId
    const tracer = trace.getTracer('voice-pipeline')

    this.componentLatency = new Histogram({
      name: 'voice_component_latency_ms',
      help: 'Latency per voice processing component',
      labelNames: ['component', 'operation'],
      buckets: [10, 25, 50, 100, 200, 300, 500, 1000, 2000]
    })

    this.endToEndLatency = new Histogram({
      name: 'voice_end_to_end_latency_ms',
      help: 'End-to-end latency from user speech end to response start',
      buckets: [200, 400, 600, 800, 1000, 1500, 2000, 3000]
    })

    this.latencyBudgetExceeded = new Counter({
      name: 'voice_latency_budget_exceeded_total',
      help: 'Count of times latency budget was exceeded',
      labelNames: ['component']
    })
  }

  startSpan(component: string, operation: string): string {
    const id = `${component}:${operation}:${Date.now()}`
    this.points.set(id, {
      component,
      operation,
      startTime: performance.now()
    })
    return id
  }

  endSpan(id: string, metadata?: Record<string, unknown>) {
    const point = this.points.get(id)
    if (!point) return

    point.endTime = performance.now()
    point.durationMs = point.endTime - point.startTime
    point.metadata = metadata

    // Record in Prometheus
    this.componentLatency.observe(
      { component: point.component, operation: point.operation },
      point.durationMs
    )

    // Check budget
    this.checkBudget(point)

    this.points.delete(id)
  }

  private checkBudget(point: LatencyPoint) {
    const budgets: Record<string, number> = {
      'vad': 20,
      'stt': 300,
      'ai': 300,
      'tts': 200,
      'network': 30,
      'audio_capture': 10,
      'audio_output': 10,
      'media_server': 50
    }

    const budget = budgets[point.component]
    if (budget && point.durationMs! > budget) {
      this.latencyBudgetExceeded.inc({ component: point.component })
      console.warn(
        `[LATENCY] ${point.component}.${point.operation} took ${point.durationMs}ms ` +
        `(budget: ${budget}ms) for call ${this.callId}`
      )
    }
  }

  recordEndToEnd(startTime: number) {
    const duration = performance.now() - startTime
    this.endToEndLatency.observe(duration)
  }

  getCurrentLatencies(): Record<string, number> {
    const result: Record<string, number> = {}
    for (const [id, point] of this.points) {
      if (point.durationMs !== undefined) {
        result[id] = point.durationMs
      }
    }
    return result
  }
}
```

## WebSocket Performance

```typescript
// server/websocket/performance.ts
// WebSocket-specific performance monitoring

import prometheus from 'prom-client'

export const wsPerformance = {
  connectionTime: new Histogram({
    name: 'ws_connection_time_ms',
    help: 'Time to establish WebSocket connection',
    buckets: [50, 100, 200, 500, 1000, 2000, 5000]
  }),

  messageLatency: new Histogram({
    name: 'ws_message_latency_ms',
    help: 'End-to-end message delivery latency',
    labelNames: ['event_type'],
    buckets: [5, 10, 25, 50, 100, 250, 500]
  }),

  messageSize: new Histogram({
    name: 'ws_message_size_bytes',
    help: 'WebSocket message size distribution',
    buckets: [64, 256, 1024, 4096, 16384, 65536]
  }),

  roomsPerConnection: new Gauge({
    name: 'ws_rooms_per_connection',
    help: 'Number of rooms per connection',
    labelNames: ['percentile']
  }),

  reconnectionTime: new Histogram({
    name: 'ws_reconnection_time_ms',
    help: 'Time to complete WebSocket reconnection',
    buckets: [100, 500, 1000, 2000, 5000, 10000]
  }),

  eventsPerSecond: new Gauge({
    name: 'ws_events_per_second',
    help: 'Events emitted per second',
    labelNames: ['node_id']
  })
}

// Track message delivery latency
function measureMessageLatency(io: Server) {
  io.on('connection', (socket) => {
    // Client sends ping, server responds with pong and measures
    socket.on('latency:ping', (timestamp: number) => {
      const latency = Date.now() - timestamp
      wsPerformance.messageLatency.observe(
        { event_type: 'latency_check' },
        latency
      )
      socket.emit('latency:pong', { timestamp, serverTime: Date.now(), latency })
    })
  })
}
```

## Audio Quality Metrics

```typescript
// server/media/quality-metrics.ts
// Audio quality monitoring for WebRTC/SIP calls

interface AudioQualityReport {
  callId: string
  mos: number              // Mean Opinion Score (1-5)
  rFactor: number          // Transmission rating factor (0-100)
  jitterMs: number         // Jitter in milliseconds
  packetLossPercent: number // Packet loss percentage
  roundTripTimeMs: number  // Round-trip time
  codec: string
  sampleRate: number
  concealRatio: number     // PLC conceal ratio
}

export function calculateMOS(metrics: {
  rtt: number
  jitter: number
  packetLoss: number
  codec: string
}): number {
  // ITU-T G.107 E-model for MOS calculation
  const codecFactors: Record<string, number> = {
    'opus': 4.4,
    'PCMU': 4.1,
    'PCMA': 4.1,
    'G722': 4.0,
    'G729': 3.9
  }

  const baseMos = codecFactors[metrics.codec] ?? 4.0

  // Deductions
  const rttDeduction = Math.min(metrics.rtt / 1000, 1.0) * 0.5
  const jitterDeduction = Math.min(metrics.jitter / 50, 1.0) * 0.3
  const packetLossDeduction = metrics.packetLoss * 0.1

  const mos = baseMos - rttDeduction - jitterDeduction - packetLossDeduction
  return Math.max(1.0, Math.min(5.0, mos))
}

// Prometheus metrics
const audioQualityMetrics = {
  mos: new Gauge({
    name: 'audio_mos_score',
    help: 'Mean Opinion Score per call',
    labelNames: ['codec']
  }),

  jitter: new Histogram({
    name: 'audio_jitter_ms',
    help: 'Audio jitter in milliseconds',
    buckets: [5, 10, 20, 30, 50, 100, 200]
  }),

  packetLoss: new Histogram({
    name: 'audio_packet_loss_percent',
    help: 'Audio packet loss percentage',
    buckets: [0.1, 0.5, 1, 2, 5, 10, 20]
  }),

  concealedSeconds: new Counter({
    name: 'audio_concealed_seconds_total',
    help: 'Total seconds of audio concealment',
    labelNames: ['call_id']
  })
}
```

## Performance Optimization Techniques

### 1. Audio Buffer Optimization

```typescript
// server/media/buffer-optimization.ts

// Adaptive jitter buffer
class AdaptiveJitterBuffer {
  private buffer: Buffer[] = []
  private targetLatency = 50  // ms
  private currentLatency = 0

  push(packet: Buffer, timestamp: number) {
    // Adaptive delay based on network conditions
    const jitter = this.calculateJitter(timestamp)
    const delay = Math.max(0, this.targetLatency - jitter)

    setTimeout(() => {
      this.buffer.push(packet)
    }, delay)
  }

  private calculateJitter(timestamp: number): number {
    // Smoothed jitter calculation using moving average
    return this.currentLatency * 0.7 + Math.abs(timestamp - Date.now()) * 0.3
  }
}
```

### 2. Opus Encoding Optimization

```typescript
// Opus encoder with application-specific tuning
const encoderConfig = {
  // Voice conversation optimization
  application: 'voip',          // Optimized for voice
  frameSize: 20,               // 20ms frames (standard)
  bitrate: 'auto',              // Adaptive bitrate (16-48kbps)
  fec: true,                    // Forward error correction
  dtx: true,                    // Discontinuous transmission (silence suppression)
  complexity: 5,                // Encoder complexity (0-10, 5 is good balance)
  packetLossPercentage: 15     // Expected packet loss for FEC tuning
}
```

### 3. Stream Prioritization

```typescript
// In calls with multiple streams (transcript, sentiment, etc.)
// Prioritize audio data over metadata

enum StreamPriority {
  CRITICAL = 0,  // Audio packets — never delay
  HIGH = 1,      // Transcript chunks — low delay
  MEDIUM = 2,    // Sentiment updates
  LOW = 3        // Analytics, logging
}

interface PrioritizedPacket {
  priority: StreamPriority
  data: Buffer
  timestamp: number
}
```

## Performance Testing

```typescript
// tests/performance/latency.test.ts
import { describe, it, expect } from 'vitest'

describe('Real-time Latency', () => {
  it('should establish WebSocket connection under 200ms', async () => {
    const start = Date.now()
    const socket = io(WS_URL, { auth: { token: TEST_TOKEN } })
    await new Promise<void>((resolve) => socket.on('connect', resolve))
    const latency = Date.now() - start
    expect(latency).toBeLessThan(200)
    socket.close()
  })

  it('should deliver messages under 50ms', async () => {
    const socket1 = io(WS_URL, { auth: { token: TEST_TOKEN } })
    const socket2 = io(WS_URL, { auth: { token: TEST_TOKEN } })

    await Promise.all([
      new Promise(r => socket1.on('connect', r)),
      new Promise(r => socket2.on('connect', r))
    ])

    const room = `test:${Date.now()}`
    socket1.emit('subscribe', room)

    const start = Date.now()
    socket2.emit('message', { room, data: 'test' })

    await new Promise<void>((resolve) => {
      socket1.on('message', () => {
        const latency = Date.now() - start
        expect(latency).toBeLessThan(50)
        resolve()
      })
    })

    socket1.close()
    socket2.close()
  })
})
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Latency Budget | 800ms end-to-end | Industry standard for natural conversation |
| Measurement | OpenTelemetry + Prometheus | Consistent observability across services |
| Jitter Buffer | Adaptive (not fixed) | Adjusts to network conditions |
| Codec | Opus (VoIP profile) | Best quality at low bitrate |
| FEC | Enabled for audio | Recovers ~15% packet loss without retransmission |

## Integration Points

- **Part 24 (Scaling)** — Latency targets drive auto-scaling decisions
- **Part 04 (Core Voice Engine)** — Voice pipeline must meet per-component budgets
- **Part 23 (DevOps)** — Monitoring dashboards track these metrics

## Production Considerations

- **Latency Alerts**: P95 latency exceeds 2x budget → critical alert
- **Geographic Distribution**: Deploy media servers close to users (<100ms RTT)
- **Packet Loss Mitigation**: FEC for <15% loss; PLC for >15% loss; TURN relay for high loss
- **Codec Negotiation**: Always try Opus first; downgrade to PCMU for legacy systems
- **Load Shedding**: If CPU >80%, stop non-critical processing (analytics, sentiment) before audio
- **Capacity Planning**: 10K concurrent calls requires ~40 CPU cores, 80GB RAM, 10Gbps bandwidth
