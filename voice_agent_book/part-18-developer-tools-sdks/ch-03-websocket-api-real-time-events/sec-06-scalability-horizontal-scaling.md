# Section 06: Scalability & Horizontal Scaling

## Overview

WebSocket servers scale horizontally by sharing state through Redis pub/sub and avoiding sticky sessions. Any server can handle any WebSocket connection because all servers receive all events through the Redis adapter. Load balancing uses layer 4 (TCP) to preserve WebSocket connections, and autoscaling policies react to connection count and message throughput.

## Architecture

```
Horizontal Scaling Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Load Balancer (TCP)]
         │
    ┌────┴────┐────┐
    │         │    │
  [WS Svr 1] [WS Svr 2] [WS Svr N]
    │         │    │
    └────┬────┘────┘
         │
    [Redis Cluster]
    ├── Pub/Sub: Channel event distribution
    ├── Connection Registry: connection → server mapping
    └── Subscription State: channel → subscribers

Event Publishing Flow:
  [Call Service] ──→ Publish event to Redis
                            │
                    [Redis Pub/Sub]
                            │
                ┌───────────┴───────────┐
                │                       │
          [WS Server 1]          [WS Server 2]
                │                       │
          ┌─────┴─────┐           ┌─────┴─────┐
          │ Connection │           │ Connection │
          │ 1, 2, 3   │           │ 4, 5, 6   │
          └───────────┘           └───────────┘

No Sticky Sessions (preferred):
  Client connects to any server
  On reconnect, may connect to different server
  Redis pub/sub ensures all servers have all events
```

## Design Decisions

- **Redis Pub/Sub Over Sticky Sessions**: Sticky sessions (hash on IP) concentrate load; Redis distributes events to all servers uniformly
- **TCP Load Balancing**: Layer 4 (TCP) load balancer preserves WebSocket upgrade — no layer 7 WebSocket termination
- **Connection-to-Server Registry**: Redis maps connection IDs to server IDs for targeted message delivery (e.g., unsubscribe)
- **Autoscaling Based on Connections**: Scale up when average connections per server exceeds 8,000; scale down below 2,000

## Implementation Approach

```typescript
// Redis adapter for multi-server event distribution
interface RedisAdapterConfig {
  host: string;
  port: number;
  channelPrefix: string;
  serverId: string;
}

class WebSocketRedisAdapter {
  private publisher: Redis;
  private subscriber: Redis;
  private serverId: string;
  private eventHandlers: Map<string, (message: string) => void> = new Map();

  constructor(config: RedisAdapterConfig) {
    this.publisher = new Redis({ host: config.host, port: config.port });
    this.subscriber = new Redis({ host: config.host, port: config.port });
    this.serverId = config.serverId;

    this.subscriber.on('message', (channel, message) => {
      const handler = this.eventHandlers.get(channel);
      if (handler) {
        handler(message);
      }
    });
  }

  async publish(channel: string, event: EventEnvelope): Promise<void> {
    const message = JSON.stringify({
      serverId: this.serverId,
      event,
    });
    await this.publisher.publish(`ws:${channel}`, message);
  }

  async subscribe(channel: string): Promise<void> {
    await this.subscriber.subscribe(`ws:${channel}`);
  }

  async unsubscribe(channel: string): Promise<void> {
    await this.subscriber.unsubscribe(`ws:${channel}`);
  }

  onEvent(channel: string, handler: (event: EventEnvelope) => void): void {
    this.eventHandlers.set(`ws:${channel}`, (message) => {
      const parsed = JSON.parse(message);
      if (parsed.serverId !== this.serverId) {
        handler(parsed.event);
      }
    });
  }

  // Track which server owns which connection
  async registerConnection(connectionId: string): Promise<void> {
    await this.publisher.set(`conn:${connectionId}`, this.serverId, 'EX', 3600);
  }

  async unregisterConnection(connectionId: string): Promise<void> {
    await this.publisher.del(`conn:${connectionId}`);
  }

  async getConnectionServer(connectionId: string): Promise<string | null> {
    return this.publisher.get(`conn:${connectionId}`);
  }
}

// Autoscaling controller
class WebSocketScaler {
  private connectionsPerServer: Map<string, number> = new Map();

  constructor(private redis: Redis) {}

  async recordConnection(serverId: string): Promise<void> {
    await this.redis.hincrby('ws:server:connections', serverId, 1);
  }

  async recordDisconnection(serverId: string): Promise<void> {
    await this.redis.hincrby('ws:server:connections', serverId, -1);
  }

  async getServerConnections(): Promise<Map<string, number>> {
    const data = await this.redis.hgetall('ws:server:connections');
    const map = new Map();
    for (const [server, count] of Object.entries(data)) {
      map.set(server, parseInt(count));
    }
    return map;
  }

  async shouldScaleUp(threshold = 8000): Promise<boolean> {
    const conns = await this.getServerConnections();
    for (const count of conns.values()) {
      if (count > threshold) return true;
    }
    return false;
  }

  async shouldScaleDown(threshold = 2000): Promise<boolean> {
    const conns = await this.getServerConnections();
    for (const count of conns.values()) {
      if (count < threshold) return true;
    }
    return false;
  }
}

// Graceful shutdown with connection draining
async function gracefulShutdown(adapter: WebSocketRedisAdapter, connections: Map<string, WebSocketConnection>): Promise<void> {
  // Stop accepting new connections
  // Notify all connections to reconnect
  for (const [id, conn] of connections) {
    try {
      conn.sendSystemMessage({
        type: 'server_shutdown',
        message: 'Server restarting — please reconnect',
        reconnectDelay: 2000,
      });
    } catch {
      // Connection may already be dead
    }
  }

  // Wait for drain
  await new Promise(resolve => setTimeout(resolve, 10_000));

  // Close remaining connections
  for (const [, conn] of connections) {
    conn.close(4401, 'Server shutdown');
  }
}
```

## Integration Points

- **Redis Cluster**: Provides pub/sub and state storage; cluster mode for high availability
- **Load Balancer**: TCP load balancer (NGINX, HAProxy) with health checks on WebSocket servers
- **Auto-Scaler**: Kubernetes HPA based on custom metrics — connections per pod

## Production Considerations

- **Redis as Single Point of Failure**: Redis Sentinel or Redis Cluster for high availability
- **Network Latency**: Multi-region deployment requires region-local Redis clusters with cross-region replication
- **Connection Draining**: During rolling deployments, drain connections gradually to avoid mass reconnection storms
- **Server Health Checks**: Load balancer health checks via HTTP endpoint on WebSocket server

## Open-Source Tools

- **Redis**: Pub/sub for cross-server event distribution
- **HAProxy/NGINX**: TCP load balancing for WebSocket connections
- **Kubernetes HPA**: Horizontal pod autoscaling based on custom metrics
