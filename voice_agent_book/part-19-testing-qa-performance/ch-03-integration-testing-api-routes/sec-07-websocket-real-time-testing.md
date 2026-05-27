# Section 07: WebSocket & Real-Time API Testing

## Overview

Real-time API testing validates WebSocket connections, event streaming, and bidirectional communication between clients and the voice AI platform. WebSocket endpoints handle call status updates, live transcript streaming, agent state changes, and real-time analytics. Testing these endpoints requires specialized techniques for connection management, event assertions, and asynchronous message validation.

The WebSocket testing architecture uses a test client that connects to the same server instance as the HTTP integration tests. The test client manages connection lifecycle (connect, authenticate, subscribe, disconnect), sends and receives messages, and asserts on event sequences. Real-time testing also covers reconnection behavior, backpressure handling, and concurrent connections.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Simulator|--->| Utterance|--->| Flow     |--->| Debug    |--->| Report   |
| (in-     |    | Player   |    | Executor |    | Panel    |    | (pass/   |
|  browser)|    | (text/   |    | (step    |    | (log,    |    |  fail    |
|          |    |  audio)  |    |  thru)   |    |  state)  |    |  + trace)|
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **In-Browser Simulator**: Full conversation simulation with WASM runtime. No backend needed.
- **Utterance Testing**: Pre-defined test utterances with assertions on path and response.
- **Flow Validation**: Graph analysis for unreachable nodes, infinite loops, missing required fields.
## Implementation Approach

```typescript
// WebSocket test utilities
import WebSocket from 'ws';

class WebSocketTestClient {
  private ws: WebSocket | null = null;
  private listeners: Map<string, (data: any) => void> = new Map();
  private eventQueue: Array<{ event: string; data: any }> = [];

  async connect(url: string, token: string): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(`${url}?token=${token}`);
      
      this.ws.on('open', () => resolve());
      this.ws.on('message', (data) => {
        const parsed = JSON.parse(data.toString());
        this.eventQueue.push(parsed);
        const listener = this.listeners.get(parsed.event);
        if (listener) listener(parsed.data);
      });
      this.ws.on('error', reject);
      
      setTimeout(() => reject(new Error('Connection timeout')), 5000);
    });
  }

  async waitForEvent(eventPattern: string, { timeout = 5000 } = {}): Promise<any> {
    const existing = this.eventQueue.find(e => e.event.match(eventPattern));
    if (existing) return existing.data;

    return new Promise((resolve, reject) => {
      const handler = (data: any) => {
        this.listeners.delete(eventPattern);
        resolve(data);
      };
      this.listeners.set(eventPattern, handler);
      setTimeout(() => {
        this.listeners.delete(eventPattern);
        reject(new Error(`Timeout waiting for event: ${eventPattern}`));
      }, timeout);
    });
  }

  async close(): Promise<void> {
    this.ws?.close();
  }
}

// Test usage
describe('WebSocket Call Events', () => {
  let ws: WebSocketTestClient;
  let app: Express.Application;

  beforeEach(async () => {
    ws = new WebSocketTestClient();
    await ws.connect(`ws://localhost:${appPort}`, authToken);
  });

  afterEach(async () => {
    await ws.close();
  });

  it('receives call.started event when call begins', async () => {
    const call = await apiRequest(app)
      .post('/api/calls')
      .as(authToken)
      .body({ phoneNumber: '+1234567890' })
      .expect(201);

    const event = await ws.waitForEvent('call.started', { timeout: 3000 });
    expect(event.callId).toBe(call.body.id);
    expect(event.status).toBe('ringing');
  });

  it('handles reconnection gracefully', async () => {
    await ws.close();
    await ws.connect(`ws://localhost:${appPort}`, authToken);
    
    // System should recover state
    await ws.subscribe('call.*');
    const event = await ws.waitForEvent('call.started', { timeout: 5000 });
    expect(event).toBeDefined();
  });
});
```

## Integration Points

- **HTTP Server Reuse**: WebSocket endpoints share the HTTP server instance
- **Auth Integration**: WebSocket authentication uses the same JWT tokens as HTTP
- **Event Bus**: WebSocket events originate from the platform's event bus
- **Redis Adapter**: Horizontal scaling of WebSockets tested with Redis adapter
- **Monitoring**: WebSocket metrics (connections, messages) monitored in integration tests

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Connection State**: WebSocket tests must properly close connections to prevent leaks
- **Test Timeouts**: WebSocket operations need longer timeouts than HTTP operations
- **Resource Cleanup**: Active WebSocket connections consume server resources; clean up after tests
- **Parallel Connections**: Test threads share server; ensure WebSocket namespaces don't conflict
- **Flaky Detection**: WebSocket tests are prone to flakiness; implement retry logic
