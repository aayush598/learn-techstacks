# Section 01: Vitest Configuration

## Overview

Vitest serves as the primary test runner for the voice agent platform, providing fast, TypeScript-native unit and integration testing. With workspace support for the monorepo, Vitest runs tests across all packages with shared configuration while allowing per-package overrides.

## Workspace Configuration

```typescript
// vitest.workspace.ts
import { defineWorkspace } from "vitest/config";

export default defineWorkspace([
  // Share config across all packages
  {
    test: {
      name: "unit",
      include: ["packages/*/src/**/*.{test,spec}.ts"],
      exclude: ["packages/*/src/**/*.e2e.test.ts"],
    },
  },
  {
    test: {
      name: "integration",
      include: ["apps/*/src/**/*.integration.test.ts"],
      testTimeout: 30000,
      hookTimeout: 60000,
    },
  },
]);
```

## Root Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    // Environment
    globals: true,
    environment: "node",
    environmentMatch: {
      "packages/ui/**": "jsdom",
      "apps/web/**": "jsdom",
    },

    // Timeouts
    testTimeout: 10000,
    hookTimeout: 15000,
    teardownTimeout: 5000,

    // Coverage
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html", "lcov"],
      reportsDirectory: "./coverage",
      exclude: [
        "**/node_modules/**",
        "**/dist/**",
        "**/coverage/**",
        "**/*.config.*",
        "**/*.d.ts",
        "**/types/**",
      ],
      thresholds: {
        statements: 80,
        branches: 75,
        functions: 80,
        lines: 80,
      },
    },

    // File processing
    include: ["**/*.{test,spec}.{ts,tsx}"],
    exclude: [
      "**/node_modules/**",
      "**/dist/**",
      "**/.next/**",
      "**/.turbo/**",
    ],

    // Global setup
    setupFiles: ["./vitest.setup.ts"],

    // TypeScript
    typecheck: {
      tsconfig: "./tsconfig.json",
      include: ["**/*.{test,spec}.{ts,tsx}"],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@voice-agent/ui": path.resolve(__dirname, "./packages/ui/src"),
      "@voice-agent/db": path.resolve(__dirname, "./packages/db/src"),
      "@voice-agent/types": path.resolve(__dirname, "./packages/types/src"),
      "@voice-agent/voice": path.resolve(__dirname, "./packages/voice/src"),
      "@voice-agent/ai": path.resolve(__dirname, "./packages/ai/src"),
    },
  },
});
```

## Package-Specific Configuration

### UI Package

```typescript
// packages/ui/vitest.config.ts
import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./vitest.setup.ts"],
    include: ["src/**/*.{test,spec}.{ts,tsx}"],
    css: {
      modules: {
        classNameStrategy: "non-scoped",
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

### Database Package

```typescript
// packages/db/vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "node",
    globals: true,
    include: ["src/**/*.{test,spec}.ts"],
    testTimeout: 30000,
    globalSetup: ["./vitest.global-setup.ts"],
    setupFiles: ["./vitest.setup.ts"],
    pool: "forks",
    poolOptions: {
      forks: {
        singleFork: true,
      },
    },
  },
});
```

## Global Setup Files

```typescript
// vitest.setup.ts
import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach, vi } from "vitest";

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock environment variables
vi.mock("@voice-agent/config", () => ({
  env: () => ({
    NODE_ENV: "test",
    DATABASE_URL: "postgresql://postgres:postgres@localhost:5432/voice_agent_test",
    REDIS_URL: "redis://localhost:6379",
    OPENAI_API_KEY: "test-key",
    JWT_SECRET: "test-secret-that-is-at-least-32-characters-long!!",
  }),
  validateEnv: () => ({}),
}));

// Mock console methods to reduce noise
vi.spyOn(console, "log").mockImplementation(() => {});
vi.spyOn(console, "debug").mockImplementation(() => {});
vi.spyOn(console, "info").mockImplementation(() => {});
```

## Test Utilities

```typescript
// packages/config/src/test-utils.ts
import { vi } from "vitest";

export function mockDate(isoDate: string): void {
  const date = new Date(isoDate);
  vi.setSystemTime(date);
}

export function advanceTime(ms: number): void {
  vi.advanceTimersByTime(ms);
}

export function createMockResponse<T>(data: T, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

export function createMockError(status = 500, message = "Internal Server Error"): Response {
  return new Response(
    JSON.stringify({ error: { code: "INTERNAL_ERROR", message } }),
    { status, headers: { "Content-Type": "application/json" } },
  );
}
```

## Running Tests

```bash
# Run all tests
pnpm test

# Run tests for a specific package
pnpm --filter @voice-agent/db test

# Run tests in watch mode
pnpm --filter @voice-agent/ui test -- --watch

# Run with coverage
pnpm test -- --coverage

# Run specific test file
pnpm --filter @voice-agent/api test -- --run src/services/call.service.test.ts

# Run tests with UI
pnpm test -- --ui

# Run only unit tests
pnpm test -- --project unit

# Run only integration tests
pnpm test -- --project integration

# Update snapshots
pnpm test -- --update
```

## Mocking Patterns

```typescript
// packages/voice/src/services/__tests__/voice-service.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";

// Mock external dependencies
vi.mock("../../stt/deepgram", () => ({
  DeepgramSTT: vi.fn().mockImplementation(() => ({
    transcribe: vi.fn().mockResolvedValue({ text: "Hello world", confidence: 0.95 }),
  })),
}));

vi.mock("../../tts/elevenlabs", () => ({
  ElevenLabsTTS: vi.fn().mockImplementation(() => ({
    synthesize: vi.fn().mockResolvedValue(Buffer.from("audio-data")),
  })),
}));

import { VoiceService } from "../voice-service";

describe("VoiceService", () => {
  let service: VoiceService;

  beforeEach(() => {
    vi.clearAllMocks();
    service = new VoiceService();
  });

  it("should transcribe audio", async () => {
    const result = await service.transcribe(Buffer.from("audio"));
    expect(result.text).toBe("Hello world");
    expect(result.confidence).toBe(0.95);
  });

  it("should synthesize speech", async () => {
    const result = await service.synthesize("Hello world");
    expect(result).toBeInstanceOf(Buffer);
  });
});
```

## Design Decisions

### Vitest vs. Jest

| Feature | Vitest | Jest |
|---------|--------|------|
| Performance | Faster (esbuild) | Slower |
| TypeScript | Native | Requires ts-jest |
| ESM support | Native | Experimental |
| Monorepo workspaces | Built-in | Requires config |
| Watch mode | Instant HMR | Reload-based |
| Compatibility | Jest-compatible API | Standard |

**Decision**: Vitest is significantly faster for TypeScript projects, supports ESM natively, and provides better monorepo workspace integration. Its Jest-compatible API means no learning curve.

### jsdom vs. node environment

UI packages use `jsdom` for DOM APIs (rendering components). Backend packages use `node` for faster execution. The `environmentMatch` config applies the right environment automatically based on the file path.

## Integration Points

- **VS Code**: Vitest extension for inline test running
- **CI**: Vitest runs with `--reporter=junit` for CI integration
- **Coverage**: Istanbul reports integrate with Codecov or Coveralls
- **Playwright**: E2E tests complement Vitest unit/integration tests

## Production Considerations

1. **Test isolation**: Each test file should be independent. Use `beforeEach` for setup and `afterEach` for cleanup. The `pool: 'forks'` setting isolates tests by running them in separate processes
2. **Flaky tests**: Set `retry: 2` in CI to retry flaky tests. Track flaky tests and prioritize fixing them
3. **Performance**: Large test suites can be slow. Use `--project` to run only relevant tests during development. CI runs the full suite
4. **Snapshot management**: Keep snapshots small and review them during code review. Delete unused snapshots with `--update`
5. **Coverage thresholds**: Set thresholds that reflect the current coverage level and increase them gradually. Never lower thresholds without team discussion
