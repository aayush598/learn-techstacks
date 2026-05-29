# Section 03: Room/Channel Subscription

## Overview

WebSocket clients subscribe to channels to receive events. Channels are named topics that follow hierarchical patterns — `tenant:{id}`, `call:{id}`, `agent:{id}`. The subscription management system handles subscribe/unsubscribe messages, validates authorization per channel, and maintains the subscription registry in Redis for horizontal scaling.

## Architecture

```
Channel Subscription Model
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Channel Hierarchies:
  tenant:tenant_xyz           → All events for a tenant
  tenant:tenant_xyz:call:*    → All call events for a tenant
  call:call_def_456           → Events for a specific call
  agent:agent_abc_789         → Events for a specific agent
  system:maintenance          → System-wide announcements

Subscription Flow:
  [Client]                           [Server]
     │                                   │
     │── {"type":"subscribe","channel":  │
     │    "call:call_def_456"}          │
     │                                   │── Auth check: can subscribe?
     │                                   │── Add to subscriber registry
     │                                   │── Join Redis pub/sub channel
     │←── {"type":"subscribed",         │
     │     "channel":"call:call_def_456"}│
     │                                   │
     │── [Event published to channel]    │
     │←── {"type":"call.status_changed", │
     │     "channel":"call:call_def_456",│
     │     "data":{...}}                 │
     │                                   │
     │── {"type":"unsubscribe",          │
     │     "channel":"call:call_def_456"}│
     │                                   │── Remove from registry
     │                                   │── Leave Redis channel
```

## Design Decisions

- **Explicit Subscribe/Unsubscribe**: Clients send subscription messages — no implicit subscription on connect
- **Channel-Level Authorization**: Permissions checked per channel — a client may subscribe to `agent:abc` but not `agent:xyz`
- **Wildcard Subscriptions**: `tenant:tenant_xyz:*` subscribes to all sub-channels under a tenant
- **Redis Pub/Sub**: Channel subscriptions map to Redis pub/sub channels for horizontal scaling

## Implementation Approach

```typescript
// Channel subscription types
interface SubscribeMessage {
  type: 'subscribe';
  channel: string;
}

interface UnsubscribeMessage {
  type: 'unsubscribe';
  channel: string;
}

interface SubscribedMessage {
  type: 'subscribed';
  channel: string;
  subscribedAt: string;
}

interface UnsubscribedMessage {
  type: 'unsubscribed';
  channel: string;
}

// Channel authorization
interface ChannelPermission {
  channelPattern: RegExp;
  requiredScopes: string[];
}

class ChannelAuthorizer {
  private permissions: ChannelPermission[] = [
    { channelPattern: /^tenant:[a-z0-9_]+$/, requiredScopes: ['events:read'] },
    { channelPattern: /^call:[a-z0-9_]+$/, requiredScopes: ['calls:read'] },
    { channelPattern: /^agent:[a-z0-9_]+$/, requiredScopes: ['agents:read'] },
    { channelPattern: /^campaign:[a-z0-9_]+$/, requiredScopes: ['campaigns:read'] },
  ];

  authorize(channel: string, scopes: string[]): boolean {
    const matching = this.permissions.find(p => p.channelPattern.test(channel));

    if (!matching) {
      return false; // Unknown channel pattern
    }

    return matching.requiredScopes.every(scope => scopes.includes(scope));
  }
}

// Subscription manager with Redis
class SubscriptionManager {
  private subscriptions: Map<string, Set<string>> = new Map(); // connectionId → Set<channel>
  private authorizer = new ChannelAuthorizer();
  private redis: Redis;

  constructor(redis: Redis) {
    this.redis = redis;
  }

  async subscribe(
    connectionId: string,
    channel: string,
    authContext: AuthContext,
  ): Promise<boolean> {
    // Authorize
    if (!this.authorizer.authorize(channel, authContext.scopes)) {
      return false;
    }

    // Track subscription locally
    if (!this.subscriptions.has(connectionId)) {
      this.subscriptions.set(connectionId, new Set());
    }
    this.subscriptions.get(connectionId)!.add(channel);

    // Subscribe to Redis pub/sub
    const subscriberCount = await this.redis.sadd(`channel:subs:${channel}`, connectionId);
    if (subscriberCount === 1) {
      // First subscriber — subscribe Redis to this channel
      await this.redis.subscribe(channel);
    }

    return true;
  }

  async unsubscribe(connectionId: string, channel: string): Promise<void> {
    const connSubs = this.subscriptions.get(connectionId);
    if (connSubs) {
      connSubs.delete(channel);
      if (connSubs.size === 0) {
        this.subscriptions.delete(connectionId);
      }
    }

    const remaining = await this.redis.srem(`channel:subs:${channel}`, connectionId);
    if (remaining === 0) {
      await this.redis.unsubscribe(channel); // Last subscriber — unsubscribe
    }
  }

  async unsubscribeAll(connectionId: string): Promise<void> {
    const channels = this.subscriptions.get(connectionId);
    if (channels) {
      for (const channel of channels) {
        await this.unsubscribe(connectionId, channel);
      }
    }
  }

  getConnectionChannels(connectionId: string): string[] {
    return Array.from(this.subscriptions.get(connectionId) || []);
  }
}

// Message router
class MessageRouter {
  constructor(private subscriptionManager: SubscriptionManager) {}

  async handleIncoming(connectionId: string, message: unknown): Promise<void> {
    const msg = message as { type: string };

    switch (msg.type) {
      case 'subscribe': {
        const subMsg = msg as SubscribeMessage;
        await this.subscriptionManager.subscribe(connectionId, subMsg.channel);
        break;
      }
      case 'unsubscribe': {
        const unsubMsg = msg as UnsubscribeMessage;
        await this.subscriptionManager.unsubscribe(connectionId, unsubMsg.channel);
        break;
      }
      default:
        throw new Error(`Unknown message type: ${msg.type}`);
    }
  }
}
```

## Integration Points

- **Redis Pub/Sub**: Cross-server event distribution via Redis channels
- **Auth Service**: Channel permission evaluation during subscription
- **SDK**: Simplified subscribe API — `client.events.subscribe('call:*', handler)`

## Production Considerations

- **Channel Limits**: Maximum 100 subscriptions per connection; prevent resource exhaustion
- **Wildcard Expansion**: Wildcard subscriptions are expanded to individual channel subscriptions at subscribe time
- **Subscription Persistence**: On reconnect, restore previous subscriptions from Redis
- **Authorization Caching**: Channel permissions are cached for 5 minutes to reduce auth service load

## Open-Source Tools

- **Redis Pub/Sub**: Channel-based message distribution across WebSocket servers
- **ioredis**: Robust Redis client with pub/sub support
