# Section 08: Fallback to Polling

## Overview

When WebSocket connections cannot be established (firewalls, proxies, restrictive networks), clients automatically fall back to alternative real-time communication methods. The fallback chain is Server-Sent Events (SSE) first, then long polling as last resort. The transition is transparent to application code — events arrive through the same interface regardless of transport.

## Architecture

```
Fallback Chain
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Transport Priority:
  1. WebSocket (full-duplex, low latency)
  2. SSE (server→client streaming, HTTP-based)
  3. Long Polling (compatible with all networks)

Auto-Detection Flow:
  [Client] → Attempt WebSocket Connection
     │
     ├── Success → Use WebSocket
     │
     └── Failure → Check reason
           │
           ├── 401 Auth error → Stop (show auth error)
           │
           └── Network error → Fallback to SSE
                  │
                  ├── SSE endpoint: GET /v1/events/stream
                  │   (same auth, same events)
                  │
                  ├── Success → Use SSE
                  │
                  └── Failure → Fallback to Long Polling
                         │
                         └── Long Poll endpoint: GET /v1/events/poll
                             (with cursor for missed events)

Transport Comparison:
  Feature         WebSocket   SSE          Long Polling
  ──────────────────────────────────────────────────────
  Direction       Bidirect.   Server→Client Server→Client
  Latency         Low         Low           Medium-High
  HTTP Compat.    Upgrade     Standard      Standard
  Firewall        Blocked     Usually OK    Usually OK
  Reconnection    Complex     Simple        Simple
  Server State    Per-conn    Per-conn      Stateless
```

## Design Decisions

- **SSE Preferred Fallback**: SSE uses standard HTTP, works through most proxies, and provides native reconnection via EventSource API
- **Long Polling Last Resort**: Most compatible but highest latency; only used when SSE fails
- **Same Event Format**: All transports deliver the same event envelope — application code is transport-agnostic
- **Automatic Fallback Detection**: Client library detects WebSocket failure and switches transport without developer intervention

## Implementation Approach

```typescript
// Transport abstraction
interface Transport {
  connect(): Promise<void>;
  disconnect(): void;
  onEvent(handler: (event: EventEnvelope) => void): void;
  send(data: unknown): void;
  getType(): TransportType;
}

type TransportType = 'websocket' | 'sse' | 'long_polling';
type FallbackChain = [TransportType, TransportType, TransportType];

// Fallback manager
class FallbackManager {
  private currentTransport: Transport | null = null;
  private readonly fallbackChain: FallbackChain = ['websocket', 'sse', 'long_polling'];
  private eventHandlers: Array<(event: EventEnvelope) => void> = [];

  constructor(
    private baseUrl: string,
    private token: string,
    private config: { eventHandler: (event: EventEnvelope) => void },
  ) {
    this.eventHandlers.push(config.eventHandler);
  }

  async connect(): Promise<Transport> {
    let lastError: Error | null = null;

    for (const transportType of this.fallbackChain) {
      try {
        const transport = this.createTransport(transportType);
        await transport.connect();
        this.currentTransport = transport;

        transport.onEvent((event) => {
          for (const handler of this.eventHandlers) {
            handler(event);
          }
        });

        console.info(`Connected via ${transportType}`);
        return transport;
      } catch (error) {
        lastError = error as Error;
        console.warn(`Failed to connect via ${transportType}:`, error.message);
      }
    }

    throw new Error(`All transports failed. Last error: ${lastError?.message}`);
  }

  async getCurrentTransport(): Promise<Transport> {
    if (!this.currentTransport) {
      return this.connect();
    }
    return this.currentTransport;
  }

  private createTransport(type: TransportType): Transport {
    switch (type) {
      case 'websocket':
        return new WebSocketTransport(this.baseUrl, this.token);
      case 'sse':
        return new SSETransport(this.baseUrl, this.token);
      case 'long_polling':
        return new LongPollingTransport(this.baseUrl, this.token);
    }
  }
}

// SSE transport implementation
class SSETransport implements Transport {
  private eventSource: EventSource | null = null;
  private eventHandlers: Array<(event: EventEnvelope) => void> = [];

  constructor(private baseUrl: string, private token: string) {}

  async connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      const url = `${this.baseUrl}/v1/events/stream?token=${this.token}`;
      this.eventSource = new EventSource(url, { withCredentials: true });

      this.eventSource.onopen = () => resolve();

      this.eventSource.addEventListener('message', (event) => {
        const envelope: EventEnvelope = JSON.parse(event.data);
        for (const handler of this.eventHandlers) {
          handler(envelope);
        }
      });

      this.eventSource.onerror = (error) => {
        if (this.eventSource?.readyState === EventSource.CLOSED) {
          reject(new Error('SSE connection failed'));
        }
      };
    });
  }

  disconnect(): void {
    this.eventSource?.close();
    this.eventSource = null;
  }

  onEvent(handler: (event: EventEnvelope) => void): void {
    this.eventHandlers.push(handler);
  }

  send(_data: unknown): void {
    console.warn('SSE does not support client-to-server messaging');
  }

  getType(): TransportType {
    return 'sse';
  }
}

// Long polling transport implementation
class LongPollingTransport implements Transport {
  private active = false;
  private cursor: string | null = null;
  private eventHandlers: Array<(event: EventEnvelope) => void> = [];

  constructor(private baseUrl: string, private token: string) {}

  async connect(): Promise<void> {
    this.active = true;
    // Start polling loop
    this.pollLoop();
  }

  private async pollLoop(): Promise<void> {
    while (this.active) {
      try {
        const params = new URLSearchParams({ token: this.token });
        if (this.cursor) {
          params.set('cursor', this.cursor);
        }

        const response = await fetch(
          `${this.baseUrl}/v1/events/poll?${params}`,
          { signal: AbortSignal.timeout(60_000) },
        );

        if (response.ok) {
          const data = await response.json();
          for (const event of data.events) {
            this.cursor = event.id;
            for (const handler of this.eventHandlers) {
              handler(event);
            }
          }
        }
      } catch (error) {
        if (!this.active) break;
        // Wait before retry
        await new Promise(resolve => setTimeout(resolve, 5000));
      }
    }
  }

  disconnect(): void {
    this.active = false;
  }

  onEvent(handler: (event: EventEnvelope) => void): void {
    this.eventHandlers.push(handler);
  }

  send(_data: unknown): void {
    console.warn('Long polling does not support client-to-server messaging');
  }

  getType(): TransportType {
    return 'long_polling';
  }
}
```

## Integration Points

- **SDK**: All transport logic encapsulated in SDK — single `client.events.subscribe()` API
- **Server**: SSE and long polling endpoints alongside WebSocket; share event distribution via Redis pub/sub
- **Fallback Metrics**: Track transport type usage to identify network restrictions

## Production Considerations

- **SSE Connection Limits**: Browsers limit concurrent SSE connections (6 per domain); reuse connections
- **Long Polling Latency**: Events delivered with up to 60-second delay (poll interval); acceptable for non-real-time use
- **Polling Amplification**: Long polling creates more HTTP requests; ensure server capacity for polling connections
- **Graceful Degradation**: Alerts when fallback transport is in use — may indicate network issues

## Open-Source Tools

- **EventSource**: Standard browser API for SSE consumption
- **Socket.IO**: Provides WebSocket → long polling fallback out of the box
