# Section 07: WebSocket Authentication

## Overview

WebSocket authentication happens during the HTTP upgrade handshake, not after the connection is established. The client includes an Authorization header (Bearer token or API key) in the upgrade request. The server validates the token before switching protocols, rejecting invalid credentials with a 401 response before the WebSocket connection is ever created.

## Architecture

```
WebSocket Authentication Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Successful Auth:
  [Client]                              [Server]
     │                                       │
     │── GET /ws/v1/events HTTP/1.1         │
     │   Upgrade: websocket                 │
     │   Authorization: Bearer <jwt_token>  │
     │── ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ →│
     │                                       │── Validate token
     │                                       │── Extract tenant + user
     │                                       │── Create connection context
     │                                       │
     │←── 101 Switching Protocols ──────────│
     │                                       │
     │── [WebSocket connection established]  │

Failed Auth:
     │── GET /ws/v1/events                  │
     │   Upgrade: websocket                 │
     │   (no Authorization header)          │
     │── ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ →│
     │                                       │── Missing auth
     │                                       │
     │←── 401 Unauthorized ────────────────│
     │   WWW-Authenticate: Bearer           │
     │   realm="api.voiceagent.com"         │

Re-Authentication on Reconnect:
     │── [Reconnect with token]             │
     │── {                                   │
     │     "type": "reconnect",             │
     │     "token": "<new_or_same_token>",   │
     │     "lastEventId": "evt_abc_123"     │
     │── }───────────────────────────────→  │
     │                                       │── Validate token again
     │                                       │── Resume subscriptions
     │                                       │── Replay missed events
```

## Design Decisions

- **Auth at Upgrade Time**: Standard WebSocket authentication pattern — token validated before protocol switch; no post-connection auth messages needed
- **Token in URL (Alternative)**: Some clients can't set WebSocket headers; fallback to `?token=<jwt>` query parameter
- **Re-authentication on Reconnect**: Validate token again on reconnect — token may have expired since initial connection
- **Connection Authorization Level**: Each connection stores an AuthContext used for channel subscription authorization

## Implementation Approach

```typescript
// WebSocket authentication handler
interface WsAuthConfig {
  tokenValidator: TokenValidator;
  enableQueryParamAuth?: boolean;
  allowedOrigins?: string[];
}

class WebSocketAuthHandler {
  constructor(private config: WsAuthConfig) {}

  async authenticateUpgrade(req: Request): Promise<AuthContext> {
    // Extract token from header or query parameter
    let token: string | null = null;

    // Check Authorization header first
    const authHeader = req.headers.get('Authorization');
    if (authHeader?.startsWith('Bearer ')) {
      token = authHeader.slice(7);
    }

    // Fallback to query parameter
    if (!token && this.config.enableQueryParamAuth) {
      const url = new URL(req.url);
      token = url.searchParams.get('token');
    }

    if (!token) {
      throw new AuthenticationError(
        'WebSocket upgrade requires authentication. Provide Bearer token.',
        `Bearer realm="api.voiceagent.com", error="invalid_request"`,
      );
    }

    // Validate token
    try {
      const payload = await this.config.tokenValidator.validate(token);
      return {
        tenantId: payload.tenant_id,
        userId: payload.sub,
        scopes: payload.scopes || [],
        authMethod: 'oauth2',
      };
    } catch (error) {
      throw new AuthenticationError(
        'Invalid or expired authentication token.',
        `Bearer realm="api.voiceagent.com", error="invalid_token"`,
      );
    }
  }

  async authenticateReconnect(connectionId: string, token: string): Promise<AuthContext> {
    // Same validation as upgrade
    const payload = await this.config.tokenValidator.validate(token);
    return {
      tenantId: payload.tenant_id,
      userId: payload.sub,
      scopes: payload.scopes || [],
      authMethod: 'oauth2',
    };
  }
}

// Hono WebSocket upgrade middleware
function wsAuthMiddleware(authHandler: WebSocketAuthHandler) {
  return async (c: Context, next: Next) => {
    const upgrade = c.req.header('Upgrade');

    if (upgrade?.toLowerCase() === 'websocket') {
      try {
        const authContext = await authHandler.authenticateUpgrade(c.req);
        c.set('authContext', authContext);
      } catch (error) {
        // Return 401 for failed WebSocket auth
        if (error instanceof AuthenticationError) {
          c.status(401);
          c.header('WWW-Authenticate', error.wwwAuthenticate || 'Bearer');
          return c.json(error.toJson(c.get('requestId')));
        }
        throw error;
      }
    }

    await next();
  };
}

// Server-side upgrade handler
function handleWebSocketUpgrade(
  ws: WebSocket,
  authContext: AuthContext,
  subscriptionManager: SubscriptionManager,
): void {
  const connection = new WebSocketConnection(ws, authContext);

  ws.on('message', async (data) => {
    try {
      const message = JSON.parse(data.toString());

      // Handle re-authentication
      if (message.type === 'reconnect' && message.token) {
        const newContext = await authHandler.authenticateReconnect(
          connection.id,
          message.token,
        );
        connection.updateAuthContext(newContext);
        // Restore subscriptions and replay events
        await subscriptionManager.restore(connection.id);
        return;
      }

      // Handle subscription messages
      await messageRouter.handleIncoming(connection.id, message);
    } catch (error) {
      connection.sendError('Invalid message');
    }
  });
}
```

## Integration Points

- **Auth Service**: Token validation via JWKS endpoint
- **API Gateway**: WebSocket upgrade routing with auth middleware
- **SDK**: Handles token inclusion in WebSocket upgrade — transparent to developer

## Production Considerations

- **Token Expiry During Connection**: Long-lived connections may outlive token expiration; implement token refresh via reconnect message
- **Query Parameter Auth Security**: Token in URL may be logged by proxies; warn users about this risk
- **Rate Limit on Upgrade**: Rate-limit WebSocket upgrade attempts per IP to prevent connection flooding
- **Connection Hijacking Prevention**: Validate that token tenant matches any existing connection context

## Open-Source Tools

- **Jose**: JWT validation for WebSocket upgrade tokens
- **Hono**: WebSocket upgrade middleware for Edge runtimes
