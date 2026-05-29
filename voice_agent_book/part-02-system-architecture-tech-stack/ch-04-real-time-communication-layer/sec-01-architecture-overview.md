# Section 01: Architecture Overview

## Real-Time Communication Stack

The real-time communication layer handles all live data flow between the platform and its users — dashboard updates, call monitoring, agent state changes, and audio streaming. It combines WebSocket (for data), WebRTC (for audio), and media servers (for processing).

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   REAL-TIME COMMUNICATION LAYER                        │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    CLIENT CONNECTIONS                            │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │ Dashboard│  │ Mobile   │  │ Voice    │  │ 3rd Party│        │    │
│  │  │ (Browser)│  │ (App)    │  │ (Browser)│  │ (SDK)   │        │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │    │
│  │       │              │              │              │             │    │
│  │  ┌────┴──────────────┴──────────────┴──────────────┴────────┐   │    │
│  │  │                    LOAD BALANCER                           │   │    │
│  │  │  (Sticky sessions for WebSocket, L4 for WebRTC)           │   │    │
│  │  └──────────────────────────┬────────────────────────────────┘   │    │
│  └─────────────────────────────┼───────────────────────────────────┘    │
│                                │                                        │
│  ┌─────────────────────────────┼───────────────────────────────────┐    │
│  │                             ▼                                   │    │
│  │  ┌─────────────────────────────────────────────────────────┐    │    │
│  │  │              REALTIME GATEWAY                            │    │    │
│  │  │                                                          │    │    │
│  │  │  ┌──────────────────┐   ┌──────────────────┐            │    │    │
│  │  │  │  WebSocket       │   │  WebRTC          │            │    │    │
│  │  │  │  Server          │   │  Signaling Server│            │    │    │
│  │  │  │  (Socket.IO)     │   │  (PeerJS/DIY)    │            │    │    │
│  │  │  └────────┬─────────┘   └────────┬─────────┘            │    │    │
│  │  └───────────┼──────────────────────┼──────────────────────┘    │    │
│  │              │                      │                             │    │
│  │  ┌───────────┼──────────────────────┼──────────────────────┐    │    │
│  │  │           ▼                      ▼                      │    │    │
│  │  │  ┌──────────────────┐   ┌──────────────────┐            │    │    │
│  │  │  │  Redis Pub/Sub   │   │  Media Server    │            │    │    │
│  │  │  │  (Horizontal     │   │  (Janus/Mediasoup)│           │    │    │
│  │  │  │   WebSocket      │   │                  │            │    │    │
│  │  │  │   Scaling)       │   │  • Audio Bridge  │            │    │    │
│  │  │  └──────────────────┘   │  • Recording     │            │    │    │
│  │  │                         │  • Mixing        │            │    │    │
│  │  │                         │  • Transcoding   │            │    │    │
│  │  │                         └──────────────────┘            │    │    │
│  │  └──────────────────────────────────────────────────────────┘    │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐    │    │
│  │  │              EVENT BUS (Apache Kafka)                    │    │    │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐   │    │    │
│  │  │  │ Call     │  │ Agent    │  │ System   │  │ Billing│   │    │    │
│  │  │  │ Events   │  │ Events   │  │ Events   │  │ Events │   │    │    │
│  │  │  └──────────┘  └──────────┘  └──────────┘  └────────┘   │    │    │
│  │  └──────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Communication Protocols

| Protocol | Purpose | Latency Target | Transport |
|----------|---------|---------------|-----------|
| WebSocket | Dashboard data, call events, agent state | <50ms message delivery | TCP (with upgrade) |
| WebRTC | Peer-to-peer audio | <10ms packet delivery | UDP (SRTP/SCTP) |
| SIP | PSTN integration | <100ms setup | TCP/UDP |
| Kafka | Service-to-service events | <100ms end-to-end | TCP |
| Redis Pub/Sub | WebSocket scaling | <5ms internal | TCP |

## Key Design Principles

1. **Separation of Data and Media**: WebSocket handles data (events, state), WebRTC handles media (audio). Never mix concerns.
2. **Event-Driven**: All state changes produce events. Consumers subscribe to events, not data polling.
3. **Horizontal Scaling**: WebSocket servers scale via Redis pub/sub. Media servers scale independently.
4. **Graceful Degradation**: If WebSocket fails, fall back to HTTP long-polling. If WebRTC fails, fall back to media server relay.
5. **Connection Resilience**: Auto-reconnection with exponential backoff. State recovery on reconnect.

## Event Flow Example: Call Update

```
┌────────┐    ┌───────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐
│ Call   │    │ Kafka     │    │ Stream  │    │ Redis    │    │ WebSocket│
│ Service│    │           │    │ Processor│   │ Pub/Sub  │    │ Server  │
└───┬────┘    └─────┬─────┘    └────┬────┘    └────┬─────┘    └────┬────┘
    │                │               │               │               │
    │ Call Status    │               │               │               │
    │ Changed        │               │               │               │
    │───────────────>│               │               │               │
    │                │ Event Produced│               │               │
    │                │──────────────>│               │               │
    │                │               │ Process Event │               │
    │                │               │──────────────>│               │
    │                │               │               │ Publish      │
    │                │               │               │──────────────>│
    │                │               │               │               │ Push to
    │                │               │               │               │ Client
    │                │               │               │               │────>
    │                │               │               │               │
```

## Integration Points

- **Part 04 (Core Voice Engine)** — Media server integration with voice pipeline
- **Part 07 (Telephony)** — SIP gateway feeds into media server
- **Part 06 (Frontend)** — Dashboard components subscribe to WebSocket events
- **Part 09 (Data Flow)** — Event-driven architecture relies on this layer
- **Part 24 (Scaling)** — Horizontal scaling of WebSocket and media servers

## Production Considerations

- **Latency Targets**: WebSocket message delivery <50ms, WebRTC audio <150ms end-to-end, media server processing <50ms
- **Concurrency**: Target 100K concurrent WebSocket connections, 10K concurrent calls per cluster
- **Monitoring**: Track connection count, message throughput, latency percentiles, reconnection rate
- **Reliability**: WebSocket with 99.9% uptime SLA, media server with 99.99%
- **Security**: WSS/TLS for WebSocket, DTLS-SRTP for WebRTC, mTLS for service communication
