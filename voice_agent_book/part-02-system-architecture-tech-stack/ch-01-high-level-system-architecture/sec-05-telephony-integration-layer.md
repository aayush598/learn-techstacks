# Section 05: Telephony Integration Layer

## Telephony Architecture

The Telephony Integration Layer bridges the gap between **traditional telecommunications networks** (PSTN, SIP) and the **modern VoIP/WebRTC stack**. This layer enables AI agents to make and receive phone calls as if they were human operators.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      TELEPHONY INTEGRATION LAYER                       │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │                        INCOMING CALLS                           │     │
│  │                                                                 │     │
│  │  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌────────┐ │     │
│  │  │  PSTN    │────▶│  SIP     │────▶│   SIP    │────▶│  IVR   │ │     │
│  │  │  Network │     │  Trunk   │     │  Server  │     │ Engine  │ │     │
│  │  └──────────┘     └──────────┘     └──────────┘     └───┬────┘ │     │
│  │                                                          │      │     │
│  │  ┌──────────┐     ┌──────────┐     ┌──────────┐         │      │     │
│  │  │  WebRTC  │────▶│ Signaling│────▶│  WebRTC  │─────────┘      │     │
│  │  │  Browser │     │  Server  │     │ Gateway   │                │     │
│  │  └──────────┘     └──────────┘     └──────────┘                │     │
│  └─────────────────────────────────────────────────────────────────┘     │
│                                   │                                      │
│  ┌────────────────────────────────┼─────────────────────────────────┐     │
│  │                                ▼                                 │     │
│  │                    MEDIA SERVER (Janus/Mediasoup)                 │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │     │
│  │  │  Audio   │  │  Codec   │  │  Record  │  │  Mixer   │         │     │
│  │  │  Bridge  │  │  Transcod│  │  Manager │  │          │         │     │
│  │  └────┬─────┘  └──────────┘  └──────────┘  └──────────┘         │     │
│  └───────┼──────────────────────────────────────────────────────────┘     │
│          │                                                               │
│  ┌───────┴──────────────────────────────────────────────────────────┐     │
│  │                    CALL ORCHESTRATION                            │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │     │
│  │  │  Dialer  │  │  Router  │  │  State   │  │  Queue   │         │     │
│  │  │  Engine  │  │  Service │  │  Machine  │  │ Manager  │         │     │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │     │
│  └──────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. SIP Server and Trunking

SIP (Session Initiation Protocol) is the standard for initiating and managing VoIP calls. The SIP server handles registration, call routing, and media negotiation with the PSTN.

```typescript
interface SIPConfig {
  trunkProvider: 'twilio' | 'telnyx' | 'bandwidth' | 'plivo' | 'custom'
  protocol: 'udp' | 'tcp' | 'tls'
  codecs: Array<'PCMU' | 'PCMA' | 'G722' | 'Opus'>
  dtmfMode: 'rfc2833' | 'info' | 'inband'
  maxChannels: number
  registrationRequired: boolean
  sipServer: string
  sipPort: number
}

interface SIPTrunk {
  id: string
  provider: string
  phoneNumbers: string[]
  status: 'active' | 'inactive' | 'error'
  metrics: {
    activeCalls: number
    totalCalls: number
    errorRate: number
    avgSetupTime: number
  }
}

// SIP INVITE flow
// 1. PSTN → SIP Trunk: INVITE sip:+14155551234@voip.provider.com
// 2. SIP Trunk → SIP Server: INVITE sip:agent@internal.voiceplatform.com
// 3. SIP Server → Media Server: Create new session with SDP offer
// 4. Media Server → SIP Server: 200 OK with SDP answer
// 5. SIP Server → SIP Trunk: 200 OK
// 6. SIP Trunk → PSTN: 200 OK
// 7. RTP stream established between PSTN and Media Server
```

### 2. Media Server (Janus/Mediasoup)

The media server handles all real-time audio processing:

```typescript
interface MediaServerConfig {
  engine: 'janus' | 'mediasoup' | 'livekit'
  workers: number          // Number of worker processes
  maxStreams: number       // Max concurrent streams per worker
  recordingPath: string    // Path to store recordings
}

interface MediaSession {
  id: string
  callId: string
  type: 'webrtc' | 'sip' | 'playback'
  streams: AudioStream[]
  state: 'connecting' | 'connected' | 'paused' | 'ended'
  
  // Audio processing
  addAudioMix(streamId: string, options: MixOptions): Promise<void>
  startRecording(options: RecordOptions): Promise<void>
  transcoder(codec: string): Promise<void>
  applyFilter(filter: AudioFilter): Promise<void>
}

interface AudioStream {
  id: string
  type: 'microphone' | 'speaker' | 'mix' | 'recording'
  codec: 'opus' | 'pcmu' | 'pcma'
  ssrc: number
  sdp: string
}
```

### 3. IVR (Interactive Voice Response) Engine

The IVR engine handles incoming calls with menu navigation:

```typescript
interface IVRConfig {
  greeting: {
    tts: string          // "Thank you for calling..."
    audioFile?: string   // Pre-recorded alternative
  }
  menu: IVRMenuNode
  timeout: number        // Seconds before timeout
  maxRetries: number     // Max retries for input
  fallbackAction: 'transfer_operator' | 'voicemail' | 'disconnect'
}

interface IVRMenuNode {
  id: string
  prompt: string         // "Press 1 for sales, 2 for support..."
  options: Array<{
    key: string          // "1", "2", "3", "*", "#"
    label: string
    action: 'navigate' | 'agent_transfer' | 'play_message' | 'execute'
    target?: string      // Next node or agent group
    params?: Record<string, unknown>
  }>
  voiceInput?: boolean   // Enable speech recognition
  timeoutNode?: string   // Where to go on timeout
}

// DTMF collection
interface DTMFCollector {
  collect(options: {
    numDigits: number
    timeout: number
    terminator?: string
    validDigits: RegExp
  }): Promise<string>
}
```

### 4. Call Router

The call router determines which AI agent should handle a call:

```typescript
interface CallRouter {
  route(incomingCall: IncomingCall): Promise<RoutingDecision>
}

interface IncomingCall {
  from: string           // Caller ID
  to: string             // Called number
  trunkId: string
  timestamp: Date
  ivrPath?: string[]     // IVR menu selections
  metadata?: Record<string, unknown>
}

interface RoutingDecision {
  agentId: string
  campaignId?: string
  priority: number
  maxWaitTime: number
  fallbackAgentId?: string
}

// Routing logic
async function routeCall(call: IncomingCall): Promise<RoutingDecision> {
  // 1. Check if caller has an active conversation (call-back)
  const existingConv = await conversationService.findActiveByNumber(call.from)
  if (existingConv) {
    return { agentId: existingConv.agentId, priority: 1 }
  }

  // 2. Check DID routing (which number was called)
  const didConfig = await didService.getConfig(call.to)
  if (didConfig?.agentId) {
    return { agentId: didConfig.agentId, priority: 2 }
  }

  // 3. IVR-based routing
  if (call.ivrPath?.length) {
    const intent = await ivrRouter.resolve(call.ivrPath)
    const agent = await agentService.findByCapability(intent)
    if (agent) {
      return { agentId: agent.id, priority: 3 }
    }
  }

  // 4. Round-robin default agent
  const defaultAgent = await agentService.nextAvailable()
  return { agentId: defaultAgent.id, priority: 4 }
}
```

### 5. Dialer Engine (Outbound)

For outbound campaigns, the dialer engine manages call pacing:

```typescript
interface DialerConfig {
  mode: 'preview' | 'power' | 'predictive' | 'progressive'
  maxConcurrent: number
  callAttempts: number
  callInterval: number          // Minutes between attempts
  timeZone: string
  callingHours: { start: number; end: number }
  compliance: {
    dncList: boolean
    maxDailyAttempts: number
    abideByTimeZone: boolean
  }
}

interface DialerEngine {
  startCampaign(campaignId: string): Promise<void>
  pauseCampaign(campaignId: string): Promise<void>
  getNextContact(): Promise<Contact | null>
  reportOutcome(callId: string, outcome: CallOutcome): Promise<void>
  adjustPacing(metrics: DialerMetrics): Promise<void>
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| SIP Provider | Multi-provider (Twilio + Telnyx) | Redundancy, better pricing, geographic coverage |
| Media Server | Janus Gateway | Full-featured, supports SIP, recording, streaming |
| Codec Priority | Opus > G722 > PCMU | Opus provides best quality at low bitrate |
| DTMF Handling | RFC 2833 (in-band) | Most reliable across carriers |
| IVR vs AI-first | AI-first with optional IVR | Better user experience, IVR as fallback |
| Outbound Dialer | Predictive mode default | Maximizes agent utilization |

## Integration Points

- **Part 07 (Telephony & Communication)** — Full implementation of telephony features
- **Part 08 (Human Hand-off)** — Call routing can escalate to human agents
- **Part 09 (Campaign Management)** — Outbound dialer drives campaign execution
- **Part 04 (Core Voice Engine)** — Media server feeds audio to voice pipeline

## Production Considerations

- **Regulatory Compliance**: Must comply with TCPA (US), GDPR (EU), and local telephony regulations
- **DNC (Do Not Call) List**: Every outbound call checks against national and internal DNC lists
- **Call Recording Consent**: Required in 2-party consent states; beep tone before recording
- **Failover**: Automatic failover between SIP providers; if one trunk fails, traffic routes to the secondary
- **Monitoring**: Call quality metrics (MOS score), setup time, drop rate, jitter, packet loss
- **Scaling**: Media server scales horizontally; each instance handles 500-1000 concurrent calls
- **Emergency Calls**: 911 calls must be routed differently with location information
