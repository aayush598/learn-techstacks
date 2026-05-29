# Section 07: Media Server Integration

## Media Server Architecture

The media server is the bridge between real-time audio sources (WebRTC browsers, SIP phones) and the voice processing pipeline. It handles audio routing, transcoding, recording, and mixing. We use Janus or Mediasoup as the core media engine.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      MEDIA SERVER ARCHITECTURE                         │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     MEDIA SERVER (Janus/Mediasoup)               │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │                    WORKER PROCESSES                       │   │    │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │    │
│  │  │  │ Worker 1 │  │ Worker 2 │  │ Worker 3 │  │ Worker N │  │   │    │
│  │  │  │(500 calls)│  │(500 calls)│  │(500 calls)│  │(500 calls)│  │   │    │
│  │  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │   │    │
│  │  └───────┼──────────────┼──────────────┼──────────────┼───────┘   │    │
│  └──────────┼──────────────┼──────────────┼──────────────┼───────────┘    │
│             │              │              │              │                │
│  ┌──────────┴──────────────┴──────────────┴──────────────┴───────────┐    │
│  │                      AUDIO PIPELINE                                │    │
│  │                                                                     │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │    │
│  │  │  Audio   │  │  Codec   │  │  Audio   │  │  Gain    │           │    │
│  │  │  Input   │──▶  Decode  │──▶  Filter  │──▶  Control │           │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │    │
│  │                                                                     │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │    │
│  │  │  Audio   │  │  VAD     │  │  Echo    │  │  Noise   │           │    │
│  │  │  Mixer   │  │  Detect  │  │  Cancel  │  │  Suppress│           │    │
│  │  └────┬─────┘  └──────────┘  └──────────┘  └──────────┘           │    │
│  │       │                                                            │    │
│  │  ┌────┴─────┐  ┌──────────┐  ┌──────────┐                         │    │
│  │  │ Codec    │  │ Recording│  │  Output  │                         │    │
│  │  │ Encode   │  │  Manager │  │  Stream  │                         │    │
│  │  └──────────┘  └──────────┘  └──────────┘                         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    GATEWAYS & PROTOCOLS                             │    │
│  │                                                                      │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │    │
│  │  │  WebRTC  │  │   SIP    │  │   RTMP   │  │  File    │            │    │
│  │  │  Gateway │  │  Gateway │  │  Gateway │  │  Playback│            │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Mediasoup Integration

```typescript
// server/media/mediasoup-server.ts
import * as mediasoup from 'mediasoup'
import { Worker, Router, WebRtcTransport, Producer, Consumer } from 'mediasoup/node/lib/types'
import { EventEmitter } from 'events'
import { logger } from '@/lib/logger'

interface MediaServerConfig {
  numWorkers: number
  rtcMinPort: number
  rtcMaxPort: number
  listenIp: string
  announcedIp: string
}

export class MediasoupServer extends EventEmitter {
  private workers: Worker[] = []
  private routers: Map<string, Router> = new Map()
  private sessions: Map<string, MediaSession> = new Map()

  async initialize(config: MediaServerConfig) {
    for (let i = 0; i < config.numWorkers; i++) {
      const worker = await mediasoup.createWorker({
        logLevel: 'warn',
        logTags: ['info', 'ice', 'dtls', 'rtp', 'srtp'],
        rtcMinPort: config.rtcMinPort + (i * 10000),
        rtcMaxPort: config.rtcMaxPort + (i * 10000)
      })

      worker.on('died', () => {
        logger.error({ workerId: worker.pid }, 'Media worker died')
        this.emit('worker.died', worker.pid)
      })

      this.workers.push(worker)
      logger.info({ workerId: worker.pid }, 'Media worker created')
    }
  }

  async createRouter(roomId: string): Promise<Router> {
    // Round-robin worker selection
    const worker = this.workers[this.routers.size % this.workers.length]

    const router = await worker.createRouter({
      mediaCodecs: [
        {
          kind: 'audio',
          mimeType: 'audio/opus',
          clockRate: 48000,
          channels: 2,
          parameters: {
            useinbandfec: 1
          }
        },
        {
          kind: 'audio',
          mimeType: 'audio/PCMU',
          clockRate: 8000,
          channels: 1
        },
        {
          kind: 'audio',
          mimeType: 'audio/PCMA',
          clockRate: 8000,
          channels: 1
        },
        {
          kind: 'audio',
          mimeType: 'audio/G722',
          clockRate: 16000,
          channels: 1
        }
      ]
    })

    this.routers.set(roomId, router)
    return router
  }

  async createSession(callId: string, direction: 'incoming' | 'outgoing'): Promise<MediaSession> {
    const router = await this.getOrCreateRouter(callId)

    // Create WebRTC transport
    const transport = await router.createWebRtcTransport({
      listenIps: [
        {
          ip: process.env.MEDIASOUP_LISTEN_IP ?? '0.0.0.0',
          announcedIp: process.env.MEDIASOUP_ANNOUNCED_IP
        }
      ],
      enableUdp: true,
      enableTcp: true,
      preferUdp: true,
      initialAvailableOutgoingBitrate: 128000,
      maxSctpMessageSize: 262144,
      // Data channel for stats
      enableSctp: true,
      numSctpStreams: { OS: 16, MIS: 2048 }
    })

    const session: MediaSession = {
      callId,
      router,
      transport,
      producer: null,
      consumer: null,
      state: 'new',
      createdAt: new Date(),
      metrics: {
        bytesReceived: 0,
        bytesSent: 0,
        packetsLost: 0,
        jitter: 0,
        roundTripTime: 0
      }
    }

    // Transport event handlers
    transport.on('icestatechange', (iceState) => {
      session.state = iceState
      this.emit('transport.ice', { callId, iceState })
    })

    transport.on('dtlsstatechange', (dtlsState) => {
      this.emit('transport.dtls', { callId, dtlsState })
    })

    // Periodic stats collection
    const statsInterval = setInterval(async () => {
      try {
        const stats = await transport.getStats()
        for (const stat of Array.from(stats.values())) {
          if (stat.type === 'inbound-rtp') {
            session.metrics.bytesReceived += (stat as any).bytesReceived ?? 0
            session.metrics.packetsLost = (stat as any).packetsLost ?? 0
            session.metrics.jitter = (stat as any).jitter ?? 0
          }
          if (stat.type === 'outbound-rtp') {
            session.metrics.bytesSent += (stat as any).bytesSent ?? 0
            session.metrics.roundTripTime = (stat as any).roundTripTime ?? 0
          }
        }
      } catch {
        clearInterval(statsInterval)
      }
    }, 5000)

    this.sessions.set(callId, session)

    return session
  }

  async connectProducer(callId: string, kind: 'audio') {
    const session = this.sessions.get(callId)
    if (!session) throw new Error('Session not found')

    const producer = await session.transport.produce({
      kind,
      rtpParameters: await this.createProducerRtpParameters(session.router)
    })

    session.producer = producer

    producer.on('transportclose', () => {
      session.producer = null
    })

    return producer
  }

  async connectConsumer(
    callId: string,
    producerId: string,
    rtpCapabilities: any
  ) {
    const session = this.sessions.get(callId)
    if (!session) throw new Error('Session not found')

    if (!session.router.canConsume({ producerId, rtpCapabilities })) {
      throw new Error('Cannot consume producer')
    }

    const consumer = await session.transport.consume({
      producerId,
      rtpCapabilities,
      paused: false
    })

    session.consumer = consumer

    consumer.on('transportclose', () => {
      session.consumer = null
    })

    return consumer
  }

  async destroySession(callId: string) {
    const session = this.sessions.get(callId)
    if (!session) return

    if (session.producer) await session.producer.close()
    if (session.consumer) await session.consumer.close()
    await session.transport.close()

    this.sessions.delete(callId)
    logger.info({ callId }, 'Media session destroyed')
  }

  private async getOrCreateRouter(callId: string): Promise<Router> {
    // Use same router for related calls (e.g., transfer)
    const roomId = callId.split('-')[0] // Simplified grouping
    let router = this.routers.get(roomId)
    if (!router) {
      router = await this.createRouter(roomId)
    }
    return router
  }

  private async createProducerRtpParameters(router: Router) {
    // Get router RTP capabilities
    const rtpCapabilities = router.rtpCapabilities

    // Find Opus codec
    const opusCodec = rtpCapabilities.codecs.find(
      c => c.mimeType.toLowerCase() === 'audio/opus'
    )

    if (!opusCodec) {
      throw new Error('Opus codec not available')
    }

    return {
      codecs: [opusCodec],
      headerExtensions: [],
      encodings: [{ maxBitrate: 128000 }],
      rtcp: { reducedSize: true }
    }
  }

  getMetrics() {
    return {
      totalWorkers: this.workers.length,
      activeSessions: this.sessions.size,
      sessionsByState: this.getSessionsByState()
    }
  }

  private getSessionsByState() {
    const states: Record<string, number> = {}
    for (const session of this.sessions.values()) {
      states[session.state] = (states[session.state] ?? 0) + 1
    }
    return states
  }
}

interface MediaSession {
  callId: string
  router: Router
  transport: WebRtcTransport
  producer: Producer | null
  consumer: Consumer | null
  state: string
  createdAt: Date
  metrics: {
    bytesReceived: number
    bytesSent: number
    packetsLost: number
    jitter: number
    roundTripTime: number
  }
}
```

## Audio Recording

```typescript
// server/media/recording.ts
import { minio } from '@/lib/minio'
import { logger } from '@/lib/logger'

export class RecordingManager {
  private recordings: Map<string, RecordingSession> = new Map()

  async startRecording(
    callId: string,
    options: {
      format: 'wav' | 'mp3' | 'opus'
      monoAgent: boolean
      monoCaller: boolean
      stereo: boolean
    }
  ) {
    const session: RecordingSession = {
      callId,
      startTime: Date.now(),
      format: options.format,
      agentBuffer: Buffer.alloc(0),
      callerBuffer: Buffer.alloc(0),
      stereoBuffer: Buffer.alloc(0),
      chunkIndex: 0
    }

    this.recordings.set(callId, session)
    logger.info({ callId, format: options.format }, 'Recording started')

    return session
  }

  async writeAudioChunk(
    callId: string,
    source: 'agent' | 'caller',
    audioData: Buffer
  ) {
    const session = this.recordings.get(callId)
    if (!session) return

    if (source === 'agent') {
      session.agentBuffer = Buffer.concat([session.agentBuffer, audioData])
    } else {
      session.callerBuffer = Buffer.concat([session.callerBuffer, audioData])
    }

    // Flush to MinIO every 10 seconds
    if (session.agentBuffer.length > 160000) { // ~10s of audio
      await this.flushBuffer(callId, session)
    }
  }

  private async flushBuffer(callId: string, session: RecordingSession) {
    const timestamp = Date.now()
    const tenantId = await this.getTenantId(callId)

    if (session.agentBuffer.length > 0) {
      const key = `recordings/${tenantId}/${callId}/agent_${session.chunkIndex}.${session.format}`
      await minio.putObject('call-recordings', key, session.agentBuffer)
      session.agentBuffer = Buffer.alloc(0)
    }

    if (session.callerBuffer.length > 0) {
      const key = `recordings/${tenantId}/${callId}/caller_${session.chunkIndex}.${session.format}`
      await minio.putObject('call-recordings', key, session.callerBuffer)
      session.callerBuffer = Buffer.alloc(0)
    }

    session.chunkIndex++
  }

  async stopRecording(callId: string): Promise<RecordingResult> {
    const session = this.recordings.get(callId)
    if (!session) throw new Error('Recording not found')

    await this.flushBuffer(callId, session)
    this.recordings.delete(callId)

    const duration = Math.floor((Date.now() - session.startTime) / 1000)

    logger.info({ callId, duration }, 'Recording completed')

    return {
      callId,
      duration,
      format: session.format,
      chunkCount: session.chunkIndex
    }
  }

  private async getTenantId(callId: string): Promise<string> {
    // Lookup from call service
    const response = await fetch(
      `${process.env.CALL_SERVICE_URL}/calls/${callId}/tenant`,
      { headers: { 'Authorization': `Bearer ${process.env.INTERNAL_API_KEY}` } }
    )
    const data = await response.json()
    return data.tenantId
  }
}

interface RecordingSession {
  callId: string
  startTime: number
  format: string
  agentBuffer: Buffer
  callerBuffer: Buffer
  stereoBuffer: Buffer
  chunkIndex: number
}

interface RecordingResult {
  callId: string
  duration: number
  format: string
  chunkCount: number
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Media Engine | Mediasoup (primary), Janus (fallback) | Mediasoup: lower latency, JS-native; Janus: SIP, recording, streaming |
| Codec Priority | Opus > PCMU > PCMA | Opus best quality/bandwidth; PCMU universal compatibility |
| Recording | Server-side mixing to MinIO | Avoid client bandwidth; centralized storage |
| Audio Processing | Client-side AEC + server-side noise gate | Split processing for optimal quality |
| Worker Isolation | 500 calls per worker process | Crash isolation, predictable resource usage |

## Integration Points

- **Part 04 (Core Voice Engine)** — Audio pipeline consumes media from media server
- **Part 07 (Telephony)** — SIP gateway integrates with media server
- **Part 12 (Recording)** — Recording manager stores to MinIO
- **Part 14 (Multi-Tenant)** — Per-tenant media server isolation for enterprise

## Production Considerations

- **Resource Usage**: Each 100 concurrent calls: ~2 CPU cores, 4GB RAM, 100Mbps bandwidth
- **GPU Offloading**: Whisper STT can run on GPU (NVIDIA T4) for lower latency
- **Port Range**: Open 40000-50000 UDP in security groups for media traffic
- **Monitoring**: Track packet loss, jitter, round-trip time, MOS score per call
- **Scaling**: Auto-scale media workers based on active call count (target 70% CPU utilization)
- **Redundancy**: Active-passive media server pair; failover in <5 seconds
