# Section 01: Provider Abstraction Architecture

## Overview

The LLM provider abstraction layer decouples the conversation engine from any specific LLM vendor. This enables the platform to: (1) switch between OpenAI, Anthropic, Google, and custom models without code changes, (2) implement automatic failover when a provider is down, (3) route calls to the most cost-effective model for each task, and (4) support bring-your-own-key deployments for enterprise tenants.

The abstraction follows the Adapter pattern: each provider implements a common `LLMProvider` interface, while the `LLMRouter` handles provider selection, failover, and load balancing. The system supports streaming and non-streaming completions, function calling, and structured output parsing.

## Architecture

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Conversation │──▶│  LLM Router  │──▶│  Provider    │──▶│  API Adapter │──▶│  LLM API     │
│ Engine       │   │              │   │  Chain       │   │  (OpenAI/    │   │  (Cloud)     │
│ (P5 Ch 02)   │   │  - Provider  │   │  (primary →  │   │   Anthropic/ │   └──────────────┘
└──────────────┘   │    selection │   │   fallback)  │   │   Google)    │
                   │  - Failover  │   └──────────────┘   └──────────────┘
                   │  - Load bal. │
                   └──────────────┘
```

## Design Decisions

- **Adapter Pattern**: Each provider adapter implements: `complete(messages, opts)`, `stream(messages, opts)`, `completeWithTools(messages, tools, opts)`. The adapters handle API-specific authentication, request formatting, and response parsing.
- **Chain-of-Failover**: Provider chain: primary → secondary → tertiary. Each level has a timeout (primary: 10s, secondary: 15s, tertiary: 20s). Circuit breaker trips after 5 consecutive failures.
- **Cost-Based Routing**: For tasks that don't require high intelligence (sentiment analysis, keyword extraction), route to cheaper models (Gemini Flash, Claude Haiku). For complex reasoning, use premium models (GPT-4o, Claude Opus).
- **Streaming Normalization**: Each provider streams tokens differently. The abstraction normalizes to a common `AsyncIterable<string>` interface with consistent event structure.

## Implementation Approach

```typescript
interface LLMProvider {
  complete(messages: Message[], opts?: CompleteOpts): Promise<Completion>;
  stream(messages: Message[], opts?: CompleteOpts): AsyncIterable<string>;
  completeWithTools(messages: Message[], tools: Tool[], opts?: CompleteOpts): Promise<Completion>;
  getModelInfo(): ModelInfo;
}

interface ProviderConfig {
  name: string;
  model: string;
  apiKey: string;
  baseUrl?: string;
  timeout: number;
  maxRetries: number;
  costPer1KTokens: number;
}

class LLMRouter {
  private providers: Map<string, LLMProvider>;
  private chains: Map<string, string[]>; // task -> provider chain

  async complete(messages: Message[], task: string): Promise<Completion> {
    const chain = this.chains.get(task) || ['default'];
    for (const providerName of chain) {
      try {
        const provider = this.providers.get(providerName)!;
        return await provider.complete(messages);
      } catch (err) {
        console.warn(`${providerName} failed:`, err.message);
        continue;
      }
    }
    throw new Error('All providers exhausted');
  }
}
```

## Integration Points

- **Conversation Memory (P5 Ch 02)**: Provider receives conversation history with token budget enforcement.
- **Function Calling**: Tools are defined per agent and passed to provider for function calling.
- **Cost Tracking**: Each completion is logged with token count and cost for billing.

## Open-Source Tools

- **Vercel AI SDK** (MIT): Unified provider interface. Supports OpenAI, Anthropic, Google, Mistral, and custom models.
- **LangChain** (MIT): Provider abstraction with chain-of-thought and tool use.
- **OpenAI SDK** (MIT): Reference implementation for provider adapter pattern.

## Production Considerations

- **API Key Rotation**: Rotate API keys every 90 days. Use Vault for storage. Monitor for key leakage via GitHub secret scanning.
- **Rate Limiting**: Each provider has tiered rate limits. Implement client-side rate limiting with token bucket algorithm.
- **Latency SLO**: p95 completion time <2s for streaming, <5s for full completion. Route to faster provider if SLO breached.
- **Fallback Testing**: Weekly chaos engineering: disable primary provider and verify automatic failover.
- **Cost Controls**: Set per-tenant, per-agent monthly spending caps. Alert when 80% of cap reached.
