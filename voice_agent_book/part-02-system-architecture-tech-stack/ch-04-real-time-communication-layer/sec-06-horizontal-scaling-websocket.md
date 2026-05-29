# Section 06: Horizontal Scaling for WebSocket

## Scaling Architecture

Horizontal scaling of WebSocket servers requires solving the **state distribution problem** — connections are spread across multiple servers, but events must reach the correct connections regardless of which server they're on. The solution uses Redis pub/sub as a message bus between WebSocket server instances.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   HORIZONTAL WEBSOCKET SCALING                         │
│                                                                         │
│                     ┌──────────────────────┐                           │
│                     │   Load Balancer      │                           │
│                     │  (Sticky Sessions)   │                           │
│                     └────┬──────┬──────┬───┘                           │
│                          │      │      │                               │
│          ┌───────────────┼──────┼──────┼───────────────────┐           │
│          │               │      │      │                   │           │
│          ▼               ▼      │      ▼                   ▼           │
│  ┌───────────┐   ┌───────────┐  │  ┌───────────┐   ┌───────────┐      │
│  │  WS Node 1  │   │  WS Node 2  │  │  WS Node 3  │   │  WS Node N  │  │
│  │  (1000 conn)│   │  (1200 conn)│  │  (800 conn) │   │  (900 conn)  │  │
│  └──────┬──────┘   └──────┬──────┘  └──────┬──────┘   └──────┬──────┘  │
│         │                 │                │                 │         │
│         └─────────────────┼────────────────┼─────────────────┘         │
│                           │                │                           │
│                    ┌──────┴────────────────┴──────┐                    │
│                    │       Redis Cluster           │                    │
│                    │                               │                    │
│                    │  ┌──────────────────────┐    │                    │
│                    │  │   Pub/Sub Channels   │    │                    │
│                    │  │                      │    │                    │
│                    │  │  • ws:call:{id}      │    │                    │
│                    │  │  • ws:tenant:{id}    │    │                    │
│                    │  │  • ws:agent:{id}     │    │                    │
│                    │  │  • ws:global         │    │                    │
│                    │  └──────────────────────┘    │                    │
│                    │                               │                    │
│                    │  ┌──────────────────────┐    │                    │
│                    │  │   Connection Registry │    │                    │
│                    │  │                      │    │                    │
│                    │  │  sock_id → node_id   │    │                    │
│                    │  │  user_id → [sock_ids]│    │                    │
│                    │  │  room → [sock_ids]   │    │                    │
│                    │  └──────────────────────┘    │                    │
│                    └──────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Redis Adapter for Socket.IO

```typescript
// server/websocket/cluster.ts
import { createServer } from 'http'
import { Server } from 'socket.io'
import { createAdapter } from '@socket.io/redis-adapter'
import { Redis } from 'ioredis'
import { logger } from '@/lib/logger'

export function createClusteredWebSocketServer() {
  const httpServer = createServer()

  // Redis clients (separate for pub/sub)
  const pubClient = new Redis(process.env.REDIS_URL!, {
    enableReadyCheck: false,
    maxRetriesPerRequest: null,
    retryStrategy: (times) => Math.min(times * 50, 2000)
  })

  const subClient = pubClient.duplicate()

  const io = new Server(httpServer, {
    transports: ['websocket', 'polling'],
    pingInterval: 25000,
    pingTimeout: 20000,
    adapter: createAdapter(pubClient, subClient, {
      // Socket.IO Redis adapter options
      key: 'ws:',  // Redis key prefix
      requestsTimeout: 5000,
      publishOnSpecificResponse: true
    }),
    // Sticky session support
    cookie: {
      name: 'ws-sid',
      httpOnly: true,
      sameSite: 'strict'
    }
  })

  // Monitor adapter events
  io.of('/').adapter.on('create-room', (room) => {
    logger.debug({ room }, 'Room created')
  })

  io.of('/').adapter.on('delete-room', (room) => {
    logger.debug({ room }, 'Room deleted')
  })

  io.of('/').adapter.on('join-room', (room, id) => {
    logger.debug({ room, socketId: id }, 'Socket joined room')
  })

  io.of('/').adapter.on('leave-room', (room, id) => {
    logger.debug({ room, socketId: id }, 'Socket left room')
  })

  return { io, httpServer, pubClient, subClient }
}

// Graceful shutdown
export async function shutdownWebSocketServer(
  io: Server,
  pubClient: Redis,
  subClient: Redis
) {
  logger.info('Shutting down WebSocket server')

  // Disconnect all connected sockets
  const sockets = await io.fetchSockets()
  for (const socket of sockets) {
    socket.emit('server.shutdown', {
      message: 'Server is shutting down for maintenance',
      reconnect: true,
      reconnectDelay: 5000
    })
    socket.disconnect(true)
  }

  // Close Redis connections
  await pubClient.quit()
  await subClient.quit()

  // Close Socket.IO
  await io.close()

  logger.info('WebSocket server shutdown complete')
}
```

## Connection Draining

```typescript
// Kubernetes preStop hook for graceful draining
import { io } from './server'

export async function drainConnections() {
  const drainTimeout = 30000  // 30 seconds max drain time
  const startTime = Date.now()

  logger.info('Starting connection drain')

  // Notify all connected clients
  const sockets = await io.fetchSockets()
  for (const socket of sockets) {
    try {
      // Send drain notice with timeout
      await socket.emitWithAck('server.draining', {
        reconnectUrl: process.env.WS_FALLBACK_URL,
        reconnectDelay: 1000,
        drainTimeout: drainTimeout
      }).timeout(5000)
    } catch {
      // Client didn't acknowledge, force disconnect
    }
  }

  // Wait for connections to drain or timeout
  while (Date.now() - startTime < drainTimeout) {
    const remaining = await io.engine.clientsCount
    if (remaining === 0) {
      logger.info('All connections drained')
      return
    }
    await new Promise(resolve => setTimeout(resolve, 1000))
  }

  // Force close remaining connections
  const remaining = await io.engine.clientsCount
  if (remaining > 0) {
    logger.warn({ count: remaining }, 'Force closing remaining connections')
    for (const socket of await io.fetchSockets()) {
      socket.disconnect(true)
    }
  }
}
```

## Sticky Session Configuration

```yaml
# Kubernetes Ingress with NGINX for sticky sessions
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: websocket-ingress
  annotations:
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "ws-sid"
    nginx.ingress.kubernetes.io/session-cookie-expires: "86400"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "86400"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-body-size: "1m"
    nginx.ingress.kubernetes.io/server-snippet: |
      location /socket.io/ {
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
      }
spec:
  rules:
    - host: ws.voiceplatform.com
      http:
        paths:
          - path: /socket.io
            pathType: Prefix
            backend:
              service:
                name: websocket-service
                port:
                  number: 3001
```

## Multi-Region Deployment

```typescript
// server/websocket/regions.ts
// Cross-region event forwarding for global deployment

interface RegionConfig {
  name: string
  wsUrl: string
  redisUrl: string
}

const REGIONS: RegionConfig[] = [
  { name: 'us-east', wsUrl: 'wss://us-east.ws.voiceplatform.com', redisUrl: process.env.REDIS_US_EAST! },
  { name: 'eu-west', wsUrl: 'wss://eu-west.ws.voiceplatform.com', redisUrl: process.env.REDIS_EU_WEST! },
  { name: 'ap-southeast', wsUrl: 'wss://ap-southeast.ws.voiceplatform.com', redisUrl: process.env.REDIS_AP_SOUTHEAST! }
]

export class CrossRegionEventBridge {
  private redis: Redis
  private channel = 'ws:cross-region'

  constructor(redis: Redis) {
    this.redis = redis
    this.startListening()
  }

  // Forward an event to all regions
  async broadcastToAllRegions(event: string, data: unknown, excludeRegion?: string) {
    const message = {
      event,
      data,
      sourceRegion: process.env.REGION,
      timestamp: new Date().toISOString()
    }

    await this.redis.publish(this.channel, JSON.stringify(message))
  }

  // Listen for events from other regions
  private startListening() {
    this.redis.subscribe(this.channel, (err) => {
      if (err) {
        logger.error({ err }, 'Failed to subscribe to cross-region channel')
        return
      }
    })

    this.redis.on('message', (channel, message) => {
      if (channel !== this.channel) return

      const { event, data, sourceRegion } = JSON.parse(message)

      // Don't process our own events
      if (sourceRegion === process.env.REGION) return

      // Emit to local WebSocket connections
      const { io } = require('./server')
      io.emit(event, data)
    })
  }
}
```

## Monitoring WebSocket Cluster

```typescript
// Prometheus metrics for WebSocket cluster
import prometheus from 'prom-client'

export const wsMetrics = {
  connections: new prometheus.Gauge({
    name: 'ws_connections_total',
    help: 'Current number of WebSocket connections',
    labelNames: ['node_id', 'region']
  }),

  rooms: new prometheus.Gauge({
    name: 'ws_rooms_total',
    help: 'Current number of rooms',
    labelNames: ['node_id']
  }),

  messagesIn: new prometheus.Counter({
    name: 'ws_messages_in_total',
    help: 'Messages received from clients',
    labelNames: ['event_type']
  }),

  messagesOut: new prometheus.Counter({
    name: 'ws_messages_out_total',
    help: 'Messages sent to clients',
    labelNames: ['event_type']
  }),

  eventLatency: new prometheus.Histogram({
    name: 'ws_event_latency_ms',
    help: 'Event delivery latency in ms',
    labelNames: ['event_type'],
    buckets: [5, 10, 25, 50, 100, 250, 500]
  }),

  reconnections: new prometheus.Counter({
    name: 'ws_reconnections_total',
    help: 'Client reconnections',
    labelNames: ['reason']
  }),

  redisPubLatency: new prometheus.Histogram({
    name: 'ws_redis_pub_latency_ms',
    help: 'Redis pub/sub latency',
    buckets: [1, 5, 10, 25, 50]
  })
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Scaling Method | Redis pub/sub adapter | Battle-tested, built into Socket.IO |
| Sticky Sessions | Cookie-based affinity | Required for Socket.IO HTTP fallback |
| Connection Registry | Redis hash sets | Fast lookup, TTL-based cleanup |
| Multi-Region | Redis cross-region pub/sub | Forward events between geographic clusters |
| Shutdown | Graceful drain with client notification | Zero-downtime deployments |

## Integration Points

- **Part 23 (DevOps/CI-CD)** — K8s deployment configuration for WebSocket
- **Part 24 (Scaling)** — Horizontal scaling of real-time layer
- **Part 04 (Real-Time)** — Core scaling mechanism for WebSocket

## Production Considerations

- **Redis Performance**: Redis handles 100K+ msg/sec on a single node; scale to cluster for higher
- **Sticky Session Impact**: Uneven distribution if sessions aren't evenly balanced
- **Network Latency**: Cross-region event forwarding adds 50-200ms depending on distance
- **Failure Mode**: If Redis goes down, WebSocket still works but new connections must hit the same node
- **Cost**: Redis Cluster with replication costs $100-500/mo depending on size
- **Load Testing**: Test with 10K+ concurrent connections across multiple nodes before production
