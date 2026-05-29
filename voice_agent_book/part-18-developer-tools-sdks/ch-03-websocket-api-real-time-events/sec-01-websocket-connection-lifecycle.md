# Section 01: WebSocket Connection Lifecycle

## Overview

WebSocket connections in the Voice Agent API follow a stateful lifecycle: connection establishment via HTTP upgrade, message framing over the persistent socket, and graceful closure with cleanup. The connection lifecycle is managed by a state machine that tracks connection states — connecting, connected, reconnecting, and closed — with proper error handling at each stage.

## Architecture

```
WebSocket Lifecycle State Machine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

         ┌──────────┐
         │ INITIAL  │
         └────┬─────┘
              │ HTTP Upgrade Request
              ▼
         ┌──────────┐    Upgrade     ┌───────────┐
         │CONNECTING│────Failure───▶│  CLOSED   │
         └────┬─────┘               └───────────┘
              │ Upgrade Success
              ▼
         ┌──────────┐   Heartbeat    ┌───────────┐
         │CONNECTED │───Timeout────▶│  CLOSED   │
         └────┬─────┘               └───────────┘
              │ Disconnect
              ▼
         ┌──────────┐   Retry      ┌───────────┐
         │RECONNECT │───Exhausted─▶│  CLOSED   │
         └────┬─────┘              └───────────┘
              │ Reconnect Success
              ▼
         ┌──────────┐
         │CONNECTED │
         └──────────┘

Upgrade Handshake:
  Client → Server: GET /ws/v1/events HTTP/1.1
                   Upgrade: websocket
                   Connection: Upgrade
                   Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
                   Sec-WebSocket-Version: 13
                   Authorization: Bearer <token>

  Server → Client: HTTP/1.1 101 Switching Protocols
                   Upgrade: websocket
                   Connection: Upgrade
                   Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

## Design Decisions

- **State Machine Pattern**: Explicit state tracking prevents invalid operations and simplifies reconnection logic
- **Token Auth at Upgrade**: Authentication happens during the HTTP upgrade handshake — validated before WebSocket connection is established
- **Graceful Close**: Server sends close frame with reason code before terminating; clients acknowledge and clean up
- **Connection Metadata**: Each connection stores tenant ID, subscription channels, and connection timestamps

## Implementation Approach

```typescript
// Connection state machine
enum ConnectionState {
  INITIAL,
  CONNECTING,
  CONNECTED,
  RECONNECTING,
  CLOSED,
}

interface ConnectionMetadata {
  connectionId: string;
  tenantId: string;
  userId?: string;
  connectedAt: Date;
  lastHeartbeatAt: Date;
  subscriptions: Set<string>;
  state: ConnectionState;
}

class WebSocketConnection {
  private state: ConnectionState = ConnectionState.INITIAL;
  private metadata: ConnectionMetadata;
  private heartbeatInterval?: NodeJS.Timeout;
  private readonly HEARTBEAT_TIMEOUT = 30_000; // 30 seconds

  constructor(
    private ws: WebSocket,
    private readonly authContext: AuthContext,
  ) {
    this.metadata = {
      connectionId: crypto.randomUUID(),
      tenantId: authContext.tenantId,
      userId: authContext.userId,
      connectedAt: new Date(),
      lastHeartbeatAt: new Date(),
      subscriptions: new Set(),
      state: ConnectionState.INITIAL,
    };
  }

  async establish(): Promise<void> {
    this.setState(ConnectionState.CONNECTING);

    try {
      // Authentication already happened during upgrade
      this.setState(ConnectionState.CONNECTED);
      this.startHeartbeat();
      this.sendConnectionEstablished();
    } catch (error) {
      this.setState(ConnectionState.CLOSED);
      this.ws.close(4401, 'Authentication failed');
    }
  }

  handleMessage(data: WebSocket.Data): void {
    if (this.state !== ConnectionState.CONNECTED) {
      return; // Ignore messages in non-connected state
    }

    try {
      const message = JSON.parse(data.toString());
      this.routeMessage(message);
    } catch (error) {
      this.sendError('Invalid message format');
    }
  }

  handleClose(code: number, reason: string): void {
    this.setState(ConnectionState.CLOSED);
    this.stopHeartbeat();
    this.cleanup();
  }

  handlePong(): void {
    this.metadata.lastHeartbeatAt = new Date();
  }

  private startHeartbeat(): void {
    this.heartbeatInterval = setInterval(() => {
      const elapsed = Date.now() - this.metadata.lastHeartbeatAt.getTime();

      if (elapsed > this.HEARTBEAT_TIMEOUT) {
        this.ws.close(4400, 'Heartbeat timeout');
        return;
      }

      this.ws.ping();
    }, 10_000); // Ping every 10 seconds
  }

  private stopHeartbeat(): void {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = undefined;
    }
  }

  private setState(state: ConnectionState): void {
    this.state = state;
    this.metadata.state = state;
  }

  private cleanup(): void {
    // Unsubscribe from all channels
    for (const channel of this.metadata.subscriptions) {
      this.unsubscribeFromChannel(channel);
    }
  }
}

// Server-side WebSocket handler
function wsUpgradeHandler(req: Request, ws: WebSocket, context: AuthContext): void {
  const connection = new WebSocketConnection(ws, context);

  ws.on('message', (data) => connection.handleMessage(data));
  ws.on('close', (code, reason) => connection.handleClose(code, reason));
  ws.on('pong', () => connection.handlePong());

  connection.establish();
}
```

## Integration Points

- **API Gateway**: WebSocket upgrade requests are routed to WebSocket server pool
- **Auth Service**: Token validation during upgrade handshake
- **Redis Adapter**: Connection state stored in Redis for reconnection recovery

## Production Considerations

- **Connection Limits**: Max 10,000 concurrent connections per server; scale horizontally with Redis adapter
- **Graceful Shutdown**: Drain connections before server shutdown — send close frame, wait for acknowledgment
- **Stale Connection Cleanup**: Cron job scans and closes connections that missed heartbeats for >60 seconds
- **Connection Metrics**: Track connection count, message throughput, and heartbeat health per server

## Open-Source Tools

- **uWebSockets.js**: High-performance WebSocket server implementation
- **WS**: Popular WebSocket library for Node.js with robust event handling
- **Socket.IO**: WebSocket library with built-in fallback and reconnection (if higher-level abstraction preferred)
