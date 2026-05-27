# Section 01: Vitest Configuration & Setup

## Overview

Vitest is the primary test runner for the voice AI platform, chosen for its native TypeScript support, ESM compatibility, fast watch mode, and compatibility with the Vite build system. Configuration is centralized in `vitest.config.ts` with environment-specific overrides. The setup includes global test utilities, path aliases, coverage configuration, and worker pool management for parallel execution.

The configuration supports multiple test environments (node for backend, jsdom for frontend) and custom setup files that initialize test-wide mocks, database connections, and test helpers. Global test utilities are exposed without imports for frequently used helpers (factories, matchers, context setup).

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
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.test.ts', 'src/**/*.spec.ts'],
    exclude: ['node_modules', 'dist', 'e2e'],
    setupFiles: ['./test/setup.ts'],
    globalSetup: ['./test/global-setup.ts'],
    globalTeardown: ['./test/global-teardown.ts'],
    
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'lcov', 'html'],
      include: ['src/**/*.ts'],
      exclude: ['src/**/*.test.ts', 'src/**/*.spec.ts', 'src/**/*.d.ts'],
      thresholds: {
        branches: 75,
        functions: 75,
        lines: 80,
        statements: 80,
      },
    },
    
    pool: 'forks',
    poolOptions: {
      forks: {
        singleFork: false,
        isolate: true,
      },
    },
    
    testTimeout: 10000,
    hookTimeout: 15000,
    teardownTimeout: 5000,
    
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@test': path.resolve(__dirname, './test'),
    },
  },
});
```

## Integration Points

- **IDE Integration**: Vitest VS Code extension for inline test running and debugging
- **CI Integration**: `vitest run` for CI, `vitest` for local development
- **Coverage Reports**: Integrated with Codecov for PR coverage comments
- **Path Aliases**: Aligned with TypeScript path aliases for consistent imports
- **Pre-commit Hooks**: `lint-staged` runs vitest on changed files

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Configuration Drift**: Keep vitest.config.ts aligned with tsconfig.json and vite.config.ts
- **Memory Usage**: Fork pool uses more memory but provides better isolation; tune based on CI resources
- **Cache Invalidation**: Clear Vitest cache when configuration changes significantly
- **Environment Detection**: Use `process.env.VITEST` for conditional logic in source code
- **Version Pinning**: Pin Vitest major version to avoid breaking changes in CI
