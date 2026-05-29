# Section 02: Test Utilities & Helpers

## Overview

Test utilities, factories, and helpers make tests easier to write, more maintainable, and more comprehensive. By centralizing test data generation, mocking utilities, and custom matchers, we reduce boilerplate and ensure consistent testing patterns across the codebase.

## Test Data Builders (Factory Pattern)

```typescript
// packages/types/src/test-builders.ts
import { faker } from "@faker-js/faker";
import type {
  Agent,
  Call,
  Campaign,
  Contact,
  Organization,
  User,
  AgentStatus,
  CallStatus,
} from "../domain";

// ── Builder class for type-safe test data ─────────────────
class Builder<T> {
  private overrides: Partial<T> = {};

  with(overrides: Partial<T>): this {
    this.overrides = { ...this.overrides, ...overrides };
    return this;
  }

  build(defaults: T): T {
    return { ...defaults, ...this.overrides };
  }
}

// ── Organization Builder ──────────────────────────────────
export function buildOrganization(
  overrides: Partial<Organization> = {},
): Organization {
  return new Builder<Organization>()
    .with({
      id: faker.string.ulid(),
      name: faker.company.name(),
      slug: faker.helpers.slugify(faker.company.name()).toLowerCase(),
      plan: "professional",
      settings: { timezone: "UTC", language: "en-US" },
      createdAt: faker.date.recent(),
      updatedAt: faker.date.recent(),
    })
    .with(overrides)
    .build();
}

// ── Agent Builder ────────────────────────────────────────
export function buildAgent(
  overrides: Partial<Agent> = {},
): Agent {
  return new Builder<Agent>()
    .with({
      id: faker.string.ulid(),
      organizationId: faker.string.ulid(),
      name: "Test Agent",
      description: "A test agent for unit tests",
      voiceConfig: {
        provider: "elevenlabs",
        voiceId: faker.string.alphanumeric(20),
        speed: 1.0,
        stability: 0.7,
        similarityBoost: 0.8,
      },
      llmConfig: {
        provider: "openai",
        model: "gpt-4",
        temperature: 0.7,
        maxTokens: 1024,
        systemPrompt: "You are a helpful test agent.",
      },
      greetingMessage: "Hello! This is a test agent.",
      maxCallDuration: 600,
      status: "active",
      createdAt: faker.date.recent(),
      updatedAt: faker.date.recent(),
    })
    .with(overrides)
    .build();
}

// ── Call Builder ─────────────────────────────────────────
export function buildCall(
  overrides: Partial<Call> = {},
): Call {
  const status: CallStatus = "completed";
  const duration = faker.number.int({ min: 30, max: 1800 });

  return new Builder<Call>()
    .with({
      id: faker.string.ulid(),
      organizationId: faker.string.ulid(),
      agentId: faker.string.ulid(),
      contactId: faker.string.ulid(),
      campaignId: faker.string.ulid(),
      status,
      direction: "inbound",
      fromNumber: faker.phone.number({ style: "international" }),
      toNumber: faker.phone.number({ style: "international" }),
      duration,
      recordingUrl: `https://storage.example.com/recordings/${faker.string.uuid()}.wav`,
      transcriptUrl: `https://storage.example.com/transcripts/${faker.string.uuid()}.json`,
      cost: faker.number.float({ min: 0.01, max: 5.0 }),
      startedAt: faker.date.recent(),
      endedAt: faker.date.recent(),
      createdAt: faker.date.recent(),
      updatedAt: faker.date.recent(),
    })
    .with(overrides)
    .build();
}

// ── Contact Builder ──────────────────────────────────────
export function buildContact(
  overrides: Partial<Contact> = {},
): Contact {
  return new Builder<Contact>()
    .with({
      id: faker.string.ulid(),
      organizationId: faker.string.ulid(),
      firstName: faker.person.firstName(),
      lastName: faker.person.lastName(),
      email: faker.internet.email(),
      phone: faker.phone.number({ style: "international" }),
      tags: ["test", faker.helpers.arrayElement(["vip", "new", "returning"])],
      customFields: { source: "test-factory" },
      createdAt: faker.date.recent(),
      updatedAt: faker.date.recent(),
    })
    .with(overrides)
    .build();
}
```

## Fixture Utilities

```typescript
// packages/db/src/test-fixtures.ts
import { prisma } from "../client";
import { buildAgent, buildOrganization, buildCall } from "@voice-agent/types/test-builders";

export class TestFixtures {
  async createOrganization(overrides = {}) {
    const data = buildOrganization(overrides);
    return prisma.organization.create({ data });
  }

  async createAgent(organizationId: string, overrides = {}) {
    const data = buildAgent({ ...overrides, organizationId });
    return prisma.agent.create({ data });
  }

  async createCall(organizationId: string, agentId: string, contactId: string, overrides = {}) {
    const data = buildCall({ ...overrides, organizationId, agentId, contactId });
    return prisma.call.create({ data });
  }

  async createFullScenario() {
    const org = await this.createOrganization();
    const agent = await this.createAgent(org.id);
    return { org, agent };
  }

  async cleanup() {
    await prisma.call.deleteMany();
    await prisma.campaign.deleteMany();
    await prisma.agent.deleteMany();
    await prisma.contact.deleteMany();
    await prisma.user.deleteMany();
    await prisma.organization.deleteMany();
  }
}
```

## Custom Matchers

```typescript
// packages/config/src/test/matchers.ts
import { expect } from "vitest";

interface CustomMatchers<R = unknown> {
  toBeValidULID(): R;
  toBeValidPhoneNumber(): R;
  toBeWithinRange(min: number, max: number): R;
  toHaveBeenCalledOnceWith(expected: unknown): R;
}

declare module "vitest" {
  interface Assertion extends CustomMatchers {}
  interface AsymmetricMatchersContaining extends CustomMatchers {}
}

expect.extend({
  toBeValidULID(received: string) {
    const ULID_REGEX = /^[0-9A-HJKMNP-TV-Z]{26}$/;
    const pass = ULID_REGEX.test(received);
    return {
      pass,
      message: () =>
        pass
          ? `expected ${received} not to be a valid ULID`
          : `expected ${received} to be a valid ULID`,
    };
  },

  toBeValidPhoneNumber(received: string) {
    const pass = /^\+[1-9]\d{1,14}$/.test(received);
    return {
      pass,
      message: () =>
        pass
          ? `expected ${received} not to be a valid phone number`
          : `expected ${received} to be a valid E.164 phone number`,
    };
  },

  toBeWithinRange(received: number, min: number, max: number) {
    const pass = received >= min && received <= max;
    return {
      pass,
      message: () =>
        pass
          ? `expected ${received} not to be within range (${min}..${max})`
          : `expected ${received} to be within range (${min}..${max})`,
    };
  },
});
```

## Mock Service Worker Handlers

```typescript
// packages/voice/src/test/msw-handlers.ts
import { http, HttpResponse } from "msw";
import { faker } from "@faker-js/faker";

export const handlers = [
  // OpenAI API mock
  http.post("https://api.openai.com/v1/chat/completions", () => {
    return HttpResponse.json({
      id: faker.string.alphanumeric(24),
      object: "chat.completion",
      choices: [
        {
          index: 0,
          message: {
            role: "assistant",
            content: "This is a mock response from the AI assistant.",
          },
          finish_reason: "stop",
        },
      ],
      usage: {
        prompt_tokens: 50,
        completion_tokens: 20,
        total_tokens: 70,
      },
    });
  }),

  // ElevenLabs TTS mock
  http.post("https://api.elevenlabs.io/v1/text-to-speech/:voiceId", () => {
    return HttpResponse.arrayBuffer(
      new ArrayBuffer(1024),
      { headers: { "Content-Type": "audio/mpeg" } },
    );
  }),

  // Deepgram STT mock
  http.post("https://api.deepgram.com/v1/listen", () => {
    return HttpResponse.json({
      results: {
        channels: [
          {
            alternatives: [
              {
                transcript: "Hello, this is a test call.",
                confidence: 0.95,
                words: [
                  { word: "Hello", start: 0.0, end: 0.5, confidence: 0.99 },
                  { word: "this", start: 0.6, end: 0.8, confidence: 0.98 },
                ],
              },
            ],
          },
        ],
      },
    });
  }),

  // MinIO health check mock
  http.get("http://localhost:9000/minio/health/live", () => {
    return HttpResponse.json({ status: "ok" });
  }),
];
```

## Testing React Components

```typescript
// packages/ui/src/test/test-utils.tsx
import { render, type RenderOptions } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { type ReactElement } from "react";

// Custom render with providers
function AllTheProviders({ children }: { children: React.ReactNode }) {
  return (
    <div data-testid="test-wrapper">
      {children}
    </div>
  );
}

function customRender(
  ui: ReactElement,
  options?: Omit<RenderOptions, "wrapper">,
) {
  return {
    user: userEvent.setup(),
    ...render(ui, { wrapper: AllTheProviders, ...options }),
  };
}

// Re-export everything
export * from "@testing-library/react";
export { customRender as render };
export { userEvent };
```

## Async Test Helpers

```typescript
// packages/config/src/test/async-helpers.ts
export function waitForPromise<T>(
  promise: Promise<T>,
  timeout = 5000,
): Promise<T> {
  return Promise.race([
    promise,
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error("Promise timed out")), timeout),
    ),
  ]);
}

export async function expectToReject(
  fn: () => Promise<unknown>,
  errorMessage?: string,
): Promise<void> {
  try {
    await fn();
    throw new Error("Expected function to reject");
  } catch (error) {
    if (errorMessage && error instanceof Error) {
      expect(error.message).toContain(errorMessage);
    }
  }
}

export function createDeferred<T>(): {
  promise: Promise<T>;
  resolve: (value: T) => void;
  reject: (error: Error) => void;
} {
  let resolve!: (value: T) => void;
  let reject!: (error: Error) => void;
  const promise = new Promise<T>((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}
```

## Design Decisions

### Builder pattern vs. plain objects

**Decision**: Use the Builder pattern for test data.

**Rationale**: Builders provide:
- **Type safety**: Full TypeScript type checking
- **Defaults**: Sensible defaults that can be overridden
- **Readability**: `buildAgent({ status: "paused" })` is clearer than spreading a large default object
- **Maintainability**: Adding a new field to the builder automatically provides a default for all tests

### faker.js vs. static data

Faker.js produces realistic data that's different on every test run. This helps surface assumptions about data format (e.g., phone number format, name length). Tests that fail with some faker outputs but pass with others reveal hidden assumptions.

## Integration Points

- **Vitest**: Test utilities are imported in test files
- **MSW**: Mock handlers for HTTP requests
- **Playwright**: Similar factory functions for E2E test data
- **Storybook**: Factory functions used for generating story data

## Production Considerations

1. **Test data size**: Factory functions should generate minimal data by default. A `buildLargeSet(n)` helper can generate bulk data for performance tests
2. **Deterministic tests**: For tests that need deterministic data, pass a seed to faker: `faker.seed(42)`. This produces the same "random" data every time
3. **Cleanup**: Always clean up test data created in databases. Use `afterEach` hooks to delete test records
4. **Shared state**: Factory functions should not share state between calls. Each call should produce independent data
5. **Documentation**: Export factory functions with JSDoc that documents default values and expected overrides
