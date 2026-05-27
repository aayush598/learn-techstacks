# Chapter 04: Real-Time Communication Layer

> **Part:** 02 - System Architecture & Technology Stack

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Architecture Overview](sec-01-architecture-overview.md) | WebSocket server (Socket.IO/uWebSockets.js), WebRTC signaling, real-time event bus |
| 02 | [WebSocket Server Design](sec-02-websocket-server-design.md) | Connection management, rooms/groups, event schema, reconnection strategy, horizontal scaling |
| 03 | [WebRTC Signaling Server](sec-03-webrtc-signaling-server.md) | Offer/answer exchange, ICE candidate relay, NAT traversal, STUN/TURN integration |
| 04 | [Real-Time Event Catalog](sec-04-real-time-event-catalog.md) | Call events (ringing, connected, ended), transcript events, sentiment events, agent state |
| 05 | [Presence & Availability](sec-05-presence-availability.md) | User presence tracking, connection state, away detection, multi-device handling |
| 06 | [Horizontal Scaling for WebSocket](sec-06-horizontal-scaling-websocket.md) | Redis pub/sub adapter, sticky sessions, connection draining, multi-region deployment |
| 07 | [Media Server Integration](sec-07-media-server-integration.md) | Janus/Mediasoup, audio pipeline, codec negotiation, stream mixing, recording |
| 08 | [Latency & Performance Targets](sec-08-latency-performance-targets.md) | Message delivery <50ms, connection setup <1s, reconnection <3s, heartbeat 10s |

---

## Key Takeaways

- WebSocket for real-time dashboard, call monitoring, and agent state
- WebRTC for peer-to-peer audio with fallback to TURN
- Redis pub/sub for horizontal WebSocket scaling across nodes
- Janus/Mediasoup for media server with recording and mixing
- Target: message delivery under 50ms, connection setup under 1s
- Auto-reconnection with exponential backoff and state recovery
