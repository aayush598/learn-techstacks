# Section 03: WebRTC Signaling Server

## Signaling Architecture

WebRTC signaling establishes peer-to-peer audio connections between browsers and the media server. The signaling server coordinates the exchange of Session Description Protocol (SDP) offers/answers and ICE candidates needed to establish a direct media path.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      WEBRTC SIGNALING FLOW                            │
│                                                                         │
│  ┌──────────┐                    ┌──────────┐                    ┌────┐ │
│  │  Browser │                    │Signaling │                    │Media│ │
│  │  Client  │                    │  Server  │                    │Srvr │ │
│  └────┬─────┘                    └────┬─────┘                    └──┬──┘ │
│       │                               │                             │    │
│       │  1. Create Offer (SDP)        │                             │    │
│       │──────────────────────────────>│                             │    │
│       │                               │  2. Forward Offer           │    │
│       │                               │────────────────────────────>│    │
│       │                               │                             │    │
│       │                               │  3. Create Answer (SDP)     │    │
│       │                               │<────────────────────────────│    │
│       │  4. Receive Answer            │                             │    │
│       │<──────────────────────────────│                             │    │
│       │                               │                             │    │
│       │  5. ICE Candidates (repeat)   │                             │    │
│       │══════════════════════════════>│════════════════════════════>│    │
│       │<══════════════════════════════│<════════════════════════════│    │
│       │                               │                             │    │
│       │  6. Direct P2P Connection     │                             │    │
│       │═════════════════════════════════════════════════════════════>│    │
│       │  (SRTP/SCTP encrypted audio)  │                             │    │
│       │<═════════════════════════════════════════════════════════════│    │
│       │                               │                             │    │
│       │  7. Connection Established    │                             │    │
│       │  ICE State: connected         │                             │    │
│       │  DTLS State: connected        │                             │    │
│       │                               │                             │    │
│       │  8. Call Ended                │                             │    │
│       │──────────────────────────────>│────────────────────────────>│    │
│       │                               │                             │    │
└───────┴───────────────────────────────┴─────────────────────────────┴────┘
```

## Signaling Server Implementation

```typescript
// server/webrtc/signaling.ts
import { Server as SocketIOServer } from 'socket.io'
import { MediaServer } from './media-server'
import { STUN_SERVERS, TURN_SERVERS } from './ice-config'
import { logger } from '@/lib/logger'

interface PeerConnection {
  callId: string
  userId: string
  peerId: string  // Media server session ID
  iceState: 'new' | 'checking' | 'connected' | 'completed' | 'failed' | 'disconnected' | 'closed'
  dtlsState: 'new' | 'connecting' | 'connected' | 'failed' | 'closed'
  iceCandidates: number
  createdAt: Date
}

export class WebRTCSignalingServer {
  private connections: Map<string, PeerConnection> = new Map()
  private io: SocketIOServer
  private mediaServer: MediaServer

  constructor(io: SocketIOServer, mediaServer: MediaServer) {
    this.io = io
    this.mediaServer = mediaServer
    this.setupHandlers()
  }

  private setupHandlers() {
    this.io.on('connection', (socket) => {
      // WebRTC-specific namespace
      const namespace = socket.nsp.name

      if (namespace === '/webrtc') {
        this.handleWebRTCConnection(socket)
      }
    })
  }

  private async handleWebRTCConnection(socket: Socket) {
    const { userId, tenantId } = socket.data

    // Client requests to start a call
    socket.on('call:start', async (data: { agentId: string; callerNumber?: string }) => {
      try {
        // Create media server session
        const session = await this.mediaServer.createSession({
          agentId: data.agentId,
          tenantId,
          direction: 'outgoing'
        })

        // Get STUN/TURN config
        const iceConfig = await this.getICEConfig(tenantId)

        socket.emit('call:offer', {
          sessionId: session.id,
          iceServers: iceConfig,
          sdp: session.offerSdp
        })

        this.connections.set(socket.id, {
          callId: session.callId,
          userId,
          peerId: session.id,
          iceState: 'new',
          dtlsState: 'new',
          iceCandidates: 0,
          createdAt: new Date()
        })

      } catch (error) {
        logger.error({ error }, 'Failed to start call')
        socket.emit('error', { message: 'Failed to start call' })
      }
    })

    // Client sends SDP answer
    socket.on('sdp:answer', async (data: { sessionId: string; sdp: string }) => {
      try {
        await this.mediaServer.setRemoteDescription(data.sessionId, data.sdp)
        logger.info({ sessionId: data.sessionId }, 'Remote SDP set')
      } catch (error) {
        logger.error({ error, sessionId: data.sessionId }, 'Failed to set remote SDP')
      }
    })

    // Client sends ICE candidates
    socket.on('ice:candidate', async (data: { sessionId: string; candidate: RTCIceCandidate }) => {
      try {
        await this.mediaServer.addIceCandidate(data.sessionId, data.candidate)
        const conn = Array.from(this.connections.values())
          .find(c => c.peerId === data.sessionId)
        if (conn) {
          conn.iceCandidates++
        }
      } catch (error) {
        logger.warn({ error }, 'Failed to add ICE candidate')
      }
    })

    // Client ICE state changes
    socket.on('ice:state', (data: { sessionId: string; state: string }) => {
      const conn = Array.from(this.connections.values())
        .find(c => c.peerId === data.sessionId)
      if (conn) {
        conn.iceState = data.state as PeerConnection['iceState']
      }
    })

    // DTLS state changes
    socket.on('dtls:state', (data: { sessionId: string; state: string }) => {
      const conn = Array.from(this.connections.values())
        .find(c => c.peerId === data.sessionId)
      if (conn) {
        conn.dtlsState = data.state as PeerConnection['dtlsState']
      }
    })

    // Call ended
    socket.on('call:end', async (data: { sessionId: string }) => {
      await this.endCall(socket, data.sessionId)
    })

    socket.on('disconnect', () => {
      const conn = this.connections.get(socket.id)
      if (conn) {
        this.mediaServer.destroySession(conn.peerId).catch(console.error)
        this.connections.delete(socket.id)
      }
    })
  }

  private async endCall(socket: Socket, sessionId: string) {
    await this.mediaServer.destroySession(sessionId)
    this.connections.delete(socket.id)
    socket.emit('call:ended', { sessionId })
  }

  private async getICEConfig(tenantId: string) {
    // Can customize per tenant (e.g., enterprise gets dedicated TURN)
    return {
      iceServers: [
        ...STUN_SERVERS,
        ...TURN_SERVERS,
      ],
      iceTransportPolicy: 'all' as RTCIceTransportPolicy,
      iceCandidatePoolSize: 10
    }
  }
}

// ICE server configuration
const STUN_SERVERS: RTCIceServer[] = [
  { urls: 'stun:stun.l.google.com:19302' },
  { urls: 'stun:stun1.l.google.com:19302' },
  { urls: 'stun:stun2.l.google.com:19302' }
]

const TURN_SERVERS: RTCIceServer[] = [
  {
    urls: process.env.TURN_URL ?? 'turn:turn.voiceplatform.com:3478',
    username: process.env.TURN_USERNAME,
    credential: process.env.TURN_CREDENTIAL
  }
]
```

## Media Server Integration

```typescript
// server/webrtc/media-server.ts (Mediasoup implementation)
import * as mediasoup from 'mediasoup'
import { Worker, Router, WebRtcTransport, Producer, Consumer } from 'mediasoup/node/lib/types'

export class MediaServer {
  private worker!: Worker
  private router!: Router
  private sessions: Map<string, MediaSession> = new Map()

  async initialize() {
    this.worker = await mediasoup.createWorker({
      logLevel: 'warn',
      logTags: ['info', 'ice', 'dtls', 'rtp', 'srtp', 'rtcp'],
      rtcMinPort: 40000,
      rtcMaxPort: 49999
    })

    this.router = await this.worker.createRouter({
      mediaCodecs: [
        {
          kind: 'audio',
          mimeType: 'audio/opus',
          clockRate: 48000,
          channels: 2
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
        }
      ]
    })

    logger.info('Media server initialized')
  }

  async createSession(options: {
    agentId: string
    tenantId: string
    direction: 'incoming' | 'outgoing'
  }): Promise<MediaSession> {
    // Create WebRTC transport
    const transport = await this.router.createWebRtcTransport({
      listenIps: [
        { ip: process.env.MEDIASOUP_LISTEN_IP ?? '0.0.0.0', announcedIp: process.env.MEDIASOUP_ANNOUNCED_IP }
      ],
      enableUdp: true,
      enableTcp: true,
      preferUdp: true,
      initialAvailableOutgoingBitrate: 128000
    })

    const session: MediaSession = {
      id: crypto.randomUUID(),
      callId: crypto.randomUUID(),
      transport,
      state: 'connecting',
      producer: null,
      consumer: null,
      createdAt: new Date()
    }

    // Handle transport events
    transport.on('dtlsstatechange', (dtlsState) => {
      session.state = dtlsState
      logger.info({ sessionId: session.id, dtlsState }, 'DTLS state changed')
    })

    this.sessions.set(session.id, session)
    return session
  }

  async setRemoteDescription(sessionId: string, sdp: string) {
    // In Mediasoup, remote description is handled via connect() method
    const session = this.sessions.get(sessionId)
    if (!session) throw new Error('Session not found')

    await session.transport.connect({
      dtlsParameters: JSON.parse(sdp)
    })
  }

  async addIceCandidate(sessionId: string, candidate: RTCIceCandidate) {
    // Mediasoup handles ICE internally
    // This is informational only
  }

  async destroySession(sessionId: string) {
    const session = this.sessions.get(sessionId)
    if (!session) return

    if (session.producer) await session.producer.close()
    if (session.consumer) await session.consumer.close()
    await session.transport.close()

    this.sessions.delete(sessionId)
    logger.info({ sessionId }, 'Media session destroyed')
  }
}

interface MediaSession {
  id: string
  callId: string
  transport: WebRtcTransport
  state: string
  producer: Producer | null
  consumer: Consumer | null
  createdAt: Date
}
```

## Client-Side WebRTC

```typescript
// client/webrtc/call-client.ts
export class CallClient {
  private peerConnection: RTCPeerConnection | null = null
  private localStream: MediaStream | null = null
  private signalingSocket: Socket | null = null

  async startCall(signalingSocket: Socket, agentId: string) {
    this.signalingSocket = signalingSocket

    // Get microphone access
    this.localStream = await navigator.mediaDevices.getUserMedia({
      audio: {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true,
        sampleRate: 48000,
        channelCount: 1
      }
    })

    // Listen for offer from signaling server
    signalingSocket.on('call:offer', async (data) => {
      await this.createPeerConnection(data.iceServers)
      await this.handleOffer(data)
    })

    // Initiate call
    signalingSocket.emit('call:start', { agentId })
  }

  private async createPeerConnection(iceServers: RTCIceServer[]) {
    this.peerConnection = new RTCPeerConnection({
      iceServers,
      iceCandidatePoolSize: 10,
      bundlePolicy: 'max-bundle',
      rtcpMuxPolicy: 'require'
    })

    // Add local audio track
    for (const track of this.localStream!.getAudioTracks()) {
      this.peerConnection.addTrack(track, this.localStream!)
    }

    // ICE candidate handler
    this.peerConnection.onicecandidate = (event) => {
      if (event.candidate) {
        this.signalingSocket?.emit('ice:candidate', {
          sessionId: this.sessionId,
          candidate: event.candidate
        })
      }
    }

    // ICE state changes
    this.peerConnection.oniceconnectionstatechange = () => {
      this.signalingSocket?.emit('ice:state', {
        sessionId: this.sessionId,
        state: this.peerConnection?.iceConnectionState
      })
    }

    // DTLS state changes
    this.peerConnection.ondtlsstatechange = () => {
      this.signalingSocket?.emit('dtls:state', {
        sessionId: this.sessionId,
        state: this.peerConnection?.connectionState
      })
    }
  }

  private async handleOffer(data: { sessionId: string; sdp: string; iceServers: RTCIceServer[] }) {
    await this.peerConnection!.setRemoteDescription(
      new RTCSessionDescription({ type: 'offer', sdp: data.sdp })
    )

    const answer = await this.peerConnection!.createAnswer()
    await this.peerConnection!.setLocalDescription(answer)

    this.signalingSocket?.emit('sdp:answer', {
      sessionId: data.sessionId,
      sdp: JSON.stringify(answer)
    })
  }

  endCall() {
    // Close local tracks
    this.localStream?.getTracks().forEach(track => track.stop())
    this.peerConnection?.close()
    this.signalingSocket?.emit('call:end', {
      sessionId: this.sessionId
    })
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Signaling Protocol | WebSocket (Socket.IO) | Already established, reliable transport |
| Media Server | Mediasoup (preferred) | Lower latency, more control, JavaScript-native |
| ICE Strategy | STUN + TURN fallback | Most connections direct; TURN for NAT traversal |
| Codec | Opus primary, PCMU fallback | Best quality/bandwidth tradeoff |
| Audio Processing | Client-side (echo cancellation) | Offload processing, reduce server cost |

## Integration Points

- **Part 04 (Core Voice Engine)** — WebRTC feeds audio into voice pipeline
- **Part 07 (Telephony)** — SIP-to-WebRTC bridging via media server
- **Part 06 (Frontend)** — Browser client uses WebRTC API

## Production Considerations

- **TURN Server**: Deploy Coturn (open-source) in each region; costs ~$50-200/mo per region
- **Port Range**: Mediasoup uses 40000-49999 UDP; open in firewall/security groups
- **NAT Traversal**: 10-15% of users require TURN relay; monitor TURN bandwidth costs
- **Codec Negotiation**: Always negotiate Opus first; fall back to PCMU for legacy PBX integration
- **Quality Monitoring**: Track ICE state, DTLS state, packet loss, jitter, round-trip time per call
- **Scaling**: 500-1000 concurrent calls per Mediasoup worker; scale by adding workers
