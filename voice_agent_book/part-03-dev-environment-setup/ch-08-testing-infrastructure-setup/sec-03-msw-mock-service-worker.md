# Section 03: MSW (Mock Service Worker)

## Overview

Mock Service Worker (MSW) provides API mocking at the network level, intercepting HTTP requests in both browser and Node.js environments. For the voice agent platform, MSW enables testing of API integrations (OpenAI, ElevenLabs, Deepgram) without making real network calls, making tests fast, reliable, and offline-capable.

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              MSW Architecture                                 │
│                                                              │
│  Browser Environment:                                       │
│  ┌──────────────────┐      ┌──────────────────────┐        │
│  │  Application      │      │  Service Worker       │        │
│  │  (fetch/XMLHttpReq)│─────►│  (native intercept)   │        │
│  │                    │      │                        │        │
│  │  fetch()           │      │  matches handler?     │        │
│  │  POST /api/agents  │      │  ┌───yes───► response │        │
│  └──────────────────┘      │  └───no────► passthrough │        │
│                             └──────────────────────┘        │
│                                                              │
│  Node.js Environment (Vitest):                              │
│  ┌──────────────────┐      ┌──────────────────────┐        │
│  │  Test              │      │  MSW Server           │        │
│  │  (node-fetch)      │─────►│  (intercepts at       │        │
│  │                    │      │   http module level)  │        │
│  │  fetch(client)     │      │                        │        │
│  └──────────────────┘      └──────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Server Setup (Node.js / Vitest)

```typescript
// packages/voice/src/test/msw-server.ts
import { setupServer } from "msw/node";
import { handlers } from "./msw-handlers";

// Create MSW server for Node.js tests
export const server = setupServer(...handlers);
```

## Browser Setup

```typescript
// packages/ui/src/test/msw-browser.ts
import { setupWorker } from "msw/browser";
import { handlers } from "../../voice/src/test/msw-handlers";

// Create MSW worker for browser tests (Storybook, E2E)
export const worker = setupWorker(...handlers);
```

## Vitest Integration

```typescript
// vitest.setup.ts (root)
import { server } from "@voice-agent/voice/test/msw-server";
import { beforeAll, afterAll, afterEach } from "vitest";

// Start MSW server before all tests
beforeAll(() => server.listen({ onUnhandledRequest: "warn" }));

// Reset handlers after each test (clean state)
afterEach(() => server.resetHandlers());

// Clean up after all tests
afterAll(() => server.close());
```

## Handler Definitions

```typescript
// packages/voice/src/test/msw-handlers.ts
import { http, HttpResponse, delay } from "msw";

// ── OpenAI API ────────────────────────────────────────────
export const handlers = [
  http.post("https://api.openai.com/v1/chat/completions", async ({ request }) => {
    const body = await request.json() as { model?: string };
    await delay(200); // Simulate network latency

    return HttpResponse.json({
      id: "chatcmpl-mock123",
      object: "chat.completion",
      created: Date.now(),
      model: body.model ?? "gpt-4",
      choices: [
        {
          index: 0,
          message: {
            role: "assistant",
            content: "I understand your request. Let me help you with that.",
          },
          finish_reason: "stop",
        },
      ],
      usage: { prompt_tokens: 50, completion_tokens: 20, total_tokens: 70 },
    });
  }),

  // ── ElevenLabs TTS ──────────────────────────────────────
  http.post("https://api.elevenlabs.io/v1/text-to-speech/:voiceId", async () => {
    await delay(300);
    return HttpResponse.arrayBuffer(
      new ArrayBuffer(2048), // Mock audio data
      {
        headers: {
          "Content-Type": "audio/mpeg",
          "Content-Length": "2048",
        },
      },
    );
  }),

  // ── Deepgram STT ────────────────────────────────────────
  http.post("https://api.deepgram.com/v1/listen", async () => {
    await delay(500);
    return HttpResponse.json({
      metadata: {
        transaction_key: "mock",
        request_id: "mock-request-id",
        sha256: "mock-hash",
        created: new Date().toISOString(),
        duration: 5.2,
        channels: 1,
      },
      results: {
        channels: [
          {
            alternatives: [
              {
                transcript: "Hello, I'd like to speak with customer support please.",
                confidence: 0.97,
                words: [
                  { word: "Hello", start: 0.0, end: 0.4, confidence: 0.99, speaker: 0 },
                  { word: "I'd", start: 0.5, end: 0.7, confidence: 0.98, speaker: 0 },
                  { word: "like", start: 0.8, end: 1.0, confidence: 0.97, speaker: 0 },
                ],
              },
            ],
          },
        ],
      },
    });
  }),

  // ── Anthropic Claude ────────────────────────────────────
  http.post("https://api.anthropic.com/v1/messages", async () => {
    await delay(200);
    return HttpResponse.json({
      id: "msg_mock123",
      type: "message",
      role: "assistant",
      content: [
        {
          type: "text",
          text: "I'll help you with your request. Here's what I can do...",
        },
      ],
      model: "claude-3-opus",
      stop_reason: "end_turn",
      usage: { input_tokens: 50, output_tokens: 30 },
    });
  }),

  // ── MinIO Health ────────────────────────────────────────
  http.get("http://localhost:9000/minio/health/live", () => {
    return HttpResponse.json({ status: "ok" });
  }),

  // ── Kafka (no direct HTTP — covered by connection tests) ─
];
```

## Scenario-Based Mocking

```typescript
// packages/voice/src/test/scenarios.ts
import { http, HttpResponse } from "msw";
import { server } from "./msw-server";

export const Scenarios = {
  // ── OpenAI: Successful response ─────────────────────────
  openAISuccess() {
    server.use(
      http.post("https://api.openai.com/v1/chat/completions", () => {
        return HttpResponse.json({
          choices: [{ message: { content: "Successful response" } }],
        });
      }),
    );
  },

  // ── OpenAI: Rate limited ────────────────────────────────
  openAIRateLimited() {
    server.use(
      http.post("https://api.openai.com/v1/chat/completions", () => {
        return HttpResponse.json(
          { error: { message: "Rate limit exceeded", type: "rate_limit_error" } },
          { status: 429 },
        );
      }),
    );
  },

  // ── OpenAI: Timeout ─────────────────────────────────────
  openAITimeout() {
    server.use(
      http.post("https://api.openai.com/v1/chat/completions", async () => {
        await delay(30000); // Exceeds test timeout
        return HttpResponse.json({});
      }),
    );
  },

  // ── OpenAI: Server error ────────────────────────────────
  openAIServerError() {
    server.use(
      http.post("https://api.openai.com/v1/chat/completions", () => {
        return HttpResponse.json(
          { error: { message: "Internal server error" } },
          { status: 500 },
        );
      }),
    );
  },

  // ── ElevenLabs: Success ─────────────────────────────────
  elevenLabsSuccess() {
    server.use(
      http.post("https://api.elevenlabs.io/v1/text-to-speech/:voiceId", () => {
        return HttpResponse.arrayBuffer(new ArrayBuffer(2048), {
          headers: { "Content-Type": "audio/mpeg" },
        });
      }),
    );
  },

  // ── ElevenLabs: Voice not found ─────────────────────────
  elevenLabsVoiceNotFound() {
    server.use(
      http.post("https://api.elevenlabs.io/v1/text-to-speech/:voiceId", () => {
        return HttpResponse.json(
          { detail: { status: "voice_not_found", message: "Voice not found" } },
          { status: 404 },
        );
      }),
    );
  },

  // ── Network error ───────────────────────────────────────
  networkError() {
    server.use(
      http.post("https://api.openai.com/v1/chat/completions", () => {
        return HttpResponse.error();
      }),
    );
  },

  // ── Reset all handlers to defaults ──────────────────────
  reset() {
    server.resetHandlers();
  },
};
```

## Usage in Tests

```typescript
// packages/voice/src/services/__tests__/llm-service.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { Scenarios } from "../../test/scenarios";
import { LLMService } from "../llm-service";

describe("LLMService", () => {
  let llm: LLMService;

  beforeEach(() => {
    Scenarios.reset();
    llm = new LLMService();
  });

  it("should return a response from OpenAI", async () => {
    Scenarios.openAISuccess();
    const response = await llm.generateResponse("Hello");
    expect(response).toBe("Successful response");
  });

  it("should handle rate limiting gracefully", async () => {
    Scenarios.openAIRateLimited();
    await expect(llm.generateResponse("Hello")).rejects.toThrow(
      "Rate limit exceeded",
    );
  });

  it("should retry on server error", async () => {
    Scenarios.openAIServerError();
    // Service should have retry logic
    await expect(llm.generateResponse("Hello")).rejects.toThrow();
  });

  it("should handle network errors", async () => {
    Scenarios.networkError();
    await expect(llm.generateResponse("Hello")).rejects.toThrow();
  });
});
```

## Integration with Storybook

```typescript
// packages/ui/.storybook/preview.ts
import { initialize, mswDecorator } from "msw-storybook-addon";
import { handlers } from "@voice-agent/voice/test/msw-handlers";

// Initialize MSW in Storybook
initialize();

export const decorators = [mswDecorator];

export const parameters = {
  msw: {
    handlers,
  },
};
```

## Integration with Playwright

```typescript
// apps/web/e2e/msw-integration.ts
import { test as base, type Page } from "@playwright/test";
import { createWorker } from "msw";
import { handlers } from "@voice-agent/voice/test/msw-handlers";

// Extend Playwright test with MSW
export const test = base.extend<{
  msw: { use: (...handlers: unknown[]) => Promise<void>; reset: () => Promise<void> };
}>({
  msw: async ({ page }, use) => {
    // Create MSW worker in the browser context
    await page.addInitScript(() => {
      // MSW is loaded from node_modules
    });

    const msw = {
      use: async (...scenarios: unknown[]) => {
        // Override handlers for specific scenarios
      },
      reset: async () => {
        // Reset to default handlers
      },
    };

    await use(msw);
  },
});

export { expect } from "@playwright/test";
```

## Design Decisions

### MSW vs. nock vs. jest.mock

| Feature | MSW | nock | jest.mock |
|---------|-----|------|-----------|
| Network level | Yes (service worker) | Yes (http) | No (module) |
| Browser support | Yes | No | No |
| Node.js support | Yes | Yes | Yes |
| Unhandled request tracking | Yes | No | No |
| Scenario switching | Runtime | Runtime | Re-import required |
| TypeScript support | Excellent | Good | Good |
| React Native | Experimental | No | Yes |

**Decision**: MSW provides the most complete solution — it works at the network level in both browser and Node.js, supports runtime scenario switching, and integrates natively with Vitest, Storybook, and Playwright.

### Why not jest.mock for API calls?

`jest.mock` replaces modules at the import level, which means you're testing with mocked functions, not real network behavior. MSW intercepts actual HTTP requests, so your code runs the same fetch/axios calls it would in production — just the network is simulated.

## Integration Points

- **Vitest**: MSW server runs alongside test suite
- **Storybook**: Stories use MSW to mock API responses
- **Playwright**: Browser-based MSW for E2E tests
- **Development**: MSW can run in development mode to mock unreliable APIs

## Production Considerations

1. **Handler maintenance**: Keep MSW handlers in sync with actual API contracts. When an API changes, update the handler and the real implementation together
2. **Unhandled requests**: Configure MSW to `"error"` on unhandled requests in tests (not just `"warn"`). This catches tests that make real network calls
3. **Request matching**: Use specific URL patterns to avoid accidentally matching the wrong endpoint. Register handlers for all external APIs used by the code under test
4. **Scenario coverage**: For each external API, create scenarios for success, rate limiting, timeouts, server errors, and network errors. Test that your application handles each case
5. **Fallback URL patterns**: If your application constructs URLs dynamically (e.g., different model names), use URL pattern matching: `http.post("https://api.openai.com/v1/:resource")`
