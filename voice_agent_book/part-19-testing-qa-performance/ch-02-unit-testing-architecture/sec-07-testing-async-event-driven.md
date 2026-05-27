# Section 07: Testing Async & Event-Driven Code

## Overview

The voice AI platform is heavily asynchronous and event-driven: call events flow through pub/sub channels, WebSocket connections handle real-time updates, and job queues process background tasks. Testing these asynchronous patterns requires specialized techniques to ensure reliable, deterministic test outcomes.

Key patterns include: testing promise-based async operations with proper timeout handling, verifying event emitter behavior with subscription tracking, testing pub/sub message delivery and ordering, validating background job processing, and handling race conditions in concurrent operations. The testing framework uses a combination of async matchers, deferred assertions, and controlled time progression.

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
// Testing event-driven code
describe('CallEventBus', () => {
  const bus = new CallEventBus();

  it('emits call.started event when call begins', () => {
    const spy = vi.fn();
    bus.on('call.started', spy);

    bus.emit('call.started', { callId: 'call-1' });

    expect(spy).toHaveBeenCalledWith({ callId: 'call-1' });
  });

  it('handles multiple subscribers for same event', () => {
    const spy1 = vi.fn();
    const spy2 = vi.fn();
    bus.on('call.ended', spy1);
    bus.on('call.ended', spy2);

    bus.emit('call.ended', { callId: 'call-1', duration: 120 });

    expect(spy1).toHaveBeenCalled();
    expect(spy2).toHaveBeenCalled();
  });
});

// Testing async operations with timeouts
describe('CallProcessor', () => {
  it('times out if AI processing takes too long', async () => {
    vi.useFakeTimers();
    
    const processor = new CallProcessor(mockAi);
    const slowAi = mockAi.process.mockImplementation(
      () => new Promise(resolve => setTimeout(resolve, 10000))
    );

    const processPromise = processor.processCall(callData);
    
    // Advance time past timeout
    await vi.advanceTimersByTimeAsync(5000);
    
    await expect(processPromise).rejects.toThrow('Processing timeout');
    
    vi.useRealTimers();
  });
});

// Polling helper for async conditions
async function waitForCondition(
  condition: () => boolean | Promise<boolean>,
  timeout = 5000,
  interval = 100
): Promise<void> {
  const start = Date.now();
  while (Date.now() - start < timeout) {
    const result = await condition();
    if (result) return;
    await new Promise(r => setTimeout(r, interval));
  }
  throw new Error('Condition not met within timeout');
}
```

## Integration Points

- **Message Queue**: Test BullMQ job processing with real queue and mocked processors
- **WebSocket Testing**: Use ws or Socket.IO test client for WebSocket interaction testing
- **Event Store**: Event sourcing patterns tested with event stream verification
- **Stream Processing**: Test streaming data processing with controlled input streams
- **Real-Time UI**: Test real-time UI updates by simulating WebSocket events

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Async Test Flakiness**: Async tests are the most common source of flakiness; invest in stability
- **Timeout Selection**: Timeouts should be generous enough to avoid false failures but short enough for fast feedback
- **Resource Cleanup**: Ensure async operations are cleaned up in `afterEach` to prevent test leakage
- **Determinism**: Use controlled timing (fake timers) whenever possible to eliminate timing-dependent failures
- **Queue State**: Always drain queues between tests to prevent state leakage
