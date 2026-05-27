# Section 05: WebSocket Update Integration

## Overview

WebSocket update integration is the communication backbone of the real-time monitoring dashboard. It provides persistent, bidirectional connections between the dashboard client and the server, enabling sub-second delivery of call events, metric updates, transcription snippets, and command acknowledgments. The integration layer handles connection lifecycle (connect, reconnect, heartbeat), message serialization (protocol buffers over JSON for efficiency), channel subscriptions (per tenant, per campaign, per call), and backpressure management.

The architecture uses a dedicated WebSocket gateway service that sits between the dashboard clients and the internal event infrastructure (Kafka, Redis). The gateway authenticates connections via JWT, maintains a registry of connected clients and their subscriptions, and multiplexes events from internal streams to the appropriate client connections. For horizontal scaling, gateway instances communicate via Redis Pub/Sub to broadcast events across instances when needed.

## Architecture

```
              WebSocket Integration Architecture

   Client → Load Balancer → WS Gateway (Instance 1)
                            WS Gateway (Instance 2)
                            WS Gateway (Instance N)
                                |
                    ┌───────────┴───────────┐
                    |                        |
              Redis Pub/Sub             Kafka Consumer
           (Cross-instance broadcast)   (Internal events)
                    |                        |
              Redis Streams             Stream Processor
           (Live feed buffer)               |
                                        Event Bus
```

## Design Decisions

- **Dedicated WebSocket gateway over embedding in the API server:** Separating the WebSocket gateway into its own service (or set of instances) allows independent scaling of HTTP API requests and persistent connections. The gateway can be deployed with a higher connection limit (each instance handles 10,000 concurrent connections) and can be optimized for I/O without competing with HTTP request processing. Trade-off: the gateway introduces network hop latency and requires synchronization (Redis Pub/Sub) to broadcast events to all instances.

- **Protocol Buffers over JSON for message serialization:** For high-throughput real-time feeds (transcription snippets arriving every 200ms per call), JSON serialization adds ~40% overhead in message size. Protocol Buffers reduce message size by 60% and serialization/deserialization time by 50%. The gateway negotiates the serialization format during the WebSocket handshake based on the client's `Accept-Encoding`-style header. Fallback to JSON for clients that do not support Protobuf. Trade-off: Protobuf requires schema management and code generation; schema changes require coordinated deployment of server and client.

- **Redis Pub/Sub for cross-instance broadcast over Kafka:** When a stream processor emits an event, the gateway instance that receives it must broadcast to all connected clients across all gateway instances. Redis Pub/Sub is faster (sub-millisecond) than Kafka (2-5 ms) for this use case because messages are ephemeral and do not require persistence. Trade-off: Redis Pub/Sub messages are lost if a gateway instance disconnects, but this is acceptable because the gateway re-reads from Redis Streams (the persistent buffer) on reconnection.

## Implementation Approach

```typescript
import { WebSocket as WsServer } from 'ws';
import { PubSub } from 'ioredis';
import { Kafka } from 'kafkajs';

// Message envelope
interface WsMessage {
  type: 'event' | 'metric' | 'transcription' | 'ack' | 'heartbeat' | 'error';
  channel: string;
  payload: Uint8Array | Record<string, unknown>;
  sequence: number;      // monotonic per channel for ordering
  timestamp: number;
}

interface ClientSubscription {
  clientId: string;
  tenantId: string;
  userId: string;
  channels: Set<string>;   // e.g., 'feed:tenant_123', 'metrics:tenant_123'
  metadata: Record<string, string>;
  connectedAt: number;
}

class WebSocketGateway {
  private clients: Map<string, { ws: WebSocket; subscription: ClientSubscription }>;
  private pubSub: PubSub;
  private kafkaConsumer: KafkaConsumer;
  private heartbeatInterval: NodeJS.Timer;

  constructor() {
    this.clients = new Map();
    this.pubSub = new PubSub({ host: process.env.REDIS_HOST });
    this.setupPubSub();
    this.startHeartbeat(30000); // 30-second heartbeat
  }

  async handleConnection(ws: WebSocket, req: IncomingMessage): Promise<void> {
    const token = this.extractToken(req);
    const decoded = verifyJwt(token);
    const clientId = generateId();

    const subscription: ClientSubscription = {
      clientId,
      tenantId: decoded.tenantId,
      userId: decoded.sub,
      channels: new Set(),
      metadata: decoded,
      connectedAt: Date.now(),
    };

    this.clients.set(clientId, { ws, subscription });

    // Subscribe to tenant-level Redis Pub/Sub channels
    await this.pubSub.subscribe(`tenant:${decoded.tenantId}:events`);
    await this.pubSub.subscribe(`tenant:${decoded.tenantId}:metrics`);
    await this.pubSub.subscribe(`tenant:${decoded.tenantId}:alerts`);

    ws.on('message', (data: Buffer) => this.handleMessage(clientId, data));
    ws.on('close', () => this.handleDisconnect(clientId));
    ws.on('error', (err) => this.handleError(clientId, err));

    // Send initial connection ack
    this.send(ws, { type: 'ack', channel: 'system', payload: { clientId }, sequence: 0, timestamp: Date.now() });
  }

  private async handleMessage(clientId: string, data: Buffer): Promise<void> {
    const client = this.clients.get(clientId);
    if (!client) return;

    let message: WsMessage;
    if (this.isProtobuf(client.ws)) {
      message = ProtobufWsMessage.decode(data);
    } else {
      message = JSON.parse(data.toString());
    }

    switch (message.type) {
      case 'subscribe':
        await this.handleSubscribe(client, message.payload as { channels: string[] });
        break;
      case 'unsubscribe':
        await this.handleUnsubscribe(client, message.payload as { channels: string[] });
        break;
      case 'pong':
        client.subscription.metadata.lastPong = Date.now();
        break;
    }
  }

  private async handleSubscribe(
    client: { ws: WebSocket; subscription: ClientSubscription },
    payload: { channels: string[] }
  ): Promise<void> {
    for (const channel of payload.channels) {
      // Validate channel access
      if (!this.canAccessChannel(client.subscription, channel)) {
        this.send(client.ws, {
          type: 'error',
          channel: 'system',
          payload: { message: `Access denied to channel: ${channel}` },
          sequence: 0,
          timestamp: Date.now(),
        });
        continue;
      }
      client.subscription.channels.add(channel);
    }
  }

  private canAccessChannel(subscription: ClientSubscription, channel: string): boolean {
    // e.g., 'feed:tenant_123' — user must be in tenant_123
    const channelTenant = channel.split(':')[1];
    return channelTenant === subscription.tenantId;
  }

  // Broadcast an event to all connected clients subscribed to the channel
  async broadcast(channel: string, payload: Uint8Array, sequence: number): Promise<void> {
    const message: WsMessage = {
      type: 'event',
      channel,
      payload,
      sequence,
      timestamp: Date.now(),
    };

    for (const [clientId, { ws, subscription }] of this.clients) {
      if (subscription.channels.has(channel) && ws.readyState === WebSocket.OPEN) {
        this.send(ws, message);
      }
    }
  }

  private send(ws: WebSocket, message: WsMessage): void {
    const data = this.isProtobuf(ws)
      ? ProtobufWsMessage.encode(message).finish()
      : Buffer.from(JSON.stringify(message));
    ws.send(data);
  }

  private startHeartbeat(intervalMs: number): void {
    this.heartbeatInterval = setInterval(() => {
      const now = Date.now();
      for (const [clientId, { ws, subscription }] of this.clients) {
        const lastPong = subscription.metadata.lastPong as number || 0;
        if (now - lastPong > intervalMs * 3) {
          // Client unresponsive, close connection
          ws.close(1000, 'Heartbeat timeout');
          this.clients.delete(clientId);
        } else {
          this.send(ws, {
            type: 'heartbeat',
            channel: 'system',
            payload: { timestamp: now },
            sequence: 0,
            timestamp: now,
          });
        }
      }
    }, intervalMs);
  }
}

// Client-side reconnection with exponential backoff
class WsClient {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectDelay = 30000;

  async connect(url: string, token: string): Promise<void> {
    this.ws = new WebSocket(`${url}?token=${token}`);

    this.ws.onclose = () => {
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), this.maxReconnectDelay);
      setTimeout(() => this.connect(url, token), delay);
      this.reconnectAttempts++;
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'heartbeat') {
        this.ws?.send(JSON.stringify({ type: 'pong' }));
      }
      this.handleMessage(message);
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ws (MIT) | Server | WebSocket server library |
| Socket.IO (MIT) | Server/Client | WebSocket with fallback transport |
| Protocol Buffers (Apache 2.0) | Both | Message serialization |
| Redis Pub/Sub (RSAL) | Server | Cross-instance event broadcast |

## Production Considerations

**Scaling:** Each WebSocket gateway instance can handle 10,000 concurrent connections on a 2-CPU instance. Use a Layer 4 load balancer (AWS NLB, HAProxy) with proxy protocol to preserve client IP. For sticky sessions, use a Redis-backed session store to route returning clients to the same gateway instance. When scaling up, drain connections from existing instances gracefully by sending a "reconnect" message with a delay hint.

**Security:** WebSocket connections authenticate via JWT in the query string (first connection) or via a dedicated auth message (reconnecting). Tokens expire every 15 minutes — the gateway validates the token on connect and rejects connections with expired tokens. Implement per-IP connection rate limiting (100 connections per minute per IP). Use WSS (TLS WebSockets) in production to prevent message interception. Channel names include the tenant ID to prevent cross-tenant data leakage.

**Monitoring:** Track active connection count, messages per second per instance, average message size, reconnection rate, and heartbeat failure rate. Alert if heartbeat failure rate exceeds 5% — this may indicate network issues or client-side bugs. Monitor Redis Pub/Sub message loss rate by comparing published vs received message sequence numbers. Log all connection errors with client IP and reason for debugging.
