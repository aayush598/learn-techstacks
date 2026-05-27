# Section 02: Test Patterns for Services

## Overview

Service layer testing validates the orchestration logic that coordinates domain operations, external integrations, and data persistence. Services in the voice AI platform typically handle multi-step operations: processing a call event, updating conversation state, calling external AI services, and persisting results. Testing these services requires careful mocking of dependencies and verification of interaction patterns.

The testing patterns for services follow the Arrange-Act-Assert structure with dependency injection. Each service test creates the service with mocked dependencies, executes the operation, and verifies both the return value and the mock interactions. This approach ensures services correctly handle success paths, error conditions, and edge cases without requiring real infrastructure.

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
// Service test pattern
describe('CallProcessingService', () => {
  let service: CallProcessingService;
  let mockDb: jest.Mocked<DatabaseClient>;
  let mockAi: jest.Mocked<AIClient>;  
  let mockLogger: jest.Mocked<Logger>;

  beforeEach(() => {
    mockDb = createMockDb();
    mockAi = createMockAi();
    mockLogger = createMockLogger();
    service = new CallProcessingService(mockDb, mockAi, mockLogger);
  });

  describe('processIncomingCall', () => {
    it('processes call through full pipeline on success', async () => {
      const callData = createCallData({ phoneNumber: '+1234567890' });
      mockDb.call.create.mockResolvedValue({ id: 'call-1', ...callData, status: 'pending' });
      mockAi.processTranscript.mockResolvedValue({ intent: 'support', confidence: 0.95 });
      mockDb.call.update.mockResolvedValue({ id: 'call-1', status: 'completed' });

      const result = await service.processIncomingCall(callData);

      expect(result.status).toBe('completed');
      expect(mockDb.call.create).toHaveBeenCalledWith(expect.objectContaining({
        phoneNumber: '+1234567890',
      }));
      expect(mockAi.processTranscript).toHaveBeenCalled();
      expect(mockDb.call.update).toHaveBeenCalledWith('call-1', expect.objectContaining({
        status: 'completed',
      }));
    });

    it('handles AI service failure gracefully', async () => {
      mockAi.processTranscript.mockRejectedValue(new Error('AI timeout'));
      mockDb.call.update.mockResolvedValue({ id: 'call-1', status: 'failed' });

      const result = await service.processIncomingCall(createCallData());

      expect(result.status).toBe('failed');
      expect(mockLogger.error).toHaveBeenCalledWith(
        expect.stringContaining('AI processing failed')
      );
    });
  });
});
```

## Integration Points

- **Repository Pattern**: Services depend on repository interfaces, not ORM directly
- **Event Emission**: Services emit events that are verified in tests
- **Cache Integration**: Cache interaction tested with mock cache client
- **Queue Integration**: Message queue publishing verified via mock queue
- **Error Monitoring**: Error reporting integration verified in error paths

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Mock Fidelity**: Mocks must accurately reflect real behavior; review when real implementations change
- **Test Granularity**: One behavior per test; avoid testing multiple scenarios in a single test
- **Service Complexity**: Break large services into smaller, testable units
- **Integration Overlap**: Don't duplicate integration tests; focus service tests on orchestration logic
- **Performance**: Service tests should complete in milliseconds; slow tests indicate poor separation
