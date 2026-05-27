# Chapter 03: WebSocket API & Real-Time Events

> **Part:** 18 - Developer Tools, SDKs & API Layer

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [WebSocket Connection Lifecycle](sec-01-websocket-connection-lifecycle.md) | Connection establishment, upgrade handshake, message framing, graceful close, error handling |
| 02 | [Event Schema Design](sec-02-event-schema-design.md) | Event types, payload structure, metadata envelope, versioning, event catalog |
| 03 | [Room/Channel Subscription](sec-03-room-channel-subscription.md) | Pub/sub channels, room management, subscription messages, auto-subscribe, channel permissions |
| 04 | [Reconnection Strategy](sec-04-reconnection-strategy.md) | Exponential backoff, last-known-event replay, state reconciliation, connection state machine |
| 05 | [Heartbeat & Keepalive](sec-05-heartbeat-keepalive.md) | Ping/pong frames, idle connection detection, stale connection cleanup, health checking |
| 06 | [Scalability & Horizontal Scaling](sec-06-scalability-horizontal-scaling.md) | Redis pub/sub adapter, sticky sessions vs shared state, scaling WebSocket servers, load balancing |
| 07 | [WebSocket Authentication](sec-07-websocket-authentication.md) | Auth during upgrade, token validation, re-authentication on reconnect, connection authorization |
| 08 | [Fallback to Polling](sec-08-fallback-to-polling.md) | SSE (Server-Sent Events), long polling, automatic fallback detection, fallback compatibility |

---

## WebSocket Event Envelope

```json
{
  "type": "call.status_changed",
  "id": "evt_abc_123",
  "timestamp": "2025-06-01T10:00:00.000Z",
  "channel": "tenant:tenant_xyz",
  "data": {
    "call_id": "call_def_456",
    "previous_status": "ringing",
    "current_status": "in_progress",
    "duration_seconds": 120
  }
}
```

---

## Learning Objectives

- Implement WebSocket connection lifecycle management
- Design event schema with versioning and metadata
- Build room/channel subscription with pub/sub
- Implement reconnection strategy with event replay
- Create heartbeat and keepalive mechanisms
- Scale WebSocket horizontally with Redis adapter
- Implement WebSocket authentication and authorization
- Build fallback to SSE/long polling
