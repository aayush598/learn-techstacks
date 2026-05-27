# Section 01: Telephony Architecture Overview

## Overview

The telephony layer bridges the AI voice agent platform with the Public Switched Telephone Network (PSTN) and VoIP networks. It handles SIP signaling, RTP media transport, WebRTC browser calling, and carrier interconnects. Understanding these protocols is essential for building a reliable voice communication system.

The architecture consists of a signaling plane (SIP, WebRTC signaling) and a media plane (RTP, audio codecs). The signaling plane manages call setup, teardown, and features (transfer, hold, conferencing). The media plane transports encoded audio between endpoints. Both planes must be highly available with automatic failover.

## Architecture

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  SIP Trunk  │──▶│  FreeSWITCH │──▶│  Media       │──▶│  AI Voice   │
│  (Carrier)  │   │  (Signaling │   │  Processor   │   │  Agent      │
│  Twilio,    │   │   + Media)  │   │  (mix,       │   │  Engine     │
│  Telnyx)    │   └──────────────┘   │   transcode) │   └──────────────┘
└──────────────┘                      └──────────────┘
       │
       ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  WebRTC     │──▶│  Janus/     │──▶│  Browser or │
│  Client     │   │  Mediasoup │   │  Mobile App│
│  (Browser)  │   │  (SFU)     │   └──────────────┘
└──────────────┘   └──────────────┘
```

## Design Decisions

- **FreeSWITCH over Asterisk**: FreeSWITCH has better multi-threaded performance, native WebRTC support, and mod_verto for modern signaling. Asterisk is simpler for basic PBX but lacks in scalability.
- **Separate Signaling and Media**: Signaling servers can be scaled independently from media servers. Media servers are CPU-intensive (codec transcoding); signaling is I/O-bound.
- **WebRTC SFU**: Mediasoup (MIT) as the Selective Forwarding Unit for browser calls. Lightweight, high performance, and no single point of failure.

## Implementation Approach

```typescript
interface CallSession {
  callId: string;
  caller: string;
  callee: string;
  state: 'ringing' | 'connected' | 'held' | 'ended';
  media: MediaStream;
  startedAt: Date;
}

interface SignalingGateway {
  createCall(from: string, to: string): Promise<CallSession>;
  answerCall(callId: string): Promise<void>;
  hangupCall(callId: string): Promise<void>;
  transferCall(callId: string, target: string): Promise<void>;
  holdCall(callId: string): Promise<void>;
  resumeCall(callId: string): Promise<void>;
}

class CallManager {
  private calls: Map<string, CallSession>;
  private signaling: SignalingGateway;
  private mediaServer: MediaServer;

  async handleInbound(callerId: string, calledNumber: string): Promise<CallSession> {
    const call = await this.signaling.createCall(callerId, calledNumber);
    this.calls.set(call.callId, call);

    // Route to AI agent
    const agentSession = await this.connectAgent(call);
    return call;
  }

  private async connectAgent(call: CallSession): Promise<void> {
    const agentAudio = await this.mediaServer.createBridge();
    await this.mediaServer.connect(call.media, agentAudio);
  }
}
```

## Integration Points

- **Voice Engine (P4)**: Media processor connects audio streams to VAD/STT/TTS pipeline.
- **IVR (P7 Ch 07)**: Signaling routes calls through IVR flow before connecting to agent.
- **Transfers (P8 Ch 02)**: SIP REFER for warm/cold transfers.

## Open-Source Tools

- **FreeSWITCH** (MPL 2.0): Media server and softswitch. 10k+ concurrent calls per instance.
- **Mediasoup** (MIT): WebRTC SFU with Node.js API. 0-dependency C++ core.
- **Coturn** (BSD): STUN/TURN server for NAT traversal.
- **SIP.js** (MIT): SIP over WebSocket for browser clients.

## Production Considerations

- **Redundancy**: Active-active signaling cluster (3+ nodes). Active-passive media servers with media state replication.
- **Codec Prioritization**: Opus > PCMU > PCMA > G.729. Opus provides best quality at lowest bitrate.
- **Latency Budget**: Signaling: <50ms. Media transport: <100ms RTT between media server and client.
- **Regulatory**: E.164 number formatting, local number portability support, emergency call handling (e911).
