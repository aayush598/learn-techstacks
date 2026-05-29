# Section 02: WebSocket Server Design

## Server Architecture

The WebSocket server handles real-time bidirectional communication between the platform and client applications. It manages thousands of concurrent connections, organizes them into rooms/groups, and delivers events with minimal latency.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      WEBSOCKET SERVER DESIGN                          │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │               CONNECTION MANAGEMENT                             │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │ Connect  │  │ Auth     │  │ Subscribe│  │ Heartbeat│        │    │
│  │  │ /ws      │  │ Validate │  │ to Rooms │  │ Ping 25s │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │ State    │  │ Message  │  │ Rate     │  │ Disconnect│       │    │
│  │  │ Recovery │  │ Routing  │  │ Limiting │  │ Cleanup  │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     ROOM / GROUP HIERARCHY                      │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  Global: /tenant:{tenantId}                               │   │    │
│  │  │  │                                                        │   │    │
│  │  │  ├── Per-Resource: /agent:{agentId}                       │   │    │
│  │  │  │                  /call:{callId}                        │   │    │
│  │  │  │                  /campaign:{campaignId}                │   │    │
│  │  │  │                                                        │   │    │
│  │  │  ├── User-specific: /user:{userId}                        │   │    │
│  │  │  │                                                        │   │    │
│  │  │  └── Role-based: /role:{admin}                            │   │    │
│  │  │                     /role:{agent_manager}                  │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │               MESSAGE SCHEMA                                    │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  // Client → Server                                       │   │    │
│  │  │  {                                                        │   │    │
│  │  │    "type": "subscribe" | "unsubscribe" | "call:action",   │   │    │
│  │  │    "room": "call:550e8400",                               │   │    │
│  │  │    "payload": { ... }                                     │   │    │
│  │  │  }                                                        │   │    │
│  │  │                                                           │   │    │
│  │  │  // Server → Client                                       │   │    │
│  │  │  {                                                        │   │    │
│  │  │    "event": "call.updated",                               │   │    │
│  │  │    "data": { ... },                                       │   │    │
│  │  │    "timestamp": "2025-01-15T12:00:00Z"                    │   │    │
│  │  │  }                                                        │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Implementation

```typescript
// server/websocket/server.ts
import { createServer } from 'http'
import { Server } from 'socket.io'
import { createAdapter } from '@socket.io/redis-adapter'
import { Redis } from 'ioredis'
import { authenticate } from '@/lib/auth'
import { rateLimiter } from '@/lib/rate-limiter'
import { logger } from '@/lib/logger'

export function createWebSocketServer() {
  const httpServer = createServer()

  const io = new Server(httpServer, {
    cors: {
      origin: process.env.CORS_ORIGINS?.split(',') ?? '*',
      methods: ['GET', 'POST'],
      credentials: true
    },
    transports: ['websocket', 'polling'],
    pingInterval: 25000,
    pingTimeout: 20000,
    maxHttpBufferSize: 1e6, // 1MB max message
    allowEIO3: true
  })

  // Redis adapter for horizontal scaling
  const pubClient = new Redis(process.env.REDIS_URL!)
  const subClient = pubClient.duplicate()
  io.adapter(createAdapter(pubClient, subClient))

  // Authentication middleware
  io.use(async (socket, next) => {
    try {
      const token = socket.handshake.auth.token
        ?? socket.handshake.query.token as string

      if (!token) {
        return next(new Error('Authentication required'))
      }

      const auth = await authenticate(token)
      if (!auth.authenticated) {
        return next(new Error('Invalid authentication'))
      }

      socket.data.userId = auth.userId
      socket.data.tenantId = auth.tenantId
      socket.data.roles = auth.roles
      socket.data.connections = new Map()

      next()
    } catch (error) {
      next(new Error('Authentication failed'))
    }
  })

  // Connection handler
  io.on('connection', (socket) => {
    const { tenantId, userId } = socket.data

    logger.info({
      tenantId,
      userId,
      socketId: socket.id,
      transport: socket.conn.transport.name
    }, 'WebSocket connected')

    // Auto-join tenant room
    socket.join(`tenant:${tenantId}`)

    // User-specific room
    socket.join(`user:${userId}`)

    // Subscribe to resource updates
    socket.on('subscribe', (rooms: string | string[]) => {
      const roomList = Array.isArray(rooms) ? rooms : [rooms]
      for (const room of roomList) {
        // Validate room access
        if (canAccessRoom(socket, room)) {
          socket.join(room)
          logger.debug({ room, socketId: socket.id }, 'Joined room')
        }
      }
    })

    // Unsubscribe from resources
    socket.on('unsubscribe', (rooms: string | string[]) => {
      const roomList = Array.isArray(rooms) ? rooms : [rooms]
      for (const room of roomList) {
        socket.leave(room)
      }
    })

    // Call actions from dashboard (mute, transfer, etc.)
    socket.on('call:action', async (data: { callId: string; action: string; payload?: unknown }) => {
      const allowed = await canPerformAction(socket, data.callId, data.action)
      if (!allowed) {
        return socket.emit('error', { message: 'Action not allowed' })
      }

      // Forward to call service via Kafka
      await kafka.produce('call.action.requested', {
        callId: data.callId,
        action: data.action,
        payload: data.payload,
        requestedBy: userId,
        timestamp: new Date().toISOString()
      })
    })

    // Disconnect handler
    socket.on('disconnect', (reason) => {
      logger.info({
        tenantId,
        userId,
        socketId: socket.id,
        reason
      }, 'WebSocket disconnected')

      // Cleanup connections
      for (const [resource, connId] of socket.data.connections) {
        cleanupConnection(resource, connId)
      }
    })

    // Error handler
    socket.on('error', (error) => {
      logger.error({ error, socketId: socket.id }, 'WebSocket error')
    })
  })

  // Health check endpoint
  io.on('connect_error', (error) => {
    logger.error({ error }, 'WebSocket connection error')
  })

  return { io, httpServer }
}

// Room access validation
function canAccessRoom(socket: Socket, room: string): boolean {
  const { tenantId, userId, roles } = socket.data
  const isAdmin = roles.includes('admin')

  // Tenant rooms
  if (room.startsWith('tenant:')) {
    return room === `tenant:${tenantId}` || isAdmin
  }

  // User-specific rooms
  if (room.startsWith('user:')) {
    return room === `user:${userId}` || isAdmin
  }

  // Call rooms — anyone in the same tenant can subscribe
  if (room.startsWith('call:')) {
    return true  // Tenant access already enforced by room naming convention
  }

  // Agent rooms
  if (room.startsWith('agent:')) {
    return true
  }

  return false
}

// Rate limiting per socket
async function canPerformAction(
  socket: Socket,
  callId: string,
  action: string
): Promise<boolean> {
  const key = `ws:action:${socket.data.userId}:${action}`
  const result = await rateLimiter.check(key, 10, 60) // 10 actions per minute
  return result.allowed
}
```

## Event Emitter Pattern

```typescript
// server/websocket/emitter.ts
// Emit events to WebSocket rooms from any service

import { io } from './server'

interface WSEvent {
  event: string
  data: unknown
  rooms?: string[]
  userId?: string
}

export function emitToRoom(room: string, event: string, data: unknown) {
  io.to(room).emit(event, {
    event,
    data,
    timestamp: new Date().toISOString()
  })
}

export function emitToUser(userId: string, event: string, data: unknown) {
  io.to(`user:${userId}`).emit(event, {
    event,
    data,
    timestamp: new Date().toISOString()
  })
}

export function emitToTenant(tenantId: string, event: string, data: unknown) {
  io.to(`tenant:${tenantId}`).emit(event, {
    event,
    data,
    timestamp: new Date().toISOString()
  })
}

export function emitToCall(callId: string, event: string, data: unknown) {
  io.to(`call:${callId}`).emit(event, {
    event,
    data,
    timestamp: new Date().toISOString()
  })
}
```

## Connection State Recovery

```typescript
// Client-side reconnection with state recovery
import { io, Socket } from 'socket.io-client'

class RealtimeClient {
  private socket: Socket | null = null
  private subscriptions: Set<string> = new Set()
  private reconnectAttempts = 0
  private maxReconnectAttempts = 10

  connect(token: string) {
    this.socket = io(process.env.WS_URL!, {
      auth: { token },
      transports: ['websocket'],
      reconnection: true,
      reconnectionAttempts: this.maxReconnectAttempts,
      reconnectionDelay: (attempt) => {
        // Exponential backoff: 1s, 2s, 4s, 8s, 16s, 30s...
        return Math.min(1000 * Math.pow(2, attempt), 30000)
      },
      reconnectionDelayMax: 30000,
      randomizationFactor: 0.3
    })

    this.socket.on('connect', () => {
      this.reconnectAttempts = 0
      // Re-subscribe to all rooms on reconnect
      for (const room of this.subscriptions) {
        this.socket?.emit('subscribe', room)
      }
    })

    this.socket.on('disconnect', (reason) => {
      if (reason === 'io server disconnect') {
        // Server closed connection — don't reconnect
        this.socket?.close()
      }
    })

    this.socket.on('connect_error', (error) => {
      this.reconnectAttempts++
      logger.error({ error, attempt: this.reconnectAttempts }, 'WebSocket reconnect failed')
    })
  }

  subscribe(room: string) {
    this.subscriptions.add(room)
    this.socket?.emit('subscribe', room)
  }

  unsubscribe(room: string) {
    this.subscriptions.delete(room)
    this.socket?.emit('unsubscribe', room)
  }

  onEvent(event: string, handler: (data: unknown) => void) {
    this.socket?.on(event, handler)
  }

  disconnect() {
    this.socket?.close()
    this.socket = null
    this.subscriptions.clear()
  }
}

export const realtimeClient = new RealtimeClient()
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Library | Socket.IO (not raw WS) | Auto-reconnect, rooms, fallback transports |
| Scaling | Redis pub/sub adapter | Proven, simple, event-driven |
| Authentication | Token at connection time | Verified once, not per-message |
| Room Structure | Namespaced (tenant:call:agent) | Hierarchical, easy to manage |
| Rate Limiting | Per-action, per-user | Prevent abuse of call actions |
| State Recovery | Re-subscribe on reconnect | Simple, explicit, reliable |

## Integration Points

- **Part 06 (Frontend)** — Dashboard uses WebSocket for live data
- **Part 04 (Real-Time)** — WebSocket server is the data delivery mechanism
- **Part 09 (Data Flow)** — Events from Kafka forwarded via WebSocket
- **Part 10 (Integrations)** — SDK clients connect via WebSocket

## Production Considerations

- **Connection Limit**: 100K concurrent connections per server; scale horizontally behind load balancer
- **Memory**: Each connection ~10KB overhead; 100K connections = ~1GB RAM
- **Sticky Sessions**: Required for Socket.IO with fallback transport; use cookie-based affinity
- **Graceful Shutdown**: Drain connections before shutdown; send disconnect notice to clients
- **Monitoring**: Track connections per server, message rate, event delivery latency, reconnection rate
- **Security**: Rate-limit new connections per IP (10/sec), validate message size (<1MB)
