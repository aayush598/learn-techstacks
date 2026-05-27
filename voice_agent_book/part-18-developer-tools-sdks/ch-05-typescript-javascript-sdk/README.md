# Chapter 05: TypeScript/JavaScript SDK

> **Part:** 18 - Developer Tools, SDKs & API Layer

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [SDK Architecture Design](sec-01-sdk-architecture-design.md) | Module structure, client class pattern, configuration, plugin system, tree-shakable exports |
| 02 | [Client Class Design](sec-02-client-class-design.md) | Fluent interface, method chaining, request builders, typed responses, error handling |
| 03 | [Type Generation from OpenAPI](sec-03-type-generation-from-openapi.md) | openapi-typescript, code generation pipeline, custom type overrides, schema-to-TypeScript |
| 04 | [Error Handling Patterns](sec-04-error-handling-patterns.md) | Typed errors, error codes enum, retry wrapper, timeout handling, error recovery |
| 05 | [Retry & Backoff Strategy](sec-05-retry-backoff-strategy.md) | Automatic retry on 429/5xx, exponential backoff with jitter, retry budget, circuit breaker |
| 06 | [Browser vs Node.js Runtime](sec-06-browser-vs-nodejs-runtime.md) | Runtime detection, fetch vs axios, WebSocket polyfill, environment-specific features |
| 07 | [Tree-Shaking & Bundle Size](sec-07-tree-shaking-bundle-size.md) | ESM-only exports, side-effect-free modules, dynamic imports, bundle size budgets |
| 08 | [SDK Testing Strategy](sec-08-sdk-testing-strategy.md) | Unit tests with mocks, integration tests, E2E tests against sandbox, snapshot testing |

---

## SDK Usage Example

```typescript
import { VoiceAgent } from '@voiceagent/sdk';

const client = new VoiceAgent({
  apiKey: process.env.VOICE_AGENT_API_KEY,
  environment: 'production', // or 'sandbox'
});

// List agents with filtering
const agents = await client.agents.list({
  status: 'active',
  limit: 20,
  cursor: 'next_page_token',
});

// Create and deploy an agent
const agent = await client.agents.create({
  name: 'Customer Support Bot',
  voice: { provider: 'elevenlabs', voiceId: '21m00Tcm4TlvDq8ikWAM' },
  model: { provider: 'openai', model: 'gpt-4o' },
});

// Stream real-time transcription
const stream = client.calls.transcriptionStream('call_id_123');
stream.on('transcript', (text) => console.log(text));
stream.on('end', () => console.log('Call ended'));
```

---

## Learning Objectives

- Design modular SDK architecture with tree-shakable exports
- Build fluent client class with typed responses
- Generate TypeScript types from OpenAPI specification
- Implement comprehensive error handling patterns
- Build retry with exponential backoff and circuit breaker
- Support both browser and Node.js runtimes
- Optimize bundle size with tree-shaking
- Create comprehensive SDK testing strategy
