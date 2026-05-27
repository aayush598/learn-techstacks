# Section 04: Test Utilities & Helpers

## Overview

Test utilities and helpers reduce boilerplate and enforce consistent patterns across the test suite. The voice AI platform provides a rich set of custom matchers, test context builders, assertion helpers, and fixture generators that make tests more readable and maintainable. These utilities are globally available via Vitest's global configuration, removing the need for imports in every test file.

Custom matchers extend Vitest's built-in assertions with domain-specific checks (e.g., `toBeValidAudioBuffer`, `toHaveConversationState`, `toBeWithinLatencyBudget`). Test context helpers manage the lifecycle of test dependencies (database connections, server instances, authentication contexts). Assertion helpers provide common validation patterns for voice pipeline operations.

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
// Custom matcher example
import { expect } from 'vitest';

interface AudioBuffer {
  samples: Float32Array;
  sampleRate: number;
  duration: number;
  channels: number;
}

function toBeValidAudioBuffer(received: AudioBuffer) {
  const pass = received instanceof Float32Array || 
    (typeof received.duration === 'number' && 
     received.duration > 0 &&
     typeof received.sampleRate === 'number' &&
     received.sampleRate >= 8000);
     
  return {
    pass,
    message: () => pass
      ? `Expected ${received} not to be a valid audio buffer`
      : `Expected ${received} to be a valid audio buffer with sampleRate >= 8000`,
    actual: received,
    expected: 'AudioBuffer with sampleRate >= 8000',
  };
}

expect.extend({ toBeValidAudioBuffer });

declare module 'vitest' {
  interface Assertion {
    toBeValidAudioBuffer(): void;
  }
}

// Test context helper
export async function createTestContext(): Promise<TestContext> {
  const dbClient = await createTestDb();
  const redis = await createTestRedis();
  const server = await createTestServer(dbClient, redis);
  
  return {
    db: dbClient,
    redis,
    request: supertest(server),
    async teardown() {
      await dbClient.$disconnect();
      await redis.quit();
      await server.close();
    },
  };
}
```

## Integration Points

- **Global Setup**: Registered in Vitest's `setupFiles` array
- **Type Augmentation**: Matcher types merged via declaration merging
- **Factory Integration**: Test utilities consume factory functions for data creation
- **Framework Integration**: Helpers abstract away framework-specific setup (Next.js, tRPC)
- **Documentation**: Usage examples maintained in the test utility modules

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Utility Bloat**: Maintain utilities, don't let them accumulate unused code
- **Version Drift**: Keep utilities in sync with framework upgrades
- **Learning Curve**: New team members need documentation to discover and use utilities
- **Performance**: Lazy-load expensive helpers; avoid side effects at import time
- **Test Readability**: Prioritize test readability over clever utility abstractions
