# Section 05: Presence & Availability

## Presence Architecture

The presence system tracks user connection state across multiple devices and surfaces. It enables real-time visibility into who is online, their current activity status, and whether they're available for calls or other tasks.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      PRESENCE & AVAILABILITY SYSTEM                   │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    PRESENCE STATES                               │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │    │
│  │  │  Online  │  │  Away    │  │  Busy    │  │  Offline │        │    │
│  │  │          │  │          │  │          │  │          │        │    │
│  │  │ • Active │  │ • Idle   │  │ • On Call│  │ • Disconn│        │    │
│  │  │ • Connected│ │ >5 min   │  │ • In Meet│  │ • Closed │        │    │
│  │  │ • Available│ │ • AFK    │  │ • Do Not │  │ • Expired│        │    │
│  │  │          │  │          │  │   Disturb│  │          │        │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  State Transitions:                                                    │
│  ┌─────────┐  active   ┌─────────┐  idle >5m  ┌─────────┐            │
│  │ Offline │──────────▶│  Online │───────────▶│  Away   │            │
│  └─────────┘           └─────────┘            └─────────┘            │
│       ▲                                         │    │                │
│       │              ┌─────────┐                │    │                │
│       │              │  Busy   │◀───────────────┘    │                │
│       │              └─────────┘                    │                │
│       │                 │                           │                │
│       └─────────────────┴───────────────────────────┘                │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                MULTI-DEVICE MANAGEMENT                          │  │
│  │                                                                  │  │
│  │  User: alice@acme.com                                           │  │
│  │                                                                  │  │
│  │  ├── Device: Chrome Desktop (WebSocket connected, active)       │  │
│  │  ├── Device: Safari Laptop (WebSocket connected, idle)          │  │
│  │  └── Device: Mobile App (WebSocket connected, background)       │  │
│  │                                                                  │  │
│  │  Aggregate State: Online (at least one active device)           │  │
│  │  Aggregate Availability: Available (no device on a call)        │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Implementation

```typescript
// server/presence/presence-service.ts
import { Redis } from 'ioredis'
import { logger } from '@/lib/logger'

interface PresenceState {
  userId: string
  tenantId: string
  status: PresenceStatus
  activity: string | null        // Current activity (e.g., "In call", "Editing agent")
  lastSeen: Date
  lastActivity: Date
  devices: DeviceInfo[]
  currentCallId?: string
  metadata?: Record<string, unknown>
}

interface DeviceInfo {
  id: string
  type: 'browser' | 'mobile' | 'desktop' | 'api'
  name: string
  status: 'active' | 'idle' | 'background' | 'disconnected'
  lastSeen: Date
  ip?: string
  userAgent?: string
}

type PresenceStatus = 'online' | 'away' | 'busy' | 'offline'

export class PresenceService {
  private redis: Redis
  private readonly PRESENCE_TTL = 120  // 2 minutes TTL for presence keys
  private readonly IDLE_THRESHOLD = 5 * 60 * 1000  // 5 minutes
  private readonly AWAY_THRESHOLD = 30 * 60 * 1000  // 30 minutes

  constructor(redis: Redis) {
    this.redis = redis
  }

  // Called when a user connects
  async userConnected(
    userId: string,
    tenantId: string,
    device: Omit<DeviceInfo, 'lastSeen'>
  ): Promise<void> {
    const deviceKey = `presence:device:${userId}:${device.id}`
    const userKey = `presence:user:${userId}`
    const tenantKey = `presence:tenant:${tenantId}`

    const now = new Date()

    // Store device info
    await this.redis.hset(deviceKey, {
      ...device,
      lastSeen: now.toISOString(),
      status: 'active'
    })
    await this.redis.expire(deviceKey, this.PRESENCE_TTL)

    // Add to tenant's online set
    await this.redis.sadd(tenantKey, userId)
    await this.redis.expire(tenantKey, this.PRESENCE_TTL)

    // Compute aggregate state
    const aggregateStatus = await this.computeAggregateStatus(userId)

    // Update user presence
    await this.redis.hset(userKey, {
      userId,
      tenantId,
      status: aggregateStatus,
      lastSeen: now.toISOString(),
      lastActivity: now.toISOString()
    })
    await this.redis.expire(userKey, this.PRESENCE_TTL)

    // Broadcast presence update
    await this.broadcastPresence(userId, tenantId, aggregateStatus)
  }

  // Called when a user disconnects
  async userDisconnected(userId: string, deviceId: string): Promise<void> {
    const deviceKey = `presence:device:${userId}:${deviceId}`
    const userKey = `presence:user:${userId}`

    await this.redis.del(deviceKey)

    // Check remaining devices
    const remainingDevices = await this.getUserDevices(userId)

    if (remainingDevices.length === 0) {
      // No more devices — user is offline
      await this.redis.hset(userKey, {
        status: 'offline',
        lastSeen: new Date().toISOString()
      })
      await this.redis.expire(userKey, this.PRESENCE_TTL)

      await this.broadcastPresence(userId, await this.getUserTenant(userId), 'offline')
    } else {
      // Recompute based on remaining devices
      const status = await this.computeAggregateStatus(userId)
      await this.redis.hset(userKey, { status, lastSeen: new Date().toISOString() })
      await this.broadcastPresence(userId, await this.getUserTenant(userId), status)
    }
  }

  // Called when user activity detected (heartbeat, click, etc.)
  async userActivity(userId: string, deviceId: string, activity?: string): Promise<void> {
    const deviceKey = `presence:device:${userId}:${deviceId}`
    const userKey = `presence:user:${userId}`
    const now = new Date()

    await this.redis.hset(deviceKey, {
      lastSeen: now.toISOString(),
      status: 'active'
    })
    await this.redis.expire(deviceKey, this.PRESENCE_TTL)

    await this.redis.hset(userKey, {
      lastActivity: now.toISOString(),
      activity: activity ?? null
    })
    await this.redis.expire(userKey, this.PRESENCE_TTL)

    // If user was away, restore to online
    const current = await this.getUserPresence(userId)
    if (current?.status === 'away') {
      await this.broadcastPresence(userId, current.tenantId, 'online')
    }
  }

  // Periodically check for idle users
  async checkIdleUsers(): Promise<void> {
    const tenantKeys = await this.redis.keys('presence:tenant:*')

    for (const tenantKey of tenantKeys) {
      const userIds = await this.redis.smembers(tenantKey)
      const now = Date.now()

      for (const userId of userIds) {
        const presence = await this.getUserPresence(userId)
        if (!presence) continue

        const lastActivity = new Date(presence.lastActivity).getTime()
        const timeSinceActivity = now - lastActivity

        if (timeSinceActivity > this.AWAY_THRESHOLD && presence.status !== 'busy') {
          await this.setUserStatus(userId, 'away')
          await this.broadcastPresence(userId, presence.tenantId, 'away')
        } else if (timeSinceActivity > this.IDLE_THRESHOLD && presence.status === 'online') {
          await this.setUserStatus(userId, 'away')
          await this.broadcastPresence(userId, presence.tenantId, 'away')
        }
      }
    }
  }

  // Set user as busy (e.g., on a call)
  async setUserBusy(userId: string, callId: string): Promise<void> {
    const userKey = `presence:user:${userId}`
    await this.redis.hset(userKey, {
      status: 'busy',
      currentCallId: callId,
      lastSeen: new Date().toISOString()
    })
    await this.redis.expire(userKey, this.PRESENCE_TTL)

    const tenantId = await this.getUserTenant(userId)
    if (tenantId) {
      await this.broadcastPresence(userId, tenantId, 'busy')
    }
  }

  // Set user available after call
  async setUserAvailable(userId: string): Promise<void> {
    const userKey = `presence:user:${userId}`
    await this.redis.hdel(userKey, 'currentCallId')
    await this.redis.hset(userKey, {
      status: 'online',
      lastSeen: new Date().toISOString()
    })
    await this.redis.expire(userKey, this.PRESENCE_TTL)

    const tenantId = await this.getUserTenant(userId)
    if (tenantId) {
      await this.broadcastPresence(userId, tenantId, 'online')
    }
  }

  // Get online users in a tenant
  async getOnlineUsers(tenantId: string): Promise<PresenceState[]> {
    const userIds = await this.redis.smembers(`presence:tenant:${tenantId}`)
    const presences = await Promise.all(
      userIds.map(uid => this.getUserPresence(uid))
    )
    return presences.filter((p): p is PresenceState => p !== null)
  }

  // Get single user presence
  async getUserPresence(userId: string): Promise<PresenceState | null> {
    const data = await this.redis.hgetall(`presence:user:${userId}`)
    if (!data || Object.keys(data).length === 0) return null

    return {
      userId: data.userId,
      tenantId: data.tenantId,
      status: data.status as PresenceStatus,
      activity: data.activity ?? null,
      lastSeen: new Date(data.lastSeen),
      lastActivity: new Date(data.lastActivity),
      devices: await this.getUserDevices(userId),
      currentCallId: data.currentCallId
    }
  }

  private async getUserDevices(userId: string): Promise<DeviceInfo[]> {
    const deviceKeys = await this.redis.keys(`presence:device:${userId}:*`)
    const devices: DeviceInfo[] = []

    for (const key of deviceKeys) {
      const data = await this.redis.hgetall(key)
      if (data && data.id) {
        devices.push({
          id: data.id,
          type: data.type as DeviceInfo['type'],
          name: data.name,
          status: data.status as DeviceInfo['status'],
          lastSeen: new Date(data.lastSeen),
          ip: data.ip
        })
      }
    }

    return devices
  }

  private async computeAggregateStatus(userId: string): Promise<PresenceStatus> {
    const devices = await this.getUserDevices(userId)

    if (devices.length === 0) return 'offline'

    const hasActive = devices.some(d => d.status === 'active')
    const hasBusy = devices.some(d => d.status === 'background')
    const hasCall = await this.redis.hexists(`presence:user:${userId}`, 'currentCallId')

    if (hasCall) return 'busy'
    if (hasActive) return 'online'
    if (hasBusy) return 'away'
    return 'offline'
  }

  private async broadcastPresence(
    userId: string,
    tenantId: string,
    status: PresenceStatus
  ): Promise<void> {
    const { io } = await import('@/server/websocket/server')
    io.to(`tenant:${tenantId}`).emit('user.presence', {
      userId,
      status,
      timestamp: new Date().toISOString()
    })
  }

  private async getUserTenant(userId: string): Promise<string | null> {
    const data = await this.redis.hget(`presence:user:${userId}`, 'tenantId')
    return data ?? null
  }

  private async setUserStatus(userId: string, status: PresenceStatus): Promise<void> {
    await this.redis.hset(`presence:user:${userId}`, { status })
  }
}
```

## Presence Heartbeat

```typescript
// Client-side presence heartbeat
class PresenceClient {
  private heartbeatInterval: NodeJS.Timeout | null = null
  private readonly HEARTBEAT_INTERVAL = 30000  // 30 seconds
  private readonly IDLE_TIMEOUT = 300000       // 5 minutes
  private lastActivity = Date.now()
  private socket: Socket

  constructor(socket: Socket) {
    this.socket = socket
    this.setupActivityTracking()
    this.startHeartbeat()
  }

  private setupActivityTracking() {
    const events = ['mousemove', 'keydown', 'click', 'scroll', 'touchstart']
    for (const event of events) {
      window.addEventListener(event, () => {
        this.lastActivity = Date.now()
      })
    }
  }

  private startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      const now = Date.now()
      const idleTime = now - this.lastActivity

      let status: 'active' | 'idle' | 'away' = 'active'
      if (idleTime > 300000) status = 'away'       // >5 min
      else if (idleTime > 60000) status = 'idle'    // >1 min

      this.socket.emit('presence:heartbeat', {
        status,
        timestamp: new Date().toISOString(),
        activeTab: document.visibilityState === 'visible',
        page: window.location.pathname
      })

      this.lastActivity = now
    }, this.HEARTBEAT_INTERVAL)
  }

  destroy() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval)
    }
  }
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Storage | Redis (not PostgreSQL) | Ephemeral, fast, TTL-based, pub/sub for broadcast |
| Heartbeat | 30-second intervals | Balances accuracy vs load |
| Idle Detection | Client-side activity + server timeout | Accurate even if client stops sending |
| Multi-Device | Aggregated state per user | One presence per user, not per device |
| TTL | 2 minutes (double heartbeat) | Auto-cleanup of stale connections |

## Integration Points

- **Part 16 (User Management)** — Presence linked to user accounts
- **Part 08 (Human Hand-off)** — Agent availability determines routing
- **Part 06 (Frontend)** — UI shows presence indicators

## Production Considerations

- **Scale**: 10K users × 30s heartbeat = ~333 writes/sec to Redis (easily handled)
- **Cleanup**: TTL auto-cleans stale presence; monitor for orphaned keys
- **Idle Detection**: Don't mark away during calls (busy overrides idle)
- **Privacy**: Allow users to set invisible/offline status manually
- **Monitoring**: Track active users, average session duration, device distribution
