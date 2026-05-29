# Section 05: Heartbeat & Keepalive

## Overview

Heartbeat mechanisms maintain WebSocket connection health by detecting silent disconnections. The server sends periodic ping frames; clients respond with pong frames. If a pong is not received within the timeout window, the connection is considered dead and closed. Heartbeat intervals are configurable per connection profile, and health metrics are tracked for monitoring.

## Architecture

```
Heartbeat Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Server-Initiated Heartbeat:
  [Server]                            [Client]
     │──── Ping Frame ────────────────→│
     │                                  │
     │←─── Pong Frame ─────────────────│
     │                                  │
     │ [Reset heartbeat timer]          │
     │                                  │
     │──── [Wait 10 seconds] ──────────│
     │                                  │
     │──── Ping Frame ────────────────→│
     │                                  │
     │ [No pong received in 30s]        │
     │                                  │
     │ [Close connection — 4400]        │
     │── Close Frame ────────────────→│
     │                                  │
     │ [Clean up subscriptions]         │

Heartbeat Timing:
  Ping interval:  10 seconds
  Pong timeout:   30 seconds (3 missed pings)
  Grace period:   5 seconds after close for last-message delivery

Connection Health Metrics:
  ┌─────────────────────────────────────┐
  │ Connection: ws_abc_123              │
  │ Uptime: 45m 23s                     │
  │ Last Pong: 2s ago                   │
  │ Avg Round Trip: 45ms                │
  │ Missed Pings: 0                     │
  │ Messages Sent: 1,234                │
  │ Messages Recv: 56                   │
  └─────────────────────────────────────┘
```

## Design Decisions

- **Server-Initiated Heartbeats**: Server controls heartbeat timing; clients only respond to pings
- **Ping/Pong Over Custom Messages**: WebSocket protocol-level ping/pong frames are more efficient than application-level messages
- **Missing Pong Threshold**: 3 consecutive missed pings before closing — tolerates transient network issues
- **Round-Trip Latency Tracking**: Timestamp pings to measure connection latency; exposed in connection metrics

## Implementation Approach

```typescript
// Heartbeat configuration
interface HeartbeatConfig {
  pingInterval: number;  // ms — time between pings
  pongTimeout: number;   // ms — wait for pong before considering dead
  maxMissedPings: number; // consecutive missed pings before close
}

const DEFAULT_HEARTBEAT_CONFIG: HeartbeatConfig = {
  pingInterval: 10_000,
  pongTimeout: 30_000,
  maxMissedPings: 3,
};

// Heartbeat manager
class HeartbeatManager {
  private pingInterval?: NodeJS.Timeout;
  private pongTimeout?: NodeJS.Timeout;
  private missedPings = 0;
  private lastPongAt: Date = new Date();
  private roundTripHistory: number[] = [];

  constructor(
    private ws: WebSocket,
    private connectionId: string,
    private config: HeartbeatConfig = DEFAULT_HEARTBEAT_CONFIG,
    private onDead: (connectionId: string) => void,
  ) {}

  start(): void {
    this.pingInterval = setInterval(() => this.sendPing(), this.config.pingInterval);
  }

  stop(): void {
    if (this.pingInterval) {
      clearInterval(this.pingInterval);
      this.pingInterval = undefined;
    }
    if (this.pongTimeout) {
      clearTimeout(this.pongTimeout);
      this.pongTimeout = undefined;
    }
  }

  handlePong(): void {
    this.missedPings = 0;
    this.lastPongAt = new Date();

    if (this.pongTimeout) {
      clearTimeout(this.pongTimeout);
      this.pongTimeout = undefined;
    }

    // Track round-trip time
    const rtt = Date.now() - this.lastPingTimestamp;
    this.roundTripHistory.push(rtt);
    if (this.roundTripHistory.length > 100) {
      this.roundTripHistory.shift();
    }
  }

  private lastPingTimestamp = 0;

  private sendPing(): void {
    try {
      this.lastPingTimestamp = Date.now();
      this.ws.ping();

      this.pongTimeout = setTimeout(() => {
        this.missedPings++;

        if (this.missedPings >= this.config.maxMissedPings) {
          console.warn(`Connection ${this.connectionId} dead after ${this.missedPings} missed pings`);
          this.ws.close(4400, 'Heartbeat timeout');
          this.onDead(this.connectionId);
        }
      }, this.config.pongTimeout);
    } catch (error) {
      console.error(`Failed to send ping to ${this.connectionId}:`, error);
      this.onDead(this.connectionId);
    }
  }

  getMetrics(): HeartbeatMetrics {
    return {
      connectionId: this.connectionId,
      uptime: Date.now() - this.lastPongAt.getTime(),
      lastPongAgo: Date.now() - this.lastPongAt.getTime(),
      missedPings: this.missedPings,
      avgRoundTripMs: this.roundTripHistory.length > 0
        ? this.roundTripHistory.reduce((a, b) => a + b, 0) / this.roundTripHistory.length
        : 0,
      status: this.missedPings === 0 ? 'healthy' : this.missedPings >= this.config.maxMissedPings ? 'dead' : 'degraded',
    };
  }
}

interface HeartbeatMetrics {
  connectionId: string;
  uptime: number;
  lastPongAgo: number;
  missedPings: number;
  avgRoundTripMs: number;
  status: 'healthy' | 'degraded' | 'dead';
}

// Connection health monitor
class ConnectionHealthMonitor {
  private heartbeats: Map<string, HeartbeatManager> = new Map();

  register(connectionId: string, ws: WebSocket, onDead: (id: string) => void): HeartbeatManager {
    const hb = new HeartbeatManager(ws, connectionId, DEFAULT_HEARTBEAT_CONFIG, onDead);
    this.heartbeats.set(connectionId, hb);
    hb.start();
    return hb;
  }

  unregister(connectionId: string): void {
    const hb = this.heartbeats.get(connectionId);
    if (hb) {
      hb.stop();
      this.heartbeats.delete(connectionId);
    }
  }

  getMetrics(): HealthSummary {
    const allMetrics = Array.from(this.heartbeats.values()).map(hb => hb.getMetrics());
    return {
      total: allMetrics.length,
      healthy: allMetrics.filter(m => m.status === 'healthy').length,
      degraded: allMetrics.filter(m => m.status === 'degraded').length,
      dead: allMetrics.filter(m => m.status === 'dead').length,
      averageRtt: allMetrics.length > 0
        ? allMetrics.reduce((a, m) => a + m.avgRoundTripMs, 0) / allMetrics.length
        : 0,
    };
  }
}
```

## Integration Points

- **Metrics Pipeline**: Heartbeat metrics feed into monitoring dashboard (Datadog, Grafana)
- **Alerting**: High missed-ping rates trigger alerts for network issues or server overload
- **Auto-Scaling**: Dead connection rate influences WebSocket server auto-scaling decisions

## Production Considerations

- **Heartbeat Jitter**: Add random jitter to ping intervals to prevent synchronized ping storms
- **Large Connection Monitoring**: For 10K+ connections, batch ping sends to avoid CPU spikes
- **Client-Initiated Heartbeats**: Some clients may send their own pings; server must handle both directions
- **Resource Cleanup**: Always clean up heartbeat timers on connection close to prevent memory leaks

## Open-Source Tools

- **uWebSockets.js**: Built-in ping/pong support with high performance
- **WS**: WebSocket library with ping/pong event handling
